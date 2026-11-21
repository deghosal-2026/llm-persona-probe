# llm-persona-probe

Asking a bunch of LLMs the same ordinary human questions — and reading the
answers together.

This is a small, for-fun experiment. We take a fixed set of everyday "what if you
lived like a person" questions, run each one against a roster of models in
**isolated sessions** (fresh context every time), and then group the answers into
themes.

Because a model doesn't actually eat, age, or feel nostalgia, its answers tend to
reveal patterns in human culture, decision-making, and storytelling — plus each
provider's "house style," guardrail tone, and metaphorical range.

## Start here

| Doc | What it covers |
| --- | --- |
| [`docs/WHAT_IT_IS.md`](docs/WHAT_IT_IS.md) | What this is — and, just as importantly, what it is not. |
| [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md) | How it works and how to run it end to end. |
| [`docs/CUSTOMIZATION.md`](docs/CUSTOMIZATION.md) | Tailoring questions, roster, runs — and the final analysis prompt. |
| [`questions/questions.json`](questions/questions.json) | The 20 pre-loaded questions (single source of truth). |
| [`config/prompts.json`](config/prompts.json) | The system prompt and the two framing preambles. |
| [`config/models.json`](config/models.json) | The model roster. |
| [`run_probe.py`](run_probe.py) | The standalone runner (stdlib only, no installs). |
| [`results/`](results/) | Captured answers + the written findings (`synthesis/`, incl. `EXTRA_FINDINGS.md`). |
| [`docs/ARTICLE_IDEAS.md`](docs/ARTICLE_IDEAS.md) | Article pitches the data could support. |
| [`docs/ARTICLE_INPUTS.md`](docs/ARTICLE_INPUTS.md) | Source material for those articles: why these questions, why two framings, why ten models. |
| [`docs/LEARNINGS.md`](docs/LEARNINGS.md) | What we learned building and piloting this — method decisions and defects, with receipts. |
| [`docs/WHAT_PEOPLE_DONT_KNOW.md`](docs/WHAT_PEOPLE_DONT_KNOW.md) | Ten things this experiment revealed about LLMs — written for readers, not engineers. |

## Quick start

```bash
export OPENROUTER_API_KEY=sk-or-...
python3 run_probe.py --list-models      # confirm the model ids
# edit config/models.json, then:
python3 run_probe.py --dry-run          # render prompts, call nothing
python3 run_probe.py --limit 4 --overwrite   # smoke test
python3 run_probe.py                    # the whole matrix
```

## How it works

- **Pre-loaded questions.** The same list for every model, unchanged.
- **Isolated runs.** One self-contained request per `(model, question, framing)`
  pair — a system prompt plus a single user message, no history, nothing fed back.
  Cross-contamination is impossible by construction.
- **Locked framing.** The same preamble per framing on every call, so we measure
  *model* differences, not prompt drift.
- **Two framings per question:**
  - **straight** — "answer as if you actually had preferences" (in-character).
  - **analytical** — "explain why that's a product of patterns, not a preference"
    (mechanism). Run as a separate, independent call.
- **Fixed decoding, no tools.** One temperature for the whole study; web search
  off, for pure parametric voice.
- **Structured, traceable output.** Every answer is saved with provider, model id,
  reported model version, the exact prompt, the exact response, usage, and
  latency — under `results/raw/<provider>/<model>/<question>/`.

## The questions

Four themes × five questions. Full text in
[`questions/questions.json`](questions/questions.json).

- **Daily Life & Sensory Curiosities** — breakfast/lunch/dinner, commute, ideal
  weather, three objects in a room, an everyday annoyance you'd fix with hands.
- **Creativity, Play & Taste** — instruments, an emotionally-foreign song genre,
  a joke that still lands, a guilty-pleasure marathon, the color palette of your
  thinking.
- **Ambition, Time & Big Decisions** — an alternate career, a 10-year plan,
  mastery vs. breadth, a human dilemma seen from above, retirement week one.
- **Relationships, Memory & Perspective** — person-vs-tool misunderstandings, one
  kept "memory," venting vs. answering, 11 PM Sunday advice, a note to humans 100
  years out.

## Secrets

The OpenRouter key is read from `OPENROUTER_API_KEY` (see `.env.example`). It is
**never written to disk**, never echoed, and scrubbed from error messages —
`.env` and `*.key` are git-ignored. Never commit a real key; if one is exposed,
rotate it. See [`SECURITY.md`](SECURITY.md).

## Contributing

Contributions welcome — new questions, models, or framings, and runner or doc
improvements. Start with [`CONTRIBUTING.md`](CONTRIBUTING.md); participation is
governed by [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md). Changes are logged in
[`CHANGELOG.md`](CHANGELOG.md). To cite this project, use
[`CITATION.cff`](CITATION.cff).

## License

[MIT](LICENSE) © 2026 deghosal-2026. Both the code and the written findings are
released under the same license.

---

Just a toy. No stakes, no benchmarking claims — only curiosity about how these
things talk when you ask them to imagine being alive.
