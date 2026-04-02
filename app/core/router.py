'''
router.py reads the user's query and decides — is this a simple question or does it need the full multi-vector pipeline?
Simple query example: "What is this document about?" → answer directly, no heavy retrieval needed.
Complex query example: "Does this document support the claim that X causes Y?" → trigger full pipeline.

'''

from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm():
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile",
        temperature=0
    )

def route_query(query: str) -> str:
    llm = get_llm()
    prompt = f"""
You are a query classifier. Classify the following query into one of three categories:

SIMPLE - Questions asking to summarize, explain or describe what the document says.
Example: "What is this document about?" or "Summarize this document"

COMPLEX - Questions that verify, fact-check, compare or find evidence for or against 
a claim. Any question with "is", "does", "verify", "better", "worse", "claim" or 
asking you to compare two things.
Example: "Is remote work better than office work?" or "Does the document support X?"

GENERAL - Questions completely unrelated to any document.
Example: "How do I bake a cake?" or "What is the capital of France?"

Query: {query}

Respond with ONLY one word: SIMPLE, COMPLEX or GENERAL.

"""

    response = llm.invoke(prompt)
    decision = response.content.strip().upper()

    if decision not in ["SIMPLE", "COMPLEX", "GENERAL"]:
        return "COMPLEX"
    return decision

    return decision