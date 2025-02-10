import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models.schemas import ProcessedPDF
from utils.file_processing import clean_temp_files
from typing import  Dict
from utils.vector_store_utilis import init_vector_store, add_documents_to_vector_store
import os
from typing import List
from langchain_core.documents import Document
from utils.embeddings_utils import init_embiddings_model


async def load_pdf(file) -> List[Document]:
    temp_file = None
    try:
        # Create temporary file
        print("Create temporary file for PDF loading...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
            content = await file.read()
            temp.write(content)
            temp_file = temp.name

        # PDF Loading
        loader = PyPDFLoader(temp_file)
        print("Loading PDF document...")
        document = loader.load()
        return document
    except Exception as e:
        print(f"An error occurred while loading the PDF: {e}")
        raise e
    finally:
        if temp_file:
            clean_temp_files(temp_file)
        
def split_pdf(document: List[Document], chunk_size: int = 500, chunk_overlap: int = 50) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    print("Splitting documents...")
    docs = text_splitter.split_documents(document)
    return docs

async def process_pdf(file, collection_name = "documents") -> Dict:
    try:
        document = await load_pdf(file)
        docs = split_pdf(document)
        vector_store = init_vector_store(collection_name=collection_name,embeddings=init_embiddings_model()) 
        print("Adding documents to vector store...")
        await add_documents_to_vector_store(vector_store, docs)
        return {
            "chunks_number": len(docs),
        }
    except Exception as e:
        print(f"Error processing PDF: {e}")
        raise e
    
