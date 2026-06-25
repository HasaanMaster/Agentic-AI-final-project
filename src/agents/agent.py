"""Assembles the three-agent team into one runnable system (root_agent).

Topology: Orchestrator (route), then a loop of Researcher -> Reviewer -> ReviewGate
that repeats until the answer passes review. Demonstrates four patterns: sequential
flow, hierarchical delegation, parallel tool execution, and a feedback loop.
"""
from google.adk.agents import LoopAgent, SequentialAgent

from src.agents.orchestrator import orchestrator
from src.agents.researcher import researcher
from src.agents.reviewer import reviewer
from src.agents.review_gate import ReviewGate

MAX_ROUNDS = 2

review_loop = LoopAgent(
    name="ResearchReviewLoop",
    sub_agents=[researcher, reviewer, ReviewGate(name="ReviewGate")],
    max_iterations=MAX_ROUNDS,
)

root_agent = SequentialAgent(
    name="ToolStackAdvisor",
    sub_agents=[orchestrator, review_loop],
)
