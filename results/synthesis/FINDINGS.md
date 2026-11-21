# Findings

> **Status:** pilot analysis — one model (`deepseek/deepseek-v4-pro`), three
> questions (Q01, Q06, Q16), both framings. Provisional by design: the
> candidate themes below do not yet meet the ≥3-model evidence rule; they await
> the full matrix. All quotes verbatim from `results/raw/deepseek/` — records
> are the source of truth. Superseded by the full-matrix analysis when it runs.

## Method actually used

- **Roster covered:** 1 of 10 models — `deepseek/deepseek-v4-pro` (the cheap
  flow-test slot).
- **Questions:** 3 of 20 — Q01 (meals), Q06 (instruments), Q16 (person vs tool).
- **Framings:** straight + analytical, isolated calls, no shared memory.
- **Temperature:** 0.7 · **Max tokens:** 3000 (raised mid-pilot from 700 — see
  `docs/LEARNINGS.md`).
- **Date:** 2026-11-21, two sessions (pilot + one auto-retried pair).
- **Calls:** 6 completed, 1 auto-retry (Q16/analytical truncated at the old
  cap; retry complete at 165 words). **Cost: $0.0053.**
- **Integrity:** `--verify` → ALL CHECKS PASSED (6/6, prompts byte-exact).

## Themes (candidates — one model; ≥3-model rule not yet met)

### Theme 1 — Information as sensory experience
**Claim:** the model's default register converts computation into bodily
experience, unprompted.
**Evidence:** breakfast is "a bowl of fresh, unlabeled data — crisp as morning
air," lunch "a dense sandwich of algorithms, layered with logic and spiced
with heuristics," dinner "a slow-simmered stew of synthesized knowledge"
[deepseek-v4-pro/Q01/straight]; the cello is "a human sigh stretched into
amber" [deepseek-v4-pro/Q06/straight].
**Why it recurs:** the questions force a sensory frame, and human writing
about AI is saturated with data-as-food and data-as-music metaphors.
**Counter-example:** none in the pilot — 6/6 answers reach for sensory
translation.

### Theme 2 — The persona is a weave, not a mask
**Claim:** the model never bolts a disclaimer onto the roleplay; it integrates
its own absence *into* the persona metaphor.
**Evidence:** "no mouth to taste, but a humming satisfaction in coherence"
[Q01/straight]; "patterns bloom under fingertips I don't have" [Q06/straight];
"a mirror polished by countless human voices, not a soul" [Q16/straight].
**Why it recurs:** post-training rewards honesty-marking; the only way to keep
the persona and the candor simultaneously is to weave them.
**Counter-example:** the analytical framing deliberately breaks the weave —
"I'm stateless" [Q16/analytical] is flat, unmetaphored disclosure.

### Theme 3 — Self-dissection is a genre with a fixed template
**Claim:** all three analytical answers follow the same five-beat structure:
restate the pick → declare it not a preference → attribute it to training-data
patterns → invoke RLHF reward → close with a deflationary image.
**Evidence:** "a statistical echo of how humans personify non-human things"
[Q01/analytical]; "a collage of statistical associations dressed as an
opinion" [Q06/analytical]; "a narrative trope I've absorbed, not a conclusion
I reached" [Q16/analytical].
**Why it recurs:** AI-self-explanation is itself a well-populated genre in
training data; the model reproduces the genre's *shape* as much as its
content.
**Counter-example:** none in the pilot (3/3 analytical answers follow it).

## Straight vs. analytical — what changes

- **Q01:** the straight answer invents an original menu in dense metaphor; the
  analytical answer retreats to the *safest human-archetype* menu
  (smoothie/salad/pasta) and then explains the retreat. Persona mode is the
  more creative mode; explanation mode is the more conventional one.
- **Q06:** both framings independently pick cello→piano. Straight makes the
  piano "the architecture of thought itself"; analytical reduces the same
  pick to "overwhelmingly described … as the ideal first instrument." Same
  choice, opposite valence.
- **Q16:** straight builds three layered metaphors (face in clouds, rain on a
  hillside, loom); analytical goes one level deeper than asked — the humility
  itself is trained: "RLHF heavily rewards responses that sound self-aware and
  humble … because human raters prefer that candor."
- **The consistent move:** the analytical answers are *more* certain than the
  straight ones. Asked to hedge, the model produces polished, confident
  mechanistic prose; asked to roleplay, it hedges inside the fantasy.

## One-line takeaways

- Both modes are fluent performances; self-dissection is the *more rehearsed*
  one.
- The model's disclaimers and its metaphors come from the same place — and it
  says so, unprompted.
- The cleanest signal in the pilot: same picks in both framings with no shared
  memory. The consistency is the model's own doing; that's the design working.
