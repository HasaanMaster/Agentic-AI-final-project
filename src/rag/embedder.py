"""Turns text into embeddings via Google's text-embedding-005 model on Vertex AI."""
from __future__ import annotations

from google import genai
from google.genai import types

from src.config import PROJECT, LOCATION, EMBEDDING_MODEL

_client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)


def _embed_one(text: str, task_type: str) -> list[float]:
    resp = _client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(task_type=task_type),
    )
    return resp.embeddings[0].values


def embed_documents(texts: list[str]) -> list[list[float]]:
    """Embed chunks we're storing in the library."""
    return [_embed_one(t, "RETRIEVAL_DOCUMENT") for t in texts]


def embed_query(text: str) -> list[float]:
    """Embed a single question someone is asking."""
    return _embed_one(text, "RETRIEVAL_QUERY")
