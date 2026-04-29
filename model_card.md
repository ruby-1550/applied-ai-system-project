# 🎧 Model Card: VibeCraft Playlist Builder

## 1. System name

VibeCraft 1.0 (class project)

## 2. Intended use

VibeCraft generates a short playlist from a **tiny, local catalog** of songs for:
- classroom demos of retrieval + scoring + agentic self-checks
- learning about reliability testing and guardrails in AI-like systems

## 3. Non-intended use

Not intended for:
- real user music personalization
- making claims about a person’s identity, traits, or preferences
- any high-stakes setting

## 4. How it works (high level)

1) **Parse request:** extract simple constraints (ex: “avoid pop”, playlist size).  
2) **Retrieve candidates:** TF‑IDF similarity over metadata text (title/artist/genre/mood).  
3) **Score + diversify:** apply a transparent scoring function over numeric song features and add a diversity cap.  
4) **Self-check + trace:** verify constraints and emit a debug trace + logs.

## 5. Data

Catalog: `data/songs.csv` (18 songs).  
Fields: genre, mood, energy, tempo, valence, danceability, acousticness.

## 6. Known limitations and risks

- Small dataset means recommendations can feel repetitive or miss niche requests.
- Retrieval and scoring can reinforce dataset imbalances (genre/mood coverage).
- Natural language parsing is rule-based and can misunderstand nuanced phrasing.

## 7. Evaluation

Reliability checks included:
- unit tests (core behaviors, avoid-genre constraint, basic diversity)
- a small evaluation harness with predefined scenarios (`src/eval_harness.py`)

## 8. Guardrails and transparency

- Explanations include the top scoring reasons (“feature closeness” + categorical matches).
- Debug trace exposes inferred preferences, retrieval top hits, and picked genres.

## 9. Future work

- Improve the parser (richer constraint language, negation, numeric ranges).
- Add more songs and measure how retrieval quality changes with catalog size.
- Add stronger evaluation metrics (constraint satisfaction rate across many cases).

