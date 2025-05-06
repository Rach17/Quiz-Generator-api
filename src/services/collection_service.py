from langchain_core.documents import Document
from utils.embeddings_utils import init_embeddings_model
import random
from langchain_chroma import Chroma
from typing import List
from langchain_core.documents import Document
from services.caching_service import CollectionCache
import time 
from datetime import timedelta 
from slugify import slugify
import logging

logger = logging.getLogger(__name__)
cache = CollectionCache()
    
async def init_collection(documents: List[Document], size: int, language: str = "fr", collection_name: str = "collection") -> None:
    try:
        logger.info(f"Initializing collection: {collection_name} with {len(documents)} docs")
        embedding = init_embeddings_model()
        logger.info(f"Embedding model initialized: {embedding}")
        collection = await Chroma.afrom_documents(documents=documents, embedding=embedding)
        cache.add_collection(collection_name, collection, size, language)
    except Exception as e:
        logger.error(f"An error occurred while initializing collection: {str(e)}")
        raise e
    
    
async def get_random_doc(collection_name: str) -> Document:
    collection = cache.get_collection(collection_name)
    collection_store = collection.get("collection")
    if(collection_store is None):
        logger.error("Collection not found")
        raise ValueError("Collection not found")
    all_ids = collection_store.get()["ids"]
    random_id = random.choice(all_ids)
    random_document = collection_store.get_by_ids([random_id])
    return {"doc" : random_document[0], "lang": collection.get("language")}
    
def get_collection_info(collection_name: str):
    collection = cache.get_collection(collection_name)
    if collection["collection"] is None:
        return None
    return {
            "collection_name": collection_name,
            "chunks_number": len(collection["collection"].get()["ids"]),
            "lifetime": str(timedelta(seconds=(collection["expire_time"] - time.time())))  # Formate en HH:MM:SS
        }
    
from slugify import slugify  # install with: pip install python-slugify
import uuid
from datetime import datetime

def generate_collection_name(filename: str) -> str:
    # Sanitize the file name to create a URL/filename safe string.
    base_name = slugify(filename)
    # Generate a timestamp string.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Generate a short unique identifier.
    unique_suffix = uuid.uuid4().hex[:8]
    # Combine components into a collection name.
    collection_name = f"{base_name}_{timestamp}_{unique_suffix}"
    return collection_name

# async def retrive_paragraphe(collection_name: str, question: str) -> str:
#     try:
#         collection_store = cache.get_collection(collection_name).get("collection")
#         if(collection_store is None):
#             logger.error("Collection not found")
#             raise ValueError("Collection not found")
#         retrived_doc = await collection_store.asimilarity_search(question, k=1)
        
#         return {"content": retrived_doc[0].page_content, "page_number": retrived_doc[0].metadata.get("page_label")}
#     except Exception as e:
#         logger.error(f"An error occurred while retriving document: {str(e)}")
#         raise e
    