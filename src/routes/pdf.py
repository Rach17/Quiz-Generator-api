from fastapi import APIRouter, UploadFile, File, status, HTTPException
from fastapi.responses import JSONResponse
from services.pdf_service import process_pdf
from models.schemas import UploadResponse
import logging
from config import settings

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
            "filename": file.filename,
            "content_length": file.size,
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
        
        