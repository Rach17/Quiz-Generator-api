from langchain_core.documents import Document
from langchain_chroma import Chroma
from utils.vector_store_utilis import init_vector_store
import random

    
async def get_random_doc(collection_name: str = "documents") -> Document:
    vector_store = init_vector_store(collection_name)
    all_ids = vector_store.get()["ids"]
    random_id = random.choice(all_ids)
    print(f"Get random document ID: {random_id}")
    random_document = vector_store.get_by_ids([random_id])
    return random_document[0]
    
    
async def clear_vector_store(collection_name: str = "documents"):
    vector_store = init_vector_store(collection_name)
    vector_store.delete_collection()
    content = await get_random_doc()
    print(f"Clearing vector store with content: {content}")
    print("Vector store cleared")