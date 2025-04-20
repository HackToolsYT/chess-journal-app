import streamlit as st
import chess.pgn
import io
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

st.set_page_config(page_title="Chess Journal & PGN Tracker", layout="centered")
st.title("♟️ Chess Journal & PGN Tracker")

DATA_FILE = "game_data.csv"

# Load existing data
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Date", "White", "Black", "Result", "TimeControl", "ECO", "Moves", "Opponent", "Score"])

uploaded_file = st.file_uploader("Upload a PGN file", type=["pgn"])

def result_score(result, player_color, winner):
    if result == "1-0" and player_color == "White":
        return 1
    elif result == "0-1" and player_color == "Black":
        return 1
    elif result == "1/2-1/2":
        return 0.5
    else:
        return 0

if uploaded_file is not None:
    try:
        pgn_text = uploaded_file.read().decode("utf-8", errors="ignore")
        pgn_io = io.StringIO(pgn_text)
        game = chess.pgn.read_game(pgn_io)

        if game is None:
            st.error("No valid game found in the PGN.")
        else:
            st.success("Game loaded successfully!")

            headers = game.headers
            date = headers.get("Date", "")
            white = headers.get("White", "")
            black = headers.get("Black", "")
            result = headers.get("Result", "")
            time_control = headers.get("TimeControl", "")
            eco = headers.get("ECO", "")
            moves = sum(1 for _ in game.mainline_moves())

            # Determine player and opponent
            player = white if "you" in white.lower() else black
            opponent = black if player == white else white
            player_color = "White" if player == white else "Black"

            # Calculate score
            score = result_score(result, player_color, result)

            # Save game info
            new_row = {
                "Date": date,
                "White": white,
                "Black": black,
                "Result": result,
                "TimeControl": time_control,
                "ECO": eco,
                "Moves": moves,
                "Opponent": opponent,
                "Score": score
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)

            # Display game info
            st.subheader("📌 Game Info")
            for key, value in headers.items():
                st.write(f"**{key}**: {value}")

            # Show moves
            st.subheader("🔁 Moves")
            board = game.board()
            moves_list = []
            for move in game.mainline_moves():
                moves_list.append(board.san(move))
                board.push(move)
            st.text_area("Game Moves (SAN)", ' '.join(moves_list), height=300)

            # Notes
            st.subheader("📝 Add Your Notes")
            notes = st.text_area("Write notes here (not yet saved persistently):", height=150)

# Show performance tracking
if not df.empty:
    st.subheader("📊 Your Performance Overview")

    df["ParsedDate"] = pd.to_datetime(df["Date"], errors='coerce')
    df = df.sort_values("ParsedDate")

    # Score Trend
    st.markdown("**Score Trend Over Time**")
    fig, ax = plt.subplots()
    ax.plot(df["ParsedDate"], df["Score"], marker='o', linestyle='--')
    ax.set_ylabel("Score (1=Win, 0.5=Draw, 0=Loss)")
    ax.set_xlabel("Date")
    st.pyplot(fig)

    # Game Count by Result
    st.markdown("**Game Outcomes**")
    outcome_counts = df["Result"].value_counts()
    st.bar_chart(outcome_counts)

    # Opening stats
    st.markdown("**Most Played Openings (ECO Codes)**")
    st.bar_chart(df["ECO"].value_counts())

    # Table
    st.markdown("**All Tracked Games**")
    st.dataframe(df[["Date", "White", "Black", "Result", "TimeControl", "ECO", "Moves", "Opponent", "Score"]])
