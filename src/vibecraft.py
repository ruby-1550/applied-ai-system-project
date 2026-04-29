from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple
import json
import logging
import os
import re

try:
    from .catalog import SongRecord, catalog_genres, catalog_moods
    from .retrieval import TfidfRetriever
    from .recommender import score_song
except ImportError:  # Allows running as scripts (ex: `streamlit run src/streamlit_app.py`)
    from catalog import SongRecord, catalog_genres, catalog_moods
    from retrieval import TfidfRetriever
    from recommender import score_song


logger = logging.getLogger("vibecraft")


@dataclass(frozen=True)
class PlaylistRequest:
    query: str
    k: int = 8
    avoid_genres: Tuple[str, ...] = ()
    min_unique_genres: int = 2


@dataclass(frozen=True)
class PlaylistItem:
    song: SongRecord
    score: float
    explanation: str
    retrieved_score: float


@dataclass(frozen=True)
class PlaylistResult:
    items: List[PlaylistItem]
    debug: Dict


def _configure_logging(level: str = "INFO") -> None:
    if logger.handlers:
        return
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


def _extract_k(query: str) -> Optional[int]:
    m = re.search(r"\b(\d{1,2})\s*(songs|tracks)\b", query.lower())
    if not m:
        return None
    k = int(m.group(1))
    return max(1, min(k, 25))


def _parse_request(query: str, catalog: List[SongRecord]) -> PlaylistRequest:
    q = query.strip()
    k = _extract_k(q) or 8
    avoid_genres: List[str] = []
    lowered = q.lower()
    for g in catalog_genres(catalog):
        if f"no {g}" in lowered or f"avoid {g}" in lowered:
            avoid_genres.append(g)

    min_unique_genres = 2
    if "single genre" in lowered or "one genre" in lowered:
        min_unique_genres = 1

    return PlaylistRequest(
        query=q,
        k=k,
        avoid_genres=tuple(sorted(set(avoid_genres))),
        min_unique_genres=min_unique_genres,
    )


def _infer_user_prefs(query: str, catalog: List[SongRecord]) -> Dict:
    lowered = query.lower()
    genres = catalog_genres(catalog)
    moods = catalog_moods(catalog)

    genre = next((g for g in genres if re.search(rf"\b{re.escape(g)}\b", lowered)), None)
    mood = next((m for m in moods if re.search(rf"\b{re.escape(m)}\b", lowered)), None)

    energy = 0.6
    if any(w in lowered for w in ["high energy", "hype", "workout", "gym", "intense", "aggressive"]):
        energy = 0.9
    if any(w in lowered for w in ["chill", "relaxed", "calm", "study", "focus", "sleep"]):
        energy = 0.4

    acousticness = 0.2
    if any(w in lowered for w in ["acoustic", "lofi", "piano", "strings"]):
        acousticness = 0.8

    tempo_bpm = 120
    if any(w in lowered for w in ["chill", "relaxed", "calm", "sleep"]):
        tempo_bpm = 80
    if any(w in lowered for w in ["run", "workout", "hype", "dance"]):
        tempo_bpm = 130

    valence = 0.6
    if any(w in lowered for w in ["happy", "uplifting", "sunny"]):
        valence = 0.85
    if any(w in lowered for w in ["sad", "melancholic", "moody"]):
        valence = 0.25

    danceability = 0.6
    if any(w in lowered for w in ["dance", "party", "club"]):
        danceability = 0.85

    return {
        "genre": genre or "pop",
        "mood": mood or "focused" if "study" in lowered or "focus" in lowered else "chill",
        "energy": energy,
        "tempo_bpm": tempo_bpm,
        "valence": valence,
        "danceability": danceability,
        "acousticness": acousticness,
    }


def _diversify(items: List[PlaylistItem], k: int, min_unique_genres: int) -> List[PlaylistItem]:
    picked: List[PlaylistItem] = []
    genre_counts: Dict[str, int] = {}
    for item in items:
        if len(picked) >= k:
            break
        g = item.song.genre.lower()
        if genre_counts.get(g, 0) >= 3:
            continue
        picked.append(item)
        genre_counts[g] = genre_counts.get(g, 0) + 1

    if min_unique_genres <= 1:
        return picked

    unique_genres = {i.song.genre.lower() for i in picked}
    if len(unique_genres) >= min_unique_genres:
        return picked

    # Backfill with next-best new genres.
    for item in items:
        if len(picked) >= k:
            break
        g = item.song.genre.lower()
        if g in unique_genres:
            continue
        picked.append(item)
        unique_genres.add(g)
        if len(unique_genres) >= min_unique_genres:
            break
    return picked


def build_playlist(query: str, catalog: List[SongRecord]) -> PlaylistResult:
    _configure_logging(os.environ.get("VIBECRAFT_LOG_LEVEL", "INFO"))

    request = _parse_request(query, catalog)
    user_prefs = _infer_user_prefs(request.query, catalog)

    logger.info("plan.start %s", json.dumps({"query": request.query, "k": request.k}))

    retriever = TfidfRetriever(catalog)
    hits = retriever.search(request.query, k=max(25, request.k * 4))
    logger.info("retrieve.done %s", json.dumps({"hits": len(hits), "top_score": hits[0].score if hits else 0.0}))

    scored: List[PlaylistItem] = []
    for hit in hits:
        song = hit.song
        if song.genre.lower() in request.avoid_genres:
            continue

        score, reasons = score_song(
            user_prefs=user_prefs,
            song={
                "id": song.id,
                "title": song.title,
                "artist": song.artist,
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "tempo_bpm": song.tempo_bpm,
                "valence": song.valence,
                "danceability": song.danceability,
                "acousticness": song.acousticness,
            },
        )
        scored.append(
            PlaylistItem(
                song=song,
                score=score + 0.25 * hit.score,
                explanation="; ".join(reasons[:4]),
                retrieved_score=hit.score,
            )
        )

    scored.sort(key=lambda i: i.score, reverse=True)
    diversified = _diversify(scored, k=request.k, min_unique_genres=request.min_unique_genres)

    debug = {
        "request": {
            "query": request.query,
            "k": request.k,
            "avoid_genres": list(request.avoid_genres),
            "min_unique_genres": request.min_unique_genres,
        },
        "user_prefs": user_prefs,
        "retrieval_top": [
            {"id": h.song.id, "title": h.song.title, "score": round(h.score, 3)} for h in hits[:5]
        ],
        "picked_genres": [i.song.genre for i in diversified],
    }
    logger.info("check.done %s", json.dumps({"picked": len(diversified), "unique_genres": len(set(debug['picked_genres']))}))
    return PlaylistResult(items=diversified, debug=debug)
