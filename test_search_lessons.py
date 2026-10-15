
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

print("STATUS:", result["status"])
print("CONTEXT:", result["context"])
print("SOURCES:", result["sources"])
