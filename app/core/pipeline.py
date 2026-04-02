'''One function that takes a query and document, runs it through all phases in order, and returns the final verdict.'''

from app.core.router import route_query
from app.core.retriever import multi_vector_retrieve
from app.core.evaluator import evaluate_and_decide
from app.core.generator import generate_verdict, simple_answer
from app.utils.document_loader import load_and_chunk
from app.utils.embeddings import store_chunks, load_vectorstore

def process_document(file_path: str):
    chunks = load_and_chunk(file_path)
    store_chunks(chunks)
    print(f"Document processed and stored successfully")
    return len(chunks)

def run_pipeline(query: str) -> dict:
    print(f"\n{'='*50}")
    print(f"Query: {query}")
    print(f"{'='*50}")

    route = route_query(query)
    print(f"Route decided: {route}")

    if route == "SIMPLE":
        vectorstore = load_vectorstore()
        chunks = vectorstore.similarity_search(query, k=3)
        answer = simple_answer(query, chunks)
        return {
            "type": "SIMPLE",
            "query": query,
            "answer": answer,
            "verdict": None,
            "confidence": None,
            "supporting": [],
            "contradicting": []
        }
    if route == "GENERAL":
        from app.core.evaluator import web_search_fallback
        web_results = web_search_fallback(query)
        context_docs = [type('obj', (object,), {'page_content': r})() for r in web_results]
        answer = simple_answer(query, context_docs)
        return {
            "type": "SIMPLE",
        "query": query,
        "answer": answer,
        "verdict": None,
        "confidence": None,
        "supporting": [],
        "contradicting": []}
        
        
    

    chunks = multi_vector_retrieve(query)
    evaluated = evaluate_and_decide(query, chunks)
    result = generate_verdict(query, evaluated)

    parsed = parse_response(result["raw_response"])

    return {
        "type": "COMPLEX",
        "query": query,
        "answer": result["raw_response"],
        "verdict": parsed.get("verdict", "AMBIGUOUS"),
        "confidence": parsed.get("confidence", "MEDIUM"),
        "supporting": parsed.get("supporting", []),
        "contradicting": parsed.get("contradicting", [])
    }


def parse_response(raw: str) -> dict:
    lines = raw.split("\n")
    result = {
        "verdict": "AMBIGUOUS",
        "confidence": "MEDIUM",
        "supporting": [],
        "contradicting": []
    }

    current_section = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("VERDICT:"):
            verdict = line.replace("VERDICT:", "").strip()
            if "SUPPORTED" in verdict:
                result["verdict"] = "SUPPORTED"
            elif "CONTRADICTED" in verdict:
                result["verdict"] = "CONTRADICTED"
            else:
                result["verdict"] = "AMBIGUOUS"

        elif line.startswith("CONFIDENCE:"):
            confidence = line.replace("CONFIDENCE:", "").strip()
            if "HIGH" in confidence:
                result["confidence"] = "HIGH"
            elif "LOW" in confidence:
                result["confidence"] = "LOW"
            else:
                result["confidence"] = "MEDIUM"

        elif "SUPPORTING EVIDENCE" in line:
            current_section = "supporting"

        elif "CONTRADICTING EVIDENCE" in line:
            current_section = "contradicting"

        elif line.startswith("*") or line.startswith("-"):
            point = line.lstrip("*- ").strip()
            if current_section == "supporting":
                result["supporting"].append(point)
            elif current_section == "contradicting":
                result["contradicting"].append(point)

    return result