from pathlib import Path
from src.corpus.metadata import Document,DocumentChunk
from src.corpus.doc_store import DocumentStore
from chunking import chunk_recursive
def create_chunks(document: Document, chunk_size: int =200,overlap:int =40,)->list[DocumentChunk]:
    text_chunks=chunk_recursive(
        document.content,
        chunk_size=chunk_size
    )
    return[
        DocumentChunk(
            content=text,
            doc_id=document.doc_id,
            chunk_id=f"{document.doc_id}_chunk_{index}",
            chunk_index=index,
            metadata={
                "strategy": "recursive",
                "chunk_size": chunk_size,
            },
        )
        for index, text in enumerate(text_chunks)
    ]

def load_documents(strategy: str="fixed", chunk_size: int=200, overlap:int =40,)->DocumentStore:
    file_path=__path__(Path(__file__).root/"data"/"documents")
    text=file_path.read_text(encoding="utf-8")
    document=Document(content=text,title="Sample Document", source=str(file_path),)
    store=DocumentStore()
    store.add(document)
    chunks=create_chunks(document=document,chunk_size=chunk_size)
    for chunk in chunks:store.add_chunk(chunk)
    lengths=[len(chunk.content) for chunk in store.get_chunks_by_doc(document.doc_id)]
    print("Title: ", document.title)
    print("Source: ", document.source)
    print("Chunk size: ", chunk_size)
    print("Documents:", store.count()["documents"])
    print("Chunks:", store.count()["chunks"])
    if lengths:
        print("Minimum chunk length:", min(lengths))
        print("Maximum chunk length:", max(lengths))
        print("Average chunk length:", sum(lengths) / len(lengths))
        print("Total characters:", sum(lengths))
    return store

def file_document(file_path:Path) -> Document:
    project_root=Path(__file__).resolve().parents[2]
    file_path=file_path.resolve()
    lines=file_path.read_text(encoding="utf-8-sig").splitlines()

    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{file_path}: missing header (expected ---)")
    closing_index=next(
        (i for i, line in enumerate(lines[1:],start=1) if line.strip()=="---"), 
        None,
    )
    if closing_index is None:
        raise ValueError(f"{file_path}:missing closing ---")

    header={}
    for line_number,line in enumerate(lines[1:closing_index],start=2):
        if not line.strip(): continue
        key,separator,value=line.partition(":")
        if not separator:
            raise ValueError(f"{file_path}:missing colon in {line!r}")
        key=key.strip().lower()
        value=value.strip()

        if not key:
            raise ValueError(f"{file_path}:{line_number}: empty key")
        if key in header:
            raise ValueError(f"{file_path}:{line_number}: duplicate key {key!r} ")
        if not value:
            raise ValueError(f"{file_path}:{line_number}: no value for {key!r} ")
        header[key]=value

    required={"doc_id","title","version","owner"}
    missing=sorted(required-header.keys())

    if missing:
        raise ValueError(f"{file_path}: Missing required fields {', '.join(sorted(missing))}")
    
    body=lines[closing_index+1:]
    while body and not body[0].strip():
        body.pop(0)

    return Document(
        content="\n".join(body),
        doc_id=header["doc_id"],
        title=header["title"],
        version=header["version"],
        owner=header["owner"],
        source=file_path.relative_to(project_root).as_posix(),
    )