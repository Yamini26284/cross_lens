from app.core.router import route_query

queries = [
    "What is this document about?",
    "Does this document claim that remote work increases productivity?",
    "Hello, what can you do?",
    "Verify that the return policy allows 60 day returns"
]

for q in queries:
    result = route_query(q)
    print(f"Query: {q}")
    print(f"Route: {result}")
    print("---")