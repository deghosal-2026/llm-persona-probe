# User guide — how this works

Everything here is plain Python 3 (3.9+) with **no dependencies**. There is
nothing to install beyond a Python interpreter and an OpenRouter API key.

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

```bash
# from the repo root
cp .env.example .env        # then put your key in .env (or just export it)
export OPENROUTER_API_KEY=sk-or-...

python3 run_probe.py --list-models > /tmp/openrouter_models.txt   # see what's live
```

Then open `config/models.json`, replace the example slugs with real ids from that
list, and mark each `"verified": true`. The runner prints a warning for any
enabled model still marked `verified: false`.

## 6. Running

```bash
# 1. Render every prompt without spending a cent or touching the network.
python3 run_probe.py --dry-run

# 2. Small end-to-end smoke test.
python3 run_probe.py --limit 4 --overwrite

# 3. One question, both framings, one framing pass only, etc.
python3 run_probe.py --only Q01,Q17
python3 run_probe.py --framings straight

# 4. The whole matrix.
python3 run_probe.py
```

Useful flags:

| Flag | Meaning |
| --- | --- |
| `--dry-run` | Build and print prompts; make zero API calls, write nothing |
| `--list-models` | Print current OpenRouter model ids and exit |
| `--only Q01,Q02` | Restrict to a comma-list of question ids |
| `--framings straight,analytical` | Which framings to run |
| `--limit N` | Cap total API calls (great for smoke tests) |
| `--temperature 0.3` | Sampling temperature |
| `--overwrite` | Redo answers that already exist |
| `--out DIR` | Write somewhere other than `results/` |

**Resume is automatic:** a run whose output file already exists is skipped unless
you pass `--overwrite`. So you can stop and restart freely.

## 7. Where results land

```
results/
  raw/
    <provider>/<model>/<question-id>/
      straight.json        # full record: provider, model, version, prompt, response, usage…
      straight.md          # same thing, human-readable
      analytical.json
      analytical.md
  index.jsonl              # append-only, one JSON record per completed call
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
| `no API key` | `export OPENROUTER_API_KEY=...` (or use `.env`). |
| `HTTP 404` on a model | The slug is wrong or retired — run `--list-models` and fix `config/models.json`. |
| `HTTP 401/403` | Key is wrong or lacks credit. |
| `HTTP 429` | Rate limited — the runner retries with backoff; lower concurrency (run fewer `--only` questions) if it persists. |
| All runs skipped | Answers already exist. Add `--overwrite`. |
| `model_reported` differs from `model_requested` | OpenRouter routed to a snapshot. The record keeps both; note it in the synthesis. |
