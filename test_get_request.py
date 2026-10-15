
import json
from src.mcp.server import get_study_request

result = json.loads(get_study_request("REQ0006"))

print(json.dumps(result, ensure_ascii=False, indent=2))

assert result["success"] is True
assert result["data"]["request_id"] == "REQ0006"

print("Kiểm thử thành công!")
