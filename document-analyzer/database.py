import shutil

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
import os

DATA_PATH = "./data/documents"
CHROMA_PATH = "./data/chroma"

def main():
    generate_data_store()

def get_db_instance() -> Chroma:
    embedding_function = OllamaEmbeddings(model="mxbai-embed-large")
    return Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

def generate_data_store():
    documents = load_documents()
    pages = extract_pages_from_pdfs(documents)
    chunks = split_text(pages)
    save_to_chroma(chunks)

def load_documents():
    docs = [f"{DATA_PATH}/{file}" for file in os.listdir(DATA_PATH) if file.endswith(".pdf")]
    print(docs)
    return docs

def extract_pages_from_pdfs(file_paths: list[str]):
    pages = []
    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        for page in loader.lazy_load():
            pages.append(page)
    return pages

def split_text(documents: list[Document]):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=500
    )
    chunks = text_splitter.split_documents(documents)

    return chunks

def save_to_chroma(chunks: list[Document]):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    Chroma.from_documents(
        chunks,
        OllamaEmbeddings(model="mxbai-embed-large"),
        persist_directory=CHROMA_PATH
    )
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

if __name__ == "__main__":
    main()