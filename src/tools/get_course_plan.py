
from typing import TypedDict
from src.corpus.metadata import Document
from src.rag.retriever import RetrievalContext


class CoursePlanResult(TypedDict):
    success: bool
    action: str
    data: dict | None
    error: str | None


def get_course_plan(
    context: RetrievalContext,
    course_id: str,
) -> CoursePlanResult:
    """Lấy nội dung tài liệu theo mã môn học hoặc mã tài liệu."""

    if not course_id.strip():
        return {
            "success": False,
            "action": "get_course_plan",
            "data": None,
            "error": "Vui lòng nhập mã môn học hoặc mã tài liệu.",
        }

    for document in context.store.documents.values():
        if document.doc_id.lower() == course_id.strip().lower():
            return {
                "success": True,
                "action": "get_course_plan",
                "data": {
                    "doc_id": document.doc_id,
                    "title": document.title,
                    "version": document.version,
                    "owner": document.owner,
                    "source": document.source,
                    "content": document.content,
                },
                "error": None,
            }

    return {
        "success": False,
        "action": "get_course_plan",
        "data": None,
        "error": f"Không tìm thấy tài liệu có mã: {course_id.strip()}",
    }
