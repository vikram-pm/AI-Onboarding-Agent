"""Run the agent once for a joiner profile; return final state and a tool-call trace."""
import json
import uuid

from google.adk.runners import InMemoryRunner
from google.genai import types

from .agent import root_agent

APP = "p03_onboarding"


async def run_onboarding(profile: dict) -> dict:
    runner = InMemoryRunner(agent=root_agent, app_name=APP)
    session = await runner.session_service.create_session(
        app_name=APP, user_id="demo", session_id=str(uuid.uuid4()), state={"profile": profile})
    message = types.Content(role="user", parts=[types.Part(text="Onboard this joiner: " + json.dumps(profile))])
    trace = []
    async for event in runner.run_async(user_id="demo", session_id=session.id, new_message=message):
        for call in event.get_function_calls():
            trace.append({"agent": event.author, "tool": call.name})
    final = await runner.session_service.get_session(app_name=APP, user_id="demo", session_id=session.id)
    return {"state": dict(final.state), "trace": trace}
