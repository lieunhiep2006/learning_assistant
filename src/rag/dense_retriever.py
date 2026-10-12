import os
import numpy as np
from dotenv import load_dotenv
from src.rag.jina_embeddings import jina_embeddings
from src.corpus.metadata import DocumentChunk
from src.rag.retrieval_types import RetrievalResult
load_dotenv()

def _get_api_key(api_key:str|None)->str:
    if api_key is None:
        api_key=os.getenv("JINA_API_KEY")
    return api_key

def embed_text(text: str,model: str = "jina-embeddings-v3",api_key: str | None = None,)->list[float]:
    api_key=_get_api_key(api_key)
    resp=jina_embeddings(input=text, model=model,task="retrieval.query", api_key=api_key)
    return resp.data[0].embedding

def embed_chunks(
    chunks: list[DocumentChunk],
    model: str = "jina-embeddings-v3",
    api_key: str | None = None,
    batch_size: int = 64,
)->list[list[float]]:
    api_key=_get_api_key(api_key)

    embeddings:list[list[float]]=[]
    for start in range(0,len(chunks),batch_size):
        batch=chunks[start:start+batch_size]
        resp=jina_embeddings(
            input=[chunk.content for chunk in batch],
            model=model,
            task="retrieval.passage",
            api_key=api_key,
        )
        items = sorted(resp.data, key=lambda item: item.index)
        embeddings.extend(item.embedding for item in items)
    return embeddings

def batch_embed_text(input:list[str],model="jina-embeddings-v3",api_key=None)->list[list[float]]:
    if api_key is None:
        api_key=os.getenv("JINA_API_KEY")
    resp=jina_embeddings(input=input, model=model, api_key=api_key)
    return [item.embedding for item in resp.data]

def cosine_similarity(a:list[float],b:list[float])->float:
    return np.dot(a,b) / (np.linalg.norm(a)*np.linalg.norm(b))

def score_chunks(
    query:str,
    embeddings:list[list[float]],
    model:str="jina-embeddings-v3",
)->list[float]:
    query_embedding=embed_text(query, model=model)
    return [cosine_similarity(query_embedding,vector) for vector in embeddings]

def dense_search(
    query:str,
    chunks:list[DocumentChunk],
    embeddings:list[list[float]],
    top_k: int=3,
    model: str="jina-embeddings-v3",
)->list[RetrievalResult]:
    if top_k<=0:
        return []
    if not chunks:
        return []

    scores=score_chunks(query, embeddings, model=model)
    ranked=sorted(range(len(scores)), key=lambda index: scores[index], reverse=True)
    return [
        RetrievalResult(
            chunk=chunks[index],
            score=float(scores[index]),
            rank=rank,
            dense_score=float(scores[index]),
        )
        for rank, index in enumerate(ranked[:top_k], start=1)
    ]