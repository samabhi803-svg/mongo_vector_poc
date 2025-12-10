from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os
import sys
import pypdf
import io
import google.generativeai as genai
from PIL import Image

# Ensure backend directory is in path for imports if running from within backend
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import vector_store
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

@app.post("/api/ingest")
async def ingest_documents(documents: List[Document]):
    try:
        docs_data = [doc.model_dump() for doc in documents]
        vector_store.ingest_documents(docs_data)
        return {"message": f"Ingested {len(documents)} documents"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def extract_text_from_file(file_content: bytes, filename: str, content_type: str) -> str:
    if filename.lower().endswith('.pdf'):
        try:
            pdf_reader = pypdf.PdfReader(io.BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise ValueError(f"Error parsing PDF: {str(e)}")
    
    elif content_type.startswith("image/"):
        # Use Gemini to caption the image
        try:
            print(f"Generating caption for image: {filename}")
            if not os.getenv("GOOGLE_API_KEY"):
                return "[Image Upload Skipped] GOOGLE_API_KEY not found."
            
            # Configure GenAI
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Load image from bytes
            image_part = {"mime_type": content_type, "data": file_content}
            
            prompt = "Describe this image in extreme detail for retrieval purposes. Include specific objects, text, data points, colors, and context. Start with 'Image Description:'"
            
            response = model.generate_content([prompt, image_part])
            return response.text
        except Exception as e:
            print(f"Error captioning image: {e}")
            return f"[Error processing image {filename}: {str(e)}]"

    else:
        # Assume text
        return file_content.decode('utf-8', errors='ignore')

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        # Pass content_type
        text = extract_text_from_file(content, file.filename, file.content_type)
        
        if not text.strip():
             return {"message": "No content extracted from file."}
        
        # If it was an image, the 'text' is the caption.
        chunks = chunk_text(text)
        
        # Prepare for ingestion
        docs_data = [{"content": chunk, "metadata": {"source": file.filename, "type": "image" if file.content_type.startswith("image/") else "text"}} for chunk in chunks]
        vector_store.ingest_documents(docs_data)
        
        return {"message": f"Successfully uploaded '{file.filename}' and ingested {len(chunks)} chunks."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search")
def search(query: str):
    results = vector_store.vector_search(query)
    return {"results": results}

try:
    from backend.agent import RAGAgent
except ImportError:
    from agent import RAGAgent
agent = RAGAgent(vector_store)

@app.post("/api/chat")
def chat(request: ChatRequest):
    # Save User Message
    vector_store.save_chat_message("user", request.message)
    
    # Get Response
    response_text = agent.ask(request.message, history=request.history)
    
    # Save Agent Message
    vector_store.save_chat_message("agent", response_text)
    
    return {"response": response_text}

@app.get("/api/history")
def get_history():
    return vector_store.get_chat_history()

@app.delete("/api/history")
def clear_history():
    vector_store.clear_chat_history()
    return {"message": "Chat history cleared."}

# Mount Static Files (Frontend)
# Ensure this is AFTER API routes so they take precedence
frontend_dist_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist")
if os.path.exists(frontend_dist_path):
    app.mount("/", StaticFiles(directory=frontend_dist_path, html=True), name="static")
else:
    print(f"Warning: Frontend dist not found at {frontend_dist_path}. API only mode.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
