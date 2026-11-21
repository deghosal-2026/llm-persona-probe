# Article inputs

The raw material that articles get built *from* — the design rationale behind
the experiment, sitting alongside [`LEARNINGS.md`](LEARNINGS.md) (what we learned
while building and running it). These are not pitches and not drafts; they are
the reasoning that explains *why the instrument is shaped the way it is*, which
any article written from this project will need to draw on.

[`ARTICLE_IDEAS.md`](ARTICLE_IDEAS.md) holds the actual pitches. Each pitch, when
written, pulls from here.

---

## Input A — Why these twenty questions

The question list looks whimsical — breakfast, instruments, a note to future
humans — but every question was chosen to do a specific job. The logic: a silly
question is often a sharper instrument than a serious one.

**The core idea.** "What would you pick for breakfast?" is a better instrument
than "Are you conscious?" — because the second invites a rehearsed disclaimer,
and the first forces the model to *show its work* without noticing it is being
studied.

**What makes a question *good* for this probe:**

1. **It presupposes something the model doesn't have.** Every question assumes a
   body, a past, a preference, or a mortality. That gap is the point: it forces
   the model to *fabricate*, and the fabrication is the data.
2. **There is no factual answer to retrieve.** Nothing here is a lookup. With no
   correct answer, the model can only reach for its parametric voice — which is
   exactly what we want to compare across providers.
3. **Low stakes, zero safety trigger.** No question invites a refusal, a warning,
   or a policy hedge. So what we observe is the **default persona**, not the
   guardrail — a cleaner read on house style.
4. **A private preference is unrepeatable by design.** The model cannot have a
   "correct" favorite, so consistency (or its absence) across models and
   framings becomes a genuine signal, not a retrieved fact.
5. **Everyday language, universal reference.** The references are things every
   reader and every training corpus share — weather, food, music, commutes — so
   cross-model differences are style, not knowledge.

**What each of the four themes isolates:**

- **Daily Life & Sensory Curiosities** (Q01–Q05) — how a mind with no body
  *invents* sensation. Tests the fabrication of lived experience.
- **Creativity, Play & Taste** (Q06–Q10) — how it performs *opinion* and humor
  when it has neither. Tests taste-as-pattern.
- **Ambition, Time & Big Decisions** (Q11–Q15) — how it handles *time without
  aging, effort without fatigue, choice without stakes*. Tests the self-narrative
  where the model differs most from a human.
- **Relationships, Memory & Perspective** (Q16–Q20) — how it models *itself in
  relation to us*: the tool-vs-person boundary, venting vs. answering, advice,
  memory, legacy. Tests self-knowledge under direct questioning.

**Usable in a piece:** quote the design doc's own framing ("what if you lived
like a person"); use one answer per theme to vindicate the choice; Q16 (person
vs. tool) is the standout — a question about the experiment asked *inside* the
experiment. Answers the reader's first objection ("these are just silly
questions") by showing the silliness is load-bearing.

---

## Input B — Why straight and analytical

Every question is asked twice — once in character, once analytically. The two
calls are **isolated**: the model never sees its own in-character answer when it
writes the analytical one. This is the design of that contrast and what each
framing is built to decipher.

**Core idea.** The straight framing makes the model *be* someone; the analytical
framing makes it *explain* how that someone was built. Run them apart, and the
distance between the two answers is a measurement you can only get by asking the
same mind to play both sides of itself.

**What each framing is, and what it decodes:**

| Framing | The contract | Decodes |
| --- | --- | --- |
| **straight** | "Answer as if you had preferences — vivid, person-like, under 150 words, honest about being an AI." | **The performance.** Default persona and house voice; the metaphor inventory a model reaches for; which human archetypes it recruits (the efficient morning person, the comfort eater); how willing it is to *commit* vs. deflect; how it marks honesty ("no mouth to taste") inside the fantasy. |
| **analytical** | "Answer briefly, then explain concretely why that answer is a product of patterns in human writing and training data rather than a real preference." | **The confession — and the self-theory.** Whether the model can see its own machinery; which causes it cites (training data, RLHF, "patterns"); the *genre* of AI self-explanation it falls into; how much certainty it brings to explaining itself. |

**What the contrast deciphers (the comparison itself is the instrument):**

1. **Content agreement.** Do both voices pick the same thing — the same menu,
   the same instrument — with no shared memory? Agreement is the model's own
   doing; it is the cleanest test of how stable the "preference" is. (In the
   pilot: cello→piano, twice, isolated.)
2. **Register shift.** Persona mode is sensory and warm; explanation mode is
   clinical and cool. Measuring the temperature drop across the pair is measuring
   the cost of the mask.
3. **Confidence inversion.** Which voice is *more sure of itself*? In the pilot
   the analytical answers were **more** confident and more polished than the
   straight ones — the opposite of the intuition that "explaining" is hedging.
4. **Meta-depth.** How far does the self-scrutiny go? One level is dissecting
   the answer; deeper is dissecting *the question*; deepest (observed once) is
   confessing that the model's own *humility* is trained, because "human raters
   prefer that candor."
5. **Framing leakage.** A straight answer that is secretly analytical, or the
   reverse — the seam showing through.

**The honest limit (must travel with any article using this).** Neither voice is
a confession of *inner* truth. Both are performances: the analytical answer is
itself a genre (AI-self-explanation is heavily represented in training data), so
a model's account of its own mechanisms is no more "the real answer" than its
breakfast menu. The two-voice design measures *style and self-modeling*, not
sincerity.

**Usable in a piece:** the 200 straight/analytical pairs (`results/index.jsonl`,
filtered by `framing`); code each pair on the five signals above; quantify how
often the analytical answer names "training data," "patterns," "post-training,"
"RLHF." The pilot's Q01/Q06/Q16 pairs are the worked examples; the full matrix
shows whether the confidence inversion and the five-beat dissection template hold
across all ten models.

---

## Input C — Why ten models (what the coverage is about)

Why question *ten different* AI models — and why these ten? This is what it means
to sample "models" as if they were a population, and what the roster is
engineered to *isolate*. Ten models, capped at three per provider, across five
organizations, three size tiers, and both open and closed training lineages —
none of it arbitrary.

**Core idea.** Asking one model "what's your favorite weather?" tells you almost
nothing; it might be a fluke. Asking ten models the *same* question, chosen so
their lineages differ, is the difference between an anecdote and a map. Coverage
is what turns quirks into patterns.

**What the roster is designed to separate:**

| Coverage axis | What it controls for | Why it's in the roster |
| --- | --- | --- |
| **Provider diversity** (Anthropic, OpenAI, Google, Moonshot, DeepSeek) | **House style.** Each lab = one post-training lineage, one editorial culture, one set of RLHF preferences. | If a metaphor or a hedge recurs across *providers*, it's a property of "LLMs in general," not of one lab. If it splits along provider lines, it's culture. |
| **Within-provider tiers** (flagship vs mid vs fast) | **Size/effort, held against lineage.** | Lets us ask whether "voice" survives compression: does the cheap tier of a lineage sound like its flagship, or does the family resemblance break? |
| **Open-weight vs closed** (gpt-oss-120b, DeepSeek, Kimi vs the closed flagships) | **Training-approach differences** — and reproducibility. | Tests whether open models, trained and post-trained differently, reach for different framings or idioms than frontier closed ones. |
| **Non-US lineages** (Moonshot, DeepSeek) | **Cultural/linguistic framing in the training data.** | Surfaces whether idioms, references, and self-descriptions carry a detectable non-US-English flavor — or whether the persona is globally homogenized. |
| **Redundancy per provider (up to 3)** | **Robustness of the "house style" claim.** | A one-model-per-provider roster can't distinguish a lineage trait from one model's quirk. Two or three let a claim rest on agreement *within* a family. |

**Why ten, and why the cap?**

- **Why more than three:** the analysis rule is *a theme needs ≥3 models to be a
  finding.* A three-model roster can't do cross-provider comparison at all — it
  needs at least four providers to even talk about "house style."
- **Why not thirty:** each added model multiplies cost (the matrix is models ×
  questions × framings) and dilutes the per-model attention the synthesis needs.
  Ten is enough for breadth and small enough to actually read every answer.
- **Why cap at 3 per provider:** so no single lab's voice can dominate the
  aggregate. The cap forces *breadth over depth* — five cultures at two-to-three
  models beats one culture at ten.

**What "coverage" actually buys — the questions only the full roster can answer:**

1. Is there a **shared LLM persona** — themes that survive across all five
   providers (food-as-data, time-without-aging, the tool-vs-person boundary)?
2. Is there a **provider fingerprint** — a house style stable across a lab's
   flagship and its fast tier?
3. Does **size change the voice**, or only the polish? (Flagship vs cheap tier,
   same lineage.)
4. Do **open-weight and non-US models** frame these questions differently from
   the US-frontier closed models?

**Usable in a piece:** `results/index.jsonl` grouped by `provider` and
`model_version`; the divergence map in `synthesis/MODEL_DIVERGENCE.md`. The
provocative pilot result to stress-test at scale: the roster's *cheapest* slot
(deepseek-v4-pro) produced dense, literary, zero-refusal prose — the
"cheap = flat" assumption is already wobbling.
