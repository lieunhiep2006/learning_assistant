from rank_bm25 import BM25Okapi
from src.corpus.metadata import DocumentChunk
from src.rag.dense_retriever import score_chunks as score_dense
from src.rag.bm25_retriever import score_chunks as score_bm25
from src.rag.retrieval_types import RetrievalResult
def normalise_scores(scores: list[float]) -> list[float]:
    if not scores:
        return []
    min_s = min(scores)
    max_s = max(scores)
    if max_s == min_s:
        return [0.0] * len(scores)
    return [(s - min_s) / (max_s - min_s) for s in scores]

def hybrid_search(
    query: str,
    chunks: list[DocumentChunk],
    bm25_index: BM25Okapi,
    embeddings: list[list[float]],
    top_k:  int = 3,
    w_bm25: float = 0.3,
    w_vector: float = 0.7,
    model: str = "jina-embeddings-v3",
) -> list[RetrievalResult]:
    if top_k <= 0:
        return []
    bm25_scores = score_bm25(query, bm25_index)
    vector_scores = score_dense(query, embeddings, model=model)
    bm25_norm = normalise_scores(bm25_scores)
    hybrid = [
        w_bm25 * b + w_vector * v
        for b, v in zip(bm25_norm, vector_scores)
    ]

    ranked = sorted(
        range(len(hybrid)), key=lambda index: hybrid[index], reverse=True,
    )[:top_k]

    return [
        RetrievalResult(
            chunk=chunks[index],
            score=float(hybrid[index]),
            rank=rank,
            bm25_score=float(bm25_scores[index]),
            dense_score=float(vector_scores[index]),
        )
        for rank, index in enumerate(ranked, start=1)
    ]