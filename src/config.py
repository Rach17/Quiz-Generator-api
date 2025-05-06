from pydantic_settings import BaseSettings
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    HUGGINGFACE_API_KEY: str
    COHERE_API_KEY: str
    CHAT_MODEL: str = "command-r-plus"
    EMBEDDING_MODEL: str = "embed-multilingual-v3.0"
    MAX_FILE_SIZE: int = 50_000_000  # 50MB
    MAX_QUIZ_QUESTIONS: int = 100
    COLLECTION_LIFETIME: float = 60 * 60 * 24 # 24 hours :
    CORS_ORIGINS: List[str] = ["*"]  # Allow all origins
    
    class Config:
        env_file = ".env"

settings = Settings()