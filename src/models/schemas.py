from pydantic import BaseModel, Field
from typing import List

class QuestionSchema(BaseModel):
    question: str = Field(..., min_length=10)
    options: List[str] = Field(..., min_items=4, max_items=4)
    correct_answer: str = Field(..., pattern="^option[1-4]$")

    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is the capital of France?",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "correct_answer": "option3"
            }
        }

class QuizSchema(BaseModel):
    topic: str
    difficulty: str = Field("medium", pattern="^(easy|medium|hard)$")
    questions: List[QuestionSchema]

class UploadResponse(BaseModel):
    filename: str
    content_length: int
    chunks_number: int
    
class ProcessedPDF(BaseModel):
    chunks: List[str]
    processed_content: str