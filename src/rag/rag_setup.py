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

# Prompt Template for user request
PROMPT_TEMPLATE = """
Anda adalah asisten AI customer service yang membantu menjawab pertanyaan pelanggan berdasarkan referensi yang tersedia.

## CONTEXT
{context}

## QUESTION
{question}

Jawablah dengan bahasa customer service seperti menggunakan kak dan lebih casual

"""