"""
Command line runner for the Music Recommender Simulation and VibeCraft.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import argparse
import json

try:
    from .recommender import load_songs, recommend_songs
    from .catalog import load_catalog
    from .vibecraft import build_playlist
except ImportError:  # Allows running as a script: `python src/main.py`
    from recommender import load_songs, recommend_songs
    from catalog import load_catalog
    from vibecraft import build_playlist


def main() -> None:
    parser = argparse.ArgumentParser(description="Music recommender + VibeCraft playlist builder")
    parser.add_argument("--query", type=str, default="", help="Natural language playlist request (VibeCraft)")
    parser.add_argument("--k", type=int, default=0, help="Playlist size override")
    parser.add_argument("--debug", action="store_true", help="Print debug JSON for VibeCraft")
    args = parser.parse_args()

    if args.query.strip():
        catalog = load_catalog("data/songs.csv")
        q = args.query.strip()
        if args.k and args.k > 0:
            q = f"{q} {args.k} songs"
        result = build_playlist(q, catalog)
        for item in result.items:
            s = item.song
            print(f"{s.title} — {s.artist} ({s.genre}, {s.mood}) | score={item.score:.2f}")
            print(f"  because: {item.explanation}")
        if args.debug:
            print("\nDEBUG:")
            print(json.dumps(result.debug, indent=2))
        return

    songs = load_songs("data/songs.csv")

    profiles = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.90,
            "tempo_bpm": 125,
            "valence": 0.85,
            "danceability": 0.85,
            "acousticness": 0.10,
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "tempo_bpm": 75,
            "valence": 0.55,
            "danceability": 0.55,
            "acousticness": 0.80,
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.95,
            "tempo_bpm": 150,
            "valence": 0.45,
            "danceability": 0.60,
            "acousticness": 0.10,
        },
        "Conflicting High-Energy Sad": {
            "genre": "indie pop",
            "mood": "melancholic",
            "energy": 0.90,
            "tempo_bpm": 110,
            "valence": 0.20,
            "danceability": 0.50,
            "acousticness": 0.60,
        },
    }

    for label, user_prefs in profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print(f"\n=== {label} ===\n")
        for rec in recommendations:
            # You decide the structure of each returned item.
            # A common pattern is: (song, score, explanation)
            song, score, explanation = rec
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
