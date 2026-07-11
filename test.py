# local_test.py
from rag_core import RagEngine


engine = RagEngine()


print("\n=== test 1: Q&A ===")
question = "I haven't gone to work for six consecutive days; what will happen?"
answer = engine.query(question)
print(f"\nfinal answer:\n{answer}\n")

