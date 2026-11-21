# User guide — how this works

Everything here is plain Python 3 (3.9+) with **no dependencies**. There is
nothing to install beyond a Python interpreter and an OpenRouter API key.

## Quick start

Two steps — set the environment variable, run the script:

```bash
export OPENROUTER_API_KEY=sk-or-...   # 1. set the key in your shell
python3 run_probe.py                  # 2. run the probe
```

New here? Do a free rehearsal first: `python3 run_probe.py --dry-run` prints
exactly which calls would be made, writes nothing, and needs no key. The real
run prints its plan — per-model call counts and an estimated spend ceiling — and
asks for confirmation before spending anything. Pass `--yes` to skip the prompt
(required when there is no interactive terminal).

---

## 1. The mental model

```
 questions.json  ─┐
                  ├─►  run_probe.py  ─►  one isolated HTTP call per pair  ─►  results/raw/...
 prompts.json    ─┤                                                          results/index.jsonl
 models.json     ─┘
```

- **`questions/questions.json`** — the fixed question set (single source of truth).
- **`config/prompts.json`** — the system prompt and the two framing preambles
  (single source of truth for how questions are worded).
- **`config/models.json`** — the roster: which models, from which providers.
- **`run_probe.py`** — the runner. Builds one self-contained request per pair,
  sends it, saves the answer.
- **`results/`** — everything the run produces, plus the written synthesis.

The matrix is simply: **models × questions × framings**. The default roster of
10 models, 20 questions, and 2 framings = **400 calls**. Trim it with `--limit`
or `--only` for a smoke test.

## 2. Isolation — how runs avoid influencing each other

This is the rule the whole design protects:

- Each pair is sent as **one HTTP request**.
- The request's `messages` array is **exactly two entries**: the constant system
  prompt, and **one** user message containing the framing preamble plus the
  question.
- **No conversation history is ever included**, and **no response is ever fed
  back** into a later request.
- The framings run as **separate, independent calls**. The "analytical" call does
  not see the "straight" answer; its prompt is written to stand alone.

So cross-contamination is impossible by construction. The only thing shared
between runs is the files on disk.

> Want the two framings to see each other instead (answer, then critique in the
> same conversation)? That is a deliberate *different* experiment — it would break
> the isolation guarantee, so it is not what the default runner does.

## 3. Fixed settings — measure the model, not the prompt

To compare models fairly, the *input* must be constant:

- The same system prompt for every call (`config/prompts.json`).
- The same preamble per framing.
- One `--temperature` for the whole run (default `0.7`; use `0.3` for a more
  "default persona" feel, or `0.0`–`0.2` for near-repeatable output).
- **No tools, no web search** — pure parametric voice, so answers reflect the
  model rather than a live lookup.

## 4. Secrets — never stored

- The key is read from the **`OPENROUTER_API_KEY`** environment variable (or
  `--api-key`, though env is safer since CLI args can land in shell history).
- It is **never written to any file**, never echoed, and is **scrubbed from error
  messages** before anything is saved or printed.
- `.env` and `*.key` are git-ignored. `.env.example` is a safe template.

> Never commit a real key. If one is ever exposed, the only real fix is to
> **rotate it** — deleting it from a file does not un-leak it.

## 5. Setup

One environment variable — that is the whole setup:

```bash
# from the repo root — the key lives in your shell, never in a committed file
export OPENROUTER_API_KEY=sk-or-...
```

Prefer a file? `cp .env.example .env`, put the key in `.env`, then load it with
`set -a; . ./.env; set +a`. `.env` is git-ignored, and the key is never written
into any result file either way.

The roster (`config/models.json`) ships with live, verified ids. To re-check
them or pick different models (keyless, free):

```bash
python3 run_probe.py --list-models > /tmp/openrouter_models.txt
```

Edit `config/models.json` to swap ids or set `"enabled": false` to bench a
model. The runner re-verifies every id against the live catalog before any paid
call and aborts on anything it does not recognize.

## 6. Running

```bash
# 1. See the plan first — free, keyless, no calls made, nothing written.
python3 run_probe.py --dry-run

# 2. Optional smoke test: at most 4 NEW calls, no confirmation prompt.
python3 run_probe.py --limit 4 --yes

# 3. Subsets: one question, one framing, etc.
python3 run_probe.py --only Q01,Q17 --yes
python3 run_probe.py --framings straight --yes

# 4. The whole matrix: prints per-model call counts + a spend ceiling, then asks.
python3 run_probe.py

# 5. After any run: free offline integrity check of everything produced
#    (respects --model/--only/--framings like everything else).
python3 run_probe.py --verify
```

### Example: test the flow — one cheap model, three questions

The smallest real run, on the roster's cheapest slot (DeepSeek): one model,
three questions, both framings (straight + analytical). Exactly **6 calls**,
about **a cent** at current catalog prices — enough to verify the whole
pipeline without paying flagship rates:

```bash
python3 run_probe.py --model deepseek/deepseek-v4-pro --only Q01,Q06,Q16 --yes
```

- `--model` — picks roster ids as they appear in `config/models.json`
  (comma-separate several); the other nine are ignored, nothing to edit.
- `--only Q01,Q06,Q16` — breakfast, instruments, person-vs-tool; swap in any ids
  from `questions/questions.json`.
- Framings default to **both**, so each question is asked straight and
  analytical as two isolated calls.

Drop `--yes` to get the plan and an interactive confirmation instead. Results
land in `results/raw/deepseek/deepseek-deepseek-v4-pro/` — one folder per
question (`q01/`, `q06/`, `q16/`), each holding `straight.json`/`straight.md`
and `analytical.json`/`analytical.md` — plus one row per call in
`results/index.jsonl` and a session summary in `results/sessions/`.

If the six answers look right, the flow works — run the full matrix the same
way, just without the `--model` filter.

### Run the whole matrix — one paste, model by model

The full matrix is 10 models × 20 questions × 2 framings = **400 calls**. Each
model is fully independent (its own folder, its own calls), so the loop goes
cheapest-first — validate the flow at pennies before flagship rates apply.
Put your real key in the first line, paste the whole block, and walk away:

```bash
export OPENROUTER_API_KEY=sk-or-...        # your real key, once

for m in deepseek/deepseek-v4-pro openai/gpt-oss-120b anthropic/claude-haiku-5.5 \
         google/gemini-4-hydrogen moonshotai/kimi-k3.1-pro anthropic/claude-sonnet-5.5 \
         openai/gpt-6.2-sol google/gemini-4-carbon anthropic/claude-fable-5.2 \
         openai/gpt-6.2-astra; do
  python3 run_probe.py --model "$m" --yes || break      # run this model (40 calls)
  python3 run_probe.py --verify --model "$m" || break   # check it — free, offline
done
python3 run_probe.py --verify                          # whole 400-call matrix — free
```

- **If anything stops the loop** (rate limit, balance, Ctrl-C), the final
  verify tells you exactly what is missing. Fix nothing — paste the **same
  block** again: completed models print "nothing to do" for free, and it
  resumes where it stopped. Failures and truncations retry automatically;
  answered pairs are never re-paid.
- Drop `--yes` from the run line if you want a per-model plan + spend ceiling
  + confirmation instead (then it is not walk-away).
- Pairs already answered (like the pilot's six) are skipped for free.
- When the last line prints `ALL CHECKS PASSED`: the data is done — run the
  analysis prompt (see [`docs/CUSTOMIZATION.md`](CUSTOMIZATION.md)) **once**,
  on all 400 answers, to fill `results/synthesis/`.

Useful flags:

| Flag | Meaning |
| --- | --- |
| `--dry-run` | Print what would be called/skipped; zero API calls, zero writes, no key needed |
| `--verify` | Offline integrity gate over results: completeness, exact prompts, verbatim .md, index coverage |
| `--list-models` | Print current OpenRouter model ids and exit (keyless) |
| `--yes` | Skip the spend confirmation (required with no interactive terminal) |
| `--only Q01,Q02` | Restrict to a comma-list of question ids |
| `--model ID1,ID2` | Restrict to a comma-list of roster model ids |
| `--framings straight,analytical` | Which framings to run (default: both) |
| `--limit N` | Cap **NEW** calls, counted after already-answered pairs are skipped |
| `--temperature 0.3` | Sampling temperature (default 0.7) |
| `--max-tokens 3000` | Answer token cap — reasoning models spend it on thinking too (default 3000) |
| `--overwrite` | Redo successful answers too — the only way to re-spend on a pair |
| `--skip-verify` | Skip live id verification and the spend estimate |
| `--sleep 0.5` | Pause between calls, in seconds |
| `--retries 2` | Retries per call on 429/5xx/network errors |
| `--out DIR` | Write somewhere other than `results/` |

**Resume is automatic and exact:** a pair is skipped only if its saved record
parses, has a non-empty response, and has no error. Failed, empty, or corrupt
records are retried automatically on the next run — `--overwrite` is the only way
to redo a success, and the plan prints how many paid answers it would redo. All
writes are atomic, so a Ctrl-C can never leave a record that looks done but
isn't. Stop and restart freely; you never pay for the same answer twice.

**Cost accounting:** every run writes `results/sessions/<session-id>.json` —
calls planned/ok/failed, tokens in and out, and the cost OpenRouter reported —
and prints the same totals when it finishes.

## 7. Where results land

```
results/
  raw/
    <provider>/<model-id-slug>/<question-id>/
      straight.json        # full record: provider, model, reported version, prompt, response, usage…
      straight.md          # same thing, human-readable
      analytical.json
      analytical.md
  index.jsonl              # append-only, one JSON record per completed call
  sessions/<session-id>.json   # per-run summary: calls ok/failed, tokens, cost
  synthesis/               # the written findings (see below)
```

Every `*.json` record contains:

- `provider`, `model_requested`, `model_display`, `model_version`
- `model_reported` — the model string the **API actually returned** (catches
  silent routing to a different snapshot/version)
- `question_id`, `question_theme`, `question_text`, `framing`
- `system_prompt`, `user_prompt` — the **exact** text sent
- `response_text` — the **exact** text returned
- `finish_reason`, `usage`, `latency_ms`, `temperature`, `timestamp_utc`
- `error` — populated instead of `response_text` if the call failed

## 8. Turning results into findings

The `results/synthesis/` folder holds the write-ups. The workflow:

1. **Read across, not down.** For each question, read all models' answers
   side by side (`results/raw/*/*/Q07/`). Question-first, not model-first.
2. **Tag each answer with 1–2 codes:**
   - *Framing:* metaphorical/poetic · analytical/systems-level · playful/ironic ·
     literal "I don't have a body" disclaimer
   - *Core motif:* information/data-flow · pattern/rhythm · time/scale ·
     human connection · curiosity/utility
3. **Cluster into 4–6 themes** and write them into `synthesis/FINDINGS.md`.
4. **Record divergences** in `synthesis/MODEL_DIVERGENCE.md` (flagship vs. fast
   tiers; provider house styles).
5. **Record surprises** in `synthesis/EXPECTATIONS_AND_SURPRISES.md`.
6. **Record where the output is *not* human** in
   `synthesis/HOW_THEY_ARE_NOT_HUMAN.md`.

## 9. Troubleshooting

| Symptom | Fix |
| --- | --- |
| `no API key` | `export OPENROUTER_API_KEY=...` (see Quick start). |
| `refusing to spend` | No `--yes` and no interactive terminal — review the `--dry-run` plan, then pass `--yes`. |
| `unknown model id(s)` | A roster id isn't in the live catalog — re-check with `--list-models`, fix `config/models.json`. |
| `HTTP 404` on a model | The slug is wrong or retired — run `--list-models` and fix `config/models.json`. |
| `HTTP 401/403` | Key is wrong or lacks credit. |
| `HTTP 429` | Rate limited — the runner retries with backoff; add `--sleep 0.5` or run fewer questions at once. |
| Exit 1, some pairs `FAILED` | Expected after partial failures — re-run the same command; failures are retried automatically. |
| "nothing to do — all pairs already answered" | Everything succeeded earlier. Only `--overwrite` re-runs (and re-pays). |
| `model_reported` differs from `model_requested` | OpenRouter routed to a snapshot. The record keeps both; note it in the synthesis. |
