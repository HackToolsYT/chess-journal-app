import streamlit as st
import chess.pgn
import io

st.set_page_config(page_title="Chess PGN Reader", layout="centered")
st.title("♟️ PGN Viewer")

uploaded_file = st.file_uploader("Upload a PGN file", type=["pgn"])

if uploaded_file is not None:
    try:
        # Decode and parse PGN
        pgn_text = uploaded_file.read().decode("utf-8", errors="ignore")
        pgn_io = io.StringIO(pgn_text)
        game = chess.pgn.read_game(pgn_io)

        if game is None:
            st.error("No valid game found in the PGN.")
        else:
            st.success("Game loaded successfully!")
            st.subheader("📌 Game Info")
            for key, value in game.headers.items():
                st.write(f"**{key}**: {value}")

            st.subheader("🔁 Moves")
            board = game.board()
            moves = game.mainline_moves()
            move_list = []
            for move in moves:
                move_list.append(board.san(move))
                board.push(move)

            st.text_area("Moves in PGN", ' '.join(move_list), height=300)

    except Exception as e:
        st.error(f"Failed to process file: {e}")
