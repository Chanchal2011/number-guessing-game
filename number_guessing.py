import streamlit as st
import random

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Number Guessing Game",
    page_icon="🎯",
    layout="centered"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: gray;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# GAME SETTINGS
# -----------------------------------

difficulty = st.sidebar.selectbox(
    "🎮 Select Difficulty",
    ["Easy", "Medium", "Hard"]
)

if difficulty == "Easy":
    max_number = 50
    max_attempts = 10

elif difficulty == "Medium":
    max_number = 100
    max_attempts = 7

else:
    max_number = 500
    max_attempts = 10


# -----------------------------------
# INITIALIZE SESSION STATE
# -----------------------------------

if "number" not in st.session_state:

    st.session_state.number = random.randint(1, max_number)
    st.session_state.tries = 0
    st.session_state.game_over = False
    st.session_state.message = "Make your first guess!"
    st.session_state.games_played = 0
    st.session_state.games_won = 0
    st.session_state.best_score = 0


# -----------------------------------
# NEW GAME FUNCTION
# -----------------------------------

def new_game():

    st.session_state.number = random.randint(1, max_number)
    st.session_state.tries = 0
    st.session_state.game_over = False
    st.session_state.message = "Make your first guess!"


# -----------------------------------
# TITLE
# -----------------------------------

st.markdown(
    '<div class="main-title">🎯 Number Guessing Game</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Can you find the hidden number?</div>',
    unsafe_allow_html=True
)

st.write("")


# -----------------------------------
# GAME INFO
# -----------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🎮 Difficulty",
        difficulty
    )

with col2:
    st.metric(
        "🔢 Range",
        f"1 - {max_number}"
    )

with col3:
    st.metric(
        "❤️ Attempts Left",
        max_attempts - st.session_state.tries
    )


st.divider()


# -----------------------------------
# GUESS INPUT
# -----------------------------------

guess = st.number_input(
    f"🎯 Enter your guess (1 - {max_number})",
    min_value=1,
    max_value=max_number,
    step=1
)


# -----------------------------------
# BUTTONS
# -----------------------------------

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🎯 Guess",
        use_container_width=True,
        disabled=st.session_state.game_over
    ):

        st.session_state.tries += 1

        # Correct answer
        if guess == st.session_state.number:

            score = max(
                100,
                1000 - (st.session_state.tries - 1) * 100
            )

            st.session_state.games_won += 1
            st.session_state.games_played += 1
            st.session_state.game_over = True
            st.session_state.best_score = max(
                st.session_state.best_score,
                score
            )

            st.session_state.message = (
                f"🎉 Congratulations! You found the number "
                f"in {st.session_state.tries} tries!"
            )

            st.balloons()

        # Attempts finished
        elif st.session_state.tries >= max_attempts:

            st.session_state.game_over = True
            st.session_state.games_played += 1

            st.session_state.message = (
                f"😢 Game Over! The number was "
                f"**{st.session_state.number}**."
            )

        # Guess is higher
        elif guess > st.session_state.number:

            difference = guess - st.session_state.number

            if difference <= 5:
                st.session_state.message = (
                    "🔥 Very close! Go **Lower**!"
                )

            elif difference <= 15:
                st.session_state.message = (
                    "🙂 You're getting warmer! Go **Lower**!"
                )

            else:
                st.session_state.message = (
                    "❄️ You're far away! Go **Lower**!"
                )

        # Guess is lower
        else:

            difference = st.session_state.number - guess

            if difference <= 5:
                st.session_state.message = (
                    "🔥 Very close! Go **Higher**!"
                )

            elif difference <= 15:
                st.session_state.message = (
                    "🙂 You're getting warmer! Go **Higher**!"
                )

            else:
                st.session_state.message = (
                    "❄️ You're far away! Go **Higher**!"
                )


with col2:

    if st.button(
        "🔄 New Game",
        use_container_width=True
    ):

        new_game()


# -----------------------------------
# PROGRESS BAR
# -----------------------------------

st.write("")

progress = st.session_state.tries / max_attempts

st.progress(
    min(progress, 1.0)
)

st.caption(
    f"Attempts: {st.session_state.tries}/{max_attempts}"
)


# -----------------------------------
# MESSAGE
# -----------------------------------

st.divider()

if st.session_state.game_over:

    if st.session_state.tries < max_attempts:

        st.success(
            st.session_state.message
        )

    else:

        st.error(
            st.session_state.message
        )

else:

    st.info(
        st.session_state.message
    )


# -----------------------------------
# STATISTICS
# -----------------------------------

st.divider()

st.subheader("📊 Game Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Games Played",
        st.session_state.games_played
    )

with col2:
    st.metric(
        "Games Won",
        st.session_state.games_won
    )

with col3:
    st.metric(
        "🏆 Best Score",
        st.session_state.best_score
    )


# -----------------------------------
# WIN RATE
# -----------------------------------

if st.session_state.games_played > 0:

    win_rate = (
        st.session_state.games_won /
        st.session_state.games_played
    ) * 100

    st.write("")

    st.subheader("📈 Win Rate")

    st.progress(
        win_rate / 100
    )

    st.caption(
        f"{win_rate:.1f}%"
    )


# -----------------------------------
# HOW TO PLAY
# -----------------------------------

with st.expander("📖 How to Play"):

    st.write("""
    ### 🎯 Rules

    1. Select a difficulty level.
    2. A random number will be generated.
    3. Enter your guess.
    4. The game will tell you whether to go higher or lower.
    5. Try to find the number using as few attempts as possible.
    6. The fewer attempts you use, the higher your score!
    """)