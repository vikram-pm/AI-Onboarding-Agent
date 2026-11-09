"""Streamlit demo for the P03 onboarding agent."""
import asyncio
import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Key comes from .env (local) or Streamlit secrets (deployed). Never hard-code it.
load_dotenv()
try:
    os.environ.setdefault("GOOGLE_API_KEY", st.secrets["GOOGLE_API_KEY"])
except Exception:
    pass
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "FALSE")

from onboarding_agent import logic  # noqa: E402
from onboarding_agent.runner import run_onboarding  # noqa: E402

st.set_page_config(page_title="P03 · AI Onboarding Agent", layout="wide")
st.title("AI Onboarding Agent")
st.caption("Concept project · synthetic data only · not affiliated with Cognizant or any client")

with st.sidebar:
    st.header("Joiner")
    name = st.text_input("Name", "Aisha Khan")
    segment = st.radio("Segment", ["new_hire", "switcher"], format_func={"new_hire": "New hire", "switcher": "Project switcher"}.get)
    role = st.selectbox("Role", ["Consultant", "Analyst", "Developer", "Architect", "Project manager"])
    client = st.selectbox("Client", logic.known_clients() + ["Arctic Energy (no template)"])
    province = st.selectbox("Province", ["ON", "QC", "BC", "AB"])
    language = st.radio("Language", ["en", "fr"], format_func={"en": "English", "fr": "Français"}.get, horizontal=True)
    client_steps = logic.TEMPLATES["clients"].get(client, {}).get("steps", [])
    completed = st.multiselect("Already completed", [s["id"] for s in client_steps],
                               format_func=lambda i: next(s["title"] for s in client_steps if s["id"] == i))
    run = st.button("Run agent", type="primary", use_container_width=True)

if run:
    profile = {"name": name, "segment": segment, "role": role, "client": client.replace(" (no template)", ""),
               "province": province, "language": language, "completed": completed}
    with st.spinner("Agents planning, checking and writing the nudge…"):
        out = asyncio.run(run_onboarding(profile))
    state = out["state"]

    if "hr_review" in state:
        st.warning(f"Paused for HR approval: no approved template for **{state['hr_review']['client']}**. "
                   "The agent did not guess any steps.")
    else:
        plan = state["plan"]
        a, b, c = st.columns(3)
        a.metric("Ready to contribute", f"Day {plan['ready_day']}", delta=f"{plan['ready_day'] - 10:+d} vs Day 10 target", delta_color="inverse")
        b.metric("Steps in plan", len(plan["steps"]))
        c.metric("Compliance guard", "Pass" if state.get("validation", {}).get("passed") else "Issues")
        left, right = st.columns([3, 2])
        with left:
            st.subheader("Plan, ordered by lead time")
            st.dataframe(pd.DataFrame(plan["steps"])[["order", "title", "owner", "start_day", "lead_days", "source"]],
                         hide_index=True, use_container_width=True)
            st.info(state.get("planner_note", ""))
        with right:
            st.subheader("Today's nudge")
            st.success(state.get("nudge", ""))
            st.subheader("Guard verdict")
            st.code(state.get("guard_verdict", ""))

    with st.expander("Agent trace: which agent called which tool"):
        st.dataframe(pd.DataFrame(out["trace"]), hide_index=True, use_container_width=True)
else:
    st.info("Set up a joiner in the sidebar and run the agent.")
