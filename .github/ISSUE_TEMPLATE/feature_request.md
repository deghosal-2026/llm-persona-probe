---
name: Feature request
about: Suggest a question, model, framing, or runner improvement
title: "[feature] "
labels: enhancement
---

## What would you like to add or change

A clear description.

## Which part does it touch

- [ ] Questions (`questions/questions.json`)
- [ ] Roster (`config/models.json`)
- [ ] Framings / prompts (`config/prompts.json`)
- [ ] Runner (`run_probe.py`)
- [ ] Docs
- [ ] Analysis / synthesis

## Notes

- If it's a new question: does it still satisfy the design rules (no factual
  answer to retrieve, no safety trigger, universal references)? See
  `docs/CUSTOMIZATION.md`.
- If it's a model: confirm the id exists with `python3 run_probe.py --list-models`
  and keep the ≤3-per-provider cap.
- Does it preserve the isolation guarantee (one self-contained request per
  pair)?
