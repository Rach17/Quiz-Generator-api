from langchain_core.documents import Document
from utils.embeddings_utils import init_embiddings_model
import random
from langchain_chroma import Chroma
from typing import List
from langchain_core.documents import Document
from services.caching_service import CollectionCache 

cache = CollectionCache()
    
async def init_collection(collection_name: str, documents: List[Document]):
    print("Initializing collection...")
    collection = await Chroma.afrom_documents(documents=documents, embedding=init_embiddings_model())  
    print("Caching collection...")
    cache.add_collection(collection_name, collection)
    
    
async def get_random_doc(collection_name: str) -> Document:
    cache.show_cache()
    collection = cache.get_collection(collection_name)
    all_ids = collection.get()["ids"]
    random_id = random.choice(all_ids)
    print(f"Get random document ID: {random_id}")
    random_document = collection.get_by_ids([random_id])
    return random_document[0]
    
    