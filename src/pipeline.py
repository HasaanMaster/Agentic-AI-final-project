"""Shared engine: run one question through the agent team and return the result."""
from __future__ import annotations

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from src.agents.agent import root_agent
from src.config import DRAFT_ANSWER, QUERY_TYPE, REVIEW_VERDICT
from src.observability import ObservabilityPlugin

load_dotenv()

APP_NAME = "tool-stack-advisor"
USER_ID = "app"


async def run_query(question: str, session_id: str = "app") -> dict:
    """Answer one question end-to-end and return a structured result."""
    session_service = InMemorySessionService()
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)

    obs = ObservabilityPlugin()
    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service, plugins=[obs])

    message = types.Content(role="user", parts=[types.Part(text=question)])
    async for _ in runner.run_async(user_id=USER_ID, session_id=session_id, new_message=message):
        pass

    session = await session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)
    state = session.state
    return {
        "question": question,
        "answer": state.get(DRAFT_ANSWER),
        "route": state.get(QUERY_TYPE),
        "verdict": state.get(REVIEW_VERDICT),
        "metrics": obs.metrics,
    }
