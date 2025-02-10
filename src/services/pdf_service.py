import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.file_processing import clean_temp_files
from typing import  Dict
from typing import List
from langchain_core.documents import Document
from datetime import datetime
from services.vector_store_service import init_collection


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

async def process_pdf(file) -> Dict:
    try:
        document = await load_pdf(file)
        docs = split_pdf(document)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        collection_name = f"{file.filename}_{timestamp}"

        await init_collection(collection_name, docs)
        return {
            "collection_name": collection_name,
            "chunks_number": len(docs),
        }
    except Exception as e:
        print(f"Error processing PDF: {e}")
        raise e
    
    
