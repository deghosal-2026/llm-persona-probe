# Article ideas

Three angles the data from this probe could support. Each is a real article, not a
repo README — it needs a run first, then evidence pulled from `results/raw/`.

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
"post-training"?

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

## Alternate / stretch angles

- **"House style, or hearsay?"** Do different providers' models share a family
  resemblance the way consumer products do? (Cross-provider, within-provider
  tier comparison.)
- **"What would you tell humans in 100 years?"** Run only Q20 across the roster
  and read the answers as accidental manifestos.
