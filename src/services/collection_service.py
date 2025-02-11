from langchain_core.documents import Document
from utils.embeddings_utils import init_embiddings_model
import random
from langchain_chroma import Chroma
from typing import List
from langchain_core.documents import Document
from services.caching_service import CollectionCache
import time 
from datetime import timedelta 
import logging

logger = logging.getLogger(__name__)
cache = CollectionCache()
    
async def init_collection(collection_name: str, documents: List[Document]):
    try :
        collection = await Chroma.afrom_documents(documents=documents, embedding=init_embiddings_model())  
        cache.add_collection(collection_name, collection)
    except Exception as e: 
        logger.error(f"An error occurred while initializing collection: {str(e)}")
        raise e
    
    
async def get_random_doc(collection_name: str) -> Document:
    collection = cache.get_collection(collection_name)["collection"]
    if(collection is None):
        logger.error("Collection not found")
        raise ValueError("Collection not found")
    all_ids = collection.get()["ids"]
    random_id = random.choice(all_ids)
    random_document = collection.get_by_ids([random_id])
    return random_document[0]
    
def get_collection_info(collection_name: str):
    collection = cache.get_collection(collection_name)
    if collection["collection"] is None:
        return None
    return {
            "collection_name": collection_name,
            "chunks_number": len(collection["collection"].get()["ids"]),
            "lifetime": str(timedelta(seconds=(collection["expire_time"] - time.time())))  # Formate en HH:MM:SS
        }