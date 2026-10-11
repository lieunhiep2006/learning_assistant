
from pathlib import Path
import os

from groq import AsyncGroq
from src.agent.loop import run_loop


PROMPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "prompts"
    / "agent_system.txt"
)


def load_system_prompt() -> str:
    if not PROMPT_PATH.is_file():
        raise FileNotFoundError(
            f"Không tìm thấy file prompt: {PROMPT_PATH}"
        )

    prompt = PROMPT_PATH.read_text(encoding="utf-8").strip()

    if not prompt:
        raise ValueError("File system prompt đang trống.")

    return prompt


class StudyAgent:
    def __init__(self, mcp_session):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise RuntimeError(
                "Thiếu GROQ_API_KEY trong file .env"
            )

        self.client = AsyncGroq(api_key=api_key)
        self.mcp_session = mcp_session
        self.system_prompt = load_system_prompt()

    async def ask(self, question: str) -> str:
        if not question.strip():
            return "Vui lòng nhập câu hỏi."

        return await run_loop(
            client=self.client,
            mcp_session=self.mcp_session,
            question=question.strip(),
            system_prompt=self.system_prompt,
        )