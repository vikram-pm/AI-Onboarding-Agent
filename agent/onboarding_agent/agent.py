"""Multi-agent pipeline: plan builder -> compliance guard -> nudge writer."""
import os

from google.adk.agents import Agent, SequentialAgent

from .tools import build_plan, flag_template_gap, get_next_step, get_templates, validate_plan

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

plan_builder = Agent(
    name="plan_builder",
    model=MODEL,
    description="Builds a personalised onboarding plan from approved templates.",
    instruction=(
        "You build a joiner's onboarding plan. The joiner profile is already in session state.\n"
        "1. Call get_templates.\n"
        "2. If status is 'template_gap', call flag_template_gap with a one-line reason, then say "
        "HR approval is needed. Never invent or guess steps.\n"
        "3. Otherwise call build_plan, then summarise in two sentences: the ready day and why the "
        "first steps come first (longest lead times start early)."
    ),
    tools=[get_templates, flag_template_gap, build_plan],
    output_key="planner_note",
)

compliance_guard = Agent(
    name="compliance_guard",
    model=MODEL,
    description="Validates the plan against compliance rules.",
    instruction=(
        "If HR review is pending (no plan was built), reply exactly 'SKIPPED: awaiting HR approval'.\n"
        "Otherwise call validate_plan. Reply 'PASS' if it passed, or list each issue on its own line. "
        "You never mark any step complete."
    ),
    tools=[validate_plan],
    output_key="guard_verdict",
)

nudge_writer = Agent(
    name="nudge_writer",
    model=MODEL,
    description="Writes the daily next-step nudge in English or French.",
    instruction=(
        "Call get_next_step. If next_step is null, reply 'No nudge: plan not approved yet.'\n"
        "Otherwise write one Teams message under 60 words in the given language ('en' English, "
        "'fr' Canadian French): greet by first name, name the next step, say why now using the "
        "lead time, end with one call to action. Plain text, no emojis."
    ),
    tools=[get_next_step],
    output_key="nudge",
)

root_agent = SequentialAgent(
    name="onboarding_orchestrator",
    description="Plans, checks and nudges a joiner's onboarding.",
    sub_agents=[plan_builder, compliance_guard, nudge_writer],
)
