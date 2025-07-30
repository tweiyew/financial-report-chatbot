import os
from typing import List
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_vertexai.embeddings import VertexAIEmbeddings

VECTORSTORE_DIR = "data/vectorstores"
os.makedirs(VECTORSTORE_DIR, exist_ok=True)

def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def chunk_text(text: str) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " "]
    )
    return splitter.split_text(text)

def save_and_process_pdf(pdf_path: str, file_id: str):
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)

    embeddings = VertexAIEmbeddings(model_name="text-embedding-005")
    vectordb = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=os.path.join(VECTORSTORE_DIR, file_id)
    )
    vectordb.persist()
