"""The loop's exit switch: stop on a PASS verdict, otherwise let the loop revise."""
from typing import AsyncGenerator

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from google.genai import types

from src.config import REVIEW_VERDICT


class ReviewGate(BaseAgent):
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        verdict = str(ctx.session.state.get(REVIEW_VERDICT, "")).lstrip()
        passed = verdict.upper().startswith("PASS")
        note = "PASS -> stop" if passed else "FAIL -> revise"
        yield Event(
            author=self.name,
            content=types.Content(parts=[types.Part(text=f"[gate] {note}")]),
            actions=EventActions(escalate=passed),
        )
