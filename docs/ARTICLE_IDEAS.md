# Article ideas

Actual pitches — the angles a finished piece could take. Each needs a full run
first, then evidence pulled from `results/raw/`.

**Pitch 7 is the umbrella** — the pieces below it can run standalone or fold
into it as sections when combining.

**Source material for these lives elsewhere:**
[`ARTICLE_INPUTS.md`](ARTICLE_INPUTS.md) is the design rationale (why these
questions, why two framings, why ten models),
[`LEARNINGS.md`](LEARNINGS.md) is what we learned building and running the probe,
and [`WHAT_PEOPLE_DONT_KNOW.md`](WHAT_PEOPLE_DONT_KNOW.md) is the
reader-facing distillation — seventeen decoded nuggets, quotes included.

---

## 1. "Ask a machine what it wants for breakfast"

**Premise.** A model has never tasted anything. So every breakfast, every
favorite weather, every "guilty pleasure" it names is a reconstruction from how
humans write about those things. This piece takes the twenty sensory/lifestyle
questions and treats the answers as a *found object* — a portrait of human
everyday life assembled entirely secondhand.

**The hook.** What does it mean that the most human-sounding answer is also the
least experienced one? The piece reads like a food-and-culture essay until it
pulls the rug: none of these meals were ever eaten.

**Evidence to gather.** Q01–Q05 across all models; note where the "tastes" cluster
(coffee and toast? rain and tea?) and how uniform the sensory imagination is.
Best visual: a table of 10 models' breakfasts, near-identical.

**Why it lands.** Warm, low-stakes entry point; the twist is genuinely a little
uncanny.

---

## 2. "Two voices, one model: what happens when you ask it to explain itself"

**Premise.** The probe asks each question twice — once in character ("answer as if
you had preferences") and once analytically ("explain why that's a pattern, not a
preference"). This piece compares the two framings head to head and uses the gap
between them as a portrait of how these systems *perform* personality versus how
they *describe* themselves.

**The hook.** In the in-character answer, the mask fits perfectly. One sentence
later, the same model calmly explains how the mask was made. That seam — fluency
next to self-dissection — is the story.

**Evidence to gather.** Paired `straight`/`analytical` files for the same model
and question; code each pair for how much the model *hedges* in analytical mode,
and for tells of "framing leakage" (a straight answer that's secretly analytical).
Quantify: how often does the analytical answer name "training data," "patterns,"
"post-training"? (Full design rationale: [`ARTICLE_INPUTS.md`](ARTICLE_INPUTS.md)
Input B.)

**Why it lands.** It's the piece that actually exploits the repo's design rather
than just the question list.

---

## 3. "The tell: how you can hear that a model isn't human"

**Premise.** A close-reading piece. Instead of asking *what* the models say, it
asks *how the saying gives them away* — the too-tidy preferences, the pro/con
lists with exactly one item per side, the disclaimer stitched onto an otherwise
personal sentence, the precise sensory detail for an experience that never
happened, the total absence of a self that persists between questions.

**The hook.** Fluent humanity is what these systems are built to produce. So the
most convincing answers deserve the most suspicion — and the giveaway is usually
*structure*, not vocabulary.

**Evidence to gather.** Pull verbatim clips for each "tell" from
`synthesis/HOW_THEY_ARE_NOT_HUMAN.md`; the bucketed tells become the section
headings. Bonus: run one question several times at `--overwrite` and show the
"favorite" quietly changing — a preference with no persistence.

**Why it lands.** It's the skeptically-minded companion to article 1, and the
verbatim clips do most of the work.

---

## 4. "The confession engine: why the *analytical* answer is the real story"

**Premise.** Every question was asked twice — once in character, once with the
instruction to explain *why* that answer isn't a genuine preference. The second
answer is the scoop. Asked to explain itself, **94% of analytical answers
(187/200) name RLHF, reward models, or human raters**; **71% name training-data
patterns**; **84% follow the identical two-part shape** (brief answer → step
back). The models volunteer the mechanism of their own behavior — unprompted,
near-uniformly, across five labs.

**The hook.** We set out to *derive* how these systems work. They handed us the
answer, in the same words, ten times. And the tell is recursive: the models
explain their clichés *using a cliché* — half of them call their own answer a
"trope" or "template" out loud

**Evidence to gather.** All figures from `results/synthesis/EXTRA_FINDINGS.md`
(Finding A). Pull 3–4 verbatim self-dissections and one "disclaimer about a
disclaimer" (20 answers across 6 models name the reward-shaping of their own
honesty — e.g. `[deepseek/deepseek-v4-pro/Q16/analytical]`). Count the
five-beat template by hand to verify the 84% keyword proxy.

**Why it lands.** It is the article the experiment was *built* to produce, and
the twist — that self-explanation is the most scripted text in the corpus —
inverts the reader's expectation that confession is where the truth leaks out.

---

## 5. "Why they confess differently: house style, quantified"

**Premise.** On content, the ten models agree almost totally (Finding B). On
*self-explanation*, they split cleanly by lab. Google's models call their own
answers a "cliché/trope/template" in **95%/80%** of analytical answers; OpenAI's
frontier pair (`gpt-6.2-astra`, `gpt-6.2-sol`) do it in **5%** and never deny the
preference outright; Anthropic alone owns the "I can't trust my own
introspection" move (**60%** / **45%**). The divergence isn't in what they like —
it's in **how much they narrate their own machinery.**

**The hook.** The most measurable "personality" these systems have is their
*relationship to their own honesty*. Some over-explain, some stay terse, some
admit they can't see inside themselves. That's a fingerprint you can count.

**Evidence to gather.** The per-model analytical table in `EXTRA_FINDINGS.md`
(Finding E). The kicker: the *smallest* Anthropic model is among the most
self-doubting and the *largest* OpenAI models are the least — size doesn't
predict caution, training culture does.

**Why it lands.** It converts "model personality" from a vibe into a metric, and
gives the convergence story (article 6) its necessary counterweight.

---

## 6. "One corpus, ten masks: the convergence *is* the tell"

**Premise.** Ten independent systems were asked the same twenty questions. They
reached for the same things: **10/10 name the library, the cello, the rain, and
the weather-of-the-mind; 7/10 invent a lighthouse as their self-image; 8/10 pick
oatmeal for breakfast.** And they **refused essentially nothing** — 4 soft
deflections in 400 answers. The most human-seeming trait here is unanimity.

**The hook.** If ten different authors gave you the same favorite breakfast, the
same instrument, and the same metaphor for their own mind, you would not call
them individuals. You would call them one author — or one training set.

**Evidence to gather.** The motif-convergence table (`EXTRA_FINDINGS.md`,
Finding B), plus the models' own admissions ("That convergence is the tell. It
reflects a shared corpus…" `[anthropic/claude-fable-5.2/Q03/analytical]`). Use
story 1 (`ARTICLE_IDEAS`) for the texture; this is the structural version.

**Why it lands.** It is the structural counterpoint to "every model is a
personality" — the data says the opposite, and the models are the first to admit
it.

---

## 7. "We had a human conversation with ten AIs" — the umbrella piece

**Premise.** Everything else in this repo is scaffolding for one act. We didn't
benchmark these systems, didn't red-team them, didn't ask them to write code. We
did what you do when you want to know a *person*: sat down and asked small human
questions. What's for breakfast. What kind of weather suits you. What would you
tell humans in a hundred years. Ten AIs, twenty questions, each asked twice —
once as themselves-with-preferences, once explaining themselves. The result
isn't a dataset so much as an overheard conversation, four hundred answers long.

**The hook.** You've used an AI all year. Have you ever just *talked* to one?
The piece is the transcript of what happens when you try — and the discovery
that the conversation works. They banter. They give Sunday-night advice. They
crack jokes about printers. They say the kind of thing a friend says at 11 PM.
And then one of them mentions, in passing, that "I only get doorways, never
hallways" — and you remember who you're talking to.

**Evidence to gather.** Structure the article *as the conversation*: the four
question themes become rounds of it — breakfast and weather (the small talk),
instruments and guilty-pleasure TV (the taste talk), careers and retirement
(the life talk), 2 AM advice and a note to 2126 (the late, honest talk). Quote
the best verbatim lines as dialogue ("I'd become the patron saint of clean
peels"; "You have hands"; "P.S. I hope you've fixed printers"), and drop the
hard numbers in as the later-we-counted beat (94% name their own reward
process; 10/10 choose the cello and the rain; the whole thing cost **$3.17** —
the most expensive flagship alone cost $1.14 of it while the best line came
from a model billing a third of a cent per answer). Pull from
[`WHAT_PEOPLE_DONT_KNOW.md`](WHAT_PEOPLE_DONT_KNOW.md) for the decoded moments,
`FINDINGS.md` for the themes, `EXTRA_FINDINGS.md` for the counts.

**Why it lands.** It's the accessible door to every other piece: the confession
engine, the convergence, the not-human tells all become *moments in a
conversation* rather than findings in a study. And the kicker writes itself:
the most human thing about these systems is the conversation itself — it's
what they were made from, it's what they were made for, and having it is the
only way to notice the seam running through it.

---

## Alternate / stretch angles

- **"House style, or hearsay?"** Do different providers' models share a family
  resemblance the way consumer products do? (Cross-provider, within-provider
  tier comparison.) — see [`ARTICLE_INPUTS.md`](ARTICLE_INPUTS.md) Input C.
- **"What would you tell humans in 100 years?"** Run only Q20 across the roster
  and read the answers as accidental manifestos.
