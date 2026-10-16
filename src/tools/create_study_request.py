
import json
from datetime import datetime
from pathlib import Path
from typing import TypedDict, Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REQUEST_FILE = PROJECT_ROOT / "data" / "study_requests.json"


class StudyRequestResult(TypedDict):
    success: bool
    action: str
    data: dict[str, Any] | None
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
        try:
            requests = json.loads(
                REQUEST_FILE.read_text(encoding="utf-8")
            )
        except (json.JSONDecodeError, OSError) as exc:
            return {
                "success": False,
                "action": "create_study_request",
                "data": None,
                "error": f"Không thể đọc file yêu cầu học tập: {exc}",
            }

        if not isinstance(requests, list):
            return {
                "success": False,
                "action": "create_study_request",
                "data": None,
                "error": "Dữ liệu yêu cầu học tập phải là một danh sách JSON.",
            }
    else:
        requests = []

    # Tạo mã yêu cầu mới, tránh trùng mã khi danh sách có lỗ hổng
    existing_ids = {
        item.get("request_id")
        for item in requests
        if isinstance(item, dict)
    }

    number = len(requests) + 1
    request_id = f"REQ{number:04d}"

    while request_id in existing_ids:
        number += 1
        request_id = f"REQ{number:04d}"

    new_request = {
        "request_id": request_id,
        "student_id": student_id.strip(),
        "course_id": course_id.strip(),
        "request_content": request_content.strip(),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "pending",
    }

    # Lưu yêu cầu vào file JSON
    requests.append(new_request)

    try:
        REQUEST_FILE.parent.mkdir(parents=True, exist_ok=True)
        REQUEST_FILE.write_text(
            json.dumps(requests, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except OSError as exc:
        return {
            "success": False,
            "action": "create_study_request",
            "data": None,
            "error": f"Không thể lưu yêu cầu học tập: {exc}",
        }

    return {
        "success": True,
        "action": "create_study_request",
        "data": new_request,
        "error": None,
    }
