"""Live web search via Tavily, for current pricing and brand-new tools."""
from __future__ import annotations

from dataclasses import dataclass

from tavily import TavilyClient

from src.config import TAVILY_API_KEY

_client = TavilyClient(api_key=TAVILY_API_KEY)


@dataclass
class WebResult:
    """One result from the live web."""
    title: str
    url: str
    content: str


def web_search(query: str, max_results: int = 5) -> list[WebResult]:
    """Search the live web and return a few clean results."""
    response = _client.search(query=query, max_results=max_results, search_depth="basic")
    return [
        WebResult(title=i.get("title", ""), url=i.get("url", ""), content=i.get("content", ""))
        for i in response.get("results", [])
    ]
