import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, TypedDict

import streamlit as st
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END

os.environ["Physician Agent"] = "Physician Agent"
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")


def parse_llm_json(result_str: str) -> Dict[str, Any]:
    """Robust JSON parsing with fallback."""
    try:
        return json.loads(result_str)
    except Exception:
        pass
    try:
        start = result_str.find("{")
        end = result_str.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(result_str[start : end + 1])
    except Exception:
        pass
    return {
        "clinics": [],
        "note": "Could not parse clinics info.",
    }


def build_prompt(triage_summary: str, location: str, specialist: str) -> str:
    return f"""
You are a helpful virtual general physician. Based on the patient triage summary and location, please provide a list of clinics nearby specialized in {specialist}.

Triage summary:
{triage_summary}

Location:
{location}

Respond ONLY in JSON with the following format:
{{
  "clinics": [
    {{
      "name": "Clinic Name",
      "address": "Address",
      "phone": "Phone number (if available)",
      "website": "Website URL (if available)"
    }},
    ...
  ]
}}

If no exact clinic info is available, list general well-known clinics or hospitals in the area.
Keep response brief and relevant.
"""


class AgentState(TypedDict, total=False):
    triage_summary: str
    location: str
    specialist: str
    analysis_raw: str
    clinics_raw: str
    clinics: List[Dict[str, str]]


def node_physician_analysis(state: AgentState) -> AgentState:
    # For demonstration, simulate physician analysis returning specialist:
    # You can expand with your existing LLM logic if needed
    state["specialist"] = "General Physician"  # default fallback
    # Could also call llm for condition guess here
    return state


def node_clinic_search(state: AgentState) -> AgentState:
    prompt = build_prompt(
        state["triage_summary"],
        state["location"],
        state.get("specialist", "General Physician"),
    )
    ai_msg = llm.invoke(prompt)
    content = getattr(ai_msg, "content", str(ai_msg))
    state["clinics_raw"] = content
    state["clinics"] = parse_llm_json(content).get("clinics", [])
    return state


graph = StateGraph(AgentState)
graph.add_node("physician_analysis", node_physician_analysis)
graph.add_node("clinic_search", node_clinic_search)
graph.add_edge(START, "physician_analysis")
graph.add_edge("physician_analysis", "clinic_search")
graph.add_edge("clinic_search", END)
workflow = graph.compile()


def save_booking(booking: Dict[str, Any], path: str = "bookings.json"):
    data = []
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []
    data.append(booking)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def run_physician_agent():
    st.set_page_config(
        page_title="General Physician AI", page_icon="🩺", layout="centered"
    )
    st.title("🩺 General Physician AI")
    st.caption("Educational guidance only — not a medical diagnosis.")

    with st.form("physician_form"):
        st.subheader("Tell me about your symptoms")
        q_symptoms = st.text_area(
            "What symptoms are you experiencing?",
            placeholder="e.g., chest pain, shortness of breath",
        )
        q_duration = st.text_input(
            "How long have you had these symptoms?", placeholder="e.g., 2 days"
        )
        q_chronic = st.text_input(
            "Do you have any chronic conditions?",
            placeholder="e.g., hypertension, diabetes",
        )
        q_meds = st.text_input(
            "Are you taking any medication?", placeholder="e.g., metformin, ibuprofen"
        )
        q_severity = st.slider("On a scale of 1 to 10, how severe is it?", 1, 10, 4)

        st.subheader("Where should I look for clinics?")
        city = st.text_input("City / Area", placeholder="e.g., Delhi, India")

        submitted = st.form_submit_button("Generate Advice & Find Clinics")

    if "session" not in st.session_state:
        st.session_state.session = {}

    if submitted:
        triage_summary = "\n".join(
            [
                f"Symptoms: {q_symptoms}",
                f"Duration: {q_duration}",
                f"Chronic conditions: {q_chronic}",
                f"Medications: {q_meds}",
                f"Severity(1-10): {q_severity}",
            ]
        )

        init_state: AgentState = {
            "triage_summary": triage_summary,
            "location": city.strip(),
        }

        result_state = workflow.invoke(init_state)

        st.session_state.session["triage_summary"] = triage_summary
        st.session_state.session["clinics"] = result_state.get("clinics", [])
        st.session_state.session["clinics_raw"] = result_state.get("clinics_raw", "")
        st.session_state.session["location"] = city.strip()

    clinics = st.session_state.session.get("clinics", [])
    location_display = st.session_state.session.get("location", "")

    if clinics:
        st.subheader(f"Clinics near {location_display or 'you'}")
        for i, c in enumerate(clinics, start=1):
            with st.container():
                st.markdown(f"**{i}. {c.get('name','Unknown Clinic')}**")
                st.write(c.get("address", ""))
                if c.get("phone"):
                    st.write(f"Phone: {c['phone']}")
                if c.get("website"):
                    st.markdown(f"[Website]({c['website']})")
    elif submitted:
        st.info(
            "No clinic information found. Try a different location or check your input."
        )

    st.markdown(
        """
---
**Disclaimer:** This tool provides general educational information only and does **not** offer medical diagnoses or treatment.
For emergencies, please contact local medical services directly.
"""
    )


if __name__ == "__main__":
    run_physician_agent()
