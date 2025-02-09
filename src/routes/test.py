from fastapi import APIRouter, HTTPException
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

@router.get("/test-llm-connection")
async def test_llm():
    result =  await test_llm_connection()
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result