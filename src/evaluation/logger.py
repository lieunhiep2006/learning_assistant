
import json
from datetime import datetime
from pathlib import Path


# Thư mục lưu lịch sử đánh giá.
LOG_DIR = Path("data/evaluation")
LOG_FILE = LOG_DIR / "evaluation_runs.jsonl"


def save_evaluation(result: dict) -> None:
    """Lưu một lần đánh giá vào file JSONL."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        **result,
    }

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")
