import os
import time
from pathlib import Path
from typing import List, Dict, Any
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import PAPERS_DIR
from app.rag.vectorstore import get_vector_store

def load_and_split_pdf(pdf_path: str) -> List[Any]:
    filename = Path(pdf_path).name
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    # Update metadata for cleaner references
    for page in pages:
        page.metadata["source"] = filename
        if "page" in page.metadata:
            page.metadata["page"] = page.metadata["page"] + 1

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=250,
        length_function=len
    )
    chunks = text_splitter.split_documents(pages)
    return chunks

def ingest_all_papers(api_key: str = None) -> Dict[str, Any]:
    papers_path = Path(PAPERS_DIR)
    pdf_files = list(papers_path.glob("*.pdf"))

    if not pdf_files:
        return {"status": "warning", "message": f"No PDF papers found in {PAPERS_DIR}", "count": 0}

    vector_store = get_vector_store(api_key=api_key)
    total_chunks = 0
    processed_papers = []

    for pdf_file in pdf_files:
        chunks = load_and_split_pdf(str(pdf_file))
        if chunks:
            # Batch adding chunks to stay within Google API free-tier rate limits (100 RPM)
            batch_size = 20
            for i in range(0, len(chunks), batch_size):
                batch = chunks[i:i + batch_size]
                vector_store.add_documents(batch)
                time.sleep(1.5)  # Pause briefly between batches to prevent 429 Rate Limit
            
            total_chunks += len(chunks)
            processed_papers.append(pdf_file.name)

    return {
        "status": "success",
        "processed_papers": processed_papers,
        "total_chunks_added": total_chunks
    }

if __name__ == "__main__":
    print("Starting document ingestion process...")
    result = ingest_all_papers()
    print("Ingestion Result:", result)
