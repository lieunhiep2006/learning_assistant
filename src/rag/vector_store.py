from dataclasses import dataclass
from src.corpus.doc_store import DocumentStore
from src.corpus.metadata import Document,DocumentChunk
from src.rag.chunking import chunk_document
from src.rag.embeddings_similarity_helpers import embed_text,cosine_similarity
@dataclass

class VectorStore(DocumentStore):
    def add_chunk(self,chunk:DocumentChunk):
        if chunk.embedding is None:
            chunk.embedding=embed_text(chunk.content)
        return super().add_chunk(chunk)

    def add(self,doc:Document)->str:
        doc_id=super().add(doc)
        for chunk in chunk_document(doc):
            self.add_chunk(chunk)
        return doc_id

    def search(self,query:str,top_k:int=3)->list[tuple[DocumentChunk,float]]:
        if top_k <= 0:
            return []

        query_embedding=embed_text(query)
        results=[]
        for chunk in self.chunks:
            if chunk.embedding is None:
                continue
            score=cosine_similarity(query_embedding,chunk.embedding)
            results.append((chunk,score))

        results.sort(key=lambda item:item[1],reverse=True)
        return results[:top_k]

    def search_with_threshold(
        self,query:str,top_k:int=3,min_score:float=0.5
    )->list[tuple[DocumentChunk,float]]:
        return [
            (chunk,score)
            for chunk,score in self.search(query,top_k=len(self.chunks))
            if score >= min_score
        ][:max(top_k,0)]
        