from pydantic import BaseModel, Field
from typing import List
from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Literal

class QuestionSchema(BaseModel):
    question: str = Field(..., description="The multiple-choice question")
    option_a: str = Field(..., description="Option A for the question")
    option_b: str = Field(..., description="Option B for the question")
    option_c: str = Field(..., description="Option C for the question")
    option_d: str = Field(..., description="Option D for the question")
    correct_answer: Literal['A', 'B', 'C', 'D'] = Field(
        ..., 
        description="The correct answer (must match an existing option)"
    )

    @field_validator('correct_answer')
    def validate_correct_answer(cls, v: str, info: ValidationInfo) -> str:
        # Access the model's data using info.data
        option_field = f'option_{v.lower()}'
        if not info.data.get(option_field):
            raise ValueError(f'Correct answer {v} specified but corresponding option is missing')
        return v


class QuizSchema(BaseModel):
    name : str = Field("Quizz", description="The name of the quiz")
    difficulty: str = Field("Easy", pattern="^(easy|medium|hard)$")
    questions: List[QuestionSchema]

class UploadResponse(BaseModel):
    filename: str
    content_length: int
    chunks_number: int
    
class ProcessedPDF(BaseModel):
    chunks: List[str]
    processed_content: str