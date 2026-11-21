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
another call. Cross-contamination is therefore impossible by construction; the
only shared state between runs is the output written to disk.

SECRETS
-------
The OpenRouter API key is read from the OPENROUTER_API_KEY environment variable
(or --api-key) and is never written to disk, never placed in any output file,
and is scrubbed from error messages before they are logged.

USAGE
-----
    export OPENROUTER_API_KEY=sk-or-...
    python3 run_probe.py                       # run the whole matrix
    python3 run_probe.py --dry-run             # print prompts, call nothing
    python3 run_probe.py --list-models         # fetch current OpenRouter model ids
    python3 run_probe.py --only Q01,Q02        # subset of questions
    python3 run_probe.py --framings straight   # only one framing
    python3 run_probe.py --limit 3 --overwrite # smoke test
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
from pathlib import Path
from typing import Any

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


def die(msg: str, code: int = 2) -> "NoReturn":  # type: ignore[name-defined]
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(code)


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


def fetch_models(base_url: str) -> list[str]:
    url = base_url.rstrip("/") + "/models"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    ids = sorted(m.get("id", "") for m in data.get("data", []))
    return [i for i in ids if i]


# --------------------------------------------------------------------------- #
# Output writing
# --------------------------------------------------------------------------- #

def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_jsonl(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, ensure_ascii=False) + "\n")


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
        f"- **Finish reason:** {rec.get('finish_reason')}",
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
    p.add_argument("--limit", type=int, default=0,
                   help="cap total number of API calls (0 = no cap)")
    p.add_argument("--temperature", type=float, default=0.7,
                   help="sampling temperature (default: 0.7; try 0.3 for 'default persona')")
    p.add_argument("--max-tokens", type=int, default=700)
    p.add_argument("--timeout", type=int, default=90)
    p.add_argument("--base-url", default=os.environ.get("OPENROUTER_BASE_URL", DEFAULT_BASE_URL))
    p.add_argument("--api-key", default=os.environ.get("OPENROUTER_API_KEY", ""),
                   help="prefer the OPENROUTER_API_KEY env var over this flag")
    p.add_argument("--referer", default=os.environ.get("OPENROUTER_REFERER", ""))
    p.add_argument("--overwrite", action="store_true",
                   help="re-run and overwrite answers that already exist")
    p.add_argument("--dry-run", action="store_true",
                   help="build and print prompts without calling the API")
    p.add_argument("--list-models", action="store_true",
                   help="print current OpenRouter model ids and exit")
    return p.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    api_key = (args.api_key or "").strip()
    base_url = args.base_url.strip().rstrip("/")

    if args.list_models:
        try:
            for mid in fetch_models(base_url):
                print(mid)
        except Exception as exc:  # noqa: BLE001
            die(f"could not fetch model list: {redact(str(exc), api_key)}")
        return 0

    roster = load_json(args.models)
    prompts_cfg = load_json(args.prompts)
    questions_cfg = load_json(args.questions)

    system_prompt = prompts_cfg.get("system_prompt", "")
    framings_cfg: dict[str, Any] = prompts_cfg.get("framings", {})
    questions: list[dict[str, Any]] = questions_cfg.get("questions", [])

    wanted_framings = [f.strip() for f in args.framings.split(",") if f.strip()]
    for f in wanted_framings:
        if f not in framings_cfg:
            die(f"unknown framing '{f}'; available: {', '.join(sorted(framings_cfg))}")

    only = {q.strip() for q in args.only.split(",") if q.strip()}
    if only:
        questions = [q for q in questions if q.get("id") in only]
        if not questions:
            die(f"--only matched no questions: {sorted(only)}")

    enabled = [m for m in roster.get("models", []) if m.get("enabled", True)]
    if not enabled:
        die("no enabled models in the roster; edit config/models.json")

    unverified = [m.get("model") for m in enabled if m.get("verified") is False]
    if unverified and not args.dry_run:
        print("warning: these model ids are marked verified=false — confirm them "
              "with --list-models before trusting the output:", file=sys.stderr)
        for mid in unverified:
            print(f"  - {mid}", file=sys.stderr)

    if not args.dry_run and not api_key:
        die("no API key. Set OPENROUTER_API_KEY (see .env.example) or pass --api-key.")

    out_root = args.out.resolve()
    raw_root = out_root / "raw"
    index_path = out_root / "index.jsonl"

    # Build the full run matrix.
    runs: list[dict[str, Any]] = []
    for model in enabled:
        for q in questions:
            for framing in wanted_framings:
                runs.append({"model": model, "question": q, "framing": framing})
    if args.limit and args.limit > 0:
        runs = runs[: args.limit]

    print(f"planned API calls: {len(runs)} "
          f"({len(enabled)} models x {len(questions)} questions x {len(wanted_framings)} framings)")

    done = skipped = failed = 0

    for i, run in enumerate(runs, start=1):
        model = run["model"]
        q = run["question"]
        framing = run["framing"]

        provider = model.get("provider", "unknown")
        provider_slug = slug(provider)
        model_id = model["model"]
        model_slug = slug(model_id.split("/")[-1] or model_id)
        qid = str(q.get("id", "Q??"))
        preamble = framings_cfg[framing].get("preamble", "").strip()
        user_prompt = build_user_prompt(preamble, q.get("text", ""))
        messages = build_messages(system_prompt, user_prompt)

        run_dir = raw_root / provider_slug / model_slug / slug(qid)
        json_path = run_dir / f"{framing}.json"
        md_path = run_dir / f"{framing}.md"

        tag = f"[{i}/{len(runs)}] {provider} · {model_slug} · {qid} · {framing}"

        if json_path.exists() and not args.overwrite and not args.dry_run:
            print(f"{tag} — skip (exists; use --overwrite to redo)")
            skipped += 1
            continue

        if args.dry_run:
            print(f"{tag}")
            print("  system:", (system_prompt[:80] + "…") if len(system_prompt) > 80 else system_prompt)
            print("  user  :", user_prompt.replace("\n", " ")[:140] + "…")
            continue

        rec: dict[str, Any] = {
            "run_id": f"{provider_slug}__{model_slug}__{qid}__{framing}",
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
            "usage": None,
            "latency_ms": None,
            "error": None,
            "response_path": str((json_path).relative_to(out_root.parent)) if json_path.is_relative_to(out_root.parent) else str(json_path),
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
            )
            choice = (data.get("choices") or [{}])[0]
            message = choice.get("message") or {}
            rec["response_text"] = message.get("content")
            rec["finish_reason"] = choice.get("finish_reason")
            rec["model_reported"] = data.get("model")
            rec["usage"] = data.get("usage")
            if data.get("error"):
                rec["error"] = redact(json.dumps(data["error"]), api_key)
            rec["latency_ms"] = round(latency_ms)
            done += 1
            preview = (rec["response_text"] or "").replace("\n", " ")[:90]
            print(f"{tag} — ok ({rec['latency_ms']} ms, model={rec['model_reported']})")
            print(f"    {preview}…")
        except Exception as exc:  # noqa: BLE001
            rec["error"] = redact(str(exc), api_key)
            failed += 1
            print(f"{tag} — FAILED: {rec['error']}", file=sys.stderr)

        write_json(json_path, rec)
        write_text(md_path, response_markdown(rec))
        append_jsonl(index_path, rec)

    if args.dry_run:
        print(f"dry run complete: {len(runs)} prompt(s) built, 0 API calls made, nothing written.")
        return 0

    print(f"finished: {done} ok, {skipped} skipped, {failed} failed — results in {out_root}")
    if failed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
