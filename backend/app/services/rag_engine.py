from app.services.vector_store import search_similar
from app.services.llm import llm_service

def generate_answer(question: str):
    similar_chunks = search_similar(question, n_results=3)
    
    if not similar_chunks:
        return {
            "answer": "No relevant information found. Please upload a PDF first.",
            "sources": []
        }
    
    context = "\n\n---\n\n".join([
        f"Source: {chunk['source']}\n{chunk['content']}"
        for chunk in similar_chunks
    ])
    
    answer = llm_service.generate(question, context)
    
    return {
        "answer": answer,
        "sources": similar_chunks
    }