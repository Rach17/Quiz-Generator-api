from fastapi import APIRouter, UploadFile, File, status, HTTPException, Query
from fastapi.responses import JSONResponse
from services.pdf_service import process_pdf
from services.vector_store_service import query_vector_store
from models.schemas import UploadResponse
import logging
from config import settings
from typing import Optional

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
        
        
@router.get(
    "/query",
    status_code=status.HTTP_200_OK,
    summary="Query from vector store",
    description="Query the vector store for similar documents"
)
async def get_correct_docs(
    query: str = Query(..., description="The search query string"),
    top_k: Optional[int] = Query(5, description="Number of results to return"),
    threshold: Optional[float] = Query(0.5, description="Similarity score threshold"),
):
    """
    Query the vector store for documents similar to the input query.

    Args:
        query (str): The search query string.
        top_k (int): Number of results to return. Defaults to 5.
        threshold (float): Minimum similarity score for results. Defaults to 0.5.

    Returns:
        List[QueryResult]: A list of documents and their similarity scores.
    """
    try:
        results = query_vector_store(query, top_k, threshold)
        if len(results) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No similar documents found"
            )
        return {
            "results": "success",
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Vector store query failed: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Vector store query failed"}
        )