from src.corpus.metadata import Document,DocumentChunk
from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import List,Optional
from datetime import datetime
@dataclass
class DocumentStore:    
    documents: dict[str,Document] =  field(default_factory=dict)
    chunks: List[DocumentChunk] = field(default_factory=list)

    def add(self, doc: Document) -> str:
        if not doc.doc_id:
            doc.doc_id=f"DOC{len(self.documents)+1:04d}"
        if doc.doc_id in self.documents:
            raise ValueError("doc_id cannot be duplicates")
        self.documents[doc.doc_id]=doc
        return doc.doc_id
    

    def delete(self, doc_id:str) -> bool:
        if doc_id not in self.documents:
            return False
        del self.documents[doc_id]
        self.chunks = [chunk for chunk in self.chunks if chunk.doc_id != doc_id]
        return True
    
    def list_all(self)->List[Document]:
        return list(self.documents.values())
    
    def add_chunk(self,chunk:DocumentChunk)->str:
        if not chunk.chunk_id:
            chunk.chunk_id = f"{chunk.doc_id}_{len(self.chunks)}"
        if any(existing.chunk_id == chunk.chunk_id for existing in self.chunks):
            raise ValueError("chunk_id cannot be duplicates")
        self.chunks.append(chunk)
        return chunk.chunk_id
    
    def get_chunk(self,chunk_id:str)->Optional[DocumentChunk]:
        return next(
            (chunk for chunk in self.chunks if chunk.chunk_id == chunk_id),
            None,
        )
    
    def get_chunks_by_doc(self, doc_id: str) -> list[DocumentChunk]:
        return [chunk for chunk in self.chunks if chunk.doc_id == doc_id]
    
    def count(self)->dict:
        return {
            "documents": len(self.documents),
            "chunks": len(self.chunks),
        }

    def save(self, path: str) -> None:
        data = {
            "documents": [
                {
                    "content": document.content,
                    "doc_id": document.doc_id,
                    "title": document.title,
                    "source": document.source,
                    "version": document.version,
                    "owner": document.owner,
                    "created_at": document.created_at.isoformat() if document.created_at else None,
                    "metadata": document.metadata,
                }
                for document in self.documents.values()
            ],
            "chunks": [
                {
                    "content": chunk.content,
                    "chunk_id": chunk.chunk_id,
                    "doc_id": chunk.doc_id,
                    "chunk_index": chunk.chunk_index,
                    "metadata": chunk.metadata,
                    "embedding": chunk.embedding,
                }
                for chunk in self.chunks
            ],
        }
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(data,ensure_ascii=False, indent=2), encoding="utf-8")

    def load(self, path: str) -> None:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        self.documents = {
            item["doc_id"]: Document(
                content=item["content"],
                doc_id=item["doc_id"],
                title=item.get("title", ""),
                source=item.get("source", ""),
                version=item.get("version", ""),
                owner=item.get("owner", ""),
                created_at=datetime.fromisoformat(item["created_at"]) if item.get("created_at") else None,
                metadata=item.get("metadata", {}),
            )
            for item in data.get("documents", [])
        }
        self.chunks = [
            DocumentChunk(
                content=item["content"],
                chunk_id=item["chunk_id"],
                doc_id=item["doc_id"],
                chunk_index=item.get("chunk_index", 0),
                metadata=item.get("metadata", {}),
                embedding=item.get("embedding"),
            )
            for item in data.get("chunks", [])
        ]
