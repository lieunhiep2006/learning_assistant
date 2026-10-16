
import json
from datetime import datetime
from pathlib import Path
from typing import Any


# Thư mục gốc của dự án
BASE_DIR = Path(__file__).resolve().parents[2]

# Thư mục lưu log hoạt động của Agent
LOGS_DIR = BASE_DIR / "logs"

# Thư mục và file lưu kết quả Evaluation
EVALUATION_LOG_DIR = BASE_DIR / "data" / "evaluation"
EVALUATION_LOG_FILE = EVALUATION_LOG_DIR / "evaluation_runs.jsonl"


class JSONLLogger:
    """Ghi log cho các lượt xử lý câu hỏi của Agent."""

    def __init__(self):
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

        # Tạo file log riêng theo thời gian chạy
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_filepath = LOGS_DIR / f"run_{timestamp_str}.jsonl"

    def log_run(
        self,
        question: str,
        final_answer: str,
        steps_detail: list[dict[str, Any]],
        total_calls: int,
        prompt_tokens: int,
        completion_tokens: int,
    ) -> None:
        """Ghi thông tin một lượt xử lý của Agent."""

        record = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "final_answer": final_answer,
            "total_steps": len(steps_detail),
            "steps": steps_detail,
            "usage": {
                "calls": total_calls,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
            },
        }

        with self.log_filepath.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")


class EvaluationLogger:
    """Ghi kết quả đánh giá hệ thống vào file JSONL."""

    def __init__(self):
        EVALUATION_LOG_DIR.mkdir(parents=True, exist_ok=True)

    def log_run(self, result: dict[str, Any]) -> None:
        """Lưu kết quả của một lần Evaluation."""

        record = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "type": "evaluation",
            **result,
        }

        with EVALUATION_LOG_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")


def save_evaluation(result: dict[str, Any]) -> None:
    """Giữ hàm tương thích với evaluation runner hiện tại."""

    logger = EvaluationLogger()
    logger.log_run(result)
