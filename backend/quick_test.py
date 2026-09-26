import sys
from pathlib import Path

# Fix Windows console UTF-8 printing
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add backend directory to path
sys.path.append(str(Path(__file__).resolve().parent))

from app.rag.ingestion import ingest_all_papers
from app.rag.chain import ask_question

def test_rag_pipeline():
    print("1. Checking paper vector index in ChromaDB...")
    # Papers are already ingested, skip re-ingesting unless empty
    question = "What is the Transformer architecture and how does self-attention work?"
    print(f"\n2. Querying RAG pipeline with Gemini...\nQuestion: {question}\n")

    response = ask_question(question)
    print("=" * 60)
    print("ANSWER FROM GEMINI:")
    print(response["answer"])
    print("\nRETRIEVED CITATIONS:")
    for src in response["sources"]:
        print(f" - Paper: {src['paper']} (Page {src['page']})")
    print("=" * 60)

if __name__ == "__main__":
    test_rag_pipeline()
