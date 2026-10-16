
from pathlib import Path
from src.rag.retriever import build_retriever
from src.tools.search_lessons import search_lessons

from dotenv import load_dotenv

load_dotenv()

project_root = Path(__file__).resolve().parent
store_path = project_root / "data" / "documents" / "document_store.json"

context = build_retriever(store_path=store_path)

result = search_lessons(
    context=context,
    query="What is artificial intelligence?",
    top_k=3,
    mode="hybrid",
)

print("SUCCESS:", result["success"])
print("ACTION:", result["action"])
print("DATA:", result["data"])
print("ERROR:", result["error"])

if result["data"] is not None:
    print("CONTEXT:", result["data"]["context"])
    print("SOURCES:", result["data"]["sources"])
