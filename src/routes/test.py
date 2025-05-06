from fastapi import APIRouter, HTTPException
from utils.embeddings_utils import init_embeddings_model
from utils.llm_utils import init_llm_model
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

async def test_llm_connection():
    llm =  init_llm_model()
    try:
        response = await llm.ainvoke("Hello, world!")
        content = response.content
        return {"status": "success", "response": content}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
async def test_embedding_model():
    try:
        embedding = init_embeddings_model()
        print(f"Embedding model initialized: {embedding}")
        # Test embedding with a simple string
        embedding_vector = await embedding.aembed_documents(["Hello, world!", "Another sentence"])        # Check if the embedding is a list and has the expected length
        if len(embedding_vector) == 0:
            raise ValueError("Invalid embedding vector")
        # Return the embedding vector        
        return {"status": "success", "embeddings": embedding_vector}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/test-llm-connection")
async def test_llm():
    result =  await test_llm_connection()
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@router.get("/test-embedding-connection")
async def test_embedding():
    result = await test_embedding_model()
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

