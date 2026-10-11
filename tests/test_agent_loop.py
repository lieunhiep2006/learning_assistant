
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from src.agent.loop import run_loop


def make_tool_call(name, arguments, call_id="call_1"):
    return SimpleNamespace(
        id=call_id,
        function=SimpleNamespace(
            name=name,
            arguments=arguments,
        ),
    )


def make_response(content=None, tool_calls=None):
    message = SimpleNamespace(
        content=content,
        tool_calls=tool_calls,
        model_dump=lambda **kwargs: {
            "role": "assistant",
            "content": content,
            "tool_calls": [],
        },
    )

    return SimpleNamespace(
        choices=[SimpleNamespace(message=message)]
    )


@pytest.mark.asyncio
async def test_model_answers_directly():
    """Model trả lời ngay, không cần gọi tool."""
    client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(
                create=AsyncMock(
                    return_value=make_response(
                        content="Đây là câu trả lời."
                    )
                )
            )
        )
    )

    mcp_session = SimpleNamespace(
        list_tools=AsyncMock(
            return_value=SimpleNamespace(tools=[
                SimpleNamespace(
                    name="search_lessons",
                    description="Tìm bài học",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"}
                        },
                        "required": ["query"],
                    },
                )
            ])
        ),
        call_tool=AsyncMock(),
    )

    result = await run_loop(
        client,
        mcp_session,
        "Xin chào",
        "Bạn là trợ lý học tập.",
    )

    assert result == "Đây là câu trả lời."
    mcp_session.call_tool.assert_not_awaited()


@pytest.mark.asyncio
async def test_agent_calls_tool_and_returns_answer():
    """Agent gọi tool, nhận kết quả rồi trả lời."""

    tool_call = make_tool_call(
        name="search_lessons",
        arguments='{"query": "Python"}',
    )

    client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(
                create=AsyncMock(side_effect=[
                    make_response(tool_calls=[tool_call]),
                    make_response(content="Giáo án có nội dung Python."),
                ])
            )
        )
    )

    mcp_session = SimpleNamespace(
        list_tools=AsyncMock(
            return_value=SimpleNamespace(tools=[
                SimpleNamespace(
                    name="search_lessons",
                    description="Tìm kiếm bài học",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"}
                        },
                        "required": ["query"],
                    },
                )
            ])
        ),
        call_tool=AsyncMock(
            return_value=SimpleNamespace(
                content=[
                    SimpleNamespace(
                        type="text",
                        text="Tìm thấy giáo án Python."
                    )
                ],
                isError=False,
            )
        ),
    )

    result = await run_loop(
        client,
        mcp_session,
        "Tìm bài học Python",
        "Bạn là trợ lý học tập.",
    )

    assert result == "Giáo án có nội dung Python."

    mcp_session.call_tool.assert_awaited_once_with(
        "search_lessons",
        arguments={"query": "Python"},
    )

    assert client.chat.completions.create.await_count == 2

@pytest.mark.asyncio
async def test_invalid_tool_arguments_do_not_crash():
    """JSON tham số sai thì Agent báo lỗi cho model, không crash."""

    tool_call = make_tool_call(
        name="search_lessons",
        arguments='{"query": ',  # JSON không hợp lệ
    )

    client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(
                create=AsyncMock(side_effect=[
                    make_response(tool_calls=[tool_call]),
                    make_response(content="Không thể tìm kiếm do tham số không hợp lệ."),
                ])
            )
        )
    )

    mcp_session = SimpleNamespace(
        list_tools=AsyncMock(
            return_value=SimpleNamespace(tools=[
                SimpleNamespace(
                    name="search_lessons",
                    description="Tìm kiếm bài học",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"}
                        },
                        "required": ["query"],
                    },
                )
            ])
        ),
        call_tool=AsyncMock(),
    )

    result = await run_loop(
        client,
        mcp_session,
        "Tìm bài học",
        "Bạn là trợ lý học tập.",
    )

    assert result == "Không thể tìm kiếm do tham số không hợp lệ."
    mcp_session.call_tool.assert_not_awaited()
    assert client.chat.completions.create.await_count == 2


@pytest.mark.asyncio
async def test_tool_failure_does_not_crash_agent():
    """Tool bị lỗi thì Agent nhận observation và tiếp tục."""

    tool_call = make_tool_call(
        name="search_lessons",
        arguments='{"query": "Python"}',
    )

    client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(
                create=AsyncMock(side_effect=[
                    make_response(tool_calls=[tool_call]),
                    make_response(content="Hiện chưa thể tìm kiếm giáo án."),
                ])
            )
        )
    )

    mcp_session = SimpleNamespace(
        list_tools=AsyncMock(
            return_value=SimpleNamespace(tools=[
                SimpleNamespace(
                    name="search_lessons",
                    description="Tìm bài học",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"}
                        },
                        "required": ["query"],
                    },
                )
            ])
        ),
        call_tool=AsyncMock(
            side_effect=RuntimeError("MCP server unavailable")
        ),
    )

    result = await run_loop(
        client,
        mcp_session,
        "Tìm bài học Python",
        "Bạn là trợ lý học tập.",
    )

    assert result == "Hiện chưa thể tìm kiếm giáo án."
    assert client.chat.completions.create.await_count == 2
    mcp_session.call_tool.assert_awaited_once()

@pytest.mark.asyncio
async def test_agent_stops_at_max_steps():
    """Agent phải dừng khi model liên tục yêu cầu gọi tool."""

    tool_call = make_tool_call(
        name="search_lessons",
        arguments='{"query": "Python"}',
    )

    client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(
                create=AsyncMock(
                    return_value=make_response(
                        tool_calls=[tool_call]
                    )
                )
            )
        )
    )

    mcp_session = SimpleNamespace(
        list_tools=AsyncMock(
            return_value=SimpleNamespace(tools=[
                SimpleNamespace(
                    name="search_lessons",
                    description="Tìm bài học",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"}
                        },
                        "required": ["query"],
                    },
                )
            ])
        ),
        call_tool=AsyncMock(
            return_value=SimpleNamespace(
                content=[
                    SimpleNamespace(
                        type="text",
                        text="Có kết quả."
                    )
                ],
                isError=False,
            )
        ),
    )

    result = await run_loop(
        client,
        mcp_session,
        "Tìm bài học Python",
        "Bạn là trợ lý học tập.",
    )

    assert "MAX_STEPS" in result
    assert client.chat.completions.create.await_count == 5
    assert mcp_session.call_tool.await_count == 5

@pytest.mark.asyncio
async def test_missing_required_argument_does_not_call_tool():
    """JSON hợp lệ nhưng thiếu query thì không gọi MCP."""

    tool_call = make_tool_call(
        name="search_lessons",
        arguments="{}",
    )

    client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(
                create=AsyncMock(side_effect=[
                    make_response(tool_calls=[tool_call]),
                    make_response(content="Bạn chưa cung cấp từ khóa tìm kiếm."),
                ])
            )
        )
    )

    mcp_session = SimpleNamespace(
        list_tools=AsyncMock(
            return_value=SimpleNamespace(tools=[
                SimpleNamespace(
                    name="search_lessons",
                    description="Tìm bài học",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"}
                        },
                        "required": ["query"],
                    },
                )
            ])
        ),
        call_tool=AsyncMock(),
    )

    result = await run_loop(
        client,
        mcp_session,
        "Tìm bài học",
        "Bạn là trợ lý học tập.",
    )

    assert result == "Bạn chưa cung cấp từ khóa tìm kiếm."
    mcp_session.call_tool.assert_not_awaited()
    assert client.chat.completions.create.await_count == 2

@pytest.mark.asyncio
async def test_agent_rejects_unlisted_tool():
    """Agent phải từ chối tool mà MCP không công bố."""

    tool_call = make_tool_call(
        name="delete_all_data",
        arguments="{}",
    )

    client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(
                create=AsyncMock(
                    return_value=make_response(
                        tool_calls=[tool_call]
                    )
                )
            )
        )
    )

    mcp_session = SimpleNamespace(
        list_tools=AsyncMock(
            return_value=SimpleNamespace(tools=[
                SimpleNamespace(
                    name="search_lessons",
                    description="Tìm bài học",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"}
                        },
                        "required": ["query"],
                    },
                )
            ])
        ),
        call_tool=AsyncMock(),
    )

    result = await run_loop(
        client,
        mcp_session,
        "Xóa toàn bộ dữ liệu",
        "Bạn là trợ lý học tập.",
    )

    assert "Lỗi bảo mật" in result
    assert "delete_all_data" in result
    mcp_session.call_tool.assert_not_awaited()

@pytest.mark.asyncio
async def test_compare_two_courses_when_one_course_is_missing():
    """Agent không được bịa dữ liệu khi chỉ tìm thấy một trong hai môn."""
    from unittest.mock import AsyncMock, MagicMock

    client = MagicMock()
    mcp_session = MagicMock()

    # Giả sử MCP có tool tìm kiếm lesson.
    tool = MagicMock()
    tool.name = "search_lessons"
    tool.description = "Tìm lesson theo truy vấn"
    tool.inputSchema = {
        "type": "object",
        "properties": {
            "query": {"type": "string"}
        },
        "required": ["query"],
    }

    mcp_session.list_tools = AsyncMock(
        return_value=MagicMock(tools=[tool])
    )

    # Lần gọi model đầu tiên: tìm thông tin hai môn.
    tool_call = MagicMock()
    tool_call.id = "call_1"
    tool_call.function.name = "search_lessons"
    tool_call.function.arguments = '{"query": "So sánh môn A và môn B"}'

    assistant_message = MagicMock()
    assistant_message.tool_calls = [tool_call]
    assistant_message.content = None
    assistant_message.model_dump.return_value = {
        "role": "assistant",
        "tool_calls": [{
            "id": "call_1",
            "type": "function",
            "function": {
                "name": "search_lessons",
                "arguments": '{"query": "So sánh môn A và môn B"}',
            },
        }],
    }

    # Lần gọi model tiếp theo: trả lời có nêu rõ dữ liệu còn thiếu.
    final_message = MagicMock()
    final_message.tool_calls = None
    final_message.content = (
        "Tôi chỉ tìm thấy dữ liệu của môn A. "
        "Chưa có đủ thông tin về môn B nên chưa thể so sánh đáng tin cậy."
    )

    first_response = MagicMock()
    first_response.choices = [MagicMock(message=assistant_message)]

    second_response = MagicMock()
    second_response.choices = [MagicMock(message=final_message)]

    client.chat.completions.create = AsyncMock(
        side_effect=[first_response, second_response]
    )

    mcp_session.call_tool = AsyncMock(
        return_value=MagicMock(
            content=[MagicMock(type="text", text="Thông tin lesson của môn A")],
            isError=False,
        )
    )

    answer = await run_loop(
        client=client,
        mcp_session=mcp_session,
        question="So sánh môn A và môn B",
        system_prompt=(
            "Nếu thiếu dữ liệu của một môn, phải nêu rõ dữ liệu còn thiếu "
            "và không được tự bịa nội dung để so sánh."
        ),
    )

    assert "môn a" in answer.lower()
    assert "môn b" in answer.lower()
    assert any(
        phrase in answer.lower()
        for phrase in ["chưa đủ", "chưa có đủ", "thiếu dữ liệu", "chưa tìm thấy"]
    )
    assert mcp_session.call_tool.await_count == 1

