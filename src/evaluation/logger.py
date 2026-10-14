import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

LOGS_DIR = Path(__file__).resolve().parents[2] / "logs"


class JSONLLogger:
    def __init__(self):
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        # Tạo tên file có timestamp: run_YYYYMMDD_HHMMSS.jsonl
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_filepath = LOGS_DIR / f"run_{timestamp_str}.jsonl"

    def log_run(
        self,
        question: str,
        final_answer: str,
        steps_detail: List[Dict[str, Any]],
        total_calls: int,
        prompt_tokens: int,
        completion_tokens: int,
    ):
        """Ghi 1 dòng JSONL cho 1 lượt xử lý câu hỏi của Agent."""
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

        with open(self.log_filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")