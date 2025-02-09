from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from config import settings

def init_embiddings_model(model_name: str = settings.EMBEDDING_MODEL) -> HuggingFaceInferenceAPIEmbeddings:
    return HuggingFaceInferenceAPIEmbeddings(api_key=settings.HUGGINGFACE_API_KEY, model_name=model_name)