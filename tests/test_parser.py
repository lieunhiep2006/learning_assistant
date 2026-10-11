
from types import SimpleNamespace

from src.agent.parser import parse_reply


def test_final_answer():
    message = SimpleNamespace(
        tool_calls=None,
        content="Tuần 3 học về cơ sở dữ liệu."
    )

    result = parse_reply(message)

    assert result["type"] == "final"
    assert result["answer"] == "Tuần 3 học về cơ sở dữ liệu."


def test_empty_response():
    message = SimpleNamespace(
        tool_calls=None,
        content="   "
    )

    result = parse_reply(message)

    assert result["type"] == "error"


def test_tool_call():
    function = SimpleNamespace(
        name="search_lessons",
        arguments='{"query": "tuần 3"}'
    )
    call = SimpleNamespace(
        id="call_001",
        function=function
    )
    message = SimpleNamespace(
        tool_calls=[call],
        content=None
    )

    result = parse_reply(message)

    assert result["type"] == "tool_calls"
    assert result["calls"][0]["name"] == "search_lessons"
    assert result["calls"][0]["arguments_json"] == '{"query": "tuần 3"}'