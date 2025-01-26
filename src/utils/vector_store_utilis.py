from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_core.documents import Document
from typing import List
from config import settings
import os

def init_vector_store(collection_name: str = "documents") -> Chroma:
    """
    Initializes a Chroma vector store. Creates a new database and collection if they don't exist.

    Args:
        collection_name (str): Name of the collection in the vector store.

    Returns:
        Chroma: The initialized Chroma vector store.
    """
    persistent_directory = os.path.join(settings.UPLOAD_DIR, "vector_store")
    
    embeddings = HuggingFaceInferenceAPIEmbeddings(api_key=settings.HUGGINGFACE_API_KEY, model_name=settings.EMBEDDING_MODEL)
    vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory=persistent_directory,  
    )
    
    return vector_store

async def add_documents_to_vector_store(vector_store: Chroma, chunks: List[str]):
    """
    Stores document embeddings in the vector store.

    Args:
        vector_store (Chroma): The initialized Chroma vector store.
        chunks (List[Document]): List of document texts or chunks.

    """
    try:
        await vector_store.aadd_documents(chunks)
    except Exception as e:
        print(f"Error adding documents to vector store: {e}")
        raise
    

