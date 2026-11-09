"""Deterministic core: step selection, lead-time scheduling, validation.

The LLM agents decide *when* to call these and explain the result; the rules
that must never be wrong (mandatory steps, dependency order, compliance) live here.
"""
import json
from pathlib import Path

TEMPLATES = json.loads((Path(__file__).parent.parent / "data" / "templates.json").read_text())


def known_clients():
    return list(TEMPLATES["clients"])


def select_steps(profile: dict) -> list[dict] | None:
    """Approved steps for this joiner, or None if the client has no template."""
    client = TEMPLATES["clients"].get(profile["client"])
    if client is None:
        return None
    steps = list(TEMPLATES["company"]) if profile["segment"] == "new_hire" else []
    steps += client["steps"]
    steps += TEMPLATES["provinces"].get(profile["province"], [])
    access_id = next(s["id"] for s in client["steps"] if "system access" in s["title"])
    for s in TEMPLATES["project"]:
        s = dict(s, depends_on=[access_id if d == "CLIENT_ACCESS" else d for d in s["depends_on"]])
        steps.append(s)
    return [dict(s) for s in steps]


def build_schedule(steps: list[dict], completed: list[str]) -> dict:
    """Earliest-start schedule in working days; long lead times start first."""
    done = set(completed)
    todo = {s["id"]: dict(s) for s in steps if s["id"] not in done}
    finish: dict[str, int] = {}

    def fin(step_id: str) -> int:
        if step_id not in todo:  # already done, or satisfied outside this plan
            return 0
        if step_id not in finish:
            s = todo[step_id]
            s["start_day"] = max([fin(d) for d in s["depends_on"]] + [0]) + 1
            finish[step_id] = s["start_day"] + s["lead_days"] - 1
        return finish[step_id]

    for sid in todo:
        fin(sid)
    plan = sorted(todo.values(), key=lambda s: (s["start_day"], -s["lead_days"]))
    for n, s in enumerate(plan, 1):
        s.update(order=n, finish_day=finish[s["id"]], status="not_started")
    return {"steps": plan, "ready_day": max(finish.values(), default=0),
            "skipped_completed": sorted(done & {s["id"] for s in steps})}


def validate_plan(plan: dict, required: list[dict], completed: list[str]) -> dict:
    """Compliance guard: mandatory coverage, dependency order, no invented or auto-closed steps."""
    issues = []
    approved = {s["id"] for s in required}
    in_plan = {s["id"]: s for s in plan["steps"]}
    order = {s["id"]: s["order"] for s in plan["steps"]}
    for s in required:
        if s["mandatory"] and s["id"] not in in_plan and s["id"] not in completed:
            issues.append(f"Missing mandatory step {s['id']} ({s['title']})")
    for s in plan["steps"]:
        if s["id"] not in approved:
            issues.append(f"Step {s['id']} is not in an approved template")
        if s.get("compliance") and s.get("status") == "done":
            issues.append(f"Compliance step {s['id']} was marked done by the agent")
        for d in s.get("depends_on", []):
            if d in order and order[d] > s["order"]:
                issues.append(f"{s['id']} is ordered before its dependency {d}")
    return {"passed": not issues, "issues": issues}
