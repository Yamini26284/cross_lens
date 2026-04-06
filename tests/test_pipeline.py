from app.core.pipeline import process_document, run_pipeline

process_document("test.txt")

queries = [
    "What is this document about?",
    "Does this document support the claim that remote work increases productivity?"
]

for query in queries:
    result = run_pipeline(query)
    print(f"\nType: {result['type']}")
    print(f"Verdict: {result['verdict']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Supporting points: {len(result['supporting'])}")
    print(f"Contradicting points: {len(result['contradicting'])}")
    print("="*50)