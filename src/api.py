
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from retrieval import load_index, retrieve
from generation import generate_answer
from memory import ShortTermMemory

app = FastAPI(
    title="Multilingual RAG Service",
    description="Accepts English/Bangla queries, retrieves from HSC26 corpus, and generates grounded answers."
)

index, chunks = load_index()

stm = ShortTermMemory(capacity=5)

class Query(BaseModel):
    text: str

class ChatResponse(BaseModel):
    answer: str
    contexts: List[str]

@app.post("/chat", response_model=ChatResponse)
def chat(q: Query):
    stm.add("user", q.text)
    contexts = retrieve(q.text, index=index, chunks=chunks, top_k=5)
    answer = generate_answer(q.text, contexts, stm_history=stm.get())
    stm.add("assistant", answer)
    return {"answer": answer, "contexts": contexts}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)
