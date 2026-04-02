'''After retrieval, before generating the answer, this step grades the retrieved chunks — are they actually relevant? If not, it triggers a web search instead of forcing a bad answer.'''
from app.core.router import get_llm
from ddgs import DDGS

def evaluate_chunks(query: str, chunks: dict) -> str:
    llm = get_llm()

    all_content = "\n---\n".join(
        chunks.get("supporting", []) +
        chunks.get("contradicting", []) +
        chunks.get("neutral", [])
    )

    prompt = f"""
    You are a relevance evaluator.
    
    Query: {query}
    
    Retrieved chunks:
    {all_content}
    
    Are these chunks relevant to answering the query?
    
    Respond with ONLY one word:
    RELEVANT - if chunks directly help answer the query
    AMBIGUOUS - if chunks are partially related but incomplete
    IRRELEVANT - if chunks have nothing to do with the query
    """

    response = llm.invoke(prompt)
    decision = response.content.strip().upper()

    if decision not in ["RELEVANT", "AMBIGUOUS", "IRRELEVANT"]:
        return "AMBIGUOUS"

    return decision


def web_search_fallback(query: str) -> list:
    print("Triggering web search fallback...")
    results = []

    with DDGS() as ddgs:
        search_results = ddgs.text(query, max_results=3)
        for r in search_results:
            results.append(r["body"])

    return results


def evaluate_and_decide(query: str, chunks: dict) -> dict:
    decision = evaluate_chunks(query, chunks)
    print(f"Evaluator decision: {decision}")

    if decision == "RELEVANT":
        return {
            "status": "RELEVANT",
            "chunks": chunks,
            "web_results": []
        }

    elif decision == "AMBIGUOUS":
        web_results = web_search_fallback(query)
        return {
            "status": "AMBIGUOUS",
            "chunks": chunks,
            "web_results": web_results
        }

    else:
        web_results = web_search_fallback(query)
        return {
            "status": "IRRELEVANT",
            "chunks": {},
            "web_results": web_results
        }