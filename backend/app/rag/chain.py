from typing import Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import GEMINI_API_KEY
from app.rag.vectorstore import get_vector_store

def ask_question(question: str, api_key: str = None, top_k: int = 4) -> Dict[str, Any]:
    key = api_key or GEMINI_API_KEY
    if not key or key == "your_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY is not configured. Please set GEMINI_API_KEY in backend/.env")

    vector_store = get_vector_store(api_key=key)
    retriever = vector_store.as_retriever(search_kwargs={"k": top_k})

    # Retrieve relevant passages matching user question
    retrieved_docs = retriever.invoke(question)

    if not retrieved_docs:
        return {
            "answer": "No relevant paper passages were found.",
            "sources": []
        }

    # Construct context string and deduplicate source metadata
    context_blocks = []
    sources = []
    seen_sources = set()

    for i, doc in enumerate(retrieved_docs):
        paper_name = doc.metadata.get("source", "Unknown Paper")
        page_num = doc.metadata.get("page", 1)
        snippet = doc.page_content[:200].replace("\n", " ").strip() + "..."
        
        context_blocks.append(
            f"--- Passage {i+1} (Paper: {paper_name}, Page: {page_num}) ---\n{doc.page_content}"
        )

        source_key = (paper_name, page_num)
        if source_key not in seen_sources:
            seen_sources.add(source_key)
            sources.append({
                "paper": paper_name,
                "page": page_num,
                "snippet": snippet
            })

    context_str = "\n\n".join(context_blocks)

    # Instantiate Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=key,
        temperature=0.2
    )

    prompt = f"""You are an expert AI research assistant. Your task is to answer questions about AI and Data Science research papers based ONLY on the provided context passages.

Guidelines:
1. Answer the question accurately and clearly using ONLY the provided context.
2. Refer to the paper titles and page numbers when stating key findings.
3. If the context does not contain enough information to answer the question, state: "I could not find sufficient information in the loaded research papers to answer this question."

Context:
{context_str}

User Question: {question}
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": sources
    }
