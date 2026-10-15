from src.rag.citation import format_citation,Source,build_numbered_context
from src.rag.retrieval_types import RetrievalResult
from src.rag.retriever import RetrievalContext,search
from typing import Literal,TypedDict
import re

class search_evidence(TypedDict):
    status:Literal["ok","no_answer"]
    context:str
    sources:list[Source]

MIN_SCORE={"bm25":0.1,"dense":0.35,"hybrid":0.3}


def search_lessons(
    context: RetrievalContext,
    query: str,
    top_k: int = 3,
    mode: Literal["bm25", "dense", "hybrid"] = "hybrid",
) -> search_evidence:
    if not query.strip() or top_k <= 0:
        return {"status": "no_answer", "context": "", "sources": []}

    query = query.strip()

    # Tìm các đoạn tài liệu liên quan.
    results = search(context, query, mode=mode, top_k=top_k)

    # Nếu câu hỏi nêu mã môn, chỉ giữ tài liệu đúng môn.
    course_ids = re.findall(r"\b[A-Z]{2,4}\d{2,3}\b", query.upper())

    if course_ids:
        results = [
            result
            for result in results
            if result.chunk.doc_id.upper() in course_ids
        ]

    # Không có kết quả đúng môn hoặc điểm quá thấp thì từ chối.
    if not results or results[0].score < MIN_SCORE[mode]:
        return {"status": "no_answer", "context": "", "sources": []}

    numbered = build_numbered_context(results)

    return {
        "status": "ok",
        "context": numbered.text,
        "sources": numbered.sources,
    }
