import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def process_pdf(file_path: str):
    """Extract text from PDF and split into chunks"""
    
    # Open the PDF
    doc = fitz.open(file_path)
    full_text = []
    
    # Get text from each page
    for page_num, page in enumerate(doc):
        text = page.get_text()
        if text.strip():
            full_text.append(f"Page {page_num + 1}\n{text}")
    
    doc.close()
    
    # Combine all pages
    combined_text = "\n\n".join(full_text)
    
    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,      # Each chunk about 1000 characters
        chunk_overlap=200,    # Overlap between chunks (preserves context)
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = splitter.split_text(combined_text)
    
    # Delete the temporary PDF file
    os.unlink(file_path)
    
    return chunks

# Splits the textbook into bite-sized pieces.