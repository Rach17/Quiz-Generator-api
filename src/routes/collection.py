from fastapi import APIRouter, status, HTTPException
from services.collection_service import get_collection_info
from models.schemas import  CheckCollectionResponse
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
        
        