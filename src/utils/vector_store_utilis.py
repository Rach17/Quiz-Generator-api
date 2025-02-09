from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_core.documents import Document
from typing import List
from config import settings
import uuid
from pathlib import Path
import os

def init_vector_store(collection_name: str = "documents", 
                      embeddings: HuggingFaceInferenceAPIEmbeddings = None,
                      pres_directory: str = "vector_store") -> Chroma:

    persistent_directory = os.path.join(settings.UPLOAD_DIR, pres_directory)
    
    print("Initializing vector store...")
    vector_store = Chroma(
    collection_name=collection_name,
    embedding_function=embeddings,
    persist_directory=persistent_directory,  
    )
    
    return vector_store

async def add_documents_to_vector_store(vector_store: Chroma, chunks: List[Document]):
    try:
        print("Adding documents to vector store...")
        ids = [str(uuid.uuid4()) for _ in chunks]
        await vector_store.aadd_documents(documents= chunks, ids=ids)
    except Exception as e:
        print(f"Error adding documents to vector store: {e}")
        raise
    

