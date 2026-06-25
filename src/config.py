"""Shared settings for the whole project, in one place."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_BASE_DIR = ROOT / "knowledge_base"
INDEX_DIR = ROOT / "faiss_index"

PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
EMBEDDING_MODEL = "text-embedding-005"

# Shared-memory keys the agents use to pass work to each other.
QUERY_TYPE = "query_type"
DRAFT_ANSWER = "draft_answer"
REVIEW_VERDICT = "review_verdict"
RETRIEVED_CONTEXT = "retrieved_context"
