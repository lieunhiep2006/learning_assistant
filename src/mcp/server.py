
from pathlib import Path
import re
import json
from datetime import datetime

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

# Xác định thư mục chứa tài liệu
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DOCUMENT_DIR = PROJECT_ROOT / "data" / "documents"
STORE_PATH = DOCUMENT_DIR / "document_store.json"

# Khởi tạo RAG context một lần khi MCP Server khởi động
retrieval_context = build_retriever(
    store_path=STORE_PATH,
    model="jina-embeddings-v3",
)


def read_documents():
    """Đọc nội dung các file Markdown."""
    documents = []

    for file_path in DOCUMENT_DIR.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        # Lấy tiêu đề từ metadata nếu có
        title_match = re.search(
            r"(?m)^title:\s*(.+)$",
            content
        )
        title = title_match.group(1).strip() if title_match else file_path.stem

        documents.append({
            "filename": file_path.name,
            "title": title,
            "content": content
        })

    return documents



@mcp.tool()
def search_lessons(query: str) -> str:
    """Tìm kiếm bài học bằng Hybrid RAG của SV1."""

    if not query.strip():
        return json.dumps({
            "status": "no_answer",
            "context": "",
            "sources": [],
        }, ensure_ascii=False)

    result = rag_search_lessons(
        context=retrieval_context,
        query=query,
        top_k=3,
        mode="hybrid",
    )

    return json.dumps(result, ensure_ascii=False)



@mcp.tool()
def get_course_plan(course_id: str) -> str:
    """Lấy nội dung kế hoạch môn học theo mã tài liệu."""

    result = find_course_plan(
        context=retrieval_context,
        course_id=course_id,
    )

    return json.dumps(result, ensure_ascii=False)




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

    result = save_study_request(
        student_id=student_id,
        course_id=course_id,
        request_content=request_content,
    )

    return json.dumps(result, ensure_ascii=False)


@mcp.tool()
def get_study_request(request_id: str) -> str:
    result = find_study_request(request_id=request_id)
    return json.dumps(result, ensure_ascii=False)

    
if __name__ == "__main__":
    mcp.run(transport="stdio")