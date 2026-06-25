"""Run once to build the searchable library: load -> chunk -> embed -> save."""
from src.config import KNOWLEDGE_BASE_DIR, INDEX_DIR
from src.rag.loader import load_documents
from src.rag.chunker import chunk_documents
from src.rag.vector_store import VectorStore


def main() -> None:
    print("Reading your documents...")
    docs = load_documents(KNOWLEDGE_BASE_DIR)
    print(f"  found {len(docs)} documents")

    print("Chopping them into chunks...")
    chunks = chunk_documents(docs)
    print(f"  made {len(chunks)} chunks")

    print(f"Embedding {len(chunks)} chunks with Google (this takes 10-30 seconds)...")
    store = VectorStore()
    store.build(chunks)

    store.save(INDEX_DIR)
    print(f"\nDone! Your searchable library is saved in: {INDEX_DIR}")


if __name__ == "__main__":
    main()
