"""Run the system on a question from the terminal. Usage: python -m src.ask "..." """
import asyncio
import sys

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from src.agents.agent import root_agent
from src.config import DRAFT_ANSWER, QUERY_TYPE, REVIEW_VERDICT
from src.observability import ObservabilityPlugin

load_dotenv()

APP_NAME = "tool-stack-advisor"
USER_ID = "demo"
SESSION_ID = "s1"


async def ask(question: str) -> None:
    session_service = InMemorySessionService()
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)

    obs = ObservabilityPlugin()
    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service, plugins=[obs])
    message = types.Content(role="user", parts=[types.Part(text=question)])

    print(f"\nQuestion: {question}\n")
    print("(the team is working...)\n")

    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if getattr(part, "function_call", None):
                    print(f"  -> {event.author} calls tool: {part.function_call.name}")

    session = await session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    print(f"\nManager's strategy: {session.state.get(QUERY_TYPE)}")
    print(f"Reviewer's verdict: {session.state.get(REVIEW_VERDICT)}")
    print("\n----- ANSWER -----\n")
    print(session.state.get(DRAFT_ANSWER, "(no answer produced)"))
    print()
    print(obs.summary())


def main() -> None:
    question = " ".join(sys.argv[1:]) or "What should my team use for taking meeting notes, and what does it cost?"
    asyncio.run(ask(question))


if __name__ == "__main__":
    main()
