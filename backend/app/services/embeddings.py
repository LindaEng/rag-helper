from sentence_transformers import SentenceTransformer
from app.core.config import settings

class EmbeddingService:
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
            cls._instance._model = SentenceTransformer(settings.EMBEDDING_MODEL)
            print("Model loaded successfully!")
        return cls._instance
    
    def embed(self, texts):
        """Convert a list of texts to vectors"""
        return self._model.encode(texts).tolist()
    
    def embed_single(self, text):
        """Convert a single text to a vector"""
        return self._model.encode([text])[0].tolist()

# Create a single instance
embedding_service = EmbeddingService()

# Takes sentences and turns them into 384 numbers that represent the meaning of those sentences.