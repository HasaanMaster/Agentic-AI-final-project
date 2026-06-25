"""The Orchestrator agent: decides the strategy (DOCS / WEB / BOTH) for each question."""
from google.adk.agents import LlmAgent

from src.config import MODEL, QUERY_TYPE

INSTRUCTION = """You are the Orchestrator of an "AI Tool Stack Advisor."
Classify the user's question into the single best strategy.

Pick exactly one label:
- DOCS - answerable from the internal AI-tools knowledge base: what a tool is,
  what it does, its features or category.
- WEB  - needs current info: pricing, the newest tools, latest versions, or news
  (signals: "price", "cost", "latest", "newest", "2026", "today").
- BOTH - needs a capability answer AND current info (e.g. "what's good for X and
  what does it cost?").

Respond with ONLY the single label: DOCS, WEB, or BOTH. Nothing else.
"""

orchestrator = LlmAgent(
    name="Orchestrator",
    model=MODEL,
    description="Classifies the question into a DOCS / WEB / BOTH strategy.",
    instruction=INSTRUCTION,
    output_key=QUERY_TYPE,
)
