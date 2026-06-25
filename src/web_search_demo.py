"""Quick test of the live web-search tool. Usage: python -m src.web_search_demo "..." """
import sys

from src.tools.web_search import web_search


def main() -> None:
    query = " ".join(sys.argv[1:]) or "Notion AI current pricing 2026"
    print(f"\nSearching the live web for: {query}\n")
    for r in web_search(query, max_results=4):
        print(f"- {r.title}")
        print(f"  {r.url}")
        print(f"  {r.content[:160]}...\n")


if __name__ == "__main__":
    main()
