import os
import time
from pathlib import Path
from typing import List, Dict, Any
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import PAPERS_DIR
from app.rag.vectorstore import get_vector_store

def load_and_split_pdf(pdf_path: str) -> List[Any]:
    """Loads a PDF file, extracts pages, adds metadata, and splits into chunks."""
    filepath = Path(pdf_path)
    filename = filepath.name

    if not filepath.exists() or filepath.stat().st_size == 0:
        raise ValueError(f"PDF file is missing or empty: {filename}")

    loader = PyPDFLoader(str(filepath))
    pages = loader.load()

    if not pages:
        raise ValueError(f"No readable pages found in PDF: {filename}")

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

def ingest_single_pdf(pdf_path: str, api_key: str = None) -> Dict[str, Any]:
    """
    Ingests a single PDF into ChromaDB using deterministic IDs 
    to prevent duplicate vector records upon re-upload or re-ingestion.
    """
    chunks = load_and_split_pdf(pdf_path)
    filename = Path(pdf_path).name

    if not chunks:
        return {"status": "warning", "message": f"No text chunks created for {filename}", "count": 0}

    vector_store = get_vector_store(api_key=api_key)
    batch_size = 20

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        # Generate deterministic IDs for chunks to prevent duplicates
        batch_ids = [f"{filename}_chunk_{i + idx}" for idx in range(len(batch))]
        vector_store.add_documents(batch, ids=batch_ids)
        time.sleep(1.5)  # Pause to remain within Google Free Tier 100 RPM limit

    return {
        "status": "success",
        "filename": filename,
        "chunks_count": len(chunks)
    }

def ingest_all_papers(api_key: str = None) -> Dict[str, Any]:
    """Scans PAPERS_DIR and ingests all PDF files into ChromaDB."""
    papers_path = Path(PAPERS_DIR)
    pdf_files = list(papers_path.glob("*.pdf"))

    if not pdf_files:
        return {"status": "warning", "message": f"No PDF papers found in {PAPERS_DIR}", "count": 0}

    processed_papers = []
    total_chunks = 0

    for pdf_file in pdf_files:
        result = ingest_single_pdf(str(pdf_file), api_key=api_key)
        if result.get("status") == "success":
            processed_papers.append(pdf_file.name)
            total_chunks += result.get("chunks_count", 0)

    return {
        "status": "success",
        "processed_papers": processed_papers,
        "total_chunks_added": total_chunks
    }

if __name__ == "__main__":
    print("Starting document ingestion process...")
    res = ingest_all_papers()
    print("Ingestion Result:", res)
