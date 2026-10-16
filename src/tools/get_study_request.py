
import json
from pathlib import Path
from typing import Any, TypedDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REQUEST_FILE = PROJECT_ROOT / "data" / "study_requests.json"


class StudyRequestResult(TypedDict):
    success: bool
    action: str
    data: dict[str, Any] | None
    error: str | None


def get_study_request(request_id: str) -> StudyRequestResult:
    """Tra cứu yêu cầu học tập theo mã yêu cầu."""

    request_id = request_id.strip()

    if not request_id:
        return {
            "success": False,
            "action": "get_study_request",
            "data": None,
            "error": "Mã yêu cầu không được để trống.",
        }

    if not REQUEST_FILE.exists():
        return {
            "success": False,
            "action": "get_study_request",
            "data": None,
            "error": "Chưa có dữ liệu yêu cầu học tập.",
        }

    try:
        requests = json.loads(
            REQUEST_FILE.read_text(encoding="utf-8")
        )
    except (json.JSONDecodeError, OSError) as exc:
        return {
            "success": False,
            "action": "get_study_request",
            "data": None,
            "error": f"Không thể đọc dữ liệu yêu cầu học tập: {exc}",
        }

    if not isinstance(requests, list):
        return {
            "success": False,
            "action": "get_study_request",
            "data": None,
            "error": "Dữ liệu yêu cầu học tập không hợp lệ.",
        }

    for request in requests:
        if (
            isinstance(request, dict)
            and request.get("request_id", "").lower() == request_id.lower()
        ):
            return {
                "success": True,
                "action": "get_study_request",
                "data": request,
                "error": None,
            }

    return {
        "success": False,
        "action": "get_study_request",
        "data": None,
        "error": f"Không tìm thấy yêu cầu {request_id}.",
    }
