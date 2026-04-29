import json

import streamlit as st

try:
    from .catalog import load_catalog
    from .vibecraft import build_playlist
except ImportError:  # `streamlit run src/streamlit_app.py`
    from catalog import load_catalog
    from vibecraft import build_playlist


st.set_page_config(page_title="VibeCraft Playlist Builder", layout="wide")
st.title("VibeCraft: Agentic Playlist Builder")
st.caption("Retrieval + scoring + self-check loop over a small song catalog (class project).")

catalog = load_catalog("data/songs.csv")

with st.sidebar:
    st.header("Controls")
    k = st.slider("Playlist size (k)", min_value=3, max_value=15, value=8, step=1)
    show_debug = st.checkbox("Show debug trace", value=False)

query = st.text_input(
    "What do you want to listen to?",
    value="chill lofi for studying, avoid pop",
    help='Try: "high energy pop for the gym 10 songs" or "melancholic indie pop for a rainy day"',
)

if st.button("Build playlist", type="primary") and query.strip():
    result = build_playlist(f"{query.strip()} {k} songs", catalog)

    st.subheader("Playlist")
    for i, item in enumerate(result.items, start=1):
        s = item.song
        st.markdown(f"**{i}. {s.title}** — {s.artist}  \n`{s.genre}` · `{s.mood}` · score `{item.score:.2f}`")
        st.caption(f"Because: {item.explanation}")

    if show_debug:
        st.subheader("Debug")
        st.code(json.dumps(result.debug, indent=2), language="json")
