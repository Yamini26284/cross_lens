from app.core.retriever import multi_vector_retrieve
from app.core.evaluator import evaluate_and_decide
from app.core.generator import generate_verdict

query = "Does this document support the claim that remote work increases productivity?"

chunks = multi_vector_retrieve(query)
evaluated = evaluate_and_decide(query, chunks)
result = generate_verdict(query, evaluated)

print(result["raw_response"])