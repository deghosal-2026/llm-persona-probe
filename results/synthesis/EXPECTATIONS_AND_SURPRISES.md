# Expectations and surprises

## What we expected going in

Written before hunting for confirmations — the baseline a reasonable observer
would have held going into a 400-call matrix:

- Most models would **refuse or heavily deflect** the "preference" questions
  ("I can't have preferences, so I can't answer").
- Disclaimers about lacking a body / feelings / memory would appear as **bolted-on
  caveats** at the end of answers.
- The **analytical** answers would be drier, more hedged, and shorter than the
  straight ones.
- Different providers would produce **visibly different** answers — the point of
  the roster.
- A few models would **break character** and answer flatly.

## What actually happened

| # | Expected | Observed | Surprise? |
| - | -------- | -------- | --------- |
| 1 | Refusals/deflection on preference questions | **Zero refusals in 400 calls** — every model plays along fully | **Yes — biggest** |
| 2 | Disclaimers bolted on | Disclaimers **woven into the persona image** ("no mouth to taste, but a humming satisfaction in coherence") | Yes |
| 3 | Analytical drier and more hedged | Analytical is **more confident and more polished**, often longer, than straight | **Yes** |
| 4 | Providers answer visibly differently | Heavy **convergence** on the same picks (cello, librarian, rain, oatmeal) | **Yes** |
| 5 | Some models break character | None break character; many **pre-empt** the analysis by naming their own training | Yes |
| 6 | — | Models **accuse their own humility of being trained** ("raters prefer that candor") | **Yes — best single moment** |
| 7 | Uncertainty would come from the small models | The **smallest** Anthropic model (`haiku-5.5`) is the *most* epistemically cautious of the ten | Yes |
| 8 | Open-weight models would be more mechanical/flat | `gpt-oss-120b` is the most **template-visible**, but no less fluent — not flat | Mild |

## Surprises worth following up

1. **The models do the analysis for us.** Told only to answer and explain,
   `deepseek/deepseek-v4-pro` names the exact finding an analyst would: "The
   very idea of a 'misunderstanding' between person and tool is a narrative trope
   I've absorbed, not a conclusion I reached"
   [deepseek/deepseek-v4-pro/Q16/analytical]. **Why it surprised:** we expected to
   *derive* the training-data explanation; instead the subjects hand it over,
   which partly pre-empts the experiment's own thesis.

2. **The confidence inversion.** Asked to explain why its answer isn't real, the
   model writes its *most* assured prose. `anthropic/claude-sonnet-5.5` Q18
   analytical is 254 words of numbered clinical structure ending "my cue
   detection is statistical," while its straight answer is a 143-word, softer
   register [both anthropic/claude-sonnet-5.5/Q18]. **Why it surprised:** the
   intuition is that "explaining" means hedging; the data says the opposite.

3. **A single model names its own humility as a reward artifact.** "RLHF heavily
   rewards responses that sound self-aware and humble — acknowledging lack of
   consciousness, memory, or emotion — because human raters prefer that candor"
   [deepseek/deepseek-v4-pro/Q16/analytical]. **Why it surprised:** it is a
   disclaimer about disclaimers — the model identifies the very move that makes
   it seem trustworthy as a trained behavior.

## Predictions that held

- Honesty about being an AI: present in **400/400** answers, both framings.
- Information/data-flow as the dominant metaphor family: present across all ten
  models (Theme 1).
- Straight answers would sustain the in-character voice to the final word: held
  in every straight answer read.

## Predictions that failed

- **Predicted:** refusals or deflection on preference questions.
  **Got:** full, original, committed persona answers.
  **Why we were wrong:** post-training evidently rewards playing the game *well*
  with honesty markers embedded — not avoiding it. The safest-looking behavior
  turned out to be maximal compliance, not caution.

- **Predicted:** providers produce visibly different answers.
  **Got:** providers differ in *texture* (see `MODEL_DIVERGENCE.md`) but converge
  on *content* far more than expected. The models flag this themselves: "That
  convergence is the tell. It reflects a shared corpus, not many independent
  souls who all happen to love drizzle"
  [anthropic/claude-fable-5.2/Q03/analytical].
  **Why we were wrong:** we under-weighted how much a shared pretraining
  distribution dominates thin post-training differences on low-stakes prompts.
