
from src.evaluation.metrics import (
    refusal_accuracy,
    answer_keyword_accuracy,
    source_retrieval_accuracy,
)


def test_refusal_accuracy():
    expected = [True, False, False, True]
    actual = [True, False, True, True]

    assert refusal_accuracy(expected, actual) == 0.75


def test_answer_keyword_accuracy():
    keywords = [
        ["Python", "list"],
        ["Java", "class"],
    ]
    answers = [
        "Python có kiểu dữ liệu list.",
        "Java có nhiều kiểu dữ liệu.",
    ]

    assert answer_keyword_accuracy(keywords, answers) == 0.5


def test_source_retrieval_accuracy():
    expected = [
        [{"doc_id": "CA101", "heading_contains": "Cơ cấu điểm"}],
        [
            {"doc_id": "CS201", "heading_contains": "Bài 3.2"},
            {"doc_id": "CS102", "heading_contains": "Bài 3.2"},
        ],
    ]

    retrieved = [
        [{"doc_id": "CA101", "heading": "Cơ cấu điểm"}],
        [{"doc_id": "CS201", "heading": "Bài 3.2"}],
    ]

    modes = ["all", "all"]

    assert source_retrieval_accuracy(expected, retrieved, modes) == 0.5


if __name__ == "__main__":
    test_refusal_accuracy()
    test_answer_keyword_accuracy()
    test_source_retrieval_accuracy()
    print("Tất cả test metrics thành công!")
