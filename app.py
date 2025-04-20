import streamlit as st
import chess.pgn
import io

st.set_page_config(page_title="Chess Journal", layout="centered")
st.title("♟ Chess Journal PGN Viewer")

uploaded_file = st.file_uploader("Upload a PGN file", type=["pgn"])

if uploaded_file:
    try:
        pgn_text = uploaded_file.getvalue().decode("utf-8", errors="ignore")
        game = chess.pgn.read_game(io.StringIO(pgn_text))

        if game is None:
            st.error("Could not parse PGN file. Please check the format.")
        else:
            st.success("PGN loaded successfully!")

            st.subheader("📋 Game Metadata")
            for key, value in game.headers.items():
                if key.lower() == "link":
                    st.markdown(f"**{key}:** [Game Link]({value})", unsafe_allow_html=True)
                else:
                    st.write(f"**{key}:** {value}")

            st.subheader("📜 Moves")
            board = game.board()
            moves = game.mainline_moves()
            move_list = []
            for i, move in enumerate(moves, 1):
                board.push(move)
                if i % 2 == 0:
                    move_list.append(f"{i//2}. {board.san(move)}")
                else:
                    move_list.append(board.san(move))
            st.text_area("Move List", " ".join(move_list), height=300)

    except Exception as e:
        st.error(f"An error occurred while processing the PGN: {e}")
