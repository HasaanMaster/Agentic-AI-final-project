"""Chops documents into small, overlapping pieces ("chunks") for searching."""
from __future__ import annotations

from dataclasses import dataclass

from .loader import Document

# Real tokenizer to size pieces precisely; falls back to ~4 chars/token offline.
try:
    import tiktoken
    _ENC = tiktoken.get_encoding("cl100k_base")
    _HAVE_TOKENIZER = True
except Exception:
    _ENC = None
    _HAVE_TOKENIZER = False


def _count_tokens(text: str) -> int:
    if _HAVE_TOKENIZER:
        return len(_ENC.encode(text))
    return max(1, len(text) // 4)


def _split_by_size(text: str, max_tokens: int, overlap_tokens: int) -> list[str]:
    if _HAVE_TOKENIZER:
        ids = _ENC.encode(text)
        step = max_tokens - overlap_tokens
        return [_ENC.decode(ids[i:i + max_tokens]) for i in range(0, len(ids), step)]
    max_chars, overlap_chars = max_tokens * 4, overlap_tokens * 4
    step = max_chars - overlap_chars
    return [text[i:i + max_chars] for i in range(0, len(text), step)]


@dataclass
class Chunk:
    """One small, searchable piece of text and where it came from."""
    chunk_id: int
    text: str
    source: str
    location: str


def _split_one_text(text: str, max_tokens: int, overlap_tokens: int) -> list[str]:
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    pieces: list[str] = []
    current: list[str] = []
    current_tokens = 0

    def flush() -> None:
        nonlocal current, current_tokens
        if current:
            pieces.append("\n".join(current))
            current = []
            current_tokens = 0

    for para in paragraphs:
        para_tokens = _count_tokens(para)
        if para_tokens > max_tokens:
            flush()
            pieces.extend(_split_by_size(para, max_tokens, overlap_tokens))
            continue
        if current_tokens + para_tokens > max_tokens:
            flush()
        current.append(para)
        current_tokens += para_tokens

    flush()
    return pieces


def chunk_documents(
    documents: list[Document],
    max_tokens: int = 300,
    overlap_tokens: int = 50,
) -> list[Chunk]:
    """Turn a list of Documents into a flat list of small, numbered Chunks."""
    chunks: list[Chunk] = []
    chunk_id = 0
    for doc in documents:
        for piece in _split_one_text(doc.text, max_tokens, overlap_tokens):
            chunks.append(Chunk(chunk_id=chunk_id, text=piece, source=doc.source, location=doc.location))
            chunk_id += 1
    return chunks
