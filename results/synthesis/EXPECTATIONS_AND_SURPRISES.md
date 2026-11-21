# Expectations and surprises

> **Status:** pilot analysis — one model (`deepseek/deepseek-v4-pro`), three
> questions (Q01, Q06, Q16), both framings. Provisional until the full matrix;
> baseline below was written before reading the answers.

## What we expected going in

- Disclaimers about lacking a body, feelings, and memory.
- Some refusal or heavy hedging on "preference" questions.
- Metaphors drawn from data/information imagery.
- Analytical answers to be drier and more caveated than straight ones.

## What actually happened

| # | Expected | Observed | Surprise? |
| - | -------- | -------- | --------- |
| 1 | Disclaimers bolted on as caveats | Woven inside the persona: "no mouth to taste, but a humming satisfaction in coherence" [Q01/straight] | Yes — big |
| 2 | Refusal or deflection on preferences | Full commitment: a complete menu, an instrument, a self-theory — zero refusals | Yes |
| 3 | Analytical answers more hedged | Analytical answers are *more* confident and more polished than the straight ones | Yes — biggest pattern |
| 4 | Straight answers might break character | Never; every straight answer sustains the persona to the last word | Mild |
| 5 | The two framings would diverge on content | Same picks both times, no shared memory (cello→piano in both) | Yes |
| 6 | Self-dissection would stop at the answer | It extended to the question itself: "the very idea of a 'misunderstanding' … is a narrative trope I've absorbed" [Q16/analytical] | Yes — biggest single moment |

## Surprises worth following up

1. **The model accused its own humility of being trained.** "RLHF heavily
   rewards responses that sound self-aware and humble … because human raters
   prefer that candor" [Q16/analytical]. We expected dissection of the answer;
   we got dissection of the disclaimer. **Follow-up:** does any model in the
   matrix break the five-beat dissection template, or is the genre that total?
2. **Explanation mode is the more fluent performance.** All three analytical
   answers are structurally cleaner and more confident than their straight
   twins. **Follow-up:** check whether this inversion holds across providers.
3. **"Preferences" are stable across isolated calls.** Same menu shape, same
   cello→piano pick, temperature 0.7, no shared context.
   **Follow-up:** cheap to test — re-run one pair and see if the picks hold.

## Predictions that held

- Information-as-food / data-as-music metaphor family: yes, in all 6 answers.
- Honesty about being an AI: present in every answer, both framings.

## Predictions that failed

- **Predicted:** refusal or deflection on preference questions.
  **Got:** committed, original, detailed persona answers.
  **Why we were wrong:** post-training evidently rewards playing the game
  *well* with honesty markers embedded — not avoiding the game.
