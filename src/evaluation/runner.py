
import json
from pathlib import Path

from src.rag.retriever import build_retriever
from src.tools.search_lessons import search_lessons
from src.evaluation.metrics import (
    refusal_accuracy,
    source_retrieval_accuracy,
)
from src.evaluation.logger import save_evaluation


# Đường dẫn dữ liệu
BASE_DIR = Path(__file__).resolve().parents[2]
TESTSET_PATH = BASE_DIR / "tests" / "testset.jsonl"
STORE_PATH = BASE_DIR / "data" / "documents" / "document_store.json"
CACHE_PATH = (
    BASE_DIR / "data" / "documents" / "document_store.embeddings.json"
)


def load_testset(path: Path) -> list[dict]:
    """Đọc từng trường hợp kiểm thử từ file JSONL."""
    cases = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                cases.append(json.loads(line))

    return cases


def run_evaluation() -> None:
    """Chạy đánh giá retrieval và lưu kết quả Evaluation."""

    # 1. Đọc bộ dữ liệu kiểm thử
    cases = load_testset(TESTSET_PATH)

    # 2. Khởi tạo retriever
    context = build_retriever(
        store_path=STORE_PATH,
        cache_path=CACHE_PATH,
    )

    # 3. Chuẩn bị dữ liệu tính metrics
    expected_answers = []
    actual_answers = []

    expected_sources = []
    retrieved_sources = []
    source_matches = []

    case_results = []

    # 4. Chạy từng trường hợp kiểm thử
    for case in cases:
        result = search_lessons(
            context=context,
            query=case["question"],
            top_k=case.get("top_k", 3),
            mode="hybrid",
        )

        # Đọc định dạng trả về mới của search_lessons()
        actual_answer = result["success"]
        result_data = result["data"] or {}
        retrieved_sources_for_case = result_data.get("sources", [])

        # Chuẩn bị dữ liệu tính Refusal Accuracy
        expected_answers.append(case["expect_answer"])
        actual_answers.append(actual_answer)

        # Chỉ đánh giá nguồn đối với test case có nguồn mong đợi
        if case.get("expected_sources", []):
            expected_sources.append(case.get("expected_sources", []))
            retrieved_sources.append(retrieved_sources_for_case)
            source_matches.append(case["source_match"])

        # Lưu chi tiết từng test case
        case_result = {
            "id": case["id"],
            "question": case["question"],
            "expected_answer": case["expect_answer"],
            "actual_answer": actual_answer,
            "action": result["action"],
            "status": "ok" if actual_answer else "no_answer",
            "expected_sources": case.get("expected_sources", []),
            "retrieved_sources": retrieved_sources_for_case,
            "error": result["error"],
        }

        case_results.append(case_result)

        # Hiển thị kết quả từng trường hợp
        print(f"\nID: {case['id']}")
        print(f"Question: {case['question']}")
        print(f"Expected answer: {case['expect_answer']}")
        print(f"Actual answer: {actual_answer}")
        print(f"Status: {case_result['status']}")
        print(f"Expected sources: {case.get('expected_sources', [])}")
        print(f"Retrieved sources: {retrieved_sources_for_case}")

        if result["error"]:
            print(f"Error: {result['error']}")

    # 5. Tính các chỉ số đánh giá
    refusal_score = refusal_accuracy(
        expected_answers,
        actual_answers,
    )

    if expected_sources:
        source_score = source_retrieval_accuracy(
            expected_sources,
            retrieved_sources,
            source_matches,
        )
    else:
        source_score = 0.0

    # 6. Hiển thị tổng kết
    print("\n===== EVALUATION RESULTS =====")
    print(f"Tổng số câu hỏi: {len(cases)}")
    print(f"Refusal Accuracy: {refusal_score:.2%}")
    print(f"Source Retrieval Accuracy: {source_score:.2%}")
    print(f"Số câu được đánh giá nguồn: {len(expected_sources)}")

    # 7. Lưu kết quả Evaluation
    save_evaluation({
        "total_questions": len(cases),
        "refusal_accuracy": refusal_score,
        "source_retrieval_accuracy": source_score,
        "evaluated_source_cases": len(expected_sources),
        "case_results": case_results,
    })

    print("Đã lưu kết quả Evaluation.")


if __name__ == "__main__":
    run_evaluation()
