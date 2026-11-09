"""ADK tools. Each reads/writes session state so agents share one source of truth."""
from google.adk.tools.tool_context import ToolContext

from . import logic


def get_templates(tool_context: ToolContext) -> dict:
    """Load the approved onboarding steps for the joiner in session state.

    Returns status 'ok' with the steps, or status 'template_gap' when the
    client has no approved template.
    """
    profile = tool_context.state["profile"]
    steps = logic.select_steps(profile)
    if steps is None:
        return {"status": "template_gap", "client": profile["client"]}
    tool_context.state["steps"] = steps
    return {"status": "ok", "steps": [{"id": s["id"], "title": s["title"]} for s in steps]}


def flag_template_gap(reason: str, tool_context: ToolContext) -> dict:
    """Pause planning and send the gap to HR for approval. Use instead of guessing steps."""
    review = {"status": "pending_hr_approval", "client": tool_context.state["profile"]["client"], "reason": reason}
    tool_context.state["hr_review"] = review
    return review


def build_plan(tool_context: ToolContext) -> dict:
    """Schedule the loaded steps by lead time, skipping steps the joiner already completed."""
    steps = tool_context.state.get("steps")
    if not steps:
        return {"error": "Call get_templates first."}
    plan = logic.build_schedule(steps, tool_context.state["profile"].get("completed", []))
    tool_context.state["plan"] = plan
    return {"ready_day": plan["ready_day"], "skipped_completed": plan["skipped_completed"],
            "steps": [{k: s[k] for k in ("order", "id", "title", "start_day", "lead_days")} for s in plan["steps"]]}


def validate_plan(tool_context: ToolContext) -> dict:
    """Check the plan: mandatory steps present, dependencies in order, no invented or auto-closed steps."""
    plan = tool_context.state.get("plan")
    if not plan:
        return {"passed": False, "issues": ["No plan to validate."]}
    result = logic.validate_plan(plan, tool_context.state["steps"], tool_context.state["profile"].get("completed", []))
    tool_context.state["validation"] = result
    return result


def get_next_step(tool_context: ToolContext) -> dict:
    """Return the joiner's first not-started step, their first name and language."""
    plan, profile = tool_context.state.get("plan"), tool_context.state["profile"]
    if not plan or not tool_context.state.get("validation", {}).get("passed"):
        return {"next_step": None}
    step = plan["steps"][0]
    return {"first_name": profile["name"].split()[0], "language": profile["language"],
            "next_step": step["title"], "lead_days": step["lead_days"], "ready_day": plan["ready_day"]}
