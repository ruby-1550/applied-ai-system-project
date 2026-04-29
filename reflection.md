# Reflection (Final Project)

## What worked

- **Retrieval before scoring** made the system feel more aligned with user intent: instead of scoring every track equally, the agent starts with a “most relevant candidates” set and then scores + diversifies within that set.
- **The self-check loop** (constraints + debug trace) helped catch common issues like returning the wrong playlist size or accidentally including an avoided genre.

## What didn’t work (yet)

- Natural language parsing is still shallow. Queries like “not too fast, but still upbeat” are hard to translate into numeric targets without a language model or more robust parsing rules.
- Because the catalog is tiny, diversity constraints can sometimes fight the user’s intent (ex: requesting a very specific niche genre).

## Limitations / bias

- Any imbalance in `data/songs.csv` (genre/mood coverage) directly shapes outcomes, because retrieval and scoring can only select what exists in the catalog.
- Explanations are faithful to the scoring math, but that doesn’t guarantee they match a real listener’s preferences.

## Misuse and prevention

This could be misused as a “real music recommender” despite being a classroom demo. I prevent that by:
- labeling non-intended use in `model_card.md`
- keeping the dataset small, local, and explicitly non-personal

## Reliability surprises

The biggest surprise was how often small parsing changes caused noticeable behavior shifts. Adding “avoid pop” support, for example, required testing because it’s easy to filter too late (after scoring) and accidentally return fewer than `k` results.

## Collaboration with AI (this project)

- Helpful: AI suggestions pushed me to make the system more *observable* (debug JSON + log events), which made the agent’s decisions easier to explain and test.
- Flawed: early on, AI suggested relying on external diagram tooling; that wasn’t reliable in my environment. Generating the architecture image locally via a script was a better, reproducible approach.

