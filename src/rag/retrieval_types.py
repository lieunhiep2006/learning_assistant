from dataclasses import dataclass
from src.corpus.metadata import DocumentChunk

@dataclass
class RetrievalResult:
    chunk:DocumentChunk
    score:float
    rank:int
    bm25_score:float|None = None
    dense_score:float|None = None