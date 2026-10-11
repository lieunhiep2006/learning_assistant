import json
from src.agent.parser import parse_reply
from jsonschema import validate, ValidationError
from src.agent.logging_utils import setup_logger

logger = setup_logger()
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

async def run_loop(
    client,
    mcp_session,
    question: str,
    system_prompt: str,
) -> str:
    listed = await mcp_session.list_tools()
    tools = mcp_tools_to_groq(listed.tools)

    logger.info("MCP tools discovered: %d", len(listed.tools))

    if not tools:
        return "Lỗi cấu hình: MCP server chưa cung cấp tool nào."

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    for step in range(MAX_STEPS):

        logger.info("Agent step %d/%d", step + 1, MAX_STEPS)

        response = await client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0,
        )

        message = response.choices[0].message
        decision = parse_reply(message)

        if decision["type"] == "final":
            logger.info("Agent completed with a final answer at step %d", step + 1)
            return decision["answer"]

        if decision["type"] != "tool_calls":
            return "Lỗi: Model trả về phản hồi không hợp lệ."


        messages.append(message.model_dump(exclude_none=True))

        for call in decision["calls"]:
            tool_name = call["name"]


            allowed_names = {tool.name for tool in listed.tools}
            if tool_name not in allowed_names:
                return f"Lỗi bảo mật: Tool không được MCP công bố: {tool_name}"

            logger.info("Calling MCP tool: %s", tool_name)

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
                
                result = await mcp_session.call_tool(
                    tool_name,
                    arguments=arguments,
                )
                observation = mcp_result_to_text(result)

                if getattr(result, "isError", False):
                    logger.warning("MCP tool returned an error: %s", tool_name)
                else:
                    logger.info("MCP tool completed: %s", tool_name)

            except (json.JSONDecodeError, ValueError, ValidationError) as exc:
                observation = f"INVALID_TOOL_ARGUMENTS: {exc}"
                logger.warning("Invalid arguments for MCP tool %s: %s", tool_name, exc,)
            except Exception as exc:
                observation = f"TOOL_ERROR: {type(exc).__name__}: {exc}"
                logger.exception("MCP tool failed: %s", tool_name)

            messages.append({
                "role": "tool",
                "tool_call_id": call["id"],
                "content": observation,
            })
    logger.warning("Agent reached MAX_STEPS=%d", MAX_STEPS)
    return (
        "Agent đã đạt MAX_STEPS nhưng chưa tạo được câu trả lời cuối đáng tin cậy."
    )