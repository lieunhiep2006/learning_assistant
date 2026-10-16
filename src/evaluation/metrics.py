
def refusal_accuracy(
    expected_answer: list[bool],
    actually_answered: list[bool],
) -> float:
    """Đánh giá quyết định trả lời hay từ chối."""
    if len(expected_answer) != len(actually_answered):
        raise ValueError("Hai danh sách phải có cùng độ dài")

    if not expected_answer:
        return 0.0

    correct = sum(
        expected == actual
        for expected, actual in zip(expected_answer, actually_answered)
    )

    return correct / len(expected_answer)


def answer_keyword_accuracy(
    expected_keywords: list[list[str]],
    answers: list[str],
) -> float:
    """Tính tỷ lệ câu trả lời chứa đủ từ khóa mong đợi."""
    if len(expected_keywords) != len(answers):
        raise ValueError("Hai danh sách phải có cùng độ dài")

    if not answers:
        return 0.0

    correct = 0

    for keywords, answer in zip(expected_keywords, answers):
        if all(keyword.casefold() in answer.casefold() for keyword in keywords):
            correct += 1

    return correct / len(answers)


def source_retrieval_accuracy(
    expected_sources: list[list[dict]],
    retrieved_sources: list[list[dict]],
    source_matches: list[str],
) -> float:
    """Đánh giá nguồn truy xuất theo quy tắc all hoặc any."""
    if not (
        len(expected_sources)
        == len(retrieved_sources)
        == len(source_matches)
    ):
        raise ValueError("Ba danh sách phải có cùng độ dài")

    if not expected_sources:
        return 0.0

    correct = 0

    for expected, retrieved, match_mode in zip(
        expected_sources, retrieved_sources, source_matches
    ):
        checks = []

        for expected_source in expected:
            matched = any(
                source.get("doc_id") == expected_source.get("doc_id")
                and expected_source.get("heading_contains", "").casefold()
                in source.get("heading_path", source.get("heading", "")).casefold()
                for source in retrieved
            )
            checks.append(matched)

        if match_mode == "all":
            passed = all(checks)
        elif match_mode == "any":
            passed = any(checks)
        else:
            raise ValueError("source_match phải là 'all' hoặc 'any'")

        if passed:
            correct += 1

    return correct / len(expected_sources)
