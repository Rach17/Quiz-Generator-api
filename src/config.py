from pydantic_settings import BaseSettings
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    HUGGINGFACE_API_KEY: str
    HUGGINGFACEHUB_API_TOKEN: str
    COHERE_API_KEY: str
    CHAT_MODEL: str = "command-r-plus"
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10_000_000  # 10MB
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"

settings = Settings()