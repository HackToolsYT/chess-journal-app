
import streamlit as st
import chess.pgn
import io
import datetime

st.set_page_config(page_title="Chess Journal", layout="centered")
st.title("Chess Journal Tracker")

# Upload PGN
uploaded_file = st.file_uploader("Upload PGN File", type="pgn")
if uploaded_file is not None:
    pgn_text = uploaded_file.read().decode("utf-8")
    game = chess.pgn.read_game(io.StringIO(pgn_text))

    st.subheader("Game Details")
    st.write(f"**White:** {game.headers.get('White')}")
    st.write(f"**Black:** {game.headers.get('Black')}")
    st.write(f"**Result:** {game.headers.get('Result')}")
    st.write(f"**Date:** {game.headers.get('Date')}")
    st.text_area("Moves", game.board().variation_san(game.mainline()), height=200)
    st.success("Game loaded successfully!")

# Training Goals
st.subheader("Training Goals")
if "goals" not in st.session_state:
    st.session_state.goals = []

new_goal = st.text_input("Enter a new training goal")
if st.button("Add Goal") and new_goal:
    st.session_state.goals.append((new_goal, datetime.date.today()))

if st.session_state.goals:
    st.write("### Your Goals:")
    for i, (goal, date) in enumerate(st.session_state.goals, 1):
        st.write(f"{i}. {goal} _(added on {date})_")
