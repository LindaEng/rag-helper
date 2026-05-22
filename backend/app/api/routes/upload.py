from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_processor import process_pdf
from app.services.vector_store import add_documents
from app.services.s3_service import s3_service
import io

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF file to S3 and index it for searching"""
    
    # Check if it's a PDF
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "Only PDF files are allowed")
    
    # Read file content
    content = await file.read()
    
    # Upload to S3
    try:
        s3_key = s3_service.upload_pdf(content, file.filename)
    except Exception as e:
        raise HTTPException(500, f"S3 upload failed: {str(e)}")
    
    # Process the PDF from bytes
    chunks, chunks_with_pages = process_pdf(io.BytesIO(content))
    chunk_count = add_documents(chunks, chunks_with_pages, file.filename)
    
    return {
        "message": "PDF processed and stored successfully",
        "filename": file.filename,
        "s3_key": s3_key,
        "chunks_stored": chunk_count
    }