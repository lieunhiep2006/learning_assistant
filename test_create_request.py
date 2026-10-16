
import json
from src.mcp.server import create_study_request

result = json.loads(
    create_study_request(
        student_id="SV001",
        course_id="AIPY_W1",
        request_content="Hỗ trợ ôn tập bài Python cơ bản.",
    )
)

print(json.dumps(result, ensure_ascii=False, indent=2))

assert result["success"] is True
assert result["data"]["request_id"].startswith("REQ")
assert result["data"]["status"] == "pending"

print("Kiểm thử thành công!")
