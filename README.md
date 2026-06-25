# AI Tool Stack Advisor — Multi-Agent Intelligence System (Google ADK)

A multi-agent assistant that recommends the right AI/software tools for a team's
needs. It grounds its answers in a curated knowledge base of product information
(**RAG**) and checks the **live web** for current pricing and new releases
(**Tavily**) — built on **Google's Agent Development Kit (ADK)**.

A **Manager** agent routes each question, a **Researcher** gathers the evidence,
and a **Fact-checker** makes sure every claim is backed by a real source before
the answer is returned.

## How it works

```
your question
      │
      ▼
  Manager (Orchestrator)  ── decides: our documents, the live web, or both
      │
      ▼
  Researcher  ── searches the document library (RAG) and/or the web (Tavily),
      │           then drafts a fully cited answer
      ▼
  Fact-checker (Reviewer)  ── is every claim backed by a source?
      │                        if not, send back to the Researcher to redo
      ▼
  a cited recommendation you can trust
```

## Project layout

| Folder / file | What lives here |
|---|---|
| `src/agents/` | The three AI agents and how they hand off work |
| `src/rag/` | Reading documents and building the searchable library |
| `src/tools/` | The Researcher's tools: library search + web search |
| `src/observability/` | Logs and metrics so we can see what the system did |
| `src/config.py` | All shared settings in one place |
| `src/main.py` | The entry point that runs the whole thing |
| `knowledge_base/` | The source documents (the AI-tools deck, etc.) |
| `tests/` | Automated checks |
| `requirements.txt` | The outside libraries the project needs |
| `.env.example` | A template for your secret keys (no real keys committed) |

## Status

🚧 Built step by step. Currently: **document loading + chunking complete.**

## Tech

Google ADK · Gemini 2.5 Flash · Vertex AI `text-embedding-005` · FAISS ·
Tavily · FastAPI · Streamlit · Cloud Run
