#!/usr/bin/env python3
"""
llm-persona-probe — ask a fixed set of everyday human questions across a roster
of LLMs and capture every response.

Standalone: Python 3.9+, standard library only. No pip install, no dependencies.

ISOLATION GUARANTEE
-------------------
Every (model, question, framing) pair is sent as ONE self-contained HTTP request
whose `messages` array contains only a system prompt and a single user message.
No prior turn is ever included, and nothing produced by one call is ever fed into
another call. The two framings are separate, independent calls by design.
Cross-contamination is impossible by construction.

COST SAFEGUARDS (spend is the enemy)
------------------------------------
1. Plan-then-confirm. The runner prints exactly which calls it is about to make
   (a per-model count), an estimated spend ceiling, and asks before spending
   anything. Non-interactive runs must pass --yes or the runner refuses.
2. Model ids are verified against the live catalog (a free, keyless GET /models)
   before any spend; unknown ids abort the run. Opt out with --skip-verify.
3. Resume is free and exact. A pair whose saved record parses, has a non-empty
   response, and has no error is NEVER re-called. Incomplete or failed records
   are retried automatically next run at no extra scope.
4. --overwrite is the only way to redo a successful answer, and the plan states
   loudly how many already-paid-for answers it would redo.
5. Writes are atomic (temp file + rename), so a killed run can never leave a
   half-written record that looks "complete" and silently swallows a retry.
6. --limit caps NEW calls (after the resume filter), not planned pairs.
7. Every run writes results/sessions/<id>.json with token and cost totals, and
   the run ends by printing actual tokens used and (when OpenRouter reports it)
   the actual cost.

SECRETS
-------
The OpenRouter API key is read from the OPENROUTER_API_KEY environment variable
(or --api-key, though env is safer since CLI args can land in shell history). It
is never written to disk, never placed in any output file, and is scrubbed from
error messages before anything is logged.

USAGE
-----
    export OPENROUTER_API_KEY=sk-or-...
    python3 run_probe.py --dry-run          # plan offline: no key, no network, no spend
    python3 run_probe.py --list-models      # print current OpenRouter model ids
    python3 run_probe.py --limit 4 --yes    # smoke test: at most 4 NEW calls
    python3 run_probe.py --only Q01,Q02    # subset of questions
    python3 run_probe.py                    # full matrix (shows plan, then asks)
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any, NoReturn

REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODELS = REPO_ROOT / "config" / "models.json"
DEFAULT_PROMPTS = REPO_ROOT / "config" / "prompts.json"
DEFAULT_QUESTIONS = REPO_ROOT / "questions" / "questions.json"
DEFAULT_OUT = REPO_ROOT / "results"

# Anything matching these is scrubbed from anything we write or print.
_SECRET_PATTERNS = [
    re.compile(r"sk-or-[A-Za-z0-9_\-]+"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._\-]+"),
    re.compile(r"ghp_[A-Za-z0-9]+"),
]


def redact(text: str, api_key: str | None = None) -> str:
    """Remove anything that looks like a secret from a string."""
    if not text:
        return text
    if api_key:
        text = text.replace(api_key, "[REDACTED]")
    for pat in _SECRET_PATTERNS:
        text = pat.sub("[REDACTED]", text)
    return text


def utc_now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")


def slug(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "unknown"


def load_json(path: Path) -> Any:
    if not path.exists():
        die(f"Missing file: {path}")
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        die(f"Could not parse {path}: {exc}")


def die(msg: str, code: int = 2) -> NoReturn:
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(code)


# --------------------------------------------------------------------------- #
# Config validation
# --------------------------------------------------------------------------- #

def validate_roster(roster: dict[str, Any]) -> list[dict[str, Any]]:
    models = roster.get("models")
    if not isinstance(models, list) or not models:
        die("config/models.json: 'models' must be a non-empty list")

    seen: set[str] = set()
    per_provider: Counter = Counter()
    for m in models:
        mid = (m.get("model") or "").strip()
        if not mid:
            die(f"config/models.json: entry without a 'model' id: {json.dumps(m)[:120]}")
        if mid in seen:
            die(f"config/models.json: duplicate model id '{mid}' "
                "(duplicate ids share output paths and would overwrite each other)")
        seen.add(mid)
        per_provider[m.get("provider") or "unknown"] += 1

    # The experiment's design caps variety at 3 models per provider. Warn, don't block.
    crowded = [f"{p} ({c})" for p, c in sorted(per_provider.items()) if c > 3]
    if crowded:
        print(f"note: more than 3 models from one provider (design cap is 3): "
              f"{', '.join(crowded)}", file=sys.stderr)
    return models


def validate_questions(questions: list[dict[str, Any]]) -> None:
    if not questions:
        die("questions file: 'questions' must be a non-empty list")
    seen: set[str] = set()
    for q in questions:
        qid = str(q.get("id") or "").strip()
        text = (q.get("text") or "").strip()
        if not qid or not text:
            die(f"questions file: every question needs a non-empty 'id' and 'text': {json.dumps(q)[:120]}")
        if qid in seen:
            die(f"questions file: duplicate question id '{qid}' (ids name output folders)")
        seen.add(qid)


# --------------------------------------------------------------------------- #
# Prompt assembly
# --------------------------------------------------------------------------- #

def build_user_prompt(preamble: str, question_text: str) -> str:
    """One self-contained user message: preamble + the question. Nothing else."""
    return f"{preamble.strip()}\n\nQuestion:\n{question_text.strip()}"


def build_messages(system_prompt: str, user_prompt: str) -> list[dict[str, str]]:
    """A fresh, two-message conversation. No history. This is the isolation rule."""
    messages: list[dict[str, str]] = []
    if system_prompt and system_prompt.strip():
        messages.append({"role": "system", "content": system_prompt.strip()})
    messages.append({"role": "user", "content": user_prompt})
    return messages


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #

def _price(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def fetch_catalog(base_url: str) -> dict[str, dict[str, float]]:
    """Keyless GET /models. Returns {model_id: {'prompt': $/token, 'completion': $/token}}."""
    url = base_url.rstrip("/") + "/models"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    catalog: dict[str, dict[str, float]] = {}
    for m in data.get("data", []):
        mid = m.get("id")
        if not mid:
            continue
        pricing = m.get("pricing") or {}
        catalog[mid] = {
            "prompt": _price(pricing.get("prompt")),
            "completion": _price(pricing.get("completion")),
        }
    return catalog


def post_chat(
    *,
    base_url: str,
    api_key: str,
    model: str,
    messages: list[dict[str, str]],
    temperature: float,
    max_tokens: int,
    timeout: int,
    referer: str | None,
    title: str | None,
    retries: int = 2,
) -> tuple[dict[str, Any], float]:
    """POST to OpenRouter's chat-completions endpoint. Returns (parsed, latency_ms)."""
    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "usage": {"include": True},
    }
    body = json.dumps(payload).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Title": title or "llm-persona-probe",
    }
    if referer:
        headers["HTTP-Referer"] = referer

    last_err: Exception | None = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        started = time.monotonic()
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
            latency_ms = (time.monotonic() - started) * 1000.0
            return json.loads(raw), latency_ms
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            last_err = RuntimeError(f"HTTP {exc.code}: {redact(detail, api_key)}")
            # Retry only on rate-limit / server errors.
            if exc.code in (408, 409, 429, 500, 502, 503, 504) and attempt < retries:
                time.sleep(2 ** attempt * 2)
                continue
            break
        except (urllib.error.URLError, TimeoutError) as exc:
            last_err = RuntimeError(f"network error: {redact(str(exc), api_key)}")
            if attempt < retries:
                time.sleep(2 ** attempt * 2)
                continue
            break

    raise last_err or RuntimeError("unknown request failure")


def estimate_ceiling(
    todo: list[dict[str, Any]],
    catalog: dict[str, dict[str, float]],
    system_prompt: str,
    framings_cfg: dict[str, Any],
    max_tokens: int,
) -> float | None:
    """Rough upper-bound spend for the planned calls (chars/4 prompt estimate)."""
    total = 0.0
    for run in todo:
        prices = catalog.get(run["model"]["model"])
        if prices is None:
            return None
        preamble = framings_cfg[run["framing"]].get("preamble", "")
        user_prompt = build_user_prompt(preamble, run["question"].get("text", ""))
        in_tokens = max(1, (len(system_prompt) + len(user_prompt)) // 4)
        total += in_tokens * prices["prompt"] + max_tokens * prices["completion"]
    return total


# --------------------------------------------------------------------------- #
# Output writing (atomic: a kill can never leave a half-written record)
# --------------------------------------------------------------------------- #

def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def atomic_write_json(path: Path, obj: Any) -> None:
    atomic_write_text(path, json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def append_jsonl(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, ensure_ascii=False) + "\n")


def is_complete(json_path: Path) -> bool:
    """A pair counts as done ONLY if its record parses, has a response, and has no error.
    Anything else (missing, corrupt, failed, empty) is retried on the next run."""
    if not json_path.exists():
        return False
    try:
        obj = json.loads(json_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    if not isinstance(obj, dict):
        return False
    return bool(obj.get("response_text")) and not obj.get("error")


def response_markdown(rec: dict[str, Any]) -> str:
    usage = json.dumps(rec.get("usage") or {}, indent=2, ensure_ascii=False)
    lines = [
        f"# {rec['question_id']} — {rec['framing']}",
        "",
        f"- **Provider:** {rec['provider']}",
        f"- **Model (requested):** `{rec['model_requested']}`",
        f"- **Model (reported):** `{rec.get('model_reported') or 'n/a'}`",
        f"- **Version:** {rec.get('model_version') or 'n/a'}",
        f"- **Framing:** {rec['framing']}",
        f"- **Temperature:** {rec['temperature']}",
        f"- **Timestamp (UTC):** {rec['timestamp_utc']}",
        f"- **Latency:** {rec.get('latency_ms')} ms",
        f"- **Finish reason:** {rec.get('finish_reason')}"
        + (" *(truncated)*" if rec.get("truncated") else ""),
        "",
        "## Theme",
        "",
        rec.get("question_theme") or "",
        "",
        "## Question",
        "",
        rec["question_text"],
        "",
        "## Prompt sent (user message)",
        "",
        "```text",
        rec["user_prompt"],
        "```",
        "",
        "## Response",
        "",
        rec.get("response_text") or rec.get("error") or "",
        "",
        "## Usage",
        "",
        "```json",
        usage,
        "```",
        "",
    ]
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Ask a fixed question set across a roster of LLMs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python3 run_probe.py --dry-run\n"
               "  python3 run_probe.py --limit 4 --yes\n"
               "  python3 run_probe.py --only Q01,Q17 --yes\n",
    )
    p.add_argument("--models", type=Path, default=DEFAULT_MODELS,
                   help=f"roster file (default: {DEFAULT_MODELS})")
    p.add_argument("--prompts", type=Path, default=DEFAULT_PROMPTS,
                   help=f"prompt/framing file (default: {DEFAULT_PROMPTS})")
    p.add_argument("--questions", type=Path, default=DEFAULT_QUESTIONS,
                   help=f"questions file (default: {DEFAULT_QUESTIONS})")
    p.add_argument("--out", type=Path, default=DEFAULT_OUT,
                   help=f"results directory (default: {DEFAULT_OUT})")
    p.add_argument("--framings", default="straight,analytical",
                   help="comma list of framings to run (default: straight,analytical)")
    p.add_argument("--only", default="",
                   help="comma list of question ids to run (default: all)")
    p.add_argument("--model", default="",
                   help="comma list of roster model ids to run (default: all enabled)")
    p.add_argument("--limit", type=int, default=0,
                   help="cap on NEW API calls, counted after already-answered pairs are skipped (0 = no cap)")
    p.add_argument("--temperature", type=float, default=0.7,
                   help="sampling temperature (default: 0.7; try 0.3 for 'default persona')")
    p.add_argument("--max-tokens", type=int, default=700)
    p.add_argument("--timeout", type=int, default=90)
    p.add_argument("--retries", type=int, default=2,
                   help="retries per call on 429/5xx/network errors (default: 2)")
    p.add_argument("--sleep", type=float, default=0.0,
                   help="pause between calls in seconds (default: 0)")
    p.add_argument("--base-url", default=os.environ.get("OPENROUTER_BASE_URL", DEFAULT_BASE_URL))
    p.add_argument("--api-key", default=os.environ.get("OPENROUTER_API_KEY", ""),
                   help="prefer the OPENROUTER_API_KEY env var over this flag (shell history)")
    p.add_argument("--referer", default=os.environ.get("OPENROUTER_REFERER", ""))
    p.add_argument("--overwrite", action="store_true",
                   help="redo successful answers too (the ONLY way to re-spend on a completed pair)")
    p.add_argument("--yes", action="store_true",
                   help="skip the spend confirmation (required when not on an interactive terminal)")
    p.add_argument("--skip-verify", action="store_true",
                   help="skip live model-id verification and the cost estimate (not recommended)")
    p.add_argument("--dry-run", action="store_true",
                   help="plan offline: print what would be called/skipped, touch nothing")
    p.add_argument("--list-models", action="store_true",
                   help="print current OpenRouter model ids and exit")
    return p.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    api_key = (args.api_key or "").strip()
    base_url = args.base_url.strip().rstrip("/")

    if args.list_models:
        try:
            catalog = fetch_catalog(base_url)
        except Exception as exc:  # noqa: BLE001
            die(f"could not fetch model catalog: {redact(str(exc), api_key)}")
        for mid in sorted(catalog):
            print(mid)
        return 0

    roster = load_json(args.models)
    prompts_cfg = load_json(args.prompts)
    questions_cfg = load_json(args.questions)

    system_prompt = prompts_cfg.get("system_prompt", "")
    framings_cfg: dict[str, Any] = prompts_cfg.get("framings", {})
    questions: list[dict[str, Any]] = questions_cfg.get("questions", [])

    validate_roster(roster)
    validate_questions(questions)

    wanted_framings = [f.strip() for f in args.framings.split(",") if f.strip()]
    for f in wanted_framings:
        if f not in framings_cfg:
            die(f"unknown framing '{f}'; available: {', '.join(sorted(framings_cfg))}")

    only = {q.strip() for q in args.only.split(",") if q.strip()}
    if only:
        questions = [q for q in questions if str(q.get("id")) in only]
        if not questions:
            die(f"--only matched no questions: {sorted(only)}")

    enabled = [m for m in roster.get("models", []) if m.get("enabled", True)]
    if not enabled:
        die("no enabled models in the roster; edit config/models.json")

    wanted_models = {m.strip() for m in args.model.split(",") if m.strip()}
    if wanted_models:
        missing = sorted(wanted_models - {m["model"] for m in enabled})
        if missing:
            die(f"--model matched no enabled roster id(s): {', '.join(missing)}")
        enabled = [m for m in enabled if m["model"] in wanted_models]

    unverified = [m.get("model") for m in enabled if m.get("verified") is False]
    if unverified:
        print("warning: these model ids are marked verified=false — confirm them "
              "with --list-models before trusting the output:", file=sys.stderr)
        for mid in unverified:
            print(f"  - {mid}", file=sys.stderr)

    out_root = args.out.resolve()
    if out_root.exists() and not out_root.is_dir():
        die(f"--out must be a directory: {out_root}")
    raw_root = out_root / "raw"
    index_path = out_root / "index.jsonl"
    sessions_root = out_root / "sessions"
    session_id = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())

    # The full matrix.
    runs: list[dict[str, Any]] = [
        {"model": m, "question": q, "framing": f}
        for m in enabled
        for q in questions
        for f in wanted_framings
    ]

    def pair_paths(run: dict[str, Any]) -> tuple[Path, Path]:
        m = run["model"]
        run_dir = (raw_root / slug(m.get("provider") or "unknown")
                   / slug(m["model"]) / slug(str(run["question"].get("id", "Q??"))))
        return run_dir / f"{run['framing']}.json", run_dir / f"{run['framing']}.md"

    complete_flags = [is_complete(pair_paths(r)[0]) for r in runs]
    n_complete = sum(complete_flags)

    # ------------------------------------------------------------------ #
    # Dry run: plan only. No key, no network, no writes.
    # ------------------------------------------------------------------ #
    if args.dry_run:
        for run, done in zip(runs, complete_flags):
            m = run["model"]
            print(f"{'SKIP (already answered)' if done else 'CALL'}  "
                  f"{m.get('provider', '?'):14} · {m['model']} · "
                  f"{run['question'].get('id')} · {run['framing']}")
        print()
        print(f"planned: {len(runs)} pairs "
              f"({len(enabled)} models x {len(questions)} questions x {len(wanted_framings)} framings)")
        print(f"already answered (would be skipped): {n_complete}")
        print(f"new calls needed: {len(runs) - n_complete}"
              + (f" (capped to {args.limit} by --limit)" if args.limit > 0 else ""))
        if args.overwrite:
            print(f"--overwrite: all {n_complete} answered pairs would be REDONE (re-spends money)")
        print("dry run complete: 0 API calls made, nothing written.")
        return 0

    # ------------------------------------------------------------------ #
    # Real run starts here. Key required.
    # ------------------------------------------------------------------ #
    if not api_key:
        die("no API key. Set OPENROUTER_API_KEY (see .env.example) or pass --api-key.")

    # Free offline repair: if a complete pair lost its .md, rebuild it from the .json.
    if not args.overwrite:
        repaired = 0
        for run, done in zip(runs, complete_flags):
            if done:
                jp, mp = pair_paths(run)
                if not mp.exists():
                    atomic_write_text(mp, response_markdown(json.loads(jp.read_text(encoding="utf-8"))))
                    repaired += 1
        if repaired:
            print(f"repaired {repaired} missing .md file(s) from existing answers (no API calls).")

    if args.overwrite:
        todo: list[dict[str, Any]] = list(runs)
        n_redo = n_complete
        n_free_skip = 0
    else:
        todo = [r for r, done in zip(runs, complete_flags) if not done]
        n_redo = 0
        n_free_skip = n_complete

    if args.limit > 0:
        todo = todo[: args.limit]

    if not todo:
        print(f"nothing to do — all {n_complete} pair(s) already answered. 0 API calls, 0 spent.")
        return 0

    # Verify ids + get pricing (free, keyless). Aborts before any spend on bad ids.
    catalog: dict[str, dict[str, float]] = {}
    if args.skip_verify:
        print("--skip-verify: model ids NOT verified; no spend estimate available.")
    else:
        try:
            catalog = fetch_catalog(base_url)
        except Exception as exc:  # noqa: BLE001
            die(f"could not verify model ids against the live catalog: {exc} "
                f"(use --skip-verify to bypass)", 1)
        unknown = [m["model"] for m in enabled if m["model"] not in catalog]
        if unknown:
            die("unknown model id(s) — fix config/models.json (ids from --list-models): "
                + ", ".join(unknown))
        print(f"verified {len(enabled)} model id(s) against the live catalog.")

    # ------------------------- plan + confirm ------------------------- #
    per_model = Counter(run["model"]["model"] for run in todo)
    print()
    print("─" * 60)
    print(f"About to make {len(todo)} NEW API call(s):")
    for mid, count in sorted(per_model.items()):
        print(f"  {mid:45} {count:4} calls")
    estimate = estimate_ceiling(todo, catalog, system_prompt, framings_cfg, args.max_tokens) if catalog else None
    if estimate is not None:
        print(f"Estimated spend ceiling: ~${estimate:,.2f} "
              f"(rough chars/4 prompt estimate + {args.max_tokens}-token completion cap)")
    else:
        print("Estimated spend ceiling: unknown (--skip-verify).")
    if n_redo:
        print(f"WARNING: --overwrite will REDO {n_redo} already-paid-for answer(s).")
    if n_free_skip:
        print(f"Skipped for free: {n_free_skip} already-answered pair(s).")
    print(f"Results directory: {out_root}")
    print("─" * 60)

    if args.yes:
        print("--yes: proceeding without confirmation.")
    else:
        if not (sys.stdin.isatty() and sys.stdout.isatty()):
            die("refusing to spend: no --yes flag and no interactive terminal to confirm on.", 1)
        try:
            answer = input(f"Proceed with {len(todo)} call(s)? [y/N] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            answer = ""
        if answer not in ("y", "yes"):
            print("aborted before any spend. 0 API calls made.")
            return 1

    # ----------------------------- execute ---------------------------- #
    done = failed = 0
    tokens_in = tokens_out = 0
    cost_total = 0.0
    per_result: dict[str, dict[str, int]] = {}

    try:
        for i, run in enumerate(todo, start=1):
            model = run["model"]
            q = run["question"]
            framing = run["framing"]
            model_id = model["model"]

            provider = model.get("provider", "unknown")
            qid = str(q.get("id", "Q??"))
            preamble = framings_cfg[framing].get("preamble", "").strip()
            user_prompt = build_user_prompt(preamble, q.get("text", ""))
            messages = build_messages(system_prompt, user_prompt)

            json_path, md_path = pair_paths(run)
            tag = f"[{i}/{len(todo)}] {provider} · {model_id} · {qid} · {framing}"

            rec: dict[str, Any] = {
                "session_id": session_id,
                "run_id": f"{slug(provider)}__{slug(model_id)}__{slug(qid)}__{framing}",
                "timestamp_utc": utc_now(),
                "provider": provider,
                "model_requested": model_id,
                "model_display": model.get("display") or model_id,
                "model_version": model.get("version"),
                "model_reported": None,
                "question_id": qid,
                "question_theme": q.get("theme"),
                "question_text": q.get("text", ""),
                "framing": framing,
                "framing_description": framings_cfg[framing].get("description"),
                "temperature": args.temperature,
                "max_tokens": args.max_tokens,
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "response_text": None,
                "finish_reason": None,
                "truncated": None,
                "usage": None,
                "latency_ms": None,
                "error": None,
            }

            try:
                data, latency_ms = post_chat(
                    base_url=base_url,
                    api_key=api_key,
                    model=model_id,
                    messages=messages,
                    temperature=args.temperature,
                    max_tokens=args.max_tokens,
                    timeout=args.timeout,
                    referer=args.referer or None,
                    title=model.get("display"),
                    retries=max(0, args.retries),
                )
                choice = (data.get("choices") or [{}])[0]
                message = choice.get("message") or {}
                rec["response_text"] = message.get("content")
                rec["finish_reason"] = choice.get("finish_reason")
                rec["truncated"] = choice.get("finish_reason") == "length"
                rec["model_reported"] = data.get("model")
                rec["usage"] = data.get("usage")
                rec["latency_ms"] = round(latency_ms)

                # A 200 with an error body, or empty content, is a FAILURE —
                # never count it as done (it must be retried next run).
                if data.get("error"):
                    rec["error"] = redact(json.dumps(data["error"]), api_key)
                elif not rec["response_text"]:
                    rec["error"] = "empty response content"

                usage = rec.get("usage") or {}
                if isinstance(usage, dict):
                    tokens_in += int(usage.get("prompt_tokens") or 0)
                    tokens_out += int(usage.get("completion_tokens") or 0)
                    if usage.get("cost") is not None:
                        try:
                            cost_total += float(usage["cost"])
                        except (TypeError, ValueError):
                            pass

                if rec["error"]:
                    failed += 1
                    print(f"{tag} — FAILED: {rec['error']}", file=sys.stderr)
                else:
                    done += 1
                    preview = (rec["response_text"] or "").replace("\n", " ")[:90]
                    print(f"{tag} — ok ({rec['latency_ms']} ms, model={rec['model_reported']})")
                    print(f"    {preview}…")
            except Exception as exc:  # noqa: BLE001
                rec["error"] = redact(str(exc), api_key)
                failed += 1
                print(f"{tag} — FAILED: {rec['error']}", file=sys.stderr)

            # Atomic: both files land whole or not at all.
            atomic_write_json(json_path, rec)
            atomic_write_text(md_path, response_markdown(rec))
            append_jsonl(index_path, rec)

            tally = per_result.setdefault(model_id, {"ok": 0, "failed": 0})
            tally["ok" if not rec["error"] else "failed"] += 1

            if args.sleep > 0 and i < len(todo):
                time.sleep(args.sleep)
    except KeyboardInterrupt:
        print(f"\ninterrupted after {done + failed}/{len(todo)} calls — "
              f"already-answered pairs are safe; re-run the same command to resume.",
              file=sys.stderr)
        _write_session_summary(sessions_root, session_id, args, todo, done, failed,
                                n_free_skip, n_redo, per_result,
                                tokens_in, tokens_out, cost_total, interrupted=True)
        return 130

    _write_session_summary(sessions_root, session_id, args, todo, done, failed,
                            n_free_skip, n_redo, per_result,
                            tokens_in, tokens_out, cost_total, interrupted=False)

    print()
    print(f"finished: {done} ok, {failed} failed, {n_free_skip} skipped (already answered).")
    print(f"tokens this session: {tokens_in} in + {tokens_out} out.")
    if cost_total:
        print(f"cost reported by OpenRouter this session: ${cost_total:,.4f}")
    if failed:
        print("failed pairs were saved as records and will be retried automatically "
              "on the next run (they are NOT counted as done).")
        return 1
    return 0


def _write_session_summary(
    sessions_root: Path,
    session_id: str,
    args: argparse.Namespace,
    todo: list[dict[str, Any]],
    done: int,
    failed: int,
    n_free_skip: int,
    n_redo: int,
    per_result: dict[str, dict[str, int]],
    tokens_in: int,
    tokens_out: int,
    cost_total: float,
    interrupted: bool,
) -> None:
    summary = {
        "session_id": session_id,
        "timestamp_utc": utc_now(),
        "interrupted": interrupted,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "calls_planned": len(todo),
        "calls_ok": done,
        "calls_failed": failed,
        "skipped_already_answered": n_free_skip,
        "redone_via_overwrite": n_redo,
        "tokens": {"prompt": tokens_in, "completion": tokens_out},
        "cost_reported_usd": round(cost_total, 6) if cost_total else 0.0,
        "per_model": per_result,
        "questions_file": str(args.questions),
        "models_file": str(args.models),
    }
    atomic_write_json(sessions_root / f"{session_id}.json", summary)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
