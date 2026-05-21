from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_processor import process_pdf
from app.services.vector_store import add_documents
import os

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF file and index it for searching"""
    
    # Check if it's a PDF
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "Only PDF files are allowed")
    
    # Create uploads folder if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    
    # Save the file temporarily
    temp_path = f"uploads/{file.filename}"
    content = await file.read()
    
    with open(temp_path, "wb") as f:
        f.write(content)
    
    # Process the PDF (extract text, chunk, embed, store)
    chunks, chunks_with_pages = process_pdf(temp_path)
    chunk_count = add_documents(chunks, chunks_with_pages, file.filename)
    
    return {
        "message": "PDF processed successfully",
        "filename": file.filename,
        "chunks_stored": chunk_count
    }