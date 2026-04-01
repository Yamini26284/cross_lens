from app.utils.document_loader import load_and_chunk
from app.utils.embeddings import store_chunks, load_vectorstore

chunks = load_and_chunk("test.txt")
store_chunks(chunks)

vectorstore = load_vectorstore()
results = vectorstore.similarity_search("API key formatting", k=2)
for r in results:
    print(r.page_content)
    print("---")