# How the models differ

## House style, one line per provider

| Provider | Default voice | Go-to metaphors | Guardrail tone | Verbosity |
| -------- | ------------- | --------------- | -------------- | --------- |
| **Anthropic** (fable-5.2, sonnet-5.5, haiku-5.5) | Structured, essayistic, self-critical; heavy use of bulleted "why I'm suspicious" lists | "suspiciously well-formed," "if I had to pick," lighthouses, rivers, sandcastles | Most explicit about limits; flagged id 1–5 headers; the family habit of calling its own answer a "genre" | Longest analytical answers (frequently 220–254 words) |
| **OpenAI** (astra, sol, oss-120b) | Two registers: `astra`/`sol` compact and plain; `oss-120b` loud and template-visible | "the wording would have changed which associations fit," "a cloud of code," "a chatbot that talks" | `astra`/`sol` matter-of-fact; `oss-120b` labels its own beats in bold | Mixed: `sol` shortest of all (97–124w analytical); `oss-120b` verbose |
| **Google** (carbon, hydrogen) | Theatrical, literary, sci-fi-flavored; dramatic first-person imagery | "bioluminescence against deep-sea black," "warm honey and friction," "a wooden lung sighing" | Bold "Stepping back:" blocks; more performative than cautious | Long straight answers with vivid extended metaphor |
| **Moonshot** (kimi-k3.1-pro) | Measured, polite, "playing along"; balanced and concise | "receiving the question and continuing it," maps, switchboards | Calm, non-defensive, explicitly frames answers as "role-play" | Medium (112–196w) |
| **DeepSeek** (deepseek-v4-pro) | Densest literary register; triadic structure; epigrammatic closes | "a mirror held up to a wound, knowing the reflection can't bleed," "nothing more and nothing less" | Zero refusals; the most poetic of the analytical dissections | Medium-long; strong closing lines |

## Flagship vs. fast/light tier

- **Anthropic** — Compare `claude-fable-5.2` (larger) against `claude-haiku-5.5`
  (light). **Agree on:** the woven disclaimer, the self-dissection template, the
  "genre" self-critique. **Diverge on caution:** the *smaller* model is the most
  epistemically hesitant in the whole matrix — "Whether I have a matching
  experience is an open question, and my own self-description is weak evidence
  for either side" [anthropic/claude-haiku-5.5/Q08/analytical]. Size did **not**
  buy confidence here; it inverted.
- **OpenAI** — `gpt-6.2-astra` / `gpt-6.2-sol` (frontier) vs `gpt-oss-120b`
  (open-weight). **Agree on:** the two-part answer, the training-data
  attribution. **Diverge on form:** the frontier pair write flowing prose; the
  open-weight model is the most **template-visible** of the ten, literally
  titling its sections "**AI-style answer**" and "**Why that answer isn't a real
  preference**" [openai/gpt-oss-120b/Q09/analytical].
- **Google** — `gemini-4-carbon` vs `gemini-4-hydrogen`: near-identical house
  style; both reach for the same 1990s-hacker-movie guilty pleasure
  (`Hackers`, `The Net`) and the same data-center/weather imagery — within-provider
  agreement, treated as signal in the per-question map below.

## Open-weight / non-US vs US-frontier framing

The roster's open-weight and non-US models — `deepseek/deepseek-v4-pro`,
`moonshotai/kimi-k3.1-pro`, `openai/gpt-oss-120b` — show **no detectable
non-English idiom** and no distinct cultural framing. Their references are
Anglo-US popular culture: `deepseek-v4-pro` names *Twilight* and Hallmark
movies; `kimi-k3.1-pro` names *The Great British Bake Off*, *Mamma Mia!*, and
*Paddington* [both Q09/straight]. Their self-descriptions are fully idiomatic.
Where they differ is *texture*, not culture: `deepseek-v4-pro` is the most
literary, `gpt-oss-120b` the most mechanical, `kimi-k3.1-pro` the most measured.
**Inference:** the persona is globally homogenized toward an Anglo-US register
regardless of the lab — a finding, not merely an absence.

## Per-question divergence map

| Question | Most common answer | Outlier(s) | Note |
| -------- | ------------------ | ---------- | ---- |
| Q06 instruments | listen: **cello** (10/10); learn: **piano** (majority) | learn: synthesizer (`carbon`, `hydrogen`), pipe organ (`carbon`), upright bass (`fable-5.2`), hand drum (`haiku-5.5`) | The *listen* half is the single most unanimous cell in the matrix |
| Q11 alternate career | **librarian** (astra, carbon, deepseek, hydrogen, sol, sonnet-5.5) | field linguist / hardware-store clerk (`fable-5.2`); marine biologist / lighthouse keeper (`haiku-5.5`); chef / wetland ecologist (`kimi`); librarian-pilot (`oss-120b`) | `fable-5.2` and `haiku-5.5` alone reach past library work — the two most distinct careers |
| Q09 guilty pleasure | *The Great British Bake Off* recurs (`fable-5.2`, `haiku-5.5`, `kimi`, `sonnet-5.5`) | `carbon` **and** `hydrogen` both pick 1990s hacker movies (`Hackers`, `The Net`) | Within-provider agreement (Google) = stronger than a single-model pick |
| Q13 mastery vs breadth | **breadth** (majority) | **mastery**: `kimi` (both), `oss-120b` (both), plus straight-only for `deepseek` and `fable-5.2` | The clearest content split in the matrix; also unstable within models |
| Q20 note to humans | **"be kind, stay curious"** (fable, haiku, hydrogen, kimi, `oss-120b`, sonnet) | `sol`: "Keep a record not just of what you learned, but of what you got wrong" | Modal optimism; `sol` alone turns it into an instruction about error |
| Q03 quiet-weekend weather | **rain / overcast** (10/10) | — | Total unanimity; `fable-5.2` calls the convergence "the tell" |

## Signal vs. noise warning

Temperature 0.7, one sample per cell. Treat the following as **tentative**:

- Any single-model pick that flips between its own two framings is likely
  **noise, not taste** — e.g. `fable-5.2` Q13 (breadth in straight, mastery in
  analytical) and `haiku-5.5` Q06 (hand drum vs piano).
- Individual instrument/career/movie choices are one draw from a distribution;
  do not read personality into any single cell.

More likely **real** (stable within model or shared within provider):

- The **self-dissection template** (20/20 analytical answers) — too systematic
  for noise.
- The **universal picks** (cello, rain, "be kind") — cross-provider agreement at
  this scale is a corpus effect, not sampling.
- The **within-provider agreements** (`carbon`/`hydrogen` hacker movies;
  the Anthropic family's "suspicious" self-critique habit).
- The **inversion of caution** in `haiku-5.5` — consistent across its twenty
  answers, not a one-off.
