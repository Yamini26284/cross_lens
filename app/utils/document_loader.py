'''
The document loader is responsible for:

    Accepting PDF, DOCX or TXT files from the user
    Reading and extracting the raw text
    Splitting it into smart chunks
    Ready to be passed to the embedding step after
'''
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def load_document(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path)
    elif ext == ".docx":
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    documents = loader.load()
    return documents


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_documents(documents)
    return chunks


def load_and_chunk(file_path: str):
    documents = load_document(file_path)
    chunks = chunk_documents(documents)
    print(f"Loaded {len(documents)} pages, split into {len(chunks)} chunks")
    return chunks