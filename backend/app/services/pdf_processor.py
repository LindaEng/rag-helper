import fitz
import os

def process_pdf(file_obj):
    """Extract text from PDF and split into chunks"""
    
    doc = fitz.open(stream=file_obj, filetype="pdf")
    chunks_with_pages = []
    seen_text = set()  # Track seen content
    
    for page_num, page in enumerate(doc):
        text = page.get_text()
        if text.strip():
            page_chunks = split_text_with_page(text, page_num + 1)
            
            # Deduplicate chunks
            for chunk in page_chunks:
                # Create a simple hash of first 200 chars
                content_hash = chunk["text"][:200]
                if content_hash not in seen_text:
                    seen_text.add(content_hash)
                    chunks_with_pages.append(chunk)
    
    doc.close()
    chunks = [chunk["text"] for chunk in chunks_with_pages]
    return chunks, chunks_with_pages

def split_text_with_page(text: str, page_num: int, chunk_size: int = 1000):
    chunks = []

    # split by paragraphs
    paragraphs = text.split('\n\n')
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) < chunk_size:
            current_chunk += para + "\n\n"
        else:
            if current_chunk:
                chunks.append({
                    "text": current_chunk.strip(),
                    "page": page_num
                })
            current_chunk = para + "\n\n"
    
    if current_chunk:
        chunks.append({
            "text": current_chunk.strip(),
            "page": page_num
        })
    
    return chunks