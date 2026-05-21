import fitz
import os

def process_pdf(file_path: str):
    ''' Extracts text from PDF and splits into chunks with page numbers'''

    doc = fitz.open(file_path)

    chunks_with_pages = []

    for page_num, page in enumerate(doc):
        text = page.get_text()
        if text.strip(): #skips blank pages
            page_chunks = split_text_with_page(text, page_num + 1)
            chunks_with_pages.extend(page_chunks)
    
    doc.close()

    chunks = [chunk["text"] for chunk in chunks_with_pages]

    os.unlink(file_path)
    # return page metadata for later use
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