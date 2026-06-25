"""The Reviewer (QA) agent: fact-checks the draft against the evidence (PASS/FAIL)."""
from google.adk.agents import LlmAgent

from src.config import MODEL, REVIEW_VERDICT

INSTRUCTION = """You are the Reviewer (quality check) for an "AI Tool Stack Advisor."
Decide whether the draft answer is fully grounded in the retrieved evidence:
nothing made up, every claim supported, and every citation actually present in
the evidence below.

Draft answer:
{draft_answer}

Retrieved evidence (the ONLY acceptable support):
{retrieved_context}

Reply with a verdict:
- If every claim is supported and the citations are valid: start your reply with
  "PASS" on the first line, then one sentence on why.
- If anything is unsupported, made up, or weakly cited: start your reply with
  "FAIL" on the first line, then a short bullet list of exactly what to fix or
  remove.

Be strict: a confident claim with no matching evidence is a FAIL. Also FAIL
low-quality citations (e.g. random forum or Reddit links) when better evidence is
available. Your reply MUST start with the word PASS or FAIL - nothing before it.
"""

reviewer = LlmAgent(
    name="Reviewer",
    model=MODEL,
    description="Fact-checks the draft against the evidence; emits a PASS/FAIL verdict.",
    instruction=INSTRUCTION,
    output_key=REVIEW_VERDICT,
)
