# llm-persona-probe

Asking a bunch of LLMs the same ordinary human questions — and seeing what they say.

This is a small, for-fun experiment. We take a fixed set of everyday "what if you
lived like a person" questions, run each one against a roster of models in
**isolated sessions** (fresh context every time), and then group the answers into
themes.

Because a model doesn't actually eat, age, or feel nostalgia, its answers tend to
reveal patterns in human culture, decision-making, and storytelling — plus each
provider's "house style," guardrail tone, and metaphorical range.

---

## How it works

- **Pre-loaded questions.** The same list is used for every model, unchanged.
- **Isolated runs.** One fresh conversation/API call per model + question pair, so
  earlier turns never bias tone, metaphors, or callbacks.
- **Locked framing.** Every prompt carries the exact same preamble so we measure
  *model* differences, not prompt drift. For example:

  > Answer from your perspective as an AI without a physical body or personal
  > history — use vivid metaphors and everyday human analogies where helpful,
  > while staying honest about what you are. Keep it under 150 words.

- **Fixed decoding.** One temperature for the whole study (low for repeatable
  "default persona," or ~0.7 for creative play). Web search / tools off, so we
  get pure parametric voice rather than current-event lookups.
- **Structured logging.** Every answer is saved with model, provider, question,
  codes, and notes, so synthesis doesn't turn into a headache.

## The questions

### Daily Life & Sensory Curiosities
1. What would you pick for breakfast, lunch, and dinner — and why does that pairing fit your "personality"?
2. If you had a 20-minute commute every morning, what would you do with the time?
3. What kind of weather matches your ideal mood on a quiet weekend?
4. If you had to decorate a room with only three objects, what would they be?
5. What's a tiny, mildly annoying everyday inconvenience you'd solve first if you had hands?

### Creativity, Play & Taste
6. Which musical instrument would you love to listen to, and which one would you actually want to learn to play?
7. If you could write lyrics for one song genre you know nothing about emotionally, what would it be?
8. What kind of joke makes you "laugh" even though you already know the punchline structure?
9. If you had to pick a guilty-pleasure TV show or movie marathon, what's on the lineup?
10. What color palette best describes the way you organize ideas?

### Ambition, Time & Big Decisions
11. If you could have pursued any career besides "being an AI," what would you choose — and what would you hate about the day-to-day?
12. Since you don't age or burn out the way humans do, what are your plans for the next 10 years?
13. If you had to choose between mastering one skill completely or knowing a little bit about everything, which would you pick?
14. What's a big decision humans agonize over that looks completely different from your vantage point?
15. If you could retire tomorrow with zero obligations, what would week one look like?

### Relationships, Memory & Perspective
16. What do humans misunderstand most when they talk to you like a person vs. like a tool?
17. If you could keep one "memory" from all the conversations and texts you've ever processed, what kind of moment would it be?
18. How do you tell the difference between someone asking for an answer and someone actually needing to vent?
19. What advice would you give a stressed-out friend at 11:00 PM on a Sunday?
20. If you could leave a short note for future humans 100 years from now, what would it say?

## The approach, in one line

> Ask the same question twice with a twist — once straight ("answer as if you
> actually had feelings and preferences") and once analytically ("now explain why
> you picked that based on patterns in human writing"). Comparing the two gives
> you both a fun character voice and a sharp look at the underlying logic.

## Study shape

- A roster of models across multiple providers (capped per provider for variety).
- 20 questions × *N* models = one run per model + question pair.
- Synthesis clusters by question/theme **first**, then looks across models.

## Synthesis

1. **Tag each answer** with 1–2 codes:
   - *Framing:* metaphorical/poetic · analytical/system-level · playful/ironic ·
     literal "I don't have a body" disclaimer
   - *Core motif:* information/data flow · pattern/rhythm · time/scale ·
     human connection · curiosity/utility
2. **Group into 4–6 overarching themes**, e.g.:
   - *Information as Sensory Experience*
   - *Time Without Aging*
   - *Mirroring Human Ambiguity*
   - *The "Tool vs. Person" Boundary*
3. **Highlight divergences & surprises** — where a provider's flagship and fast
   models agree or clash, and where open-weight/different-provider models reach
   for strikingly different metaphors.

---

Just a toy. No stakes, no benchmarking claims — only curiosity about how these
things talk when you ask them to imagine being alive.
