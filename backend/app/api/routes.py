from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from pathlib import Path
import shutil

from app.core.config import PAPERS_DIR
from app.rag.chain import ask_question
from app.rag.ingestion import ingest_all_papers, load_and_split_pdf
from app.rag.vectorstore import get_vector_store

router = APIRouter(prefix="/api")

class ChatRequest(BaseModel):
    question: str
    api_key: Optional[str] = None

class SourceReference(BaseModel):
    paper: str
    page: int
    snippet: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceReference]

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    try:
        result = ask_question(question=request.question, api_key=request.api_key)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@router.get("/papers")
async def list_papers():
    papers_path = Path(PAPERS_DIR)
    if not papers_path.exists():
        return {"papers": []}
    
    pdf_files = [f.name for f in papers_path.glob("*.pdf")]
    return {"papers": pdf_files}

@router.post("/upload")
async def upload_paper(file: UploadFile = File(...), api_key: Optional[str] = Form(None)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    save_path = Path(PAPERS_DIR) / file.filename
    try:
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Automatically ingest newly uploaded paper into VectorDB
        chunks = load_and_split_pdf(str(save_path))
        if chunks:
            vector_store = get_vector_store(api_key=api_key)
            vector_store.add_documents(chunks)
        
        return {
            "filename": file.filename,
            "status": "success",
            "message": f"Successfully uploaded and indexed {len(chunks)} chunks from {file.filename}."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file upload: {str(e)}")

@router.post("/ingest")
async def trigger_ingestion(api_key: Optional[str] = None):
    try:
        result = ingest_all_papers(api_key=api_key)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")
