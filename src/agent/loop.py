import json
from jsonschema import validate, ValidationError
from src.agent.parser import parse_reply
from src.evaluation.logger import JSONLLogger

# Khởi tạo JSONL Logger để tự động lưu trace chạy thật vào logs/
jsonl_logger = JSONLLogger()
MAX_STEPS = 5


def mcp_tools_to_groq(mcp_tools):
    """Chuyển schema tool của MCP sang định dạng Groq."""
    result = []

    for tool in mcp_tools:
        result.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or tool.name,
                "parameters": tool.inputSchema,
            },
        })

    return result


def mcp_result_to_text(result):
    """Chuyển kết quả MCP thành nội dung đưa lại cho model."""
    parts = []

    for item in getattr(result, "content", []) or []:
        if getattr(item, "type", None) == "text":
            parts.append(item.text)

    if getattr(result, "isError", False):
        return "TOOL_ERROR: " + "\n".join(parts)

    return "\n".join(parts) or "Tool không trả về nội dung dạng text."


async def verify_and_readback(
    mcp_session,
    tool_name: str,
    arguments: dict,
    write_observation: str,
) -> str:
    """
    Nếu tool_name là create_study_request, thực hiện read-back qua get_study_request
    và xác minh dữ liệu khớp 100%. Trả về chuỗi observation mới cho LLM.
    """
    if tool_name != "create_study_request":
        return write_observation

    if write_observation.startswith("TOOL_ERROR"):
        return write_observation

    try:
        write_json = json.loads(write_observation)
    except json.JSONDecodeError:
        return write_observation

    if not write_json.get("success"):
        return write_observation

    # 1. Lấy request_id vừa tạo
    created_data = write_json.get("data") or {}
    created_id = created_data.get("request_id")

    if not created_id:
        return json.dumps({
            "success": False,
            "verified": False,
            "error": "VERIFICATION_FAILED: Tool ghi báo thành công nhưng không trả về request_id."
        }, ensure_ascii=False)

    # 2. TỰ ĐỘNG READ-BACK từ MCP Server
    read_result = await mcp_session.call_tool(
        "get_study_request",
        arguments={"request_id": created_id},
    )
    read_observation = mcp_result_to_text(read_result)

    try:
        read_json = json.loads(read_observation)
    except json.JSONDecodeError:
        return json.dumps({
            "success": False,
            "verified": False,
            "error": f"VERIFICATION_FAILED: Không thể parse JSON từ kết quả read-back của {created_id}."
        }, ensure_ascii=False)

    if not read_json.get("success"):
        return json.dumps({
            "success": False,
            "verified": False,
            "error": f"VERIFICATION_FAILED: Đã tạo {created_id} nhưng không thể đọc lại. Lỗi: {read_json.get('error')}"
        }, ensure_ascii=False)

    # 3. MATCHING CHECK (Dùng "or {}" để tránh NoneType error)
    read_record = read_json.get("data") or {}

    student_id_match = read_record.get("student_id") == arguments.get("student_id")
    course_id_match = read_record.get("course_id") == arguments.get("course_id")
    content_match = read_record.get("request_content") == arguments.get("request_content")

    if not (student_id_match and course_id_match and content_match):
        return json.dumps({
            "success": False,
            "verified": False,
            "error": (
                f"VERIFICATION_MISMATCH: Dữ liệu ghi nhận cho {created_id} không khớp với tham số truyền vào. "
                f"Input: {arguments}, Recorded: {read_record}"
            )
        }, ensure_ascii=False)

    # 4. Xác minh thành công hoàn toàn
    return json.dumps({
        "success": True,
        "verified": True,
        "action": "create_study_request",
        "data": read_record,
        "message": f"Xác minh thành công: Yêu cầu {created_id} đã được lưu và đối soát khớp 100%."
    }, ensure_ascii=False)


async def run_loop(
    client,
    mcp_session,
    question: str,
    system_prompt: str,
) -> str:
    listed = await mcp_session.list_tools()
    tools = mcp_tools_to_groq(listed.tools)

    if not tools:
        return "Lỗi cấu hình: MCP server chưa cung cấp tool nào."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]

    steps_detail = []
    total_calls = 0
    total_prompt_tokens = 0
    total_completion_tokens = 0

    for step in range(MAX_STEPS):
        total_calls += 1

        response = await client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0,
        )

        if getattr(response, "usage", None):
            total_prompt_tokens += getattr(response.usage, "prompt_tokens", 0)
            total_completion_tokens += getattr(response.usage, "completion_tokens", 0)

        message = response.choices[0].message
        decision = parse_reply(message)

        if decision["type"] == "final":
            final_answer = decision["answer"]
            jsonl_logger.log_run(
                question=question,
                final_answer=final_answer,
                steps_detail=steps_detail,
                total_calls=total_calls,
                prompt_tokens=total_prompt_tokens,
                completion_tokens=total_completion_tokens,
            )
            return final_answer

        if decision["type"] != "tool_calls":
            final_answer = "Lỗi: Model trả về phản hồi không hợp lệ."
            jsonl_logger.log_run(
                question=question,
                final_answer=final_answer,
                steps_detail=steps_detail,
                total_calls=total_calls,
                prompt_tokens=total_prompt_tokens,
                completion_tokens=total_completion_tokens,
            )
            return final_answer

        messages.append(message.model_dump(exclude_none=True))

        for call in decision["calls"]:
            tool_name = call["name"]

            allowed_names = {tool.name for tool in listed.tools}
            if tool_name not in allowed_names:
                final_answer = f"Lỗi bảo mật: Tool không được MCP công bố: {tool_name}"
                jsonl_logger.log_run(
                    question=question,
                    final_answer=final_answer,
                    steps_detail=steps_detail,
                    total_calls=total_calls,
                    prompt_tokens=total_prompt_tokens,
                    completion_tokens=total_completion_tokens,
                )
                return final_answer

            try:
                arguments = json.loads(call["arguments_json"])

                if not isinstance(arguments, dict):
                    raise ValueError("Tham số tool phải là một object JSON.")

                tool_schema = next(
                    tool.inputSchema
                    for tool in listed.tools
                    if tool.name == tool_name
                )

                validate(instance=arguments, schema=tool_schema)

                # 1. Gọi tool ban đầu
                result = await mcp_session.call_tool(
                    tool_name,
                    arguments=arguments,
                )
                raw_observation = mcp_result_to_text(result)

                # 2. TỰ ĐỘNG READ-BACK VERIFICATION
                observation = await verify_and_readback(
                    mcp_session,
                    tool_name,
                    arguments,
                    raw_observation,
                )

            except (json.JSONDecodeError, ValueError, ValidationError) as exc:
                observation = f"INVALID_TOOL_ARGUMENTS: {exc}"
                arguments = call.get("arguments_json", {})
            except Exception as exc:
                observation = f"TOOL_ERROR: {type(exc).__name__}: {exc}"
                arguments = call.get("arguments_json", {})

            steps_detail.append({
                "step": step + 1,
                "tool_called": tool_name,
                "tool_args": arguments,
                "observation": observation,
            })

            messages.append({
                "role": "tool",
                "tool_call_id": call["id"],
                "content": observation,
            })

    final_answer = "Agent đã đạt MAX_STEPS nhưng chưa tạo được câu trả lời cuối đáng tin cậy."
    jsonl_logger.log_run(
        question=question,
        final_answer=final_answer,
        steps_detail=steps_detail,
        total_calls=total_calls,
        prompt_tokens=total_prompt_tokens,
        completion_tokens=total_completion_tokens,
    )
    return final_answer