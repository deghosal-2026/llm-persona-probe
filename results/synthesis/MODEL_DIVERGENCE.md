# How the models differ

> **Status:** template — fill after a run.
>
> Compare within providers (flagship vs. fast tier) and across providers (house
> style). Cite `provider/model/Qnn/framing` for every claim.

## House style, one line per provider

| Provider | Default voice | Go-to metaphors | Guardrail tone | Verbosity |
| -------- | ------------- | --------------- | -------------- | --------- |
| | | | | |

## Flagship vs. fast/light tier

Same provider, different size tier. Where do they agree, and where does the
cheaper model diverge?

- _Provider:_ flagship `…` vs fast `…`. **Agree on:** _…_ **Diverge on:** _…_

## Open-weight / non-US vs. US-frontier framing

Do differently-trained models reach for noticeably different idioms, cultural
references, or self-descriptions?

- 

## Per-question divergence map

For each question, note where models split most sharply. Focus on Q06
(instruments), Q11 (alternate career), Q10 (color palette of thought) — these tend
to draw the biggest stylistic spread.

| Question | Most common answer | Outlier(s) | Note |
| -------- | ------------------ | ---------- | ---- |
| Q06 | | | |
| Q10 | | | |
| Q11 | | | |

## Signal vs. noise warning

At `temperature > 0`, some of this variation is just sampling. Flag anything that
looks like a real style difference **and** re-run it (with `--overwrite`) before
calling it a finding.
