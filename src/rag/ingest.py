from pathlib import Path
from src.corpus.metadata import Document,DocumentChunk
from src.corpus.doc_store import DocumentStore
from src.rag.chunking import chunk_document,create_chunks_documents
def create_chunks(document: Document, strategy: str="headings",chunk_size: int =700,overlap:int =40,)->list[DocumentChunk]:
    if strategy == "headings":
        return create_chunks_documents(
            document,
            chunk_size=chunk_size,
        )
    
    if strategy == "fixed":
        return chunk_document(
            document,
            chunk_size=chunk_size,
            overlap=overlap,
        )
    raise ValueError(f"unknown chunking strategy: {strategy}")

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

def ingest_documents(source_dir:Path,output_path:Path,strategy:str="headings",chunk_size:int=700,overlap:int=40)->DocumentStore:
    md_files=sorted(source_dir.rglob("*.md"))
    if not md_files:
        raise FileNotFoundError(f"No markdown files in {source_dir}")

    store=DocumentStore()
    for file_path in md_files:
        document=file_document(file_path)
        store.add(document)
        for chunk in create_chunks(document,strategy=strategy,chunk_size=chunk_size,overlap=overlap):
            store.add_chunk(chunk)
    store.save(str(output_path))
    return store
def main()->None:
    project_root=Path(__file__).resolve().parents[2]
    source_dir=project_root/ "data"/ "documents"
    output_path=project_root/ "data"/ "documents"/"document_store.json"
    store=ingest_documents(source_dir,output_path)
    print(f"Documents: {store.count()['documents']}")
    print(f"Chunks: {store.count()['chunks']}")
    print(f"Saved to: {output_path}")
if __name__=="__main__":
    main()