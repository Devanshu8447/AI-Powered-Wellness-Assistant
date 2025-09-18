import streamlit as st

gad7_questions = [
    "Feeling nervous, anxious, or on edge",
    "Not being able to stop or control worrying",
    "Worrying too much about different things",
    "Trouble relaxing",
    "Being so restless that it's hard to sit still",
    "Becoming easily annoyed or irritable",
    "Feeling afraid as if something awful might happen"
]

def run_gad7():
    st.subheader("📊 GAD-7 Anxiety Calculator")

    scores = []
    options = ["Not at all (0)", "Several days (1)", "More than half the days (2)", "Nearly every day (3)"]

    with st.form("gad7_form"):
        for i, q in enumerate(gad7_questions):
            selected = st.radio(q, options, key=f"q{i}")
            scores.append(int(selected[-2]))  # Get score from last char
        submitted = st.form_submit_button("Calculate")

    if submitted:
        total = sum(scores)
        if total <= 4:
            level = "Minimal"
        elif total <= 9:
            level = "Mild"
        elif total <= 14:
            level = "Moderate"
        else:
            level = "Severe"

        st.info(f"Your GAD-7 Score: **{total}** → **{level} Anxiety**")
