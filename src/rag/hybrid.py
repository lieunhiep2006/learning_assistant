from dataclasses import dataclass
from rank_bm25 import BM25Okapi
from src.corpus.metadata import DocumentChunk
from src.rag.dense_retriever import embed_text,cosine_similarity
from src.rag.bm25_retriever import tokenize

@dataclass
class HybridSearchResult:
    chunk:DocumentChunk
    score: float
    rank: int
    bm25_score: float
    dense_score: float
def normalise_scores(scores: list[float]) -> list[float]:
    if not scores:
        return []
    min_s = min(scores)
    max_s = max(scores)
    if max_s == min_s:
        return [1.0] * len(scores)  # All equal → all 1.0
    return [(s - min_s) / (max_s - min_s) for s in scores]

def hybrid_search(
    query:  str,
    chunks: list,
    bm25_index: BM25Okapi,
    embeddings: list[list[float]],
    top_k:  int = 3,
    w_bm25: float = 0.3,
    w_vector: float = 0.7
) -> list[HybridSearchResult]:
    tokenized_query = tokenize(query)
    bm25_scores = bm25_index.get_scores(tokenized_query)
    # Vector scores (cosine similarity, bounded)
    query_vec = embed_text(query)
    vector_scores = [cosine_similarity(query_vec, e) for e in embeddings]

    # Normalise BM25 to [0, 1]
    bm25_norm = normalise_scores(list(bm25_scores))

    # Fuse
    hybrid = [
        w_bm25 * b + w_vector * v
        for b, v in zip(bm25_norm, vector_scores)
    ]

    # Sort by hybrid score descending, return top_k
    ranked = sorted(
        range(len(hybrid)), key=lambda index:hybrid[index], reverse=True,
    )[:top_k]

    return[
        HybridSearchResult(
            chunk=chunks[index],
            score=float(hybrid[index]),
            rank=rank,
            bm25_score=float(bm25_scores[index]),
            dense_score=float(vector_scores[index]),
        )
        for rank,index in enumerate(ranked,start=1)
    ]