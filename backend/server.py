from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import sys

# Ensure backend directory is in path for imports if running from within backend
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import vector_store. Since we are inside the package, we can use relative or absolute import
# depending on how we run it. Let's assume we run "python backend/server.py" or "uvicorn backend.server:app"
try:
    from backend import vector_store
except ImportError:
    import vector_store

app = FastAPI(title="MongoDB Vector Agent")

class Document(BaseModel):
    content: str
    metadata: Optional[dict] = {}

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"message": "Vector Store Agent API is running"}

@app.post("/ingest")
def ingest_documents(documents: List[Document]):
    try:
        docs_data = [doc.model_dump() for doc in documents]
        vector_store.ingest_documents(docs_data)
        return {"message": f"Ingested {len(documents)} documents"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
def search(query: str):
    results = vector_store.vector_search(query)
    return {"results": results}

try:
    from backend.agent import RAGAgent
except ImportError:
    from agent import RAGAgent
agent = RAGAgent(vector_store)

@app.post("/chat")
def chat(request: ChatRequest):
    response = agent.ask(request.message)
    return {"response": response}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
