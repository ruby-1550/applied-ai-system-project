from src.catalog import load_catalog
from src.vibecraft import build_playlist


def test_build_playlist_respects_avoid_genre():
    catalog = load_catalog("data/songs.csv")
    result = build_playlist("uplifting workout music, avoid pop 8 songs", catalog)
    assert len(result.items) == 8
    assert all(item.song.genre.lower() != "pop" for item in result.items)


def test_build_playlist_has_some_genre_diversity():
    catalog = load_catalog("data/songs.csv")
    result = build_playlist("chill focused study music 8 songs", catalog)
    genres = {item.song.genre.lower() for item in result.items}
    assert len(genres) >= 2

