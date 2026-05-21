from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.services.embeddings import embedding_service
import uuid

class VectorDatabase:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = QdrantClient(":memory:")
            
            cls._instance.client.create_collection(
                collection_name="pdf_documents",
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            )
        return cls._instance
    
    def get_client(self):
        return self.client

db = VectorDatabase()

def add_documents(chunks, chunks_with_pages, filename):
    """Store document chunks with their embeddings"""
    
    client = db.get_client()
    
    # Generate embeddings for all chunks
    embeddings = embedding_service.embed(chunks)
    
    # Create points for Qdrant
    points = []
    for i, (chunk, chunk_info, embedding) in enumerate(zip(chunks, chunks_with_pages, embeddings)):
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "content": chunk,
                "source": filename,
                "chunk_index": i,
                "page_number": chunk_info["page"]
            }
        ))
    
    # Add to Qdrant
    client.upsert(
        collection_name="pdf_documents",
        points=points
    )
    
    return len(chunks)

def search_similar(query, n_results=3):
    """Search for similar chunks to the query"""
    
    client = db.get_client()
    
    # Create embedding for the query
    query_embedding = embedding_service.embed_single(query)
    
    # Search
    results = client.search(
        collection_name="pdf_documents",
        query_vector=query_embedding,
        limit=n_results,
        with_payload=True
    )
    
    # Format results
    similar_chunks = []
    for result in results:
        similar_chunks.append({
            "content": result.payload["content"],
            "source": result.payload["source"],
            "similarity_score": result.score
        })
    
    return similar_chunks

def clear_all():
    """Clear all documents from the vector store"""
    client = db.get_client()
    client.delete_collection("pdf_documents")
    from qdrant_client.models import Distance, VectorParams
    client.create_collection(
        collection_name="pdf_documents",
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

# This file creates one single connection to Qdrant (the vector database) and keeps it open so other files can use it.