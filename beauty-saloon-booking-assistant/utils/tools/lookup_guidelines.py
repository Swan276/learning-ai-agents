import os
import shutil
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

PDF_PATH = "./resources/booking-guideline.pdf"
PERSIST_PATH = "./data/chroma/guideline"

class GuidelineVectorStore:
    def __init__(self, retriever=None):
        if retriever:
            self._retriever = retriever
        else:
            self._retriever = self._get_retriever(self)

    @classmethod
    def reset(cls):
        """Creates a new vector store from scratch."""
        retriever = cls._create_new_vectorstore()
        return cls(retriever=retriever)

    def query(self, query: str, k: int = 3) -> list[Document]:
        return self._retriever.similarity_search(query, k=k)

    @staticmethod
    def _get_retriever(self):
        if os.path.exists(PERSIST_PATH):
            return Chroma(
                persist_directory=PERSIST_PATH,
                embedding_function=OllamaEmbeddings(model="mxbai-embed-large")
            )
        else:
            return self._create_new_vectorstore()

    @staticmethod
    def _create_new_vectorstore() -> Chroma:
        """Loads a PDF file and creates a vector store from it."""
        # Extracts pages from a PDF file.
        loader = PyPDFLoader(PDF_PATH)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=100,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(loader.load())
        print(chunks[3])
        print("="*25)
        # Clear out the vector store first.
        if os.path.exists(PERSIST_PATH):
            shutil.rmtree(PERSIST_PATH)

        # Create a new vector store from the documents.
        return Chroma.from_documents(
            chunks,
            OllamaEmbeddings(model="mxbai-embed-large"),
            persist_directory=PERSIST_PATH
        )

retriever = GuidelineVectorStore()

def lookup_guidelines(query: str) -> dict:
    """
    Check guidelines to see available services, shop information, booking policies and procedures.

    Args:
        query (str): keyword of the required context.

    Returns:
        dict: A dictionary with the status and context.

    Example:
        lookup_guidelines(query="services")
        {
            'status': 'success',
            'context': 'Popular Services Include: Haircut, Hairstyling, Makeup, Nail'
        }
    """
    try:
        docs = retriever.query(query)
        return {"status": "success", "context": "\n\n".join([doc.page_content for doc in docs])}
    except Exception as e:
        return {"status": "failure", "message": str(e)}