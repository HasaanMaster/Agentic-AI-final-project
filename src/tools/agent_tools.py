"""The two tools the Researcher can call, wrapping the search engines for agent use.

Each tool's docstring is what the agent reads to decide when to use it, and each
stashes its findings in shared memory so the Reviewer can fact-check against them.
"""
from __future__ import annotations

from google.adk.tools import ToolContext

from src.config import INDEX_DIR, RETRIEVED_CONTEXT
from src.rag.vector_store import VectorStore
from src.tools.web_search import web_search as _web_search

_store: VectorStore | None = None


def _library() -> VectorStore:
    global _store
    if _store is None:
        _store = VectorStore()
        _store.load(INDEX_DIR)
    return _store


def _remember(tool_context: ToolContext, items: list[dict]) -> None:
    evidence = list(tool_context.state.get(RETRIEVED_CONTEXT, []))
    evidence.extend(items)
    tool_context.state[RETRIEVED_CONTEXT] = evidence


def search_documents(query: str, tool_context: ToolContext) -> dict:
    """Search the internal AI-tools knowledge base (the slide deck).

    Use this for what a tool IS and DOES - its purpose, features, and category.
    Best for stable facts that don't change often.

    Args:
        query: A focused, natural-language search query.

    Returns:
        A dict of the most relevant passages, each tagged with its source slide.
    """
    hits = _library().search(query, k=4)
    results = [
        {"source": f"{c.source} - {c.location}", "text": c.text, "score": round(score, 3)}
        for c, score in hits
    ]
    _remember(tool_context, [{"origin": "deck", "citation": r["source"], "text": r["text"]} for r in results])
    return {"source": "knowledge_base", "results": results}


def search_web(query: str, tool_context: ToolContext) -> dict:
    """Search the live web for current information.

    Use this for anything that changes or is recent: current PRICING, brand-new
    tools, latest versions, releases, or news.

    Args:
        query: A focused, natural-language search query.

    Returns:
        A dict of fresh web results, each with its source URL for citation.
    """
    hits = _web_search(query, max_results=5)
    results = [{"title": r.title, "url": r.url, "content": r.content} for r in hits]
    _remember(tool_context, [{"origin": "web", "citation": r["url"], "text": r["content"]} for r in results])
    return {"source": "web", "results": results}
