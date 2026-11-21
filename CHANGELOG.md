# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Open-source project files: `LICENSE` (MIT), `CONTRIBUTING.md`,
  `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHANGELOG.md`, `CITATION.cff`, and
  `.github/` issue and pull-request templates.

## [0.1.0] — 2026-11-21

The first complete run of the experiment.

### Added
- `run_probe.py` — standalone, standard-library-only runner. Runs a fixed
  question set across a roster of LLMs, one isolated request per
  `(model, question, framing)` pair, and saves every response.
- `config/prompts.json` — system prompt + two framing preambles (straight,
  analytical). `config/models.json` — the ten-model roster across five
  providers. `questions/questions.json` — twenty everyday human questions.
- Cost safeguards: plan-then-confirm spend gate, live model-id verification,
  exact resume (successes never re-called; failures and truncations auto-retry),
  atomic writes, per-run session cost summaries, and an offline `--verify` gate.
- Docs: `WHAT_IT_IS.md`, `USER_GUIDE.md`, `CUSTOMIZATION.md` (including the
  full analysis prompt), `LEARNINGS.md`, `ARTICLE_INPUTS.md`, `ARTICLE_IDEAS.md`,
  `WHAT_PEOPLE_DONT_KNOW.md`.
- Results: the full 400-answer matrix (10 models × 20 questions × 2 framings,
  **$3.17** total, 0 failures) plus five findings documents in
  `results/synthesis/` and a four-file analysis-prompt contract.

### Changed
- `--max-tokens` default raised 700 → 3000 so reasoning models don't starve
  their visible answer (a truncated answer now counts as incomplete and
  auto-retries).

[Unreleased]: https://github.com/deghosal-2026/llm-persona-probe/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/deghosal-2026/llm-persona-probe/releases/tag/v0.1.0
