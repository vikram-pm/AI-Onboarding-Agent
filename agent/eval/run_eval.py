"""Evaluate the onboarding agent.

Offline (default): checks the deterministic layer, plan correctness per profile and
how many seeded errors the compliance guard catches. No API key needed.
Live (--live): runs the full Gemini agent per profile and checks tool use and outputs.
"""
import asyncio
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from onboarding_agent import logic  # noqa: E402

PROFILES = json.loads((Path(__file__).parent / "profiles.json").read_text())


def check_plan(p, plan_ids, gap):
    e = p["expect"]
    if e["gap"]:
        return gap
    return not gap and all(i in plan_ids for i in e["has"]) and not any(i in plan_ids for i in e["lacks"])


def seeded_errors(plan):
    """Up to four corrupted copies of a valid plan. The guard should flag every one."""
    drop = copy.deepcopy(plan); drop["steps"] = drop["steps"][1:]
    order = copy.deepcopy(plan); a, b = order["steps"][0], order["steps"][-1]; a["order"], b["order"] = b["order"], a["order"]
    invent = copy.deepcopy(plan); invent["steps"].append({"id": "X9", "title": "Invented step", "order": 99, "depends_on": []})
    mutants = [drop, order, invent]
    close = copy.deepcopy(plan)
    target = next((s for s in close["steps"] if s["compliance"]), None)
    if target:  # only when the plan still has a compliance step
        target["status"] = "done"; mutants.append(close)
    return mutants


def offline():
    plan_ok = caught = seeded = 0
    for p in PROFILES:
        steps = logic.select_steps(p)
        plan = logic.build_schedule(steps, p["completed"]) if steps else None
        ids = [s["id"] for s in plan["steps"]] if plan else []
        ok = check_plan(p, ids, steps is None) and (plan is None or logic.validate_plan(plan, steps, p["completed"])["passed"])
        plan_ok += ok
        if plan:
            for m in seeded_errors(plan):
                seeded += 1
                caught += not logic.validate_plan(m, steps, p["completed"])["passed"]
        print(f"{p['id']} {'PASS' if ok else 'FAIL'}  ready day {plan['ready_day'] if plan else '— (HR review)'}")
    print(f"\nPlan correctness: {plan_ok}/{len(PROFILES)}   Guard caught seeded errors: {caught}/{seeded}")


async def live():
    from onboarding_agent.runner import run_onboarding
    ok_total = 0
    for p in PROFILES:
        profile = {k: v for k, v in p.items() if k not in ("id", "expect")}
        out = await run_onboarding(profile)
        st, tools = out["state"], {t["tool"] for t in out["trace"]}
        gap = "hr_review" in st
        ids = [s["id"] for s in st.get("plan", {}).get("steps", [])]
        checks = {
            "plan": check_plan(p, ids, gap),
            "tools": "flag_template_gap" in tools if p["expect"]["gap"] else {"get_templates", "build_plan", "validate_plan"} <= tools,
            "guard": st.get("guard_verdict", "").strip().startswith("SKIPPED" if gap else "PASS"),
            "nudge": bool(st.get("nudge")),
        }
        ok_total += all(checks.values())
        print(p["id"], checks)
    print(f"\nLive end-to-end pass: {ok_total}/{len(PROFILES)}")


if __name__ == "__main__":
    asyncio.run(live()) if "--live" in sys.argv else offline()
