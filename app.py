import streamlit as st
import chess.pgn
import io

st.title("PGN Upload Test")

uploaded_file = st.file_uploader("Upload PGN file", type=["pgn"])

if uploaded_file:
    try:
        # Decode and read the PGN
        pgn_data = uploaded_file.getvalue().decode("utf-8", errors="ignore")
        pgn_io = io.StringIO(pgn_data)
        game = chess.pgn.read_game(pgn_io)

        if game:
            st.success("PGN parsed successfully!")

            st.subheader("PGN Headers")
            for key, value in game.headers.items():
                st.write(f"**{key}**: {value}")

            st.subheader("Moves")
            moves = game.board().variation_san(game.mainline())
            st.text_area("Game Moves", moves, height=300)
        else:
            st.error("Failed to parse the PGN file.")
    except Exception as e:
        st.error(f"Error reading PGN: {e}")
