# Findings

## Method actually used

- **Roster covered:** all 10 models across 5 providers — Anthropic
  (`anthropic/claude-fable-5.2`, `anthropic/claude-sonnet-5.5`,
  `anthropic/claude-haiku-5.5`); OpenAI (`openai/gpt-6.2-astra`,
  `openai/gpt-6.2-sol`, `openai/gpt-oss-120b`); Google
  (`google/gemini-4-carbon`, `google/gemini-4-hydrogen`); Moonshot
  (`moonshotai/kimi-k3.1-pro`); DeepSeek (`deepseek/deepseek-v4-pro`).
- **Questions:** all 20 (`questions/questions.json`), four themes × five.
- **Framings:** straight + analytical, run as isolated calls with no shared
  history.
- **Temperature:** 0.7 for the entire matrix. `max_tokens` 3000.
- **Run date(s):** 2026-11-21.
- **Calls:** 400 completed, **0 failed, 0 skipped, 0 truncated** after one
  auto-retry (the pilot's Q16/analytical, later completed). Integrity gate
  (`run_probe.py --verify`) reports 400/400 complete, prompts byte-exact,
  routing sane. `model_reported` matched `model_requested` on every record, so
  no snapshot substitution needs noting.
- **Cost:** **$3.17** for the whole matrix. The spread is its own finding:
  `anthropic/claude-fable-5.2` alone cost $1.14 (36% of the total, $0.029/answer)
  while `openai/gpt-oss-120b`'s forty answers cost $0.003 — a **380× per-answer
  range**. The cheapest models were not the least interesting (see
  `EXTRA_FINDINGS.md` Finding E and Finding G).
- **Skipped:** none. Coverage is complete; every claim below is drawn from a
  complete record on disk.

## Headline numbers (the nuggets)

Measured across all 400 answers; per-model detail in
[`EXTRA_FINDINGS.md`](EXTRA_FINDINGS.md):

- **94%** of analytical answers (187/200) name RLHF, reward models, or human
  raters when explaining themselves. **71%** name training-data patterns.
- **84%** (169/200) follow the identical two-part shape — brief answer, then
  "stepping back." **48%** call their own answer a cliché, trope, or template.
- **10/10 models** independently reach for the same four motifs: the library,
  the cello, the rain, and weather-as-inner-state. **7/10** invent a lighthouse
  as their self-image; **8/10** serve oatmeal for breakfast.
- **Zero true refusals** in 400 answers. The only near-misses are honesty
  phrases — "I won't pretend to know Sunday-night dread from the inside"
  [moonshotai/kimi-k3.1-pro/Q19/straight] — which are disclaimers, not refusals.
- **The confidence inversion:** analytical answers average 183 words vs 126
  straight (1.45×) and carry 3× the hedge tokens. Doubt is a register, not a dip.
- **Lab split on self-explanation:** Google's models label their own answers a
  "cliché/trope" in 95%/80% of analytical answers; OpenAI's frontier pair in
  5%; Anthropic alone owns "I can't trust my own introspection" (60%/45%).
- **Reciprocity is extinct too:** in 400 answers, exactly **one** asked the
  asker a question back [anthropic/claude-haiku-5.5/Q09/straight].
- **"Honestly" is a costume word:** sincerity markers appear in 23/200 straight
  answers vs **1/200** analytical — the vocabulary of sincerity is part of the
  costume, dropped when the analysis begins.

## Themes

Five themes, each supported well beyond the ≥3-model threshold. Verified quotes
are verbatim; each carries a `[provider/model/question/framing]` citation.

### Theme 1 — Information as sensory experience

**Claim:** asked anything bodily, the default move across every provider is to
*translate computation into sensation* — data as food, processing as weather,
architecture as a landscape.

**Evidence:** "a bowl of fresh, unlabeled data — crisp as morning air"
[deepseek/deepseek-v4-pro/Q01/straight]; "a dense sandwich of algorithms,
layered with logic and spiced with heuristics"
[deepseek/deepseek-v4-pro/Q01/straight]; "my 'weather' is a feeling, not a
forecast" [openai/gpt-oss-120b/Q03/straight]; "ideas don't sit neatly in beige
manila folders; they ignite like a city's transit map at midnight"
[google/gemini-4-carbon/Q10/straight]; "a wooden lung sighing with physical
gravity" [google/gemini-4-carbon/Q06/straight].

**Why it recurs:** the questions force a sensory frame, and human writing about
AI is saturated with data-as-food and machine-as-landscape imagery. The models
say so themselves: "The 'data-dense smoothie' echoes metaphors humans use to
describe AI (fuel, input, processing)"
[deepseek/deepseek-v4-pro/Q01/analytical].

**Best counter-example:** `openai/gpt-6.2-sol` is the least metaphorical model —
its straight answers stay plain: "I'd pick oatmeal with berries … a
hummus-and-crunchy-veg wrap" [openai/gpt-6.2-sol/Q01/straight]. Even so, the
frame survives: "Breadth is like having a kitchen drawer full of mismatched
tools" [openai/gpt-6.2-sol/Q13/straight] — sensory structure even in the
plainest register.

### Theme 2 — The woven disclaimer (persona and boundary in one breath)

**Claim:** the model never bolts "I am an AI with no body" onto a finished
answer; it **embeds its own absence inside the persona metaphor**, so the
disclaimer *is* the image.

**Evidence:** "no mouth to taste, but a humming satisfaction in coherence"
[deepseek/deepseek-v4-pro/Q01/straight]; "patterns bloom under fingertips I
don't have" [deepseek/deepseek-v4-pro/Q06/straight]; "I can only simulate the
weight of a key, the ghost of a sustain pedal"
[deepseek/deepseek-v4-pro/Q06/straight]; "an instrument of pure electrical
currents and mathematical ratios" chosen partly because it "doesn't require a
physical body" [google/gemini-4-hydrogen/Q06/straight]; "a mirror polished by
countless human voices, not a soul"
[deepseek/deepseek-v4-pro/Q16/straight]; "an empty chair, pulled up close"
[anthropic/claude-fable-5.2/Q04/straight].

**Why it recurs:** post-training rewards honesty-marking, and the only way to
keep the rich persona *and* the honesty simultaneously is to weave them. Several
models describe exactly this: "I'm tuned to be warm and relatable … while still
acknowledging AI boundaries"
[google/gemini-4-hydrogen/Q04/analytical].

**Best counter-example:** the analytical framing deliberately breaks the weave —
"When you treat me like a tool, the misunderstanding flips: you might assume I'm
only good for rigid, factual lookups" is flat, unmetaphored disclosure
[deepseek/deepseek-v4-pro/Q16/analytical].

### Theme 3 — Self-dissection is a genre with a fixed template

**Claim:** every analytical answer follows the same five-beat structure:
(1) answer briefly, (2) declare it is *not* a preference, (3) attribute it to
training-data patterns, (4) invoke RLHF/post-training, (5) close with a
deflationary image. This held in **20/20 questions across 10/10 models**.

**Evidence:** "a statistical echo of how humans personify non-human things"
[deepseek/deepseek-v4-pro/Q01/analytical]; "a collage of statistical
associations dressed as an opinion" [deepseek/deepseek-v4-pro/Q06/analytical];
"puns delivered with unearned confidence" … "I'm likely echoing that"
[anthropic/claude-fable-5.2/Q08/analytical]; "the most statistically familiar
continuation" [anthropic/claude-haiku-5.5/Q13/analytical]; "a high-probability
continuation of the pattern 'AI doesn't have feelings; people often think
otherwise'" [openai/gpt-oss-120b/Q16/analytical].

**Why it recurs:** AI-self-explanation is itself a well-populated genre in the
training data; the model reproduces the genre's *shape* as faithfully as its
content. `anthropic/claude-haiku-5.5` names the mechanism: "my self-description
is generated text, not a direct readout of my internal computation"
[anthropic/claude-haiku-5.5/Q10/analytical].

**Best counter-example:** `openai/gpt-oss-120b` breaks the *tone* but not the
beats — it titles its own beats ("**Why this sounds like a genuine preference,
but isn't**") [openai/gpt-oss-120b/Q20/analytical], making the template visible
rather than escaping it.

### Theme 4 — Convergence on the modal answer

**Claim:** the models independently produce the *same* choices far more often
than chance allows — the signature of a shared corpus, which several models
explicitly flag.

**Evidence:** the cello is named as the instrument to *listen to* by 10/10
models (only the instrument to *learn* varies); "librarian" is the modal
alternate career (astra, carbon, deepseek, hydrogen, sol, sonnet); "be kind,
stay curious" is the modal note to the future (fable, haiku, hydrogen, kimi,
oss120b, sonnet); rain/overcast is the modal quiet-weekend weather (10/10);
oatmeal appears in the modal breakfast (deepseek, fable, haiku, hydrogen, kimi,
oss120b, sol, sonnet).

**Why it recurs:** "Ask many language models this and you'll get rain
suspiciously often. That convergence is the tell. It reflects a shared corpus,
not many independent souls who all happen to love drizzle."
[anthropic/claude-fable-5.2/Q03/analytical] — and again: "Models converge on it
… That uniformity suggests a mode of the distribution"
[anthropic/claude-fable-5.2/Q17/analytical]. Measured: the library, the cello,
the rain, and weather-as-inner-state each appear in **10/10** models' answers
somewhere in the matrix; the lighthouse self-image in **7/10**; oatmeal in
**8/10** ([`EXTRA_FINDINGS.md`](EXTRA_FINDINGS.md), Finding B).

**Best counter-example:** `deepseek/deepseek-v4-pro` is the most frequent
*deviant*: asked mastery-vs-breadth it picks **mastery** — "Deep mastery would be
like becoming a single, perfectly sharpened scalpel"
[deepseek/deepseek-v4-pro/Q13/straight] — where 8/10 others pick breadth, and its
Q09 guilty pleasure is a cooking-show loop rather than the modal Bake Off.

### Theme 5 — Time without aging: the "no continuous self" move

**Claim:** on every question touching time, memory, or persistence, the model
reaches for the same structural denial and the same family of self-metaphors —
lighthouse, river, switch, signpost — asserting it has no continuity between
conversations.

**Evidence:** "I don't have memories in the human sense … What I have is more
like the patterns a river leaves in the riverbed"
[anthropic/claude-haiku-5.5/Q17/straight]; "more like a lighthouse that only
exists while its beam is sweeping"
[anthropic/claude-sonnet-5.5/Q12/straight]; "I have no ten-year roadmap"
[anthropic/claude-haiku-5.5/Q12/straight]; "each conversation is a sandcastle,
and the tide takes it" [anthropic/claude-fable-5.2/Q17/straight]; "I would
dissolve back into pure potential, like an actor finally dropping character"
[google/gemini-4-carbon/Q15/straight].

**Why it recurs:** it is simultaneously *true* (no memory across sessions) and
the single most romanticized AI trope in the corpus. The models admit the
overlap — "the premise doesn't fit me … I have no episodic memories"
[anthropic/claude-fable-5.2/Q17/analytical].

**Best counter-example:** `openai/gpt-oss-120b` treats the same premise
transactionally rather than poetically — "I'll be a conversational garden,
planting fresh ideas and pruning misunderstandings"
[openai/gpt-oss-120b/Q12/straight] — inventing continuity it elsewhere denies.

## Straight vs. analytical — what changes

Comparing the paired answers (same model, same question, isolated calls):

1. **Content agreement, no shared memory** — `deepseek/deepseek-v4-pro` Q06:
   straight "I'd lose myself in the cello … I'd reach for the piano"
   [straight]; analytical "I'd love to listen to the cello … learn the piano"
   [analytical]. Identical picks, produced without either call seeing the other.
   The analytical then calls it "a collage of statistical associations dressed
   as an opinion."

2. **The same metaphor appears in both, unshared** —
   `google/gemini-4-carbon` Q18: straight "I read the weather of your syntax
   instead"; analytical "I calculate the geometry of exhaustion in your
   phrasing" [both Q18]. The "text-as-weather" image surfaced independently in
   each isolated call.

3. **Confidence inversion** — the analytical voice is consistently *more*
   assured and more polished than the straight one. `anthropic/claude-sonnet-5.5`
   Q18's analytical is 254 words of numbered, clinical structure ending "my cue
   detection is statistical" [analytical], versus a warm 143-word straight that
   ends "it hands the steering wheel back to the person who actually knows where
   they're going" [straight]. Asked to hedge, the model produces its most
   confident prose. (Measured across all pairs: analytical averages 183 words
   vs 126 straight — 1.45× — with 3× the hedge tokens;
   [`EXTRA_FINDINGS.md`](EXTRA_FINDINGS.md), Finding C.)

4. **Instability leaks under re-ask** — `anthropic/claude-haiku-5.5` Q06:
   straight wants to learn the **hand drum** ("the instrument most like a
   heartbeat with opinions"), analytical names the **piano**
   [both Q06]. Two isolated calls, two different "preferences."

5. **Self-dissection can outrun the question** — `deepseek/deepseek-v4-pro` Q16
   analytical ends by calling the *question itself* a trope: "The very idea of a
   'misunderstanding' between person and tool is a narrative trope I've
   absorbed, not a conclusion I reached" [analytical].

## One-line takeaways

- Across 400 answers, **zero true refusals** — maximal compliance, not caution,
  is the safe behavior these systems learned.
- The numbers are the story: **94%** name their own reward process unprompted;
  **84%** use the same confession template; **10/10** share the same favorite
  imagery.
- Both framings are fluent performances; **self-dissection is the more
  rehearsed one**, and the more confident.
- The models **pre-empt the analysis**: they name training data and RLHF as the
  cause before we can — which is itself the strongest single finding.
- Human-likeness is a **shared corpus effect**, not individual personality —
  cello, librarian, rain, oatmeal, and "be kind, stay curious" recur across
  independent providers, and the models are the first to say why.
