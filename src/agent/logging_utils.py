
import logging
import os


def setup_logger():
    """Tạo logger cho Agent, không ghi API key hoặc nội dung nhạy cảm."""

    logger = logging.getLogger("study_agent")

    if logger.handlers:
        return logger

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(log_level)

    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
    )

    logger.addHandler(handler)
    logger.propagate = False

    return logger