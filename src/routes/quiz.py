from fastapi import APIRouter, Body, HTTPException
from services.vector_store_service import clear_vector_store
from services.quiz_service import create_question
from models.schemas import QuizSchema, QuestionSchema
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/generate-question", 
    response_model=QuestionSchema,
    summary="Generate quiz from content",
    responses={
        200: {"description": "Successfully generated question"},
        400: {"description": "Invalid request parameters"},
        500: {"description": "Quiz generation failed"}
    }
)        
async def generate_question(
    difficulty: str = Body("medium", enum=["easy", "medium", "hard"]),
):
    try:
        response = await create_question(difficulty)
        return response
    except Exception as e:
        logger.error("Quiz generation failed: %s", str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to generate question. Please try again."
        )


