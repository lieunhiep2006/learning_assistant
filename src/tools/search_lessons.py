
from src.rag.citation import build_numbered_context
from src.rag.retriever import RetrievalContext, search
from typing import Literal, TypedDict
import re


class SearchLessonsResult(TypedDict):
    success: bool
    action: str
    data: dict | None
    error: str | None
    status: Literal["ok", "no_answer"]
    context: str
    sources: list


MIN_SCORE = {
    "bm25": 0.1,
    "dense": 0.35,
    "hybrid": 0.3,
}


def make_result(
    success: bool,
    context: str = "",
    sources: list | None = None,
    error: str | None = None,
) -> SearchLessonsResult:
    if sources is None:
        sources = []

    return {
        "success": success,
        "action": "search_lessons",
        "data": (
            {
                "context": context,
                "sources": sources,
            }
            if success
            else None
        ),
        "error": error,
        "status": "ok" if success else "no_answer",
        "context": context if success else "",
        "sources": sources,
    }


def search_lessons(
    context: RetrievalContext,
    query: str,
    top_k: int = 3,
    mode: Literal["bm25", "dense", "hybrid"] = "hybrid",
) -> SearchLessonsResult:

    # Kiểm tra câu hỏi và số lượng kết quả.
    if not query.strip() or top_k <= 0:
        return make_result(
            success=False,
            error="Câu hỏi không hợp lệ hoặc top_k phải lớn hơn 0.",
        )

    query = query.strip()

    # Tìm các đoạn tài liệu liên quan.
    results = search(
        context,
        query,
        mode=mode,
        top_k=top_k,
    )

    # Nếu câu hỏi có mã môn học, chỉ giữ tài liệu đúng mã.
    course_ids = re.findall(
        r"\b[A-Z]{2,4}\d{2,3}\b",
        query.upper(),
    )

    if course_ids:
        results = [
            result
            for result in results
            if result.chunk.doc_id.upper() in course_ids
        ]

    # Kiểm tra kết quả và điểm truy xuất.
    if not results or results[0].score < MIN_SCORE[mode]:
        return make_result(
            success=False,
            error="Không tìm thấy nội dung phù hợp trong tài liệu.",
        )

    # Tạo ngữ cảnh có đánh số và danh sách nguồn.
    numbered = build_numbered_context(results)

    return make_result(
        success=True,
        context=numbered.text,
        sources=numbered.sources,
    )
