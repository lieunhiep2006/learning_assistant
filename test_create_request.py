from src.mcp.server import create_study_request

result = create_study_request(
    student_id="SV001",
    course_id="AIPY_W1",
    request_content="Can ho tro bai tap Python"
)

print(result)
