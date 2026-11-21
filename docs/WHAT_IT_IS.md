# What this is — and what it is not

## What it is

**llm-persona-probe** is a small, for-fun experiment in *asking language models
ordinary human questions and reading the answers together.*

It does three things:

1. **Holds a fixed set of pre-loaded questions.** Twenty everyday "what if you
   lived like a person" prompts — breakfast, weather, commutes, careers,
   nostalgia, advice. The list lives in `questions/questions.json` and does not
   change between runs.
2. **Runs them across a roster of LLMs, one at a time, in isolation.** Every
   `(model, question, framing)` pair is a separate, self-contained request with no
   prior conversation history. A model answering Q07 never sees how it answered
   Q06, and no model ever sees another model's answer.
3. **Captures the results in a structured, folder-per-model layout** — provider,
   model id, reported model version, exact prompt, exact response, usage,
   latency — so they can be read, compared, and summarized by theme.

Each question is asked in **two framings**:

- **straight** — "answer as if you actually had preferences" (in-character voice).
- **analytical** — "now explain why that answer is a product of patterns in human
  writing, not a real preference" (mechanism).

Comparing the two is the point: one gives you a character voice, the other gives
you a look at the machinery underneath.

## What it is not

- **Not a benchmark.** Nothing here is scored, ranked, or claimed to measure
  capability, safety, or quality. A model writing a charming breakfast menu has
  told you *nothing* about how well it writes code.
- **Not a consciousness test.** A model saying it "would love" a rainy Sunday is
  producing text, not reporting an inner life. The project treats every
  first-person claim as an artifact to be studied, never as evidence of feeling.
- **Not a leaderboard or a product comparison.** No "best model" conclusion is
  drawn, and none should be read out of it.
- **Not reproducible in the strict sense.** A `temperature` of 0.7 means two runs
  of the same prompt can differ. This is exploratory, not controlled.
- **Not a source of factual claims about the models.** "The roster reports model
  X" is a record of one sampled response at one moment — not a fact about the
  model's design, training, or beliefs.
- **Not a home for secrets or personal data.** No API keys, tokens, or private
  conversation content are ever stored (see `docs/USER_GUIDE.md`, "Secrets").
- **Not a substitute for reading the raw answers.** The synthesis files are
  interpretations. When they disagree with a raw response, the raw response wins.

## The honest frame

The models in this study do not eat, age, commute, or feel nostalgia. So when one
answers, it is pattern-matching over how humans write about those things. That is
exactly why it is interesting: the answers are a mirror for human culture,
storytelling, and decision-making — and for each provider's "house style" — rather
than a window into a person.

If a claim in this repo can't be traced back to a stored response, it's a guess,
and it should be labeled as one.
