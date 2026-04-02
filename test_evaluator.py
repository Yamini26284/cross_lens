from app.core.retriever import multi_vector_retrieve
from app.core.evaluator import evaluate_and_decide

query = "Does this document support the claim that remote work increases productivity?"
chunks = multi_vector_retrieve(query)
result = evaluate_and_decide(query, chunks)

print(f"Status: {result['status']}")
print(f"Web results used: {len(result['web_results'])}")