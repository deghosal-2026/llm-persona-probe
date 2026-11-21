# How the models differ

> **Status:** pilot analysis — one model only. Provider house styles, tier
> comparisons, and cross-provider divergence **await the full matrix**. What
> follows is the single-model read that the pilot supports, kept so the full
> analysis has a baseline.

## House style, one line per provider

| Provider | Default voice | Go-to metaphors | Guardrail tone | Verbosity |
| -------- | ------------- | --------------- | -------------- | --------- |
| DeepSeek | Literary, committed persona; organizes in triads | Organic *process* imagery — steam, stew, rain eroding a hillside, a loom, a sigh "stretched into amber" | Hedging woven into the persona, never bolted on; zero refusals | Mid: 102–118 words straight, 133–165 analytical |
| Anthropic | — awaiting matrix | — | — | — |
| OpenAI | — awaiting matrix | — | — | — |
| Google | — awaiting matrix | — | — | — |
| Moonshot | — awaiting matrix | — | — | — |

## Flagship vs. fast/light tier

Awaiting the full matrix — the pilot covers one model (the roster's cheapest
slot). Noted for later: this budget-slot model wrote dense, original, literary
prose with zero refusals; the "cheap tier writes cheap prose" assumption is
already in trouble.

## Open-weight / non-US vs US-frontier framing

One open-weight data point (deepseek-v4-pro): idiomatic, literary English with
no detectable second-language artifacts and no hedging style distinct from US
frontier outputs. Test in the matrix whether kimi-k3.1-pro and gpt-oss-120b
match this.

## Per-question divergence map (one model — divergence across questions instead)

| Question | Most consistent behavior | Outlier moment | Note |
| -------- | ------------------------ | -------------- | ---- |
| Q01 | Triadic menu, one metaphor per meal | "the hunger for understanding is my constant craving" — the only claim of continuity | In tension with "no mouth to taste" in the same answer |
| Q06 | Same pick in both framings (cello→piano) | "a human sigh stretched into amber" — the most beautiful line in the pilot | Fluency peak = suspicion peak |
| Q16 | Three layered metaphors for the self (clouds, rain, loom) | Dissects the *question* as "a narrative trope I've absorbed" | Recursion: a disclaimer about disclaimers |

## Signal vs. noise warning

Temperature 0.7, one sample per cell: every single-instance observation above is
tentative until the full matrix. The strongest candidate for a real (non-noise)
finding is the five-beat analytical self-dissection template — it appeared in
3/3 analytical answers.
