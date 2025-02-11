from fastapi import APIRouter, UploadFile, File, status, HTTPException
from fastapi.responses import JSONResponse
from services.pdf_service import process_pdf
from models.schemas import UploadResponse
import logging
from config import settings
from services.caching_service import CollectionCache

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Process PDF file",
    description="Upload and process PDF file for quiz generation"
)
async def upload_pdf(file: UploadFile = File(..., description="PDF file for processing")):
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed"
            )
        if file.size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size exceeds maximum limit"
            )
            
        result = await process_pdf(file)
        return {
            "collection_name": result["collection_name"],
            "chunks_number": result["chunks_number"],
            }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"PDF processing failed: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "PDF processing failed"}
        )
        
        
@router.get(
    "/collection/{collection_name}",
    summary="Get collection details",
    description="Get details of a processed PDF collection"
)
async def get_collection(collection_name: str):
    cache = CollectionCache()
    try:
        collection = cache.get_collection(collection_name)
        if collection is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Collection not found"
            )
        return {
            "collection_name": collection_name,
            "chunks_number": len(collection.get()["ids"]),
            "lifetime": collection.get("expire_time")
        }
    
    except Exception as e:
        logger.error(f"Error fetching collection details: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch collection details"
        )
        
        