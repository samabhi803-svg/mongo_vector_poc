from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
import os
import sys
import pypdf
import io

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
    history: Optional[List[dict]] = []

@app.get("/")
def read_root():
    return {"message": "Vector Store Agent API is running"}

@app.post("/ingest")
async def ingest_documents(documents: List[Document]):
    try:
        docs_data = [doc.model_dump() for doc in documents]
        vector_store.ingest_documents(docs_data)
        return {"message": f"Ingested {len(documents)} documents"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def extract_text_from_file(file_content: bytes, filename: str) -> str:
    if filename.lower().endswith('.pdf'):
        try:
            pdf_reader = pypdf.PdfReader(io.BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise ValueError(f"Error parsing PDF: {str(e)}")
    else:
        # Assume text
        return file_content.decode('utf-8', errors='ignore')

def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    # Simple character splitter
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = extract_text_from_file(content, file.filename)
        
        if not text.strip():
             return {"message": "No text extracted from file."}

        chunks = chunk_text(text)
        
        # Prepare for ingestion
        docs_data = [{"content": chunk, "metadata": {"source": file.filename}} for chunk in chunks]
        vector_store.ingest_documents(docs_data)
        
        return {"message": f"Successfully uploaded '{file.filename}' and ingested {len(chunks)} chunks."}
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
    response = agent.ask(request.message, history=request.history)
    return {"response": response}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
