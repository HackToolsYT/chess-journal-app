import streamlit as st
import chess.pgn
import io
import datetime

st.set_page_config(page_title="Chess Journal", layout="centered")
st.title("Chess Journal Tracker")

# --- PGN Upload ---
uploaded_file = st.file_uploader("Upload PGN File", type="pgn")

if uploaded_file:
    pgn_text = uploaded_file.getvalue().decode("utf-8", errors="ignore")
    game = chess.pgn.read_game(io.StringIO(pgn_text))

    if game:
        st.subheader("Game Metadata")

        # Display all available headers
        for key, value in game.headers.items():
            st.write(f"**{key}:** {value}")

        # Show full PGN move text
        st.subheader("Moves")
        moves = game.board().variation_san(game.mainline())
        st.text_area("PGN Moves", moves, height=300)

        st.success("PGN loaded successfully!")
    else:
        st.error("Could not read PGN file. Please check the format.")
