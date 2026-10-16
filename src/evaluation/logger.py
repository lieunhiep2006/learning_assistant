
import json
from datetime import datetime
from pathlib import Path
from typing import Any


# Thư mục và file riêng dành cho Evaluation.
BASE_DIR = Path(__file__).resolve().parents[2]
EVALUATION_LOG_DIR = BASE_DIR / "data" / "evaluation"
EVALUATION_LOG_FILE = EVALUATION_LOG_DIR / "evaluation_runs.jsonl"


class EvaluationLogger:
    def __init__(self):
        # Tạo thư mục nếu chưa tồn tại.
        EVALUATION_LOG_DIR.mkdir(parents=True, exist_ok=True)

    def log_run(self, result: dict[str, Any]) -> None:
        """Lưu kết quả của một lần Evaluation vào file JSONL."""

        record = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "type": "evaluation",
            **result,
        }

        with EVALUATION_LOG_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")


def save_evaluation(result: dict[str, Any]) -> None:
    """Giữ hàm cũ để runner có thể tiếp tục sử dụng."""

    logger = EvaluationLogger()
    logger.log_run(result)
