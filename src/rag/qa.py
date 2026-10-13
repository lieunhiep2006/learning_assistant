import asyncio
from pathlib import Path
from groq import AsyncGroq
from dotenv import load_dotenv
from src.rag.citation import GroundedAnswer, wrap_answer
from src.rag.retriever import RetrievalContext,build_retriever
from src.tools.search_lessons import search_lessons

RAG_SYSTEM_PROMPT=(Path(__file__).resolve().parents[2]/"prompts"/"rag_system.txt")
MODEL = "qwen/qwen3.8-27b"
NO_ANSWER= "Tài liệu không có đủ thông tin để trả lời"
def build_rag_prompt()->str:
    prompt=RAG_SYSTEM_PROMPT.read_text(encoding="utf-8").strip()
    if not prompt:
        raise ValueError(f"RAG prompt đang trống: {RAG_SYSTEM_PROMPT}")
    return prompt

async def answer_question(client:AsyncGroq,retrieval:RetrievalContext,question:str,mode:str="hybrid")->GroundedAnswer:
    evidence=search_lessons(
        context=retrieval,
        query=question,
        mode=mode
    )

    if evidence["status"]=="no_answer":
        return wrap_answer(NO_ANSWER,[])

    response=await client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role":"system", "content":build_rag_prompt()},
            {"role":"user","content":(
                f"Question: {question}\n\n"
                f"Numbered evidence: \n{evidence['context']}"
                ),
            },
        ],
        temperature=0,
    )
    answer=response.choices[0].message.content
    return wrap_answer(answer,evidence["sources"])
async def main()->None:
    load_dotenv()
    project_root=Path(__file__).resolve().parents[2]
    store_path=project_root/"data"/"documents"/"document_store.json"
    retrieval=build_retriever(store_path)
    async with AsyncGroq() as client:
        result=await answer_question(
            client=client,
            retrieval=retrieval,
            question="Thanh ghi RSP dùng để làm gì?",
            mode="hybrid",
        )
    print("Answer:",result["answer"])
    print("sources:")
    for source in result["sources"]:
        print(
            f"- [{source['number']}] {source['title']}"
            f"(chunk {source['chunk_id']}, score={source['score']:.3f})"
        )
if __name__=="__main__":
    asyncio.run(main())