from typing import Any


def parse_reply(message: Any) -> dict:
    """Đọc phản hồi chuẩn của Groq/OpenAI-compatible API."""

    tool_calls = getattr(message, "tool_calls", None)

    if tool_calls:
        return {
            "type": "tool_calls",
            "calls": [
                {
                    "id": call.id,
                    "name": call.function.name,
                    "arguments_json": call.function.arguments,
                }
                for call in tool_calls
            ],
        }

    answer = getattr(message, "content", None)

    if answer and answer.strip():
        return {
            "type": "final",
            "answer": answer.strip(),
        }

    return {
        "type": "error",
        "message": "Model không trả về câu trả lời hoặc tool call.",
    }