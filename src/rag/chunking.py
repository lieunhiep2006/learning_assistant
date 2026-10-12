#reused recursive chunking from week 3
import re
from typing import List,Dict, Any
from src.corpus.metadata import Document,DocumentChunk

def split_long_text(text:str,chunk_size:int)->list[str]:
    words=text.split()
    chunks=[]
    current=""
    for word in words:
        if not current:
            current=word
        elif len(current)+1+len(word)<=chunk_size:
            current+=" "+word
        else:
            chunks.append(current)
            current=word
    if current:
        chunks.append(current) 
    return chunks

def split_sentences(text:str)->list[str]:
    return[
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", text.strip())
        if sentence.strip()
    ]

def chunk_recursive(text:str,chunk_size:int=700)->list[str]:
    paragraphs=[p.strip() for p in text.split('\n\n') if p.strip()]
    chunks=[]
    buffer=""

    def flush()-> None:
        nonlocal buffer
        if buffer:
            chunks.append(buffer)
            buffer=""
    def add_piece(piece:str)->None:
        nonlocal buffer
        separator= " " if buffer else ""

        if buffer and len(buffer)+len(separator)+len(piece) > chunk_size:
            flush()
            separator=""
        buffer+=separator+piece

    for para in paragraphs:
        separator="\n\n" if buffer else ""
        if len(buffer)+len(separator) + len(para)<= chunk_size:
            buffer+=separator+para
            continue
        flush()

        if len(para)<= chunk_size:
            buffer=para
            continue

        for sentence in split_sentences(para):
            pieces=(
                split_long_text(sentence,chunk_size)
                if len(sentence)>chunk_size
                else [sentence]
            )
            for piece in pieces:
                add_piece(piece)
    flush()
    return chunks

def chunk_document(doc:Document,chunk_size:int=512,overlap:int=64)->list[DocumentChunk]:
    chunks=[]
    text=doc.content
    start=0
    while start<len(text):
        end=min(start+chunk_size,len(text))
        chunk_text=text[start:end]
        chunk=DocumentChunk(content=chunk_text,chunk_id=f"{doc.doc_id}+{len(chunks)}",doc_id=doc.doc_id,chunk_index=len(chunks),
        metadata={
            "title":doc.title,
            "source":doc.source,
            **doc.metadata,
            "chunk_size":chunk_size,
            "overlap":overlap
        }                   
        )
        chunks.append(chunk)
        start+=chunk_size-overlap
        if start>=len(text): break
    return chunks

def headings_split(body:str)->list[dict]:
    if body is None:
        return[]
    lines= body.splitlines()
    sections = []
    stack: list[tuple[int,str]] =[]
    current_text:list[str] = []
    current_path:list[str] = []

    def finish_section(path:list[str], text_lines:list [str]):
        text = "\n".join(text_lines).strip()
        if text:
            sections.append({"path":path[:], "text":text})
    preamble_lines: list[str] =[]

    i=0
    while i<len(lines):
        line=lines[i]
        heading_match=re.match(r"^(#{1,6})\s+(.*)$",line)
        if heading_match:
            if stack:
                path=[title for _,title in stack]
                finish_section(path,current_text)
                current_text=[]
            elif preamble_lines:
                finish_section([],preamble_lines)
                preamble_lines=[]

            level=len(heading_match.group(1))
            title=heading_match.group(2).strip()

            if not title:
                i+=1
                continue
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level,title))
            current_text=[]
            i+=1
            continue
        if not stack:
            preamble_lines.append(line)
        else:
            current_text.append(line)
        i+=1

    if stack:
        path=[title for _,title in stack]
        finish_section(path,current_text)
    elif preamble_lines:
        finish_section([],preamble_lines)
    return sections

def create_chunks_documents(doc:Any,chunk_size:int=700)->list[DocumentChunk]:
    sections=headings_split(doc.content or "")
    chunks=[]
    global_index=0
    for section in sections:
        heading_path=section["path"]
        section_text=section["text"]
        
        for piece in chunk_recursive(section_text,chunk_size=chunk_size):
            if not piece.strip():
                continue

            heading_prefix=" > ".join(heading_path) if heading_path else ""
            chunk_content = f"{heading_prefix}\n{piece}" if heading_prefix else piece

            metadata={
                "title": doc.title,
                "version": doc.version,
                "owner": doc.owner,
                "source": doc.source,
                "heading_path": " > ".join(heading_path),
                "strategy": "recursive_sentence_aware",
                "chunk_size":chunk_size,
            }

            chunk = DocumentChunk(
                content=chunk_content,
                doc_id=doc.doc_id,
                chunk_index=global_index,
                chunk_id=f"{doc.doc_id}_{global_index}",
                metadata=metadata,
            )
            chunks.append(chunk)
            global_index+=1
    return chunks