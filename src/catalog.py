from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional
import csv


@dataclass(frozen=True)
class SongRecord:
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

    @property
    def text(self) -> str:
        return " ".join(
            [
                self.title,
                self.artist,
                self.genre,
                self.mood,
            ]
        ).lower()


def load_catalog(csv_path: str | Path) -> List[SongRecord]:
    path = Path(csv_path)
    songs: List[SongRecord] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append(
                SongRecord(
                    id=int(row["id"]),
                    title=row["title"],
                    artist=row["artist"],
                    genre=row["genre"],
                    mood=row["mood"],
                    energy=float(row["energy"]),
                    tempo_bpm=float(row["tempo_bpm"]),
                    valence=float(row["valence"]),
                    danceability=float(row["danceability"]),
                    acousticness=float(row["acousticness"]),
                )
            )
    return songs


def list_unique(values: Iterable[str]) -> List[str]:
    return sorted({v.strip().lower() for v in values if v and v.strip()})


def catalog_genres(catalog: List[SongRecord]) -> List[str]:
    return list_unique(s.genre for s in catalog)


def catalog_moods(catalog: List[SongRecord]) -> List[str]:
    return list_unique(s.mood for s in catalog)

