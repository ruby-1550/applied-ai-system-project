"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from .recommender import load_songs, recommend_songs
except ImportError:  # Allows running as a script: `python src/main.py`
    from recommender import load_songs, recommend_songs


def main() -> None:
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
