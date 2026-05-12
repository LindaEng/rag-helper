import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    UPLOAD_DIR = "./uploads"

settings = Settings()