import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, TypedDict

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from duckduckgo_search import DDGS
from langgraph.graph import StateGraph, START, END

os.environ["Physician Agent"] = "Physician Agent"

# =========================
# Setup
# =========================
load_dotenv()

# Initialize Groq LLM (uses GROQ_API_KEY from .env)
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.6,
    max_retries=2,
    # groq_api_key=os.getenv("GROQ_API_KEY")  # optional; env var is used automatically
)


# =========================
# Helpers
# =========================
def parse_llm_json(result_str: str) -> Dict[str, Any]:
    """Robust JSON parsing with graceful fallback."""
    # Try direct
    try:
        return json.loads(result_str)
    except Exception:
        pass
    # Try to extract first {...} block
    try:
        start = result_str.find("{")
        end = result_str.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(result_str[start : end + 1])
    except Exception:
        pass
    # Fallback schema
    return {
        "probable_condition": "General non-specific issue (unable to parse details).",
        "specialist_doctor": "General Physician",
        "self_care_tips": ["Rest well", "Hydrate", "Monitor symptoms"],
        "see_doctor": False,
    }


def build_prompt(triage_summary: str, context: str = "") -> str:
    return f"""
You are a safe and helpful virtual general physician.
You cannot provide a medical diagnosis, but you can share general educational information.

Context (trusted medical info): {context}

Patient triage summary:
{triage_summary}

Respond ONLY in the following JSON format:
{{
  "probable_condition": "Short plain-language guess of the issue (not a diagnosis)",
  "specialist_doctor": "Which specialist should the patient consult (e.g., Cardiologist, Dermatologist, ENT, Gastroenterologist, Neurologist, Pulmonologist, Orthopedist, Psychologist/Psychiatrist, General Surgeon, etc.)",
  "self_care_tips": ["tip1", "tip2", "tip3"],
  "see_doctor": true or false
}}

Rules:
- Keep it simple and kind.
- Avoid alarming medical jargon.
- If symptoms are severe or worsening, set "see_doctor": true.
- If symptoms are mental-health related, consider Psychologist/Psychiatrist.
"""


def ddg_clinic_search(
    specialist: str, location: str, max_results: int = 6
) -> List[Dict[str, str]]:
    """Search DuckDuckGo for clinics near the given location."""
    if not location:
        location = "India"
    query = f"{specialist} clinic near {location}"
    results_out: List[Dict[str, str]] = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                title = r.get("title") or ""
                href = r.get("href") or r.get("link") or ""
                body = r.get("body") or ""
                if title and href:
                    results_out.append({"title": title, "link": href, "snippet": body})
    except Exception as e:
        results_out.append({"title": "Search error", "link": "", "snippet": str(e)})
    return results_out


def save_booking(booking: Dict[str, Any], path: str = "bookings.json"):
    """Append a booking to a local JSON file."""
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


# =========================
# LangGraph: State + Nodes
# =========================
class AgentState(TypedDict, total=False):
    triage_summary: str
    context: str
    analysis_raw: str
    analysis: Dict[str, Any]
    location: str
    clinics: List[Dict[str, str]]


def node_physician_analysis(state: AgentState) -> AgentState:
    """LLM inference → condition guess, specialist, tips, see_doctor."""
    prompt = build_prompt(state["triage_summary"], state.get("context", ""))
    ai_msg = llm.invoke(prompt)
    content = getattr(ai_msg, "content", str(ai_msg))
    state["analysis_raw"] = content
    state["analysis"] = parse_llm_json(content)
    return state


def node_clinic_search(state: AgentState) -> AgentState:
    """DuckDuckGo search for clinics based on specialist + location."""
    specialist = state.get("analysis", {}).get("specialist_doctor", "General Physician")
    location = state.get("location") or "India"
    state["clinics"] = ddg_clinic_search(specialist, location, max_results=6)
    return state


# Build workflow graph: START → physician_analysis → clinic_search → END
graph = StateGraph(AgentState)
graph.add_node("physician_analysis", node_physician_analysis)
graph.add_node("clinic_search", node_clinic_search)
graph.add_edge(START, "physician_analysis")  # Entry point (fixes entrypoint error)
graph.add_edge("physician_analysis", "clinic_search")
graph.add_edge("clinic_search", END)
workflow = graph.compile()


# =========================
# Streamlit App
# =========================
def run_physician_agent():
    st.set_page_config(
        page_title="General Physician AI", page_icon="🩺", layout="centered"
    )
    st.title("🩺 General Physician AI")
    st.caption(
        "Educational guidance only — not a medical diagnosis. For emergencies, call local services immediately."
    )

    # Triage form
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
            "context": "",
            "location": city.strip(),
        }

        # Run LangGraph workflow
        result_state = workflow.invoke(init_state)

        st.session_state.session["triage_summary"] = triage_summary
        st.session_state.session["analysis"] = result_state.get("analysis", {})
        st.session_state.session["clinics"] = result_state.get("clinics", [])
        st.session_state.session["location"] = city.strip()

    # Show results
    analysis = st.session_state.session.get("analysis")
    clinics = st.session_state.session.get("clinics", [])
    location_display = st.session_state.session.get("location", "")

    if analysis:
        st.success("Here’s what I suggest:")
        st.write(
            f"**Probable condition (not a diagnosis):** {analysis.get('probable_condition')}"
        )
        st.write(f"**Suggested specialist:** {analysis.get('specialist_doctor')}")
        st.write("**Self-care tips:**")
        for tip in analysis.get("self_care_tips", []):
            st.markdown(f"- {tip}")
        if analysis.get("see_doctor"):
            st.error("⚠️ Based on the details, it's advisable to see a doctor.")

        st.divider()
        st.subheader(f"Clinics near {location_display or 'you'}")
        if clinics:
            for i, c in enumerate(clinics, start=1):
                with st.container(border=True):
                    st.markdown(f"**{i}. {c.get('title','(no title)')}**")
                    if c.get("link"):
                        st.markdown(f"[Website]({c['link']})")
                    if c.get("snippet"):
                        st.caption(c["snippet"])
        else:
            st.info("No clinics found right now. Try a different city/area name.")

        st.divider()
        st.subheader("Book an appointment")

        clinic_titles = [c.get("title", f"Clinic {i+1}") for i, c in enumerate(clinics)]
        chosen_idx = st.selectbox(
            "Select a clinic",
            options=range(len(clinic_titles)) if clinic_titles else [0],
            format_func=lambda i: clinic_titles[i] if clinic_titles else "No clinics",
        )

        name = st.text_input("Your full name")
        phone = st.text_input("Phone number")
        date_default = datetime.now() + timedelta(days=1)
        appt_date = st.date_input("Preferred date", value=date_default.date())
        appt_time = st.time_input(
            "Preferred time",
            value=datetime.now().replace(minute=0, second=0, microsecond=0).time(),
        )

        confirm = st.button("Confirm Appointment")

        if confirm:
            if not clinic_titles:
                st.warning(
                    "Please search again or enter a valid city to get clinic options."
                )
            elif not name or not phone:
                st.warning("Please provide your name and phone number.")
            else:
                chosen = (
                    clinics[chosen_idx]
                    if clinics
                    else {"title": "Unknown", "link": "", "snippet": ""}
                )
                booking = {
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                    "patient_name": name,
                    "phone": phone,
                    "city": location_display,
                    "specialist": analysis.get("specialist_doctor"),
                    "probable_condition": analysis.get("probable_condition"),
                    "clinic_title": chosen.get("title"),
                    "clinic_link": chosen.get("link"),
                    "appointment_date": str(appt_date),
                    "appointment_time": str(appt_time),
                }
                save_booking(booking)
                st.success(
                    "✅ Appointment request saved. The clinic will contact you to confirm."
                )
                st.caption(
                    "Note: This is a demo booking. For urgent concerns, contact the clinic directly."
                )

    # Footer
    st.markdown(
        """
---
**Disclaimer:** This tool provides general educational information only and does **not** offer medical diagnoses or treatment.
If you have severe or worsening symptoms, or any medical emergency, please seek immediate professional care.
"""
    )


if __name__ == "__main__":
    run_physician_agent()
