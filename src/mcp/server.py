
from pathlib import Path
import json
from datetime import datetime

from mcp.server.fastmcp import FastMCP

from src.tools.search_lessons import search_lessons as rag_search_lessons
from src.rag.retriever import build_retriever

# Khởi tạo MCP Server
mcp = FastMCP("Learning Assistant")

STORE_PATH = Path(__file__).resolve().parents[2] / "data"/ "documents" / "document_store.json"
RAG_CONTEXT = build_retriever(store_path=STORE_PATH)
@mcp.tool()
def search_lessons(query: str, top_k: int = 3, mode: str = "hybrid") -> str:
    """Tìm kiếm nội dung bài giảng liên quan trong hệ thống bằng RAG."""

    if not query.strip():
        return json.dumps({
            "success": False,
            "action": "search_lessons",
            "data": None,
            "error": "Vui lòng nhập nội dung cần tìm."
        }, ensure_ascii=False)

    try:
        # Gọi hàm RAG từ src/tools/search_lesson.py
        result = rag_search_lessons(
            context=RAG_CONTEXT,
            query=query,
            top_k=top_k,
            mode=mode
        )

        if result["status"] == "no_answer":
            return json.dumps({
                "success": False,
                "action": "search_lessons",
                "data": {
                    "context": "",
                    "sources": []
                },
                "error": "Không tìm thấy thông tin phù hợp trong tài liệu bài giảng."
            }, ensure_ascii=False)

        return json.dumps({
            "success": True,
            "action": "search_lessons",
            "data": {
                "context": result["context"],
                "sources": [
                    {
                        "doc_id": getattr(src, "doc_id", ""),
                        "heading": getattr(src, "heading", ""),
                        "filename": getattr(src, "filename", "")
                    } if hasattr(src, "__dict__") else src
                    for src in result["sources"]
                ]
            },
            "error": None
        }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({
            "success": False,
            "action": "search_lessons",
            "data": None,
            "error": f"Lỗi trong quá trình RAG retrieval: {str(e)}"
        }, ensure_ascii=False)

@mcp.tool()
def get_course_plan(doc_id: str) -> str:
    """Lấy toàn bộ tài liệu theo mã doc_id chính xác."""

    target_id = doc_id.strip().casefold()
    if not target_id:
        return json.dumps({
            "success": False,
            "action": "get_course_plan",
            "data": None,
            "error": "Vui lòng nhập mã tài liệu (doc_id)."
        }, ensure_ascii=False)

    documents = RAG_CONTEXT.store.list_all()
    matched_doc = next(
        (
            document
            for document in documents
            if document.doc_id.casefold() == target_id
        ),
        None,
    )

    if matched_doc is None:
        available_doc_ids = sorted(
            document.doc_id for document in documents
        )
        return json.dumps({
            "success": False,
            "action": "get_course_plan",
            "data": {
                "available_doc_ids": available_doc_ids,
            },
            "error": f"Không tìm thấy tài liệu có doc_id: {doc_id.strip()}",
        }, ensure_ascii=False)

    return json.dumps({
        "success": True,
        "action": "get_course_plan",
        "data": {
            "doc_id": matched_doc.doc_id,
            "title": matched_doc.title,
            "source": matched_doc.source,
            "version": matched_doc.version,
            "owner": matched_doc.owner,
            "content": matched_doc.content,
            "metadata": matched_doc.metadata,
        },
        "error": None,
    }, ensure_ascii=False)

REQUEST_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "study_requests.json"
)


@mcp.tool()
def create_study_request(
    student_id: str,
    course_id: str,
    request_content: str,
) -> str:
    """Tạo và lưu yêu cầu hỗ trợ học tập của sinh viên."""

    if not student_id.strip():
        return json.dumps({
            "success": False,
            "action": "create_study_request",
            "data": None,
            "error": "Mã sinh viên không được để trống."
        }, ensure_ascii=False)

    if not course_id.strip():
        return json.dumps({
            "success": False,
            "action": "create_study_request",
            "data": None,
            "error": "Mã môn học không được để trống."
        }, ensure_ascii=False)

    if not request_content.strip():
        return json.dumps({
            "success": False,
            "action": "create_study_request",
            "data": None,
            "error": "Nội dung yêu cầu không được để trống."
        }, ensure_ascii=False)

    # Đọc dữ liệu cũ; nếu file lỗi hoặc sai cấu trúc thì dừng, không ghi đè.
    if REQUEST_FILE.exists():
        try:
            requests = json.loads(REQUEST_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return json.dumps({
                "success": False,
                "action": "create_study_request",
                "data": None,
                "error": (
                    "File yêu cầu học tập không phải JSON hợp lệ; "
                    f"không ghi dữ liệu mới (dòng {exc.lineno}, cột {exc.colno})."
                ),
            }, ensure_ascii=False)
        except OSError as exc:
            return json.dumps({
                "success": False,
                "action": "create_study_request",
                "data": None,
                "error": (
                    "Không thể đọc file yêu cầu học tập; "
                    f"không ghi dữ liệu mới ({type(exc).__name__})."
                ),
            }, ensure_ascii=False)

        if not isinstance(requests, list) or any(
            not isinstance(item, dict)
            or not isinstance(item.get("request_id"), str)
            for item in requests
        ):
            return json.dumps({
                "success": False,
                "action": "create_study_request",
                "data": None,
                "error": (
                    "Cấu trúc file yêu cầu học tập không hợp lệ; "
                    "không ghi dữ liệu mới."
                ),
            }, ensure_ascii=False)
    else:
        requests = []

    # Tạo mã yêu cầu mới
    request_id = f"REQ{len(requests) + 1:04d}"

    new_request = {
        "request_id": request_id,
        "student_id": student_id.strip(),
        "course_id": course_id.strip(),
        "request_content": request_content.strip(),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "pending",
    }

    requests.append(new_request)

    # Ghi dữ liệu xuống file JSON
    REQUEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    REQUEST_FILE.write_text(
        json.dumps(requests, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return json.dumps({
        "success": True,
        "action": "create_study_request",
        "data": new_request,
        "error": None
    }, ensure_ascii=False)


@mcp.tool()
def get_study_request(request_id: str) -> str:
    """Lấy thông tin yêu cầu học tập theo mã yêu cầu."""

    if not request_id.strip():
        return json.dumps({
            "success": False,
            "action": "get_study_request",
            "data": None,
            "error": "Vui lòng nhập mã yêu cầu."
        }, ensure_ascii=False)

    if not REQUEST_FILE.exists():
        return json.dumps({
            "success": False,
            "action": "get_study_request",
            "data": None,
            "error": "Chưa có yêu cầu học tập nào được lưu."
        }, ensure_ascii=False)

    try:
        requests = json.loads(REQUEST_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return json.dumps({
            "success": False,
            "action": "get_study_request",
            "data": None,
            "error": "Không thể đọc dữ liệu yêu cầu học tập."
        }, ensure_ascii=False)

    for request in requests:
        if request["request_id"].lower() == request_id.strip().lower():
            return json.dumps({
                "success": True,
                "action": "get_study_request",
                "data": request,
                "error": None
            }, ensure_ascii=False)

    return json.dumps({
        "success": False,
        "action": "get_study_request",
        "data": None,
        "error": f"Không tìm thấy yêu cầu có mã: {request_id}"
    }, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run(transport="stdio")