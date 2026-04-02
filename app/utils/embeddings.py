from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
import chromadb

CHROMA_DIR = "chroma_store"

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

def store_chunks(chunks):
    import shutil
    embeddings = get_embeddings()
    
    try:
        if os.path.exists(CHROMA_DIR):
            client = chromadb.PersistentClient(path=CHROMA_DIR)
            client.delete_collection("langchain")
    except:
        if os.path.exists(CHROMA_DIR):
            shutil.rmtree(CHROMA_DIR, ignore_errors=True)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    print(f"Stored {len(chunks)} chunks in ChromaDB")
    return vectorstore

def load_vectorstore():
    embeddings = get_embeddings()
    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )
    return vectorstore