
import json
from pathlib import Path
from datetime import datetime
from typing import TypedDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REQUEST_FILE = PROJECT_ROOT / "data" / "study_requests.json"


class StudyRequestResult(TypedDict):
    success: bool
    action: str
    data: dict | None
    error: str | None


def create_study_request(
    student_id: str,
    course_id: str,
    request_content: str,
) -> StudyRequestResult:
    """Tạo và lưu yêu cầu hỗ trợ học tập của sinh viên."""

    # Kiểm tra dữ liệu đầu vào
    if not student_id.strip():
        return {
            "success": False,
            "action": "create_study_request",
            "data": None,
            "error": "Vui lòng nhập mã sinh viên.",
        }

    if not course_id.strip():
        return {
            "success": False,
            "action": "create_study_request",
            "data": None,
            "error": "Vui lòng nhập mã khóa học.",
        }

    if not request_content.strip():
        return {
            "success": False,
            "action": "create_study_request",
            "data": None,
            "error": "Vui lòng nhập nội dung yêu cầu.",
        }

    # Đọc các yêu cầu đã lưu
    if REQUEST_FILE.exists():
        requests = json.loads(
            REQUEST_FILE.read_text(encoding="utf-8")
        )
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

    # Lưu yêu cầu vào file JSON
    REQUEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    requests.append(new_request)

    REQUEST_FILE.write_text(
        json.dumps(requests, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {
        "success": True,
        "action": "create_study_request",
        "data": new_request,
        "error": None,
    }
