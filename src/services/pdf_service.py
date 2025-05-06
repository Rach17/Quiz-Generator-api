import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.file_processing import clean_temp_files
from typing import  Dict
from typing import List
from langchain_core.documents import Document
from datetime import datetime
from services.collection_service import init_collection, generate_collection_name
from langdetect import detect
import logging

logger = logging.getLogger(__name__)


def detect_pdf_language(documents) -> str:
    # Combine text from all pages for language detection
    full_text = " ".join([doc.page_content for doc in documents])
    detected_language = detect(full_text)
    return detected_language

async def load_pdf(file) -> List[Document]:
    temp_file = None
    try:
        logger.info("Create temporary file for PDF loading...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
            content = await file.read()
            temp.write(content)
            temp_file = temp.name

        # PDF Loading
        loader = PyPDFLoader(temp_file)
        logging.info("Loading PDF document...")
        documents  = loader.load()
        
        detected_language = detect_pdf_language(documents)
        logger.info(f"Detected language: {detected_language}")
        
        return documents, detected_language
    except Exception as e:
        logger.error(f"An error occurred while loading the PDF: {str(e)}")
        raise e
    finally:
        if temp_file:
            clean_temp_files(temp_file)
        
def split_pdf(document: List[Document], chunk_size: int = 500, chunk_overlap: int = 50) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    docs = text_splitter.split_documents(document)
    return docs

async def process_pdf(file) -> Dict:
    try:
        documents, detected_language = await load_pdf(file)
        docs = split_pdf(documents)
        collection_name = generate_collection_name(file.filename)
        logger.info(f"Generated collection name: {collection_name}")    
        await init_collection(docs, len(docs), detected_language, collection_name)
        return {
            "collection_name": collection_name,
            "chunks_number": len(docs),
            "language": detected_language
        }
    except Exception as e:
        raise e
    
    
