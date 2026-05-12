from fastapi import APIRouter, HTTPException
from app.services.rag_engine import generate_answer
from pydantic import BaseModel

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    sources: list

@router.post("/chat", response_model=AnswerResponse)
async def chat(question_request: QuestionRequest):
    """Ask a question about your uploaded documents"""
    
    try:
        result = generate_answer(question_request.question)
        return AnswerResponse(
            answer=result["answer"],
            sources=result["sources"]
        )
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")
    

# Receives a question from your frontend, gets the answer from the RAG engine, and sends it back.