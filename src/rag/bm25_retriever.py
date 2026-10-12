import re,unicodedata
from rank_bm25 import BM25Okapi
from src.corpus.metadata import DocumentChunk
from src.rag.retrieval_types import RetrievalResult

def tokenize(text:str)->list[str]:
    normalized=unicodedata.normalize("NFC", text)
    normalized_lower=normalized.lower()
    return re.findall(r"[^\W_]+", normalized_lower, flags=re.UNICODE)

def build_bm25_index(chunks: list[DocumentChunk]) -> BM25Okapi:
    tokenized = [tokenize(chunk.content) for chunk in chunks]
    return BM25Okapi(tokenized)

def score_chunks(query:str, bm25_index:BM25Okapi)->list[float]:
    return [float(score) for score in bm25_index.get_scores(tokenize(query))]

def bm25_search(
    query: str,
    chunks: list[DocumentChunk],
    bm25_index: BM25Okapi,
    top_k: int = 3,
) -> list[RetrievalResult]:
    if top_k <= 0:
        return []
    scores=score_chunks(query, bm25_index)

    ranked=sorted(range(len(scores)),key=lambda index:scores[index],reverse=True)
    return [
        RetrievalResult(
            chunk=chunks[index],
            score=scores[index],
            rank=rank,
            bm25_score=scores[index],
        )
        for rank, index in enumerate(ranked[:top_k], start=1)
    ]