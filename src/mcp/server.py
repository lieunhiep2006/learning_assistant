
import json
import re
from datetime import datetime
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from src.rag.retriever import build_retriever
from src.tools.search_lessons import search_lessons as rag_search_lessons
from src.tools.get_course_plan import get_course_plan as find_course_plan
from src.tools.create_study_request import (
    create_study_request as save_study_request,
)
from src.tools.get_study_request import get_study_request as find_study_request


# Khởi tạo MCP Server
mcp = FastMCP("Learning Assistant")

# Xác định thư mục gốc của dự án
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCUMENT_DIR = PROJECT_ROOT / "data" / "documents"
STORE_PATH = DOCUMENT_DIR / "document_store.json"
REQUEST_FILE = PROJECT_ROOT / "data" / "study_requests.json"

# Khởi tạo RAG context một lần khi server khởi động
retrieval_context = build_retriever(
    store_path=STORE_PATH,
    model="jina-embeddings-v3",
)


def json_result(
    success: bool,
    action: str,
    data=None,
    error=None,
) -> str:
    """Tạo kết quả JSON thống nhất cho MCP tools."""
    return json.dumps(
        {
            "success": success,
            "action": action,
            "data": data,
            "error": error,
        },
        ensure_ascii=False,
    )


def read_documents():
    """Đọc nội dung các file Markdown trong thư mục tài liệu."""
    documents = []

    if not DOCUMENT_DIR.exists():
        return documents

    for file_path in DOCUMENT_DIR.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        title_match = re.search(
            r"(?m)^title:\s*(.+)$",
            content,
        )
        title = (
            title_match.group(1).strip()
            if title_match
            else file_path.stem
        )

        documents.append(
            {
                "filename": file_path.name,
                "title": title,
                "content": content,
            }
        )

    return documents


@mcp.tool()
def search_lessons(
    query: str,
    top_k: int = 3,
    mode: str = "hybrid",
) -> str:
    """Tìm kiếm nội dung bài giảng bằng RAG."""

    if not query.strip():
        return json_result(
            False,
            "search_lessons",
            error="Vui lòng nhập nội dung cần tìm.",
        )

    try:
        result = rag_search_lessons(
            context=retrieval_context,
            query=query,
            top_k=top_k,
            mode=mode,
        )

        # Chuẩn hóa kết quả theo giao diện mà evaluation runner sử dụng
        if not result.get("success", False):
            return json_result(
                False,
                "search_lessons",
                data=result.get("data"),
                error=result.get("error") or "Không tìm thấy nội dung phù hợp.",
            )

        data = result.get("data") or {}

        return json_result(
            True,
            "search_lessons",
            data={
                "context": data.get("context", ""),
                "sources": data.get("sources", []),
            },
        )

    except Exception as exc:
        return json_result(
            False,
            "search_lessons",
            error=f"Lỗi trong quá trình truy xuất RAG: {exc}",
        )


@mcp.tool()
def get_course_plan(doc_id: str) -> str:
    """Lấy toàn bộ tài liệu theo mã doc_id."""

    if not doc_id.strip():
        return json_result(
            False,
            "get_course_plan",
            error="Vui lòng nhập mã tài liệu (doc_id).",
        )

    try:
        result = find_course_plan(
            context=retrieval_context,
            course_id=doc_id.strip(),
        )

        # Nếu tool con đã trả về chuỗi JSON thì giải mã trước khi chuẩn hóa
        if isinstance(result, str):
            result = json.loads(result)

        if isinstance(result, dict) and "success" in result:
            return json.dumps(result, ensure_ascii=False)

        return json_result(
            True,
            "get_course_plan",
            data=result,
        )

    except Exception as exc:
        return json_result(
            False,
            "get_course_plan",
            error=f"Lỗi khi lấy kế hoạch môn học: {exc}",
        )


@mcp.tool()
def create_study_request(
    student_id: str,
    course_id: str,
    request_content: str,
) -> str:
    """Tạo và lưu yêu cầu hỗ trợ học tập của sinh viên."""

    try:
        result = save_study_request(
            student_id=student_id,
            course_id=course_id,
            request_content=request_content,
        )

        if isinstance(result, str):
            return result

        return json.dumps(result, ensure_ascii=False)

    except Exception as exc:
        return json_result(
            False,
            "create_study_request",
            error=f"Lỗi khi tạo yêu cầu học tập: {exc}",
        )


@mcp.tool()
def get_study_request(request_id: str) -> str:
    """Tra cứu yêu cầu học tập theo mã yêu cầu."""

    try:
        result = find_study_request(request_id=request_id)

        if isinstance(result, str):
            return result

        return json.dumps(result, ensure_ascii=False)

    except Exception as exc:
        return json_result(
            False,
            "get_study_request",
            error=f"Lỗi khi tra cứu yêu cầu học tập: {exc}",
        )


if __name__ == "__main__":
    mcp.run(transport="stdio")
