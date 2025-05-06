from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_cohere import CohereEmbeddings
from config import settings
import logging

logger = logging.getLogger(__name__)

# def init_embeddings_model(model_name: str = settings.EMBEDDING_MODEL) -> HuggingFaceInferenceAPIEmbeddings:
#     try:
#         if not settings.HUGGINGFACE_API_KEY or settings.HUGGINGFACE_API_KEY.startswith("put your"):
#             logger.error("Missing or invalid Hugging Face API key")
#             raise ValueError("Hugging Face API key is not properly configured")
        
#         print(f"api_key: {settings.HUGGINGFACE_API_KEY}")
#         return HuggingFaceInferenceAPIEmbeddings(api_key=settings.HUGGINGFACE_API_KEY, model_name=model_name)
#     except Exception as e:
#         logger.error(f"Failed to initialize embedding model: {str(e)}")
#         raise ValueError(f"Failed to initialize embedding model: {str(e)}")

def init_embeddings_model():
    try:
        return CohereEmbeddings(
            cohere_api_key=settings.COHERE_API_KEY,
            model=settings.EMBEDDING_MODEL,
        )
    except Exception as e:
        logger.error(f"Failed to initialize embedding model: {str(e)}")
        raise ValueError(f"Failed to initialize embedding model: {str(e)}")