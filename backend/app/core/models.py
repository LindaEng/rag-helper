from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class PDFDocument(Base):
    __tablename__ = "pdf_documents"

    id = Column(Integer, primary_key=True)
    filename = Column(String, unique=True)
    s3_key = Column(String)
    upload_date = Column(DateTime, default=datetime.utcnow)
    chunk_count = Column(Integer)