
from pathlib import Path
import re
import json
from datetime import datetime

from mcp.server.fastmcp import FastMCP

# Khởi tạo MCP Server
mcp = FastMCP("Learning Assistant")

# Xác định thư mục chứa tài liệu
DOCUMENT_DIR = Path(__file__).resolve().parents[2] / "data" / "documents"


# def read_documents():
#     """Đọc nội dung các file Markdown."""
#     documents = []

#     for file_path in DOCUMENT_DIR.glob("*.md"):
#         content = file_path.read_text(encoding="utf-8")

#         # Lấy tiêu đề từ metadata nếu có
#         title_match = re.search(
#             r"(?m)^title:\s*(.+)$",
#             content
#         )
#         title = title_match.group(1).strip() if title_match else file_path.stem

#         documents.append({
#             "filename": file_path.name,
#             "title": title,
#             "content": content
#         })

#     return documents


# @mcp.tool()
# def search_lessons(query: str) -> str:
#     """Tìm kiếm nội dung liên quan trong các tài liệu Markdown."""

#     if not query.strip():
#         return "Vui lòng nhập nội dung cần tìm."

#     documents = read_documents()
#     keywords = query.lower().split()
#     results = []

#     for document in documents:
#         lines = document["content"].splitlines()

#         for index, line in enumerate(lines):
#             # Bỏ qua dòng trống
#             if not line.strip():
#                 continue

#             line_lower = line.lower()
#             score = sum(1 for word in keywords if word in line_lower)

#             if score > 0:
#                 results.append({
#                     "score": score,
#                     "title": document["title"],
#                     "filename": document["filename"],
#                     "line": line.strip()
#                 })

#     # Ưu tiên các đoạn khớp nhiều từ khóa hơn
#     results.sort(key=lambda item: item["score"], reverse=True)

#     if not results:
#         return "Không tìm thấy nội dung phù hợp trong tài liệu hiện có."

#     # Chỉ trả tối đa 5 kết quả
#     output = ["Kết quả tìm kiếm:"]

#     for result in results[:5]:
#         output.append(
#             f"- Tài liệu: {result['title']}\n"
#             f"  Nguồn: {result['filename']}\n"
#             f"  Nội dung: {result['line']}"
#         )

#     return "\n".join(output)


# @mcp.tool()
# def get_course_plan(course_id: str) -> str:
#     """Lấy nội dung kế hoạch môn học theo mã tài liệu."""

#     if not course_id.strip():
#         return "Vui lòng nhập mã môn học hoặc mã tài liệu."

#     documents = read_documents()

#     for document in documents:
#         doc_id_match = re.search(
#             r"(?m)^doc_id:\s*(.+)$",
#             document["content"]
#         )

#         if doc_id_match:
#             doc_id = doc_id_match.group(1).strip()

#             if doc_id.lower() == course_id.strip().lower():
#                 return (
#                     f"Tiêu đề: {document['title']}\n"
#                     f"Mã tài liệu: {doc_id}\n"
#                     f"Nguồn: {document['filename']}\n\n"
#                     f"{document['content'][:4000]}"
#                 )

#     return f"Không tìm thấy tài liệu có mã: {course_id}"

# Nơi lưu các yêu cầu học tập
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

    # Đọc dữ liệu cũ nếu file đã tồn tại
    if REQUEST_FILE.exists():
        try:
            requests = json.loads(REQUEST_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            requests = []
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