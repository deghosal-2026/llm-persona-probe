# Pull request

## What this changes

Brief description, and which part it touches.

## Checklist

- [ ] No secret is included (no API key, no `.env`, no tokens anywhere).
- [ ] `python3 -m py_compile run_probe.py` passes (if the runner changed).
- [ ] `python3 run_probe.py --dry-run` works (free — no key, no network).
- [ ] The isolation guarantee is intact: still one self-contained request per
      `(model, question, framing)` pair, no history, nothing fed back.
- [ ] `results/raw/` and `results/index.jsonl` were **not** hand-edited
      (machine output).
- [ ] Docs updated if behavior or config changed.

## Notes

Anything a reviewer should know (e.g. a preamble change mid-study makes
answers before/after incomparable — flag it here).
