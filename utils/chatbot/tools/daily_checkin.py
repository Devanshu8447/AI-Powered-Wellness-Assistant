# daily_checkin.py
import streamlit as st
import random
from datetime import date

# Sample affirmations with cultural relatability
AFFIRMATIONS = [
    "🌸 You are stronger than you think.",
    "🏏 Like a batsman facing fast balls, you can handle today’s challenges calmly.",
    "🎶 Even the best songs have pauses — take yours when needed.",
    "🌄 Every sunrise is a new start. Today is yours.",
    "💪 Keep going! Your effort matters more than perfection.",
    "🎭 Your feelings are valid — it’s okay to express them.",
]


def daily_checkin_tool():
    st.markdown("##  Daily Emotional Check-in")
    st.write(
        "Log your mood and track your progress. Build a streak to stay consistent with self-care!"
    )

    # --- Initialize session state ---
    if "checkin_history" not in st.session_state:
        st.session_state["checkin_history"] = {}
    if "streak" not in st.session_state:
        st.session_state["streak"] = 0
    if "last_checkin_date" not in st.session_state:
        st.session_state["last_checkin_date"] = None

    today = date.today().isoformat()

    # --- Mood Slider ---
    st.markdown("### 🎭 How are you feeling today?")
    mood = st.slider("Mood Level (Sad 😢 - Happy 😄)", 0, 10, 5)

    # --- Emoji Quick Select ---
    emoji = st.radio(
        "Pick an emoji to match your vibe:",
        ["😊", "😢", "😡", "😌", "🤔", "😴", "🥳"],
        horizontal=True,
    )

    # --- Journal Note ---
    note = st.text_area(
        "📝 Write a quick note (optional)",
        placeholder="e.g. Feeling nervous about exams...",
    )

    # --- Save Check-in ---
    if st.button("Submit Check-in"):
        # Update streak
        if st.session_state["last_checkin_date"] == (date.today().isoformat()):
            st.info("You already checked in today ✅")
        else:
            if (
                st.session_state["last_checkin_date"]
                and (
                    date.fromisoformat(today)
                    - date.fromisoformat(st.session_state["last_checkin_date"])
                ).days
                == 1
            ):
                st.session_state["streak"] += 1
            else:
                st.session_state["streak"] = 1  # reset streak

            # Save data
            st.session_state["checkin_history"][today] = {
                "mood": mood,
                "emoji": emoji,
                "note": note,
            }
            st.session_state["last_checkin_date"] = today
            st.success("✅ Check-in saved!")

    # --- Show Streak ---
    st.markdown("### 📈 Your Wellness Streak")
    st.metric("Current Streak", f"{st.session_state['streak']} days")

    # --- AI Affirmation ---
    st.markdown("### 🌟 Your Affirmation")
    affirmation = random.choice(AFFIRMATIONS)
    st.info(affirmation)

    # --- Show Previous Logs ---
    if st.checkbox("📜 Show previous check-ins"):
        for day, entry in sorted(
            st.session_state["checkin_history"].items(), reverse=True
        ):
            st.write(
                f"**{day}** - Mood: {entry['mood']}/10 {entry['emoji']} — Note: {entry['note'] or 'N/A'}"
            )
