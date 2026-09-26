"""
=============================================================================
VECTORSTORE MODULE: Vector Embeddings & Similarity Search Storage
=============================================================================

Key Concept:
  Text Passages: "Transformers use attention..."
          │
          ▼
   Embedding Model (Google Gemini: models/gemini-embedding-001)
          │
          ▼
   High-Dimensional Vector: [0.021, -0.183, 0.742, ...]
          │
          ▼
   ChromaDB (Saved locally on disk in data/vector_db/)
          │
          ▼
   Similarity Search (Finds chunks with matching vector angles)

The vector is NOT the answer itself. It is a mathematical representation of 
the semantic MEANING of the text. This allows ChromaDB to perform vector 
distance math to quickly retrieve passages relevant to any question.
=============================================================================
"""

import sys
from pathlib import Path

# Add backend directory to sys.path for direct execution
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import GEMINI_API_KEY, VECTOR_DB_DIR

def get_embedding_function(api_key: str = None) -> GoogleGenerativeAIEmbeddings:
    """
    Returns the Google Gemini Embedding model instance.
    This model converts text strings into numerical vectors.
    """
    key = api_key or GEMINI_API_KEY
    if not key or key == "your_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY is missing. Please set GEMINI_API_KEY in backend/.env")
    
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=key
    )

def get_vector_store(api_key: str = None) -> Chroma:
    """
    Initializes and returns the persistent ChromaDB vector store.
    Chroma handles storing vector embeddings along with document text & metadata 
    (Paper Name, Page Number).
    """
    embeddings = get_embedding_function(api_key)
    return Chroma(
        persist_directory=VECTOR_DB_DIR,
        embedding_function=embeddings,
        collection_name="research_papers"
    )

if __name__ == "__main__":
    print("Testing VectorStore module...")
    store = get_vector_store()
    print("Vector Store successfully initialized at:", VECTOR_DB_DIR)
