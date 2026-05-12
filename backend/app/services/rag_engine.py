from app.services.vector_store import search_similar

def generate_answer(question: str):
    """Find relevant chunks and return them as an answer"""
    
    # Step 1: Search for similar chunks
    similar_chunks = search_similar(question, n_results=3)
    
    # Step 2: If nothing found
    if not similar_chunks:
        return {
            "answer": "No relevant information found. Please upload a PDF first.",
            "sources": []
        }
    
    # Step 3: Build an answer from the chunks
    answer = "Based on your document:\n\n"
    
    for i, chunk in enumerate(similar_chunks, 1):
        answer += f"{i}. {chunk['content'][:500]}...\n\n"
        answer += f"   (Source: {chunk['source']}, Relevance: {chunk['similarity_score']:.2f})\n\n"
    
    return {
        "answer": answer,
        "sources": similar_chunks
    }

'''
The RAG engine takes a user's question, searches the vector database for the most relevant text chunks using semantic similarity, and then formats those chunks into an answer with sources. In a production version, we would feed these chunks to an LLM to generate a natural language response."
'''