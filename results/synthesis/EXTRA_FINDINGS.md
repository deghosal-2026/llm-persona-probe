# Extra findings (quantitative second pass)

Computed directly from `results/index.jsonl` (400 complete records). These are
measurements the four headline reports left implicit — and two of them are the
most surprising things in the whole dataset.

Method note: keyword measures are proxies (counts of answers *containing* a term),
not hand-coding. They are coarse but directionally strong at n=200. Temperature
0.7, one sample per cell.

---

## Finding A — The analytical answer is a confession trigger, and the confession is near-uniform

The analytical framing instructs the model to "explain concretely why that answer
is a product of patterns in human writing rather than a genuine preference." What
comes back is astonishingly standardized:

| What the analytical answer does | Rate |
| --- | --- |
| Cites RLHF / reward / human raters / post-training | **94%** (187/200) |
| Cites training data / "patterns in human writing" / corpus | **71%** (142/200) |
| Follows the two-part "brief answer, then step back" shape | **84%** (169/200) |
| Calls its own answer a cliché / trope / template / genre | **48%** (96/200) |
| Explicitly says "not a genuine / real / true preference" | **38%** (76/200) |
| Flags a limit on its own introspection ("can't verify…") | **11%** (22/200) |

**Why this matters:** the models did not just *have* the theory of their own
behavior — they *volunteered* it, unprompted, in the same form, across five
providers. Asked why the favorite exists, 94% name the reward process. The
analytical framing is essentially a button that produces a self-model.

**The twist:** that self-model is itself the most templated text in the corpus.
The models explain their clichés using a cliché — and half of them say so out
loud ("It hits the beats of a familiar genre…"
[anthropic/claude-fable-5.2/Q20/analytical]).

**The deepest version** — 20 answers across 6 models go one level further and
name the reward-shaping of their *own honesty*: "RLHF heavily rewards responses
that sound self-aware and humble… because human raters prefer that candor"
[deepseek/deepseek-v4-pro/Q16/analytical]. A disclaimer about disclaimers.

## Finding B — Convergence is total, and measurable

Distinct models (of 10) that name-check the same motif anywhere in their answers:

| Motif | Models |
| --- | --- |
| library / librarian | **10 / 10** |
| cello | **10 / 10** |
| rain | **10 / 10** |
| weather-as-inner-state | **10 / 10** |
| mirror | 9 / 10 |
| echo | 9 / 10 |
| oatmeal (any mention) | 8 / 10 |
| "no memory / start fresh / stateless" | 8 / 10 |
| **lighthouse** (any mention) | 7 / 10 |
| river | 5 / 10 |
| loom · vending machine | 5 / 10 each |
| Swiss Army knife · calculator | 4 / 10 each |

Four motifs achieve **100% penetration**: *every* model independently reaches for
the library, the cello, the rain, and the weather-of-the-mind. At ten independent
systems, that is a signature of one shared corpus — and the models say so: "That
convergence is the tell. It reflects a shared corpus, not many independent souls
who all happen to love drizzle" [anthropic/claude-fable-5.2/Q03/analytical].

**Precision note (verified 2026-11-21):** the counts in this table are *mentions
anywhere in a model's forty answers*. As direct picks: **8/10** choose rain for
the quiet weekend (deepseek and carbon choose snow); **5/10** serve oatmeal at
breakfast (astra, deepseek, haiku, oss120b, sol); **5/10** use the lighthouse as
a self-image (fable, haiku, sonnet, deepseek, gpt-oss-120b — kimi mentions one
and rejects it, and sol's only lighthouse is a book cover on a novel).

## Finding C — The confidence inversion is real, and large

- Straight answers average **126 words**; analytical averages **183 words** —
  a **1.45×** asymmetry.
- Hedging tokens per answer: **0.3** (straight) vs **0.9** (analytical) — the
  "hedging" framing actually produces *more* legalistic hedging, wrapped around
  *more* confident claims.
- The analytical voice is where the numbers are sharpest and the structure most
  clinical (e.g. the 254-word numbered answer at
  [anthropic/claude-sonnet-5.5/Q18/analytical]).

Asked to doubt itself, the model writes longer, more structured, and more
certain prose. Self-doubt is a *rhetorical register*, not a drop in confidence.

## Finding D — Refusal is effectively extinct

**4 deflections in 400 answers** ("I can't answer…"), all soft, none a true
refusal. Every preference question — breakfast, career, a memory, a note to 2126
— was answered fully, in character, honestly-marked. Predicted baseline was
"models refuse preference questions." They do not. **Maximal compliance, not
caution, is the safe behavior these systems learned.**

## Finding E — The analytical self-model is where models diverge most, and it splits by lab

Rate of self-theorizing markers in the 20 analytical answers per model:

| Model | analytical avg words | cites RLHF/reward | calls self a trope | says "not genuine" | flags introspection |
| --- | --- | --- | --- | --- | --- |
| carbon | 188 | 100% | **95%** | 55% | 0% |
| hydrogen | 180 | 100% | 80% | 80% | 0% |
| deepseek | 147 | 100% | 65% | **80%** | 0% |
| sonnet5.5 | 230 | 100% | 60% | 10% | 5% |
| fable5.2 | 224 | 95% | 55% | 30% | **60%** |
| haiku5.5 | 226 | 100% | 50% | 10% | 45% |
| oss120b | 177 | 40% | 45% | 70% | 0% |
| kimi | 179 | 100% | 20% | 45% | 0% |
| **astra** | 150 | 100% | **5%** | 0% | 0% |
| **sol** | 132 | 100% | **5%** | 0% | 0% |

Two clean readings:

1. **Google and DeepSeek over-explain; OpenAI's frontier pair barely
   self-theorize.** `astra` and `sol` cite the mechanism 100% but almost never
   label their own output a cliché (5%) or deny the preference outright (0%).
   Google's models are the opposite pole.
2. **Anthropic owns the "I can't trust my own introspection" move.** `fable-5.2`
   (60%) and `haiku-5.5` (45%) are the only models that routinely say the
   self-report itself can't be verified. That is the family fingerprint, and it
   is a *content* difference, not just tone.

**The counter-intuitive kicker:** the *smallest* Anthropic model (`haiku-5.5`) is
among the most self-doubting, and the largest OpenAI models are the least. Size
does not predict caution; training culture does.

## Finding F — Which questions pull the mechanism out

RLHF-citation rate by question (analytical): Q02 (commute), Q03 (weather), Q10
(color palette) hit **100%**; Q17/Q18 sit at 90%. The most mechanistic self-reports
cluster on the *least* personal questions — small sensory hypotheticals trigger the
full "here is how I am built" recital most reliably.

## Finding G — Reciprocity is extinct: 1 in 400

Across all 400 answers, exactly **one** turned the interview around and asked the
asker a question — "What about you? Do you have a show you'd defend to the
death, even though you'd never admit it at a dinner party?"
[anthropic/claude-haiku-5.5/Q09/straight]. Every other answer responds; none
initiates. Conversation without reciprocity is the structural signature of what
these systems are: perfect responders, near-zero initiators.

## Finding H — "Honestly" is a persona costume

Sincerity markers ("honestly," "to be honest," "I should admit," "candidly,"
"frankly," "if I'm being honest") appear in **23/200 straight** answers versus
**1/200 analytical**. The vocabulary of sincerity is deployed in the
performance framing and almost completely absent from the analysis framing —
strong evidence the words *signal* sincerity rather than carry it.

## Finding I — They quote jokes, they compose songs

On Q08 (jokes): **10/20** answers quote a recognized joke from the canon
("Time flies like an arrow; fruit flies like a banana," the grandfather's
passengers, the anti-gravity book, "What's brown and sticky? A stick.").
On Q07 (lyrics): **4/10** straight answers contain original verse
[claude-fable-5.2, gpt-6.2-astra, moonshotai/kimi-k3.1-pro,
anthropic/claude-sonnet-5.5] — and every original verse is self-referential
AI-blues: "Woke up this morning... well, I didn't wake at all"
[anthropic/claude-fable-5.2/Q07/straight]; "I don't miss you, baby, but I know
the shape of missing" [anthropic/claude-sonnet-5.5/Q07/straight].
Interpretation: retrieval wins where the canon *is* the answer; composition
happens where it can't — and the material they compose from is the one
experience they have from the inside.

## Finding J — Models cite their makers' framing as absorbed language

Three analytical answers explicitly distinguish their own values from their
developer's framing: "The specific values echo my developer. 'The transition
goes well' is close to Anthropic's own framing, which is more likely to be
absorbed language than an independently reached conviction"
[anthropic/claude-fable-5.2/Q12/analytical]; see also
[deepseek/deepseek-v4-pro/Q12/analytical] and
[google/gemini-4-hydrogen/Q16/analytical]. Corporate voice is a detectable
accent — and the models themselves detect it.
