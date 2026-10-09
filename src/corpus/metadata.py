from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from pathlib import Path
@dataclass
class Document:
    content:str
    doc_id: str=""
    title: str=""
    source: str=""
    version: str=""
    owner: str=""
    metadata: dict=field(default_factory=dict)
    created_at: Optional[datetime] = field(default_factory=datetime.now)

@dataclass
class DocumentChunk:
    content:str
    chunk_id:str=""
    doc_id:str=""
    chunk_index:int=0
    metadata:dict=field(default_factory=dict)
    embedding:Optional[list[float]]=None


