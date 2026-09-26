# Research Paper Answer Bot 🤖📚

A full-stack RAG (Retrieval-Augmented Generation) application built with **React.js**, **FastAPI**, **LangChain**, **ChromaDB**, and **Google Gemini API**.

The application retrieves relevant passages from AI & Data Science research papers and generates grounded answers with supporting paper titles and page numbers.

---

## 🏗️ Project Architecture

* **Frontend:** React.js (Vite), Axios, Lucide Icons, CSS
* **Backend:** FastAPI (Python 3.10+), Uvicorn, Pydantic
* **RAG Engine:** LangChain, PyPDF, ChromaDB (Local Persistent Vector Store)
* **LLM & Embeddings:** Google Gemini API (`models/text-embedding-004` & `gemini-2.0-flash`)

---

## 🚀 Quick Start Guide

### Step 1: Configure Gemini API Key

Open `backend/.env` and replace `your_gemini_api_key_here` with your actual Google Gemini API key:

```env
GEMINI_API_KEY=AIzaSyYourActualApiKeyHere
PAPERS_DIR=data/papers
VECTOR_DB_DIR=data/vector_db
```

---

### Step 2: Option A - Run Phase 1 CLI Test Script

To test the RAG pipeline directly in your terminal:

```bash
cd backend
.\.venv\Scripts\python test_rag.py
```

This will automatically download sample arXiv papers (*Attention Is All You Need* & *ResNet*), index them into ChromaDB, and let you ask questions interactively.

---

### Step 3: Option B - Run Full-Stack Web Application

#### 1. Start FastAPI Backend:

```bash
cd backend
.\.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
```
* Backend API: `http://localhost:8000`
* Interactive API Documentation (Swagger): `http://localhost:8000/docs`

#### 2. Start React Frontend:

Open a new terminal tab/window:

```bash
cd frontend
npm run dev
```
* Frontend Web App: `http://localhost:5173`

---

## 📂 Project Structure

```text
RAG/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py      # FastAPI endpoints (/chat, /papers, /upload)
│   │   ├── core/
│   │   │   └── config.py      # Env & path configurations
│   │   ├── rag/
│   │   │   ├── chain.py       # LangChain Q&A pipeline
│   │   │   ├── ingestion.py   # PDF splitter & embedder
│   │   │   └── vectorstore.py # ChromaDB vector store
│   │   └── main.py            # FastAPI entry point
│   ├── data/
│   │   ├── papers/            # Storage for research paper PDFs
│   │   └── vector_db/         # ChromaDB vector store database
│   ├── test_rag.py            # Phase 1 CLI test script
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/client.js
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   └── SourceCard.jsx
│   │   ├── App.jsx
│   │   └── App.css
│   └── package.json
└── README.md
```
