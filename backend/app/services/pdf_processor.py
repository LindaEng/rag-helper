import fitz
import os

def process_pdf(file_path: str):
    """Extract text from PDF and split into chunks"""
    
    doc = fitz.open(file_path)
    full_text = []
    
    for page_num, page in enumerate(doc):
        text = page.get_text()
        if text.strip():
            full_text.append(f"Page {page_num + 1}\n{text}")
    
    doc.close()
    combined_text = "\n\n".join(full_text)
    
    # Simple chunking
    chunks = []
    chunk_size = 1000
    paragraphs = combined_text.split('\n\n')
    
    current_chunk = ""
    for para in paragraphs:
        if len(current_chunk) + len(para) < chunk_size:
            current_chunk += para + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = para + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk)
    
    os.unlink(file_path)
    return chunks