from pathlib import Path
import os

from groq import AsyncGroq
from src.agent.loop import run_loop
from dotenv import load_dotenv

load_dotenv()

PROMPT_PATH = (
    Path(__file__).resolve().parents[2]
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
    def __init__(self, mcp_session=None, api_key: str | None = None):
        # Ưu tiên lấy api_key từ tham số truyền vào, nếu không mới lấy từ os.getenv
        self.api_key = api_key or os.getenv("GROQ_API_KEY")

        if not self.api_key:
            raise ValueError("GROQ_API_KEY is missing in environment or .env file.")

        self.client = AsyncGroq(api_key=self.api_key)
        self.mcp_session = mcp_session
        self.system_prompt = load_system_prompt()

    async def ask(self, question: str) -> str:
        if not question.strip():
            return "Vui lòng nhập câu hỏi."

        if not self.mcp_session:
            raise RuntimeError("MCP Session chưa được khởi tạo cho StudyAgent.")

        return await run_loop(
            client=self.client,
            mcp_session=self.mcp_session,
            question=question.strip(),
            system_prompt=self.system_prompt,
        )