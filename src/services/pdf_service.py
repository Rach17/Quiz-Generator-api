import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models.schemas import ProcessedPDF
from utils.file_processing import clean_temp_files
from typing import  Dict
from utils.vector_store_utilis import init_vector_store, add_documents_to_vector_store
import os


async def process_pdf(file) -> Dict:
    temp_file = None
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
            content = await file.read()
            temp.write(content)
            temp_file = temp.name

        # PDF Loading
        loader = PyPDFLoader(temp_file)
        document = loader.load()

        # Text Splitting
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
            is_separator_regex=False
        )
        
        print("Splitting documents...")
        docs = text_splitter.split_documents(document)

        # Store embeddings in vector store
        print("Storing embeddings in vector store...")
        vector_store = init_vector_store()
        await add_documents_to_vector_store(vector_store, docs)
        print("\n--- Finished creating vector store ---")

        return {
            "chunks_number": len(docs),
        }

    finally:
        if temp_file:
            clean_temp_files(temp_file)

