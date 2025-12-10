# Mongo Vector Agent

A Full-Stack Agentic RAG Application that combines **MongoDB Vector Search** with **Google Gemini** to answer questions using your private knowledge base, with a fallback to **Web Search** for broader knowledge.

## Features

-   **Agentic RAG**: Uses an LLM to reason whether to answer from the Knowledge Base or search the Web.
-   **Vector Search**: Semantic search over your documents using MongoDB Atlas Vector Search.
-   **Web Search**: Integrated DuckDuckGo search for up-to-date information.
-   **Modern UI**: React + Vite frontend with a chat interface.
-   **Robust Backend**: FastAPI server handling ingestion and agent logic.

## Architecture

-   **Backend**: Python, FastAPI, `sentence-transformers`, `google-generativeai`, `pymongo`.
-   **Frontend**: React, Vite.
-   **Database**: MongoDB Atlas.

## Prerequisites

-   Python 3.8+
-   Node.js & npm
-   MongoDB Atlas Cluster (M0 Sandbox is fine)
-   Google Gemini API Key (for Agent reasoning)

## Setup

### 1. Environment Variables

Create a `.env` file in the root directory:

```env
MONGO_URI=your_mongodb_atlas_uri
DB_NAME=vector_poc_db
COLLECTION_NAME=documents
GOOGLE_API_KEY=your_gemini_api_key
```

### 2. MongoDB Configuration (Crucial)

You must create a Vector Search Index on your Atlas Collection (`vector_poc_db.documents`).
**Index Name:** `vector_index`
**JSON Configuration:**
```json
{
  "fields": [
    {
      "numDimensions": 384,
      "path": "embedding",
      "similarity": "cosine",
      "type": "vector"
    }
  ]
}
```

### 3. Backend Setup

```bash
# Create virtual env
python -m venv venv

# Activate
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Frontend Setup

```bash
cd frontend
npm install
```

## Running the Application

You need two terminals.

**Terminal 1: Backend**
```bash
# From root directory
venv\Scripts\python backend/server.py
```
*Server running at http://localhost:8000*

**Terminal 2: Frontend**
```bash
cd frontend
npm run dev
```
*UI running at http://localhost:5173*

## Usage

1.  **Ingestion**: Use the top bar in the UI to type a fact (e.g., "Project X code is Blue") and click **Ingest**. This saves it to MongoDB.
2.  **Chat**: Ask questions in the chat box.
    -   *RAG*: "What is the Project X code?" -> Agent queries MongoDB.
    -   *Web*: "What is the stock price of Apple?" -> Agent searches the Web.
