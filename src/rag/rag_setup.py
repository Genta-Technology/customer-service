"""
This module sets up the customer service functionality by 
executing Chroma vector database functions. It loads documents from a 
specified directory, splits the text into chunks, and saves them to a Chroma database.
"""
import os
import shutil
from genta_langchain import GentaEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.vectorstores.chroma import Chroma
from genta import GentaAPI
from typing import List
from utilities.utilities import EnvironmentVariables

env = EnvironmentVariables()

GENTA_API_TOKEN = env['GENTA_API_KEY']
CHROMA_DATABASE_PATH = "chroma_database"
DATA_PATH = "data"

genta_api = GentaAPI(GENTA_API_TOKEN)
genta_embeddings = GentaEmbeddings(genta_api, "GentaEmbedding")

def main():
    """
    Main function that orchestrates the setup process.
    """
    database_setup()

def database_setup():
    """
    Generates the data store by loading documents, splitting text, and saving to Chroma.
    """
    documents = load_documents()
    chunks = split_documents(documents)
    save_chroma(chunks)

def load_documents():
    """
    Loads documents from the specified directory using the DirectoryLoader.
    Returns:
        List[Document]: A list of loaded documents.
    """
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    return documents

def split_documents(documents: List[Document]):  # Use List[Document] instead of list[Document]
    """
    Splits the text of the documents into chunks using the RecursiveCharacterTextSplitter.

    Args:
        documents (List[Document]): A list of documents to split.

    Returns:
        List[Document]: A list of document chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=384,
        chunk_overlap=128,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    document = chunks[10]
    print(document.page_content)
    print(document.metadata)
    return chunks

def save_chroma(chunks: List[Document]):  # Use List[Document] instead of list[Document]
    """
    Saves the document chunks to a Chroma database.

    Args:
        chunks (List[Document]): A list of document chunks to save.
    """
    # Clear out the database first.
    if os.path.exists(CHROMA_DATABASE_PATH):
        shutil.rmtree(CHROMA_DATABASE_PATH)
    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, genta_embeddings, 
                                 persist_directory=CHROMA_DATABASE_PATH)

    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_DATABASE_PATH}.")

if __name__ == "__main__":
    main()