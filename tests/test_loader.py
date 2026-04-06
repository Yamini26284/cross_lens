from app.utils.document_loader import load_and_chunk

chunks = load_and_chunk("test.txt")
print(chunks[0].page_content)