# Contributing

Thanks for wanting to help. This is a small, for-fun research project, so the
bar is: **keep it honest, keep it reproducible, and never commit a secret.**

## Ways to contribute

- **Add questions.** Edit `questions/questions.json`. Rules (see
  [`docs/CUSTOMIZATION.md`](docs/CUSTOMIZATION.md)):
  - `id` must be unique and **stable** — it names the output folder. New
    question → new id (Q21, Q22…). Never reuse an id for different text.
  - Keep `theme` within the existing small set (4–6 groups).
  - Run `python3 run_probe.py --dry-run` to confirm it loads.
- **Add or swap models.** Edit `config/models.json`. Find the real id first
  with `python3 run_probe.py --list-models` (keyless, free), and keep the
  design cap of **3 models per provider**. The runner re-verifies every id
  before any paid call.
- **Change the framings** in `config/prompts.json`. ⚠️ Changing a preamble
  mid-study makes answers before and after incomparable — say so in the PR and
  in the synthesis notes.
- **Improve the runner or docs.** `run_probe.py` is standard-library-only,
  Python 3.9+. Please keep it dependency-free.

## Before you open a pull request

1. **Never commit a secret.** The OpenRouter key is read from the
   `OPENROUTER_API_KEY` environment variable only. `.env` and `*.key` are
   git-ignored — do not remove that. If you ever leak one, rotate it (deleting
   the file does not un-leak it).
2. **Exercise the change offline first:**
   ```bash
   python3 -m py_compile run_probe.py
   python3 run_probe.py --dry-run          # plan only: no key, no network, no spend
   python3 run_probe.py --verify           # if you changed anything results-related
   ```
3. **Don't spend money in a PR.** Do not run the paid matrix as part of a
   contribution unless a maintainer asked for it. `--dry-run` and `--verify`
   are free; use those.
4. **Keep the isolation guarantee.** Every call stays a single self-contained
   request (system prompt + one user message, no history, nothing fed back).
   Do not add a flag that breaks this.
5. **Match the existing style** — file layout, naming, and the tone of the docs.

## Reporting results

If you run the probe yourself, don't hand-edit `results/raw/` or
`results/index.jsonl` — those are machine-generated; regenerate them by
re-running. The `results/synthesis/` files are hand-written and are where
findings go. Cite everything as `[provider/model/question-id/framing]`.

## Code of conduct

By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).
Security issues: see [SECURITY.md](SECURITY.md).
