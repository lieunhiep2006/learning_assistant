#reused recursive chunking from week 3
def chunk_recursive(text:str,chunk_size:int=200)->list[str]:
    paragraphs=[p for p in text.split('\n\n') if p.strip()]
    
    chunks=[]
    buffer=""

    for para in paragraphs:
        if len(buffer)+len(para)> chunk_size and buffer:
            chunks.append(buffer.strip())
            buffer=""

        if len(para)>chunk_size:
            sentences=[s.strip() + "." for s in para.split(".") if s.strip()]
            for sentence in sentences:
                if len(buffer) + len(sentence) > chunk_size and buffer:
                    chunks.append(buffer.strip())
                    buffer=sentence
                else:
                    buffer +=" " + sentence if buffer else sentence
        else:
            buffer+="\n\n" + para if buffer else para

    if buffer:
        chunks.append(buffer.strip())

    return chunks