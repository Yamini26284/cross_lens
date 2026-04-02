from app.core.router import get_llm

def generate_verdict(query: str, evaluated_result: dict) -> dict:
    llm = get_llm()

    supporting = "\n".join(evaluated_result["chunks"].get("supporting", []))
    contradicting = "\n".join(evaluated_result["chunks"].get("contradicting", []))
    neutral = "\n".join(evaluated_result["chunks"].get("neutral", []))
    web_results = "\n".join(evaluated_result.get("web_results", []))

    prompt = f"""
    You are a document claim verifier. Analyze the following evidence and give a structured verdict.

    User Query: {query}

    Supporting Evidence from document:
    {supporting if supporting else "None found"}

    Contradicting Evidence from document:
    {contradicting if contradicting else "None found"}

    Neutral/Additional Context:
    {neutral if neutral else "None found"}

    Web Search Results (if any):
    {web_results if web_results else "None"}

    Based on this evidence, provide your analysis in this EXACT format:

    SUPPORTING EVIDENCE:
    [List the key points that support the claim, with brief citations]

    CONTRADICTING EVIDENCE:
    [List the key points that contradict the claim, with brief citations]

    VERDICT: [SUPPORTED / CONTRADICTED / AMBIGUOUS]

    CONFIDENCE: [HIGH / MEDIUM / LOW]

    REASONING:
    [2-3 sentences explaining your verdict]
    """

    response = llm.invoke(prompt)

    return {
        "query": query,
        "raw_response": response.content,
        "status": evaluated_result["status"]
    }

def simple_answer(query: str, chunks: list) -> str:
    llm = get_llm()

    context = "\n".join([c.page_content for c in chunks])

    prompt = f"""
    Answer the following question based on the document context provided.
    If the answer is not in the context, say "I couldn't find that in the document."
    Be concise and helpful.

    Context: {context}

    Question: {query}
    """

    response = llm.invoke(prompt)
    return response.content