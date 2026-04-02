'''Instead of firing one search query, we fire three simultaneously — one looking for supporting evidence, one for contradicting evidence, one for neutral/ambiguous statements.'''
from app.utils.embeddings import load_vectorstore
from app.core.router import get_llm

def rewrite_query(original_query: str, perspective: str) -> str:
    llm = get_llm()

    prompt = f"""
    Rewrite the following query from a {perspective} perspective.
    You are searching a document for evidence.
    
    Original query: {original_query}
    
    If perspective is SUPPORTING - rewrite to find evidence that supports the claim.
    If perspective is CONTRADICTING - rewrite to find evidence that contradicts the claim.
    If perspective is NEUTRAL - rewrite to find general or ambiguous statements about the topic.
    
    Respond with ONLY the rewritten query. Nothing else.
    """

    response = llm.invoke(prompt)
    return response.content.strip()


def multi_vector_retrieve(query: str, k: int = 3):
    vectorstore = load_vectorstore()

    supporting_query = rewrite_query(query, "SUPPORTING")
    contradicting_query = rewrite_query(query, "CONTRADICTING")
    neutral_query = rewrite_query(query, "NEUTRAL")

    print(f"Supporting query: {supporting_query}")
    print(f"Contradicting query: {contradicting_query}")
    print(f"Neutral query: {neutral_query}")

    supporting_chunks = vectorstore.similarity_search(supporting_query, k=k)
    contradicting_chunks = vectorstore.similarity_search(contradicting_query, k=k)
    neutral_chunks = vectorstore.similarity_search(neutral_query, k=k)

    seen = set()
    all_chunks = []

    for chunk in supporting_chunks + contradicting_chunks + neutral_chunks:
        if chunk.page_content not in seen:
            seen.add(chunk.page_content)
            all_chunks.append({
                "content": chunk.page_content,
                "metadata": chunk.metadata
            })

    return {
        "supporting": [c["content"] for c in all_chunks[:k]],
        "contradicting": [c["content"] for c in all_chunks[k:k*2]],
        "neutral": [c["content"] for c in all_chunks[k*2:]]
    }