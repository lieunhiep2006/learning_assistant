import re
from dataclasses import dataclass
from typing import TypedDict
from src.rag.retrieval_types import RetrievalResult

class Source(TypedDict):
    number: int
    chunk_id: str
    doc_id: str
    title: str
    version: str
    heading_path: str
    source_file: str
    score: float

class GroundedAnswer(TypedDict):
    answer: str
    sources: list[Source]

@dataclass
class NumberedContext:
    text: str
    sources: list[Source]

def build_sources(results: list[RetrievalResult]) -> list[Source]:
    sources: list[Source] = []
    for number, result in enumerate(results, start=1):
        chunk = result.chunk
        metadata = chunk.metadata
        sources.append({
            "number": number,
            "chunk_id": chunk.chunk_id,
            "doc_id": chunk.doc_id,
            "title": metadata.get("title") or chunk.doc_id,
            "version": metadata.get("version") or "",
            "heading_path": metadata.get("heading_path") or "",
            "source_file": metadata.get("source") or chunk.doc_id,
            "score": float(result.score),
        })
    return sources

def build_numbered_context(results: list[RetrievalResult]) -> NumberedContext:
    sources = build_sources(results)
    text = "\n\n".join(
        f"[{source['number']}]\n{result.chunk.content}"
        for source, result in zip(sources, results)
    )
    return NumberedContext(text=text, sources=sources)

def validate_answer_citations(answer: str, sources: list[Source]) -> None:
    available_numbers = {source["number"] for source in sources}
    cited_numbers = {
        int(match)
        for match in re.findall(r"\[(\d+)\]", answer)
    }
    unknown_numbers = cited_numbers - available_numbers
    if unknown_numbers:
        invalid = ", ".join(f"[{number}]" for number in sorted(unknown_numbers))
        raise ValueError(f"Answer cites sources that are not in the source list: {invalid}")

def wrap_answer(answer: str, sources: list[Source]) -> GroundedAnswer:
    validate_answer_citations(answer, sources)
    return {
        "answer": answer,
        "sources": sources if sources else [],
    }

def format_citation(result:RetrievalResult, number:int = 1) -> str:
    source = build_sources([result])[0]
    heading_parts = [
        part.strip()
        for part in source["heading_path"].split(" > ")
        if part.strip()
    ]
    if heading_parts and heading_parts[0] == source["title"]:
        heading_parts = heading_parts[1:]
    details = [
        source["title"],
        " > ".join(heading_parts),
        source["source_file"],
        f"chunk {source['chunk_id']}",
    ]
    if source["version"]:
        details.append(f"version {source['version']}")
    return f"[{number}] " + " — ".join(detail for detail in details if detail)