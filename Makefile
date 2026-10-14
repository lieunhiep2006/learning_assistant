.PHONY: setup demo eval clean

setup:
	@echo "=== [1/2] Cài đặt môi trường và dependencies từ pyproject.toml ==="
	uv pip install -e . || pip install -e .
	@echo "=== Cài đặt hoàn tất! ==="

demo:
	@echo "=== [2/2] Khởi chạy SV2 Learning Assistant Agent ==="
	uv run python main.py

eval:
	@echo "=== Chạy pipeline đánh giá benchmark (3 runs) ==="
	uv run python -m src.evaluation.runner

clean:
	rm -rf __pycache__ *.egg-info .pytest_cache logs/*.tmp