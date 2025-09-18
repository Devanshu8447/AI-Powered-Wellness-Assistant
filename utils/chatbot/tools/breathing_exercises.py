# breathing_exercises.py
import streamlit as st
import time

def box_breathing():
    st.write("### Box Breathing")
    st.write("Inhale for 4, Hold for 4, Exhale for 4, Hold for 4.")
    placeholder = st.empty()

    for _ in range(3): # Do 3 cycles of box breathing
        with placeholder.container():
            st.markdown(
                """
                <style>
                @keyframes expand-contract {
                    0% { transform: scale(1); opacity: 0.5; }
                    25% { transform: scale(1.5); opacity: 1; }
                    50% { transform: scale(1); opacity: 0.5; }
                    75% { transform: scale(0.5); opacity: 0.2; }
                    100% { transform: scale(1); opacity: 0.5; }
                }
                .breathing-circle-box {
                    width: 100px;
                    height: 100px;
                    background-color: #4CAF50;
                    border-radius: 50%;
                    animation: expand-contract 16s infinite; /* 4s per phase * 4 phases = 16s per cycle */
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    margin: auto;
                }
                </style>
                <div class="breathing-circle-box">Inhale</div>
                """, unsafe_allow_html=True
            )
        time.sleep(4)
        with placeholder.container():
            st.markdown(
                """
                <style>
                /* Same CSS as above for consistency */
                @keyframes expand-contract {
                    0% { transform: scale(1); opacity: 0.5; }
                    25% { transform: scale(1.5); opacity: 1; }
                    50% { transform: scale(1); opacity: 0.5; }
                    75% { transform: scale(0.5); opacity: 0.2; }
                    100% { transform: scale(1); opacity: 0.5; }
                }
                .breathing-circle-box {
                    width: 100px;
                    height: 100px;
                    background-color: #2196F3; /* Different color for hold */
                    border-radius: 50%;
                    animation: expand-contract 16s infinite;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    margin: auto;
                }
                </style>
                <div class="breathing-circle-box">Hold</div>
                """, unsafe_allow_html=True
            )
        time.sleep(4)
        with placeholder.container():
            st.markdown(
                """
                <style>
                /* Same CSS as above for consistency */
                @keyframes expand-contract {
                    0% { transform: scale(1); opacity: 0.5; }
                    25% { transform: scale(1.5); opacity: 1; }
                    50% { transform: scale(1); opacity: 0.5; }
                    75% { transform: scale(0.5); opacity: 0.2; }
                    100% { transform: scale(1); opacity: 0.5; }
                }
                .breathing-circle-box {
                    width: 100px;
                    height: 100px;
                    background-color: #FF9800; /* Different color for exhale */
                    border-radius: 50%;
                    animation: expand-contract 16s infinite;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    margin: auto;
                }
                </style>
                <div class="breathing-circle-box">Exhale</div>
                """, unsafe_allow_html=True
            )
        time.sleep(4)
        with placeholder.container():
            st.markdown(
                """
                <style>
                /* Same CSS as above for consistency */
                @keyframes expand-contract {
                    0% { transform: scale(1); opacity: 0.5; }
                    25% { transform: scale(1.5); opacity: 1; }
                    50% { transform: scale(1); opacity: 0.5; }
                    75% { transform: scale(0.5); opacity: 0.2; }
                    100% { transform: scale(1); opacity: 0.5; }
                }
                .breathing-circle-box {
                    width: 100px;
                    height: 100px;
                    background-color: #795548; /* Different color for hold */
                    border-radius: 50%;
                    animation: expand-contract 16s infinite;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    margin: auto;
                }
                </style>
                <div class="breathing-circle-box">Hold</div>
                """, unsafe_allow_html=True
            )
        time.sleep(4)
    st.success("Box breathing exercise complete!")

def four_seven_eight_breathing():
    st.write("### 4-7-8 Breathing")
    st.write("Inhale for 4, Hold for 7, Exhale for 8.")
    placeholder = st.empty()

    for _ in range(2): # Do 2 cycles
        with placeholder.container():
            st.markdown(
                """
                <style>
                @keyframes expand-contract-478 {
                    0% { transform: scale(1); opacity: 0.5; }
                    20% { transform: scale(1.5); opacity: 1; } /* Inhale 4s */
                    55% { transform: scale(1.5); opacity: 1; } /* Hold 7s */
                    95% { transform: scale(0.7); opacity: 0.3; } /* Exhale 8s */
                    100% { transform: scale(1); opacity: 0.5; }
                }
                .breathing-circle-478 {
                    width: 100px;
                    height: 100px;
                    background-color: #4CAF50;
                    border-radius: 50%;
                    animation: expand-contract-478 19s infinite; /* 4+7+8 = 19s per cycle */
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    margin: auto;
                }
                </style>
                <div class="breathing-circle-478">Inhale</div>
                """, unsafe_allow_html=True
            )
        time.sleep(4)
        with placeholder.container():
            st.markdown(
                """
                <style>
                /* Same CSS as above for consistency */
                @keyframes expand-contract-478 {
                    0% { transform: scale(1); opacity: 0.5; }
                    20% { transform: scale(1.5); opacity: 1; }
                    55% { transform: scale(1.5); opacity: 1; }
                    95% { transform: scale(0.7); opacity: 0.3; }
                    100% { transform: scale(1); opacity: 0.5; }
                }
                .breathing-circle-478 {
                    width: 100px;
                    height: 100px;
                    background-color: #2196F3;
                    border-radius: 50%;
                    animation: expand-contract-478 19s infinite;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    margin: auto;
                }
                </style>
                <div class="breathing-circle-478">Hold</div>
                """, unsafe_allow_html=True
            )
        time.sleep(7)
        with placeholder.container():
            st.markdown(
                """
                <style>
                /* Same CSS as above for consistency */
                @keyframes expand-contract-478 {
                    0% { transform: scale(1); opacity: 0.5; }
                    20% { transform: scale(1.5); opacity: 1; }
                    55% { transform: scale(1.5); opacity: 1; }
                    95% { transform: scale(0.7); opacity: 0.3; }
                    100% { transform: scale(1); opacity: 0.5; }
                }
                .breathing-circle-478 {
                    width: 100px;
                    height: 100px;
                    background-color: #FF9800;
                    border-radius: 50%;
                    animation: expand-contract-478 19s infinite;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    margin: auto;
                }
                </style>
                <div class="breathing-circle-478">Exhale</div>
                """, unsafe_allow_html=True
            )
        time.sleep(8)
    st.success("4-7-8 breathing exercise complete!")

def mindful_pause():
    st.write("### Mindful Pause")
    st.write("Take a moment to notice your breath without changing it. Observe your body and surroundings.")
    placeholder = st.empty()

    for i in range(1, 4):
        with placeholder.container():
            st.markdown(
                f"""
                <style>
                @keyframes pulse {{
                    0% {{ transform: scale(1); }}
                    50% {{ transform: scale(1.1); }}
                    100% {{ transform: scale(1); }}
                }}
                .mindful-circle {{
                    width: 120px;
                    height: 120px;
                    background-color: #9C27B0;
                    border-radius: 50%;
                    animation: pulse 2s infinite;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    color: white;
                    font-size: 20px;
                    font-weight: bold;
                    text-align: center;
                    margin: auto;
                }}
                </style>
                <div class="mindful-circle">Pause {i}</div>
                """, unsafe_allow_html=True
            )
        time.sleep(10) # 10-second pause
    st.success("Mindful pause complete!")

def breathing_exercise_tool():
    st.markdown("## 🌬️ Breathing Exercises")
    st.write("Choose an exercise to help you relax and center yourself.")

    exercise_choice = st.selectbox(
        "Select a breathing exercise:",
        ["None", "Box Breathing", "4-7-8 Breathing", "Mindful Pause"]
    )

    if exercise_choice == "Box Breathing":
        if st.button("Start Box Breathing"):
            box_breathing()
    elif exercise_choice == "4-7-8 Breathing":
        if st.button("Start 4-7-8 Breathing"):
            four_seven_eight_breathing()
    elif exercise_choice == "Mindful Pause":
        if st.button("Start Mindful Pause"):
            mindful_pause()