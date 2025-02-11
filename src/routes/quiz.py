from fastapi import APIRouter, HTTPException, Query
from services.quiz_service import  create_quiz
from models.schemas import QuizSchema
from config import settings
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/generate-quiz/{collection_name: str}",
    response_model=QuizSchema,
    summary="Generate quiz from content",
    responses={
        200: {"description": "Successfully generated quiz"},
        400: {"description": "Invalid request parameters"},
        500: {"description": "Quiz generation failed"}
    }
)
async def generate_quiz(
    collection_name: str,
    difficulty: str = Query("medium", enum=["easy", "medium", "hard"]),
    questions_number: int = Query(5, description="Number of questions to generate"),
):
    try:
        if questions_number > settings.MAX_QUIZ_QUESTIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Questions number exceeds maximum limit of {settings.MAX_QUESTIONS}"
            )
        response = await create_quiz(collection_name, difficulty, questions_number)
        return response
    
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Quiz generation failed: %s", str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to generate quiz. Please try again."
        )