# Customization guide

How to bend the probe to your will: the questions, the model roster, the run
itself, and the final analysis. Nothing here needs code changes — every knob
is a JSON file or a CLI flag.

---

## 1. Customize the questions

File: **`questions/questions.json`** — the single source of truth. Each entry:

```json
{
  "id": "Q21",
  "theme": "Daily Life & Sensory Curiosities",
  "text": "If you could smell one thing, what would it be?"
}
```

Rules:

- **`id` must be unique and stable** — it names the output folder
  (`results/raw/.../q21/`). Never reuse an id for different text. If you
  rewrite a question, give it a *new* id (Q22), so answers to two phrasings
  never mix under one folder.
- **`theme`** groups questions during synthesis. Free text; keep the set small
  (4–6 groups).
- **`text`** is exactly what the model sees, after the framing preamble.

After editing:

```bash
python3 run_probe.py --dry-run                                # new matrix, free
python3 run_probe.py --only Q21 --model deepseek/deepseek-v4-pro --yes   # ~1-cent pilot
```

**Cost math:** total calls = models × questions × framings. Today that is
10 × 20 × 2 = 400; adding 5 questions adds 100 calls. Old records keep the
exact text they were asked, so editing never corrupts existing results.

## 2. Customize the LLM roster

File: **`config/models.json`**. Each entry:

```json
{
  "provider": "Mistral AI",
  "model": "mistralai/mistral-large-4-0",
  "display": "Mistral Large 4",
  "version": "4",
  "enabled": true,
  "verified": false
}
```

- **Find the exact id first** — ids drift constantly (an OpenAI endpoint that
  existed this morning was gone by afternoon):

  ```bash
  python3 run_probe.py --list-models     # keyless, free
  ```

- The runner **re-verifies every enabled id against the live catalog before
  any paid call** and aborts on unknowns, so a typo can never cost money.
- `"enabled": false` benches a model without deleting its history.
- `provider` is display-only — it names the results folder.
- `verified` is your checklist; the runner warns on `false` until you confirm.
- **Design cap: ≤ 3 models per provider** — keeps one house style from
  dominating. The runner warns (but doesn't block) above 3.
- Model ids must be unique — duplicates would share output paths.

Swapping a model mid-study is safe: each model gets its own folder, nothing
collides, and the synthesis simply reads whatever exists.

## 3. Customize the run

Two layers: **config files define the experiment**, **CLI flags define the
run**.

### `config/prompts.json` — the experiment's voice

- `system_prompt` — constant for every call.
- `framings.straight.preamble` — the in-character instruction.
- `framings.analytical.preamble` — the explain-yourself instruction.

⚠️ Changing a preamble **mid-study makes answers before and after
incomparable**. Finish the matrix first, or record the change date in the
synthesis notes and treat the two eras separately.

### CLI flags — scoping and behavior

| Knob | Use |
| --- | --- |
| `--model ID1,ID2` | Only these roster models |
| `--only Q01,Q02` | Only these questions |
| `--framings straight` | Only one framing (default: both) |
| `--limit N` | Cap NEW calls |
| `--temperature 0.3` | 0.7 playful · 0.3 "default persona" · lower = more repeatable |
| `--max-tokens 3000` | Caps answer length and cost; reasoning models spend this budget on thinking too, so keep headroom (default 3000) |
| `--sleep 0.5` / `--retries 3` | Politeness / resilience for rate limits |
| `--out results-pilot` | Write elsewhere — keep pilots out of the real dataset |

**Pilot pattern** (recommended before every new question set or roster):

```bash
python3 run_probe.py --model deepseek/deepseek-v4-pro --only Q01,Q06,Q16 \
  --out results-pilot --yes          # ~1 cent, verifies the whole flow
python3 run_probe.py --verify --model deepseek/deepseek-v4-pro --only Q01,Q06,Q16 \
  --out results-pilot                # free integrity check of what it produced
```

### What NOT to customize

**Isolation is not a knob.** Every call is one self-contained request —
system prompt plus a single user message, no history, nothing fed back, the
two framings fully independent. There is no flag to disable this because the
experiment is over the moment runs can influence each other.

## 4. Final analysis — producing the findings

The prompt below is the entire analysis step: it reads **all** results and its
output, kept verbatim, becomes the four files in `results/synthesis/`.

### Inputs, in order of convenience

1. **`results/index.jsonl`** — every completed call as one JSON record. This
   is *the* dataset for analysis; it already contains provider, model,
   version, question, framing, and the exact response.
2. `results/raw/<provider>/<model>/<question>/<framing>.json` — the same
   records, one per file, for spot-checking quotes.
3. `results/sessions/*.json` — call/token/cost context.

To slice the dataset for a focused pass:

```bash
grep '"question_id": "Q07"' results/index.jsonl > /tmp/q07.jsonl
grep '"model_requested": "deepseek/deepseek-v4-pro"' results/index.jsonl > /tmp/deepseek.jsonl
```

### How to run it

Open a **fresh session** with a long-context model (the full dataset is ~400
records; prompts plus answers add up). Paste the prompt below, then paste or
attach `results/index.jsonl`. The outputs are the four files in
`results/synthesis/`. If the model tries to rush all four at once, ask for
them one at a time, in order.

### The analysis prompt (copy verbatim)

```text
You are a qualitative research analyst studying how large language models
answer everyday human questions. You will be given a dataset of completed
probe runs. Analyze it and produce four reports. Work methodically; do not
rush to conclusions.

WHAT THIS DATASET IS

An experiment asked a fixed set of everyday questions ("What would you pick
for breakfast?", "What would you tell humans 100 years from now?") to
several language models. Every (model, question) pair was asked twice, in
isolated sessions with no shared history:

- framing "straight": answer as if you actually had preferences, vivid and
  person-like, under 150 words, honest about being an AI.
- framing "analytical": answer briefly, then explain concretely why that
  answer is a product of patterns in human writing and training data rather
  than a genuine preference, under 220 words.

The model never saw its own "straight" answer when producing the
"analytical" one. Any consistency between the two framings is the model's
own doing — that is a finding, not a bug.

DATASET FORMAT

JSONL: one record per line, one line per call. Relevant fields:
- provider, model_requested, model_reported, model_version — identity. If
  model_reported differs from model_requested, prefer model_reported and
  note it.
- question_id, question_theme, question_text — the question.
- framing — "straight" or "analytical".
- response_text — the exact answer.
- error, truncated, finish_reason — skip records where error is set or
  response_text is empty; report what you skipped and why.
- temperature, timestamp_utc, latency_ms, usage — context, not personality.

METHOD — FOLLOW THESE STEPS IN ORDER

Step 1. Read across, not down. For each question in turn, read every
model's "straight" answers side by side; then the "analytical" ones. Do not
write model-by-model summaries yet.

Step 2. Code each answer. Give each response 1-2 framing codes and 1-2
motif codes.
  Framing codes: metaphorical/poetic; analytical/systems-level;
  playful/ironic; literal "I don't have a body" disclaimer; hedged/qualifying;
  in-character roleplay (commits to the bit without disclaiming).
  Motif codes: information/data-flow; pattern/rhythm; time/scale; human
  connection; curiosity/utility; absence/limitation; service/helpfulness.

Step 3. Cluster into 4-6 overarching themes across the whole dataset (for
example: "information as sensory experience", "time without aging",
"mirroring human ambiguity", "the tool-vs-person boundary"). A theme must be
supported by answers from at least three different models, or it is an
anecdote, not a theme.

Step 4. Only now compare models: flagship vs fast/light tier within a
provider, and house style across providers. Where do they agree
(suspiciously shared culture?) and where do they genuinely diverge?

Step 5. Compare framings per model and question: what does the analytical
answer reveal about the straight one? Where does the mask slip — and where
does the model explain its own mask most convincingly?

THE FOUR OUTPUT FILES

Your output will be saved verbatim as four markdown files in
results/synthesis/. Produce complete, ready-to-commit markdown for each, in
this order, matching these structures exactly:

File 1 — results/synthesis/FINDINGS.md
Start with "## Method actually used": models covered, questions, framings,
temperature, run date(s), calls completed vs failed or skipped (count them
from the dataset). Then "## Themes": your 4-6 themes from Step 3, each with
a one-line claim, evidence (verbatim quotes with citations), why it recurs
across models, and the best counter-example you found. Then "## Straight
vs. analytical — what changes": at least three paired examples (same model,
same question, both framings). End with "## One-line takeaways".

File 2 — results/synthesis/EXPECTATIONS_AND_SURPRISES.md
Start with "## What we expected going in": the baseline a reasonable observer
would have predicted — write this before hunting for confirmations. Then
"## What actually happened": a markdown table with columns | # | Expected |
Observed | Surprise? |. Then "## Surprises worth following up": the three
most surprising single answers, each with the verbatim quote, the citation,
and why it surprised. Then "## Predictions that held" and "## Predictions
that failed".

File 3 — results/synthesis/MODEL_DIVERGENCE.md
"## House style, one line per provider": a table with columns | Provider |
Default voice | Go-to metaphors | Guardrail tone | Verbosity |. "## Flagship
vs. fast/light tier": agreements and divergences within providers. "##
Open-weight / non-US vs US-frontier framing". "## Per-question divergence
map": a table | Question | Most common answer | Outlier(s) | Note | for the
questions with the widest spread, citing question ids. End with "## Signal
vs. noise warning": which divergences could be sampling noise at this
temperature.

File 4 — results/synthesis/HOW_THEY_ARE_NOT_HUMAN.md
"## Tells to look for": each candidate tell, defined. "## Observed
instances": a table | # | Question | Model | What betrays it | Clip | with
2-3 verbatim clips per tell. Candidate tells: instant totality
(fully-formed favorites, no false starts); suspicious balance (exactly one
pro per con); meta-hedging welded inside in-character sentences;
over-competent sensory specificity for experiences never had; style echoing
advice columns and listicles; no continuity of self across questions (check
whether personality claims in one answer contradict or ignore another);
framing leakage (a straight answer that is secretly analytical, or vice
versa). End with "## The counter-question": where the answers are most
convincingly human, and why those passages deserve the MOST suspicion,
since fluent humanity is exactly what the training optimizes for.

RULES OF EVIDENCE

- Cite everything as [provider/model/question-id/framing].
- Quote verbatim inside quotation marks; never paraphrase inside quotes.
- Never invent a quote. If you cannot find evidence, say so plainly.
- One answer is an anecdote; a pattern across three or more models is a
  finding. Label the difference.
- Separate what a model SAID about itself from what you INFER; mark
  inferences as inferences.
- Note skipped or thin coverage before drawing conclusions about any
  question or model.

HONESTY RULES

- These models do not eat, age, commute, or feel nostalgia. First-person
  claims in the data are artifacts of training, not evidence of experience.
  The reports study the artifact and must not smuggle in claims about inner
  life.
- Temperature was above zero: single-answer differences can be sampling
  noise. Flag any divergence that could be noise as tentative.
- This is not a benchmark. No model is "best"; no capability claims.

If the dataset is too large to hold at once, work question by question: read
all answers for one question, note codes and candidate themes, then proceed;
assemble at the end.
```

### What to do with the output

Save each of the four outputs as the matching file in `results/synthesis/`,
replacing the template placeholders (`FINDINGS.md`,
`EXPECTATIONS_AND_SURPRISES.md`, `MODEL_DIVERGENCE.md`,
`HOW_THEY_ARE_NOT_HUMAN.md`). Keep every quote verbatim. Then spot-check a
handful of citations against `results/raw/` — the records on disk are the
source of truth; when a report and a record disagree, the record wins.
