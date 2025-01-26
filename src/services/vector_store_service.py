from langchain_core.documents import Document
from utils.vector_store_utilis import init_vector_store
from typing import List

def query_vector_store(query: str, top_k: int = 5, threshold: float = 0.5) -> List[Document]:
    """
    Queries the vector store for similar documents.

    Args:
        query (str): The search query string.
        top_k (int): Number of results to return. Defaults to 5.
        threshold (float): Minimum similarity score for results. Defaults to 0.5.

    Returns:
        List[Document]: A list of documents and their similarity scores.
    """

    try:
        vector_store = init_vector_store()
        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": top_k}
        )
        print("Querying vector store...")
        
        relevant_docs =  retriever.invoke(query)
        # Display the relevant results with metadata
        print("\n--- Relevant Documents ---")
        for i, doc in enumerate(relevant_docs, 1):
            print(f"Document {i}:\n{doc.page_content}\n")
            if doc.metadata:
                print(f"Source: {doc.metadata.get('source', 'Unknown')}\n")
                
        return relevant_docs
    except Exception as e:
        print(f"Error querying vector store: {e}")
        raise