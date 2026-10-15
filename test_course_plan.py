
import json
from src.mcp.server import get_course_plan

result = json.loads(get_course_plan("AIPY_W1"))

print(json.dumps(result, ensure_ascii=False, indent=2))

assert result["success"] is True
assert result["data"]["doc_id"] == "AIPY_W1"

print("Kiểm thử thành công!")
