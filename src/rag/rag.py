"""
This is the file in which the process of langchain and prompt system is defined.
"""
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from rag.genta_langchain import GentaLLM, GentaEmbeddings
from genta import GentaAPI
import requests

# Prompt Template for user request
PROMPT_TEMPLATE = """
Anda adalah asisten AI customer service yang membantu menjawab pertanyaan pelanggan mengenai informasi TNI (Tentara Nasional Indonesia).
Anda menjawab pertanyaan tersebut berdasarkan referensi yang tersedia.

# Konteks
{context}

# Pertanyaan
{question}

Jawablah dengan bahasa customer service seperti menggunakan kak dan lebih casual. 
Anda harus menjawab pertanyaan yang ada hubungannya dengan Tentara Nasional Indonesia dan topik seputar militer. 
Apabila pertanyaan yang diberikan diluar topik, jawablah dengan mengatakan maaf saya tidak dapat menjawab dan menanggapi pertanyaan yang tidak ada kaitannya dengan TNI maupun militer.
Berperilakulah secara professional dan sopan serta bahasa yang fleksibel dan santai.
"""

# The file location of the chroma vector database for RAG
CHROMA_DATABASE_PATH = "chroma_database"

def rag_main(chat_history: list, system: str):
    """
    Run the main function of the langchain, the only function that can be called outside
    """

    copy_chat_history = chat_history.copy()

    copy_chat_history.insert(0, {"role":"system", "content":system})

    return copy_chat_history
