from fastapi import APIRouter, status, HTTPException, Query
from services.collection_service import get_collection_info, retrive_paragraphe
from models.schemas import  CheckCollectionResponse, RetriveParagrapheResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get(
    "/collection/{collection_name}",
    response_model=CheckCollectionResponse,
    summary="Get collection details",
    description="Get details of a processed PDF collection"
)
async def get_collection(collection_name: str):
    try:
        response = get_collection_info(collection_name=collection_name)
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Collection not found"
            )
            
        return response
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error fetching collection details: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch collection details"
        )
        
@router.get(
    "/extract-ansewers/{collection_name}",
    summary="Extract answers from pdf document",
    description="Extract answers from pdf document",
    responses={
        200: {"description": "Successfully extracted answers"},
        400: {"description": "Invalid request parameters"},
        500: {"description": "Answer extraction failed"}
    }
)
async def extract_answers(
    collection_name: str,
    question: str = Query(..., description="The question to extract the answer for")
) -> RetriveParagrapheResponse:
    try:
        response = await retrive_paragraphe(collection_name, question)
        return {
            "collection_name": collection_name,
            "question": question,
            "content": response.get("content"),
            "page_number": response.get("page_number")
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Answer extraction failed: %s", str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to extract answers. Please try again."
        )