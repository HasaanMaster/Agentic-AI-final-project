"""Quick test of searching the library by meaning. Usage: python -m src.search_demo "..." """
import sys

from src.config import INDEX_DIR
from src.rag.vector_store import VectorStore


def main() -> None:
    question = " ".join(sys.argv[1:]) or "What tools are good for taking meeting notes?"
    store = VectorStore()
    store.load(INDEX_DIR)
    print(f"\nQuestion: {question}\n")
    for chunk, score in store.search(question, k=3):
        snippet = chunk.text.replace("\n", " ")[:180]
        print(f"  [match {score:.3f}]  {chunk.source} - {chunk.location}")
        print(f"  {snippet}...\n")


if __name__ == "__main__":
    main()
