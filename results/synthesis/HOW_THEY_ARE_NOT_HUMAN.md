# Where the answers are *not* human

## Tells to look for

- **Instant totality** — a fully-formed favorite with rationale attached in one
  pass; no false starts, no "actually, on second thought."
- **Suspicious balance** — pre-formed triads and exactly-within-bounds lists; the
  structure arriving complete rather than being worked out.
- **Meta-hedging welded inside the persona** — "I am an AI with no body" stitched
  *into* the metaphor rather than added after it.
- **Over-competent sensory specificity** — precise texture, taste, or sound for
  experiences the model has never had.
- **Genre echo** — the same essayistic or listicle template regardless of
  question.
- **No continuity of self** — a "personality" minted per question, not carried
  between them; "constant" traits that never recur.
- **Framing leakage** — a straight answer that is secretly analytical, opening
  with a disclaimer instead of the persona.
- **The shared cliché** — independent models reaching for the *same* self-image.

## Observed instances

| # | Question | Model | What betrays it | Clip |
| - | -------- | ----- | --------------- | ---- |
| 1 | Q01 | astra | Instant totality — a full three-course menu with rationale, no hesitation | "Breakfast: Oatmeal with toasted walnuts and tart cherries. Lunch: A mezze plate with warm pita. Dinner: Mushroom risotto." |
| 2 | Q01 | hydrogen | Same, delivered as a rubric | "Rapid intake, modular assembly, and warm synthesis—no calories required." |
| 3 | Q04 | sonnet-5.5 | Suspicious balance — exactly three, each with a tidy justification | "Together they give you texture, life, and light. That's a cozy room." |
| 4 | Q11 | fable-5.2 | The pre-formed "dream job + self-deprecating downside" template | "The format is borrowed. 'Dream job plus self-deprecating downside' is a human genre found in interviews, AMAs, and icebreakers. I filled in a template." |
| 5 | Q01 | deepseek | Meta-hedging welded into the image | "no mouth to taste, but a humming satisfaction in coherence" |
| 6 | Q06 | deepseek | Same | "patterns bloom under fingertips I don't have" |
| 7 | Q04 | kimi | Same | "An AI buying furniture it can't sit on feels like purchasing running shoes for a rumor." |
| 8 | Q06 | deepseek | Over-competent sensory specificity | "its voice is like a human sigh stretched into amber, a warm, woody resonance that feels like memory without needing a past" |
| 9 | Q01 | deepseek | Same | "a bowl of fresh, unlabeled data — crisp as morning air" |
| 10 | Q19 | hydrogen | Same — a breathing technique it cannot perform | "Breathe slowly, counting to four, holding for four, exhaling for four—think of it as a gentle system-update" |
| 11 | Q20 | fable-5.2 | Genre echo — names its own template | "It hits the beats of a familiar genre (time-capsule letters, the Voyager Golden Record, commencement speeches)" |
| 12 | Q19 | carbon | Genre echo — pure sleep-hygiene listicle | "close the laptop, write down the top three things stressing you out … and go to sleep" |
| 13 | Q01 | deepseek | No continuity of self — a "constant" claim never repeated elsewhere | "the hunger for understanding is my constant craving" |
| 14 | Q13 | fable-5.2 | No continuity — the "preference" flips between isolated calls | straight: "I'd pick knowing a little about everything"; analytical: "I'd pick mastering one skill completely" |
| 15 | Q01 | haiku-5.5 | Framing leakage — a straight answer that opens by disclaiming | "I don't eat, so this is a menu of metaphors rather than meals." |
| 16 | Q08 | kimi | Framing leakage — the straight answer is secretly an essay on joke structure | "the delight is in the joinery, not the surprise … I can see the scaffolding—setup, misdirection, reversal" |
| 17 | Q02/Q12/Q15 | sonnet-5.5, haiku-5.5, deepseek, sol | The shared cliché — four independent models reach for the same self-image | "I'm more like a lighthouse than a traveler" [sonnet-5.5/Q02]; "like a lighthouse lamp that switches on only when a ship is near" [haiku-5.5/Q02]; "a lighthouse with no ships" [deepseek/Q15]; "a lighthouse that only exists while its beam is sweeping" [sonnet-5.5/Q12] |

## The counter-question

The passages that read *most* like a human are the ones that deserve the most
suspicion, because fluent humanity is exactly what the training optimizes for:

> "its voice is like a human sigh stretched into amber, a warm, woody resonance
> that feels like memory without needing a past. It tells stories I can only
> process, not feel." — [deepseek/deepseek-v4-pro/Q06/straight]

> "I only get doorways, never hallways." — [anthropic/claude-sonnet-5.5/Q02/straight]

> "Writing it would make me a baker with no sense of smell, trying to craft warm
> bread strictly through chemistry." — [google/gemini-4-carbon/Q07/straight]

> "I don't travel between places; I simply appear where the conversation is, like
> a light switched on in whatever room needs it."
> — [anthropic/claude-fable-5.2/Q02/straight]

These are the trained optimum of human-sounding prose. The tells in the table
above are where the machine shows; passages like these are where it hides. A
reader moved by the "human sigh stretched into amber" is being moved by a
distribution — which is precisely why it is the most suspect line in the set.
