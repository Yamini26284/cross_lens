from app.core.retriever import multi_vector_retrieve

query = "Does this document support the claim that remote work increases productivity?"
results = multi_vector_retrieve(query)

print("SUPPORTING EVIDENCE:")
for r in results["supporting"]:
    print(r)
    print("---")

print("CONTRADICTING EVIDENCE:")
for r in results["contradicting"]:
    print(r)
    print("---")

print("NEUTRAL STATEMENTS:")
for r in results["neutral"]:
    print(r)
    print("---")