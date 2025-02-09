from langchain_huggingface  import HuggingFaceEndpoint
from langchain_cohere import ChatCohere;
from config import settings

def init_llm_model(model_name: str = settings.CHAT_MODEL) -> HuggingFaceEndpoint:
    return init_cohere_model(model_name)

def init_huggingface_endpoint(model_name: str = settings.CHAT_MODEL) -> HuggingFaceEndpoint:
    return HuggingFaceEndpoint(repo_id = model_name, huggingfacehub_api_token= settings.HUGGINGFACE_API_KEY)

def init_cohere_model(model_name: str = settings.CHAT_MODEL) -> ChatCohere:
    return ChatCohere(cohere_api_key = settings.COHERE_API_KEY, model_name = model_name)