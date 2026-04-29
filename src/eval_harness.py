from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

try:
    from .catalog import SongRecord, load_catalog
    from .vibecraft import build_playlist
except ImportError:  # Allows running as scripts
    from catalog import SongRecord, load_catalog
    from vibecraft import build_playlist


@dataclass(frozen=True)
class EvalCase:
    name: str
    query: str
    k: int
    must_include_mood: Optional[str] = None
    must_avoid_genre: Optional[str] = None
    min_unique_genres: int = 2


@dataclass(frozen=True)
class EvalResult:
    case: EvalCase
    passed: bool
    checks: Dict[str, bool]


def run_case(case: EvalCase, catalog: List[SongRecord]) -> EvalResult:
    result = build_playlist(f"{case.query} {case.k} songs", catalog)
    items = result.items
    moods = [i.song.mood.lower() for i in items]
    genres = [i.song.genre.lower() for i in items]

    checks: Dict[str, bool] = {
        "count_k": len(items) == case.k,
        "unique_genres": len(set(genres)) >= case.min_unique_genres,
    }

    if case.must_include_mood:
        checks["include_mood"] = case.must_include_mood.lower() in moods
    if case.must_avoid_genre:
        checks["avoid_genre"] = case.must_avoid_genre.lower() not in genres

    passed = all(checks.values())
    return EvalResult(case=case, passed=passed, checks=checks)


def run_suite(cases: List[EvalCase], catalog_csv: str = "data/songs.csv") -> List[EvalResult]:
    catalog = load_catalog(catalog_csv)
    return [run_case(c, catalog) for c in cases]


DEFAULT_CASES: List[EvalCase] = [
    EvalCase(
        name="Study lofi",
        query="chill lofi for studying, focus",
        k=8,
        must_include_mood="chill",
        must_avoid_genre=None,
        min_unique_genres=2,
    ),
    EvalCase(
        name="Avoid pop",
        query="uplifting workout music, avoid pop",
        k=8,
        must_include_mood=None,
        must_avoid_genre="pop",
        min_unique_genres=2,
    ),
]
