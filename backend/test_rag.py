import os
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent
sys.path.append(str(backend_dir))

from download_sample_papers import download_papers
from app.rag.ingestion import ingest_all_papers
from app.rag.chain import ask_question
from app.core.config import GEMINI_API_KEY

def main():
    print("=" * 60)
    print(" Research Paper Answer Bot - Phase 1 Test CLI")
    print("=" * 60)

    # 1. Download sample papers if needed
    print("\n[Step 1/3] Checking sample research papers...")
    download_papers()

    # 2. Check API Key
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        print("\n[IMPORTANT NOTICE]")
        print("GEMINI_API_KEY is not set in backend/.env!")
        print("Please open backend/.env and set your GEMINI_API_KEY before running the query step.")
        print("\nExample: GEMINI_API_KEY=AIzaSy...")
        return

    # 3. Perform ingestion
    print("\n[Step 2/3] Ingesting & indexing research papers into ChromaDB...")
    ingest_result = ingest_all_papers()
    print("Ingestion summary:", ingest_result)

    # 4. Interactive Q&A loop
    print("\n[Step 3/3] Ready for Q&A! Type 'exit' or 'quit' to stop.")
    print("-" * 60)

    sample_questions = [
        "What is the Transformer architecture and why does it replace recurrent layers?",
        "How do residual connections help in deep neural networks like ResNet?"
    ]

    print("Suggested sample questions to ask:")
    for q in sample_questions:
        print(f" - {q}")
    print("-" * 60)

    while True:
        try:
            query = input("\nAsk a question about the papers > ").strip()
            if not query:
                continue
            if query.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            print("\nSearching papers and generating grounded answer with Gemini...\n")
            res = ask_question(query)
            
            print("=" * 60)
            print("ANSWER:")
            print(res["answer"])
            print("\nSOURCES & CITATIONS:")
            for s in res["sources"]:
                print(f" - Paper: {s['paper']} | Page: {s['page']}")
                print(f"   Snippet: {s['snippet']}")
            print("=" * 60)

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nError processing question: {e}")

if __name__ == "__main__":
    main()
