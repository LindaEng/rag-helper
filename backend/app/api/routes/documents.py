from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.models import PDFDocument

router = APIRouter()

@router.get("/documents")
async def list_documents(db: Session = Depends(get_db)):
    """List all uploaded PDFs"""
    documents = db.query(PDFDocument).all()
    return documents