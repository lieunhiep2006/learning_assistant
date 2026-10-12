import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal
from rank_bm25 import BM25Okapi
from src.corpus.doc_store import DocumentStore
from src.corpus.metadata import DocumentChunk
from src.rag.bm25_retriever import bm25_search, build_bm25_index
from src.rag.dense_retriever import dense_search, embed_chunks
from src.rag.hybrid import hybrid_search
from src.rag.retrieval_types import RetrievalResult

@dataclass
class RetrievalContext:
    store: DocumentStore
    chunks: list[DocumentChunk]
    bm25_index: BM25Okapi
    embeddings: list[list[float]]
    model: str

def validate_retrieval_alignment(
    chunks: list[DocumentChunk],
    bm25_index: BM25Okapi,
    embeddings: list[list[float]],
)->None:
    counts= (len(chunks), bm25_index.corpus_size, len(embeddings))
    if len(set(counts))!=1:
        raise ValueError("Retrieval data is misaligned: "
            f"{counts[0]} chunks, {counts[1]} BM25 documents, "f"{counts[2]} embeddings")

def load_embedding_cache(
    cache_path: Path,
    model: str,
    chunk_ids: list[str],
) -> list[list[float]] | None:
    if not cache_path.exists():
        return None

    cache = json.loads(cache_path.read_text(encoding="utf-8"))
    if not isinstance(cache, dict):
        raise ValueError(f"Invalid embedding cache format: {cache_path}")
    if cache.get("model") != model or cache.get("chunk_ids")!=chunk_ids:
        return None

    vectors= cache.get("embeddings")
    if(
        not isinstance(vectors, list)
        or len(vectors) != len(chunk_ids)
        or any(
            not isinstance(vector, list)
            or not vector
            or any(
                not isinstance(value, (int, float))
                for value in vector
            )
            for vector in vectors
        )
    ):
        return None
    return [[float(value) for value in vector] for vector in vectors]

def save_embedding_cache(
    cache_path: Path,
    model: str,
    chunk_ids: list[str],
    embeddings: list[list[float]],
) -> None:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(
        json.dumps(
            {
                "model": model,
                "chunk_ids": chunk_ids,
                "embeddings": embeddings,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

def build_retriever(
    store_path:Path,
    cache_path:Path|None=None,
    model:str="jina-embeddings-v3",
    batch_size:int=64,
) -> RetrievalContext:
    store = DocumentStore()
    store.load(str(store_path))
    chunks = list(store.chunks)
    bm25_index = build_bm25_index(chunks)
    chunk_ids = [chunk.chunk_id for chunk in chunks]
    if cache_path is None:
        cache_path = store_path.with_name(f"{store_path.stem}.embeddings.json")

    embeddings = load_embedding_cache(cache_path, model, chunk_ids)
    if embeddings is None:
        embeddings = embed_chunks(chunks, model=model, batch_size=batch_size)
        if len(embeddings) != len(chunks):
            raise ValueError("Embedding count does not match chunk count")
        save_embedding_cache(cache_path, model, chunk_ids, embeddings)

    validate_retrieval_alignment(chunks, bm25_index, embeddings)
    return RetrievalContext(
        store=store,
        chunks=chunks,
        bm25_index=bm25_index,
        embeddings=embeddings,
        model=model,
    )

def search(
    context:RetrievalContext,
    query:str,
    mode:Literal["bm25", "dense", "hybrid"]="hybrid",
    top_k:int=3,
) -> list[RetrievalResult]:
    if mode=="bm25":
        return bm25_search(
            query, context.chunks, context.bm25_index, top_k=top_k
        )
    if mode=="dense":
        return dense_search(
            query,
            context.chunks,
            context.embeddings,
            top_k=top_k,
            model=context.model,
        )
    if mode=="hybrid":
        return hybrid_search(
            query,
            context.chunks,
            context.bm25_index,
            context.embeddings,
            top_k=top_k,
            model=context.model,
        )
    raise ValueError(f"Unknown retrieval mode: {mode}")
