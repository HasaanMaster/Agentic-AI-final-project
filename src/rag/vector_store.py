"""The searchable library: stores chunk vectors in FAISS and finds the closest ones."""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import faiss
import numpy as np

from src.rag.chunker import Chunk
from src.rag.embedder import embed_documents, embed_query

_INDEX_FILE = "index.faiss"
_CHUNKS_FILE = "chunks.json"


class VectorStore:
    def __init__(self):
        self.index = None
        self.chunks: list[Chunk] = []

    def build(self, chunks: list[Chunk]) -> None:
        """Embed every chunk and load them into the FAISS index."""
        self.chunks = chunks
        vectors = embed_documents([c.text for c in chunks])
        matrix = np.array(vectors, dtype="float32")
        faiss.normalize_L2(matrix)  # unit length, so inner product = cosine similarity
        self.index = faiss.IndexFlatIP(matrix.shape[1])
        self.index.add(matrix)

    def search(self, question: str, k: int = 4) -> list[tuple[Chunk, float]]:
        """Return the k chunks whose meaning is closest to the question."""
        q = np.array([embed_query(question)], dtype="float32")
        faiss.normalize_L2(q)
        scores, ids = self.index.search(q, k)
        return [(self.chunks[idx], float(score)) for idx, score in zip(ids[0], scores[0]) if idx != -1]

    def save(self, directory) -> None:
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(directory / _INDEX_FILE))
        with open(directory / _CHUNKS_FILE, "w", encoding="utf-8") as f:
            json.dump([asdict(c) for c in self.chunks], f, ensure_ascii=False, indent=2)

    def load(self, directory) -> None:
        directory = Path(directory)
        self.index = faiss.read_index(str(directory / _INDEX_FILE))
        with open(directory / _CHUNKS_FILE, encoding="utf-8") as f:
            self.chunks = [Chunk(**c) for c in json.load(f)]
