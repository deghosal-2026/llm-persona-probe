# Security Policy

## Reporting a vulnerability

If you find a security issue — especially anything that could expose an API
key, token, or personal data — please **do not open a public issue**. Report it
privately using GitHub's
[Security Advisories](https://github.com/deghosal-2026/llm-persona-probe/security/advisories/new)
("Report a vulnerability"). We'll acknowledge as quickly as we can.

## How this project handles secrets

The design goal is that a secret can never end up in the repository or in any
result file:

- The OpenRouter API key is read from the **`OPENROUTER_API_KEY` environment
  variable** (or `--api-key`), never from a committed file.
- It is **never written to disk**: not into `results/`, not into session
  summaries, not into logs.
- It is **scrubbed from error messages** before anything is printed or saved —
  any `sk-or-…`, `Bearer …`, or `ghp_…` pattern is replaced with `[REDACTED]`,
  so a failed call cannot leak the key into a stored record.
- `.env`, `*.env`, and `*.key` are git-ignored; `.env.example` is a safe
  placeholder.

If you contribute, keep it that way. Never commit a real key, and if one is ever
exposed, **rotate it** — removing it from a file does not un-leak it (and this
project does not rewrite public history; a leaked key is fixed by rotation and a
forward fix).

## Scanned

The repository is scanned with `gitleaks` and `trufflehog` (git history +
working tree). Both are clean as of the last scan.
