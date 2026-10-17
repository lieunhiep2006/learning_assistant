
from typing import Any, TypedDict

from src.rag.retriever import RetrievalContext


class CoursePlanResult(TypedDict):
    success: bool
    action: str
    data: dict[str, Any] | None
    error: str | None


MAX_CONTENT_LENGTH = 3000


def get_course_plan(
    context: RetrievalContext,
    course_id: str,
) -> CoursePlanResult:
    """Lấy thông tin môn học và một phần nội dung tài liệu."""

    course_id = course_id.strip()

    if not course_id:
        return {
            "success": False,
            "action": "get_course_plan",
            "data": None,
            "error": "Vui lòng nhập mã môn học hoặc mã tài liệu.",
        }

    for document in context.store.documents.values():
        if document.doc_id.lower() == course_id.lower():
            content = document.content
            truncated = len(content) > MAX_CONTENT_LENGTH

            return {
                "success": True,
                "action": "get_course_plan",
                "data": {
                    "doc_id": document.doc_id,
                    "title": document.title,
                    "version": document.version,
                    "owner": document.owner,
                    "source": document.source,
                    "content": content[:MAX_CONTENT_LENGTH],
                    "content_truncated": truncated,
                    "original_length": len(content),
                },
                "error": None,
            }

    return {
        "success": False,
        "action": "get_course_plan",
        "data": None,
        "error": f"Không tìm thấy tài liệu có mã: {course_id}",
    }
