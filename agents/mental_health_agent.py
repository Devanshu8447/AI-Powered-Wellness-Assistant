import streamlit as st
from utils.gad7_scoring import run_gad7
from utils.chatbot.frontend import run_emotion_chat
from utils.chatbot.tools.daily_checkin import daily_checkin_tool
from utils.chatbot.tools.breathing_exercises import breathing_exercise_tool


def run_mental_health_agent():
    st.subheader("🧠 Mental Health Support")

    mh_option = st.radio(
        "Choose a service",
        [
            "Calculate Anxiety Level (GAD-7)",
            "Emotion-Based Chatbot",
            "Mental Wellness Tools",
        ],
    )

    if mh_option == "Calculate Anxiety Level (GAD-7)":
        run_gad7()
    elif mh_option == "Mental Wellness Tools":
        breathing_exercise_tool()
        st.markdown("---")  # Separator
        daily_checkin_tool()
    else:
        run_emotion_chat()
