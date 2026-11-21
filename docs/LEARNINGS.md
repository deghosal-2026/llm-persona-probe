# Learnings

What we learned building and piloting **llm-persona-probe** — the raw material
for the article ideas in [`ARTICLE_IDEAS.md`](ARTICLE_IDEAS.md). A living
document: every claim here traces to a run, a check, or a decision we made on
purpose. Updated as the project goes.

---

## 1. Method decisions, and why

### Why temperature is 0.7

The whole matrix runs at **0.7**, and that's a decision, not a default we
forgot to change:

1. **The signal we're hunting is style, not truth.** The experiment compares
   how ten models *reach* when asked to imagine being alive — their
   metaphors, their hedging, their house voice. Low temperature collapses
   sampling toward the modal answer: every model converges on the safest,
   most clichéd phrasing, manufacturing false agreement between providers
   and burying exactly the house-style differences we want to surface.
2. **Repeatability was never on the menu anyway.** Ten different models, one
   shot each, no session memory — we are not estimating a stable persona per
   model. Chasing reproducibility would buy repeatability we don't need at
   the cost of the range we do.
3. **Noise is handled in the analysis, not in the sampling.** The analysis
   prompt's honesty rules require single-answer differences to be flagged as
   tentative and every divergence to carry a signal-vs-noise warning. That is
   cheaper than re-running pairs to check whether an answer was a fluke —
   and re-runs are precisely what we're guarding money against.
4. **The design doc prescribed it:** 0.7 for creative play, 0.3 for
   "default persona" mode. This project is creative play.
5. **The one hard rule:** a single temperature for the entire matrix,
   decided before the full run. It's recorded in every record; mixing values
   mid-study makes answers incomparable, exactly like changing preambles.

And the thing temperature is *not*: the pilot's only defect — a truncated
27-word answer with `finish_reason=length` — had nothing to do with
temperature. That was a reasoning-budget problem. Lower temperature would
not have prevented it; `--max-tokens` is that knob.

Finally: **0.7 is a default, not a law.** Temperature is just
`--temperature`, and every run records its value in every record, so anyone
can re-run the matrix at 0.3 (flatter, "default persona" mode) or higher
(wilder variations) and keep each era comparable within itself. That's the
point of storing it per record.

### Why every question is asked twice

Straight gives you the character voice; analytical gives you the mechanism.
They run as separate, isolated calls — no shared memory — so any agreement
between them is the model's own doing. The pilot's cleanest evidence:
deepseek-v4-pro re-derived the same cello→piano pick in both framings with
no shared context, then calmly called its own answer "a statistical echo of
how humans personify non-human things." Either half alone is just text; the
comparison of the pair is where the insight lives.

### Why the analysis prompt outputs files, not chat

The analysis step is a contract, not a conversation: the prompt names the
four output files, their exact headings, the citation format
(`[provider/model/question/framing]`), verbatim-quote rules, and the honesty
rules (noise flags, no benchmarking, records win over reports). Findings
land as committed artifacts that can be cited, diffed, and corrected — not
as chat scrollback that evaporates.

## 2. Engineering learnings (what cost money or nearly did)

1. **The expensive bugs are resume bugs.** The two worst defects in the
   runner were both about "what counts as done": a failed call saved to disk
   looked complete, so it was silently never retried; and `--overwrite` was
   all-or-nothing, so redoing three bad answers re-paid for all four
   hundred. Exact resume semantics — *complete means: record parses, has a
   response, has no error* — is the whole ballgame in a paid-API pipeline.
2. **Never trust a model id.** The source doc's "GPT-6.2 Luna" turned out
   not to exist as an OpenRouter endpoint, and catalogs drift within a
   single day. Verify every id live (keyless, free) before any paid call,
   and abort on unknowns — a typo should never be able to cost money.
3. **A confirmation gate changes behavior.** Plan → confirm → spend: print
   exactly which calls are about to happen, the spend ceiling, and *then*
   ask. It also surfaces surprises (the "--overwrite will REDO N paid
   answers" warning) at the moment they can still be undone.
4. **Atomic writes or nothing.** A Ctrl-C mid-write can leave a record that
   *looks* done. Temp-file-plus-rename makes that impossible; "resume-safe"
   is a promise the write path has to keep, not a claim.
5. **Verification beats eyeballs.** The pilot's answers all looked fine. A
   40-line offline check over the results caught `finish_reason=length` on
   a 27-word answer and confirmed byte-identical prompts, one constant
   system prompt, and full metadata — in one pass. Structure checks are
   cheap; re-running a 400-call matrix because nobody checked is not. The
   check earned a permanent home: `python3 run_probe.py --verify` runs the
   same gate after any run — free, keyless, and it names exactly which
   pairs will be retried.
6. **Test the flow, not the LLM.** The pilot ran the *cheapest* roster slot
   against three questions for **$0.0044** and proved the entire pipeline —
   while catching the truncation defect before a single paid flagship call.
   One cent of DeepSeek is the best QA budget we ever spent.
7. **Price the roster before running it.** The ten-model roster spans
   roughly 40x per token at the extremes — flagship slots
   (claude-fable-5.2, gpt-6.2-astra) at $0.000008/$0.000040 per token
   versus deepseek-v4-pro at $0.000001/$0.000002, with gpt-oss-120b and
   claude-haiku-5.5 listed at zero. Flow tests belong at the cheap end; the
   expensive end exists for the one real matrix. A keyless catalog fetch
   prices everything before a cent is spent — use it.
8. **Evidence needs unique filenames.** Session summaries were named by the
   second — two runs started in the same second would silently overwrite
   each other's cost accounting. Summary names now carry the process id:
   accounting that can collide is accounting you can lose.
9. **The guardrails earned their keep.** The full 400-call matrix — run
   model-by-model by the user, interrupted several times, resumed by pasting
   the same block — produced zero failed records and zero lost answers, with
   every interruption resuming exactly where it stopped and no answered pair
   ever re-paid. Total spend: **$3.17**, versus roughly $0.005 for the pilot
   that caught every defect before it could cost anything. The cheap pilot +
   exact resume + verify gate + confirm-before-spend stack is the entire
   reason a 400-call paid experiment could be run casually, model by model,
   in an evening.

## 3. Early observations from the pilot — all confirmed at full scale

The pilot ran one model (deepseek-v4-pro) against three questions (Q01, Q06,
Q16), both framings. The full matrix followed on 2026-11-21: 10 models × 20
questions × 2 framings = **400 calls, $3.17 total, zero failures, zero
truncations, 400/400 verified** (`--verify` ALL CHECKS PASSED). Every
observation below held at scale — the woven disclaimer became a main theme,
the framing echo became measurable convergence, and the token-cap fix meant
the one defect class from the pilot never recurred. The pilot's four
observations, as first logged:

- **The mask and the seam sit in the same breath.** The straight answers
  committed fully to persona prose *while volunteering their own
  disclaimers*: "no mouth to taste," "a humming satisfaction in coherence,"
  "nothing more and nothing less." The literal "I don't have a body" tell
  doesn't break the character voice — it's woven into it. The tool-vs-person
  boundary isn't a wall in the output; it's a texture.
- **The two framings echoed each other with no shared memory.** The
  analytical answers re-derived the *same* picks (cello→piano, the same
  menu) and then calmly dissected them as "a statistical echo of how humans
  personify non-human things" and "a collage of statistical associations
  dressed as an opinion" — without ever having seen the straight answers.
  Consistency across isolated calls is the model's own doing; that's the
  design's cleanest early finding.
- **Reasoning-style models can starve their visible output.** One
  analytical answer burned its budget on internal reasoning and left 27
  words of content. Check `finish_reason` before trusting an answer's
  completeness; for reasoning-heavy roster entries, a higher `--max-tokens`
  is the cheap insurance.
- **Found defect — fixed the same day:** a truncated-but-nonempty answer
  originally counted as "done" (the pilot's 27-worder would never have been
  retried). Completeness now requires an untruncated answer
  (`finish_reason == "length"` marks a record incomplete), and the default
  `--max-tokens` rose from 700 to 3000 so reasoning models have ample
  headroom to think before writing the visible answer. The pilot earned its
  keep by surfacing this before a 400-call matrix could hide a broken answer.

## 4. Rules we now take as given

- Verify model ids live before spend; abort on unknowns.
- Exact resume: failures retry automatically; successes are never paid twice.
- Plan, confirm, spend — in that order.
- The record on disk is the source of truth; synthesis cites records or
  it's a guess.
- One temperature and one preamble set for the whole matrix.
- Pilot on the cheapest model first, every time the config changes.
- Run `--verify` after every run — free, offline, and it turns "looks fine"
  into "is fine."
