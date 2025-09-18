import streamlit as st
from agents.physician_agent import run_physician_agent
from agents.diet_planner_agent import run_diet_planner_agent
from agents.mental_health_agent import run_mental_health_agent

st.set_page_config(page_title="Wellness Clinic AI", layout="centered")

st.title("🏥 Wellness Clinic AI")
st.subheader("Choose a service below:")

option = st.selectbox(
    "How can we help you today?",
    ["Select", "Feeling Sick?", "Diet Planner", "Mental Health Issue"],
)

if option == "Feeling Sick?":
    run_physician_agent()

elif option == "Diet Planner":
    run_diet_planner_agent()

elif option == "Mental Health Issue":
    run_mental_health_agent()
