
import json
from pathlib import Path
from typing import TypedDict


# Xác định đường dẫn thư mục gốc của project
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Đường dẫn file lưu các yêu cầu học tập
REQUEST_FILE = PROJECT_ROOT / "data" / "study_requests.json"


# Quy định cấu trúc dữ liệu trả về
class StudyRequestResult(TypedDict):
    success: bool
    action: str
    data: dict | None
    error: str | None


def get_study_request(request_id: str) -> StudyRequestResult:
    # Kiểm tra mã yêu cầu có bị bỏ trống không
    if not request_id.strip():
        return {
            "success": False,
            "action": "get_study_request",
            "data": None,
            "error": "Mã yêu cầu không được để trống."
        }

    # Kiểm tra file dữ liệu có tồn tại không
    if not REQUEST_FILE.exists():
        return {
            "success": False,
            "action": "get_study_request",
            "data": None,
            "error": "Chưa có dữ liệu yêu cầu học tập."
        }

    # Đọc danh sách yêu cầu từ file JSON
    with open(REQUEST_FILE, "r", encoding="utf-8") as file:
        requests = json.load(file)

    # Tìm yêu cầu theo mã, không phân biệt chữ hoa và chữ thường
    for request in requests:
        if request.get("request_id", "").lower() == request_id.strip().lower():
            return {
                "success": True,
                "action": "get_study_request",
                "data": request,
                "error": None
            }

    # Không tìm thấy mã yêu cầu
    return {
        "success": False,
        "action": "get_study_request",
        "data": None,
        "error": f"Không tìm thấy yêu cầu {request_id}."
    }
