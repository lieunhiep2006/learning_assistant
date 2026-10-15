
import json
from pathlib import Path

from src.rag.retriever import build_retriever
from src.tools.search_lessons import search_lessons
from src.evaluation.metrics import (
    refusal_accuracy,
    source_retrieval_accuracy,
)
from src.evaluation.logger import save_evaluation


TESTSET_PATH = Path("tests/testset.jsonl")
STORE_PATH = Path("data/documents/document_store.json")
CACHE_PATH = Path("data/documents/document_store.embeddings.json")


def load_testset(path: Path) -> list[dict]:
    """Đọc từng trường hợp kiểm thử từ file JSONL."""
    cases = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                cases.append(json.loads(line))

    return cases


def run_evaluation() -> None:
    """Chạy đánh giá retrieval và lưu kết quả."""
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
            top_k=case["top_k"],
            mode="hybrid",
        )

        actual_answer = result["status"] == "ok"

        expected_answers.append(case["expect_answer"])
        actual_answers.append(actual_answer)

        if case["expected_sources"]:
            expected_sources.append(case["expected_sources"])
            retrieved_sources.append(result["sources"])
            source_matches.append(case["source_match"])

        # Lưu chi tiết kết quả của từng câu hỏi
        case_results.append({
            "id": case["id"],
            "question": case["question"],
            "expected_answer": case["expect_answer"],
            "actual_answer": actual_answer,
            "status": result["status"],
            "expected_sources": case["expected_sources"],
            "retrieved_sources": result["sources"],
        })

        # Hiển thị kết quả từng trường hợp
        print(f"\nID: {case['id']}")
        print(f"Question: {case['question']}")
        print(f"Expected answer: {case['expect_answer']}")
        print(f"Actual answer: {actual_answer}")
        print(f"Status: {result['status']}")
        print(f"Expected sources: {case['expected_sources']}")
        print(f"Retrieved sources: {result['sources']}")

    # 5. Tính các chỉ số đánh giá
    refusal_score = refusal_accuracy(
        expected_answers,
        actual_answers,
    )

    source_score = (
        source_retrieval_accuracy(
            expected_sources,
            retrieved_sources,
            source_matches,
        )
        if expected_sources
        else 0.0
    )

    # 6. Hiển thị tổng kết
    print("\n===== EVALUATION RESULTS =====")
    print(f"Tổng số câu hỏi: {len(cases)}")
    print(f"Refusal Accuracy: {refusal_score:.2%}")
    print(f"Source Retrieval Accuracy: {source_score:.2%}")
    print(f"Số câu được đánh giá nguồn: {len(expected_sources)}")

    # 7. Lưu kết quả vào file JSONL
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
