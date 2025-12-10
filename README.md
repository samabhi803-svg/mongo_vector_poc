# MongoDB Vector Agent (RAG)

A full-stack **Agentic RAG Application** that combines local document knowledge with web search to answer questions intelligently.

## Features

- **Agentic RAG**: Intelligently switches between **MongoDB Vector Search** (for internal documents) and **DuckDuckGo Web Search** (for external knowledge).
- **Multi-Modal Support**: Upload **Images** (PNG/JPG) which are captioned by Gemini 2.0 and searchable via text.
- **Conversation Memory**: The agent remembers previous context (e.g., "How old is he?") for natural follow-up questions.
- **Chat Persistence**: Chat history is saved to MongoDB and restored upon page reload.
- **Modern UI**: Built with React + Vite, featuring **Markdown Rendering** (code, tables, lists) and file upload.
- **LLM Integration**: Uses Google's **Gemini 2.0 Flash** for fast, high-quality responses (configurable).

## Tech Stack

- **Frontend**: React, Vite, Tailwind CSS, React Markdown
- **Backend**: FastAPI, Python, Pillow
- **Database**: MongoDB Atlas (Vector Search & Chat History)
- **AI/LLM**: Google Gemini API (`gemini-2.0-flash`)
- **Search**: `ddgs` (DuckDuckGo Search)

## Structure

```
mongo_vector_poc/
├── backend/
│   ├── server.py       # FastAPI Backend & Endpoints
│   ├── agent.py        # Agentic Logic & Memory Contextualization
│   ├── vector_store.py # MongoDB Vector Search Logic
│   └── tools.py        # Web Search Tool (DuckDuckGo)
├── frontend/
│   ├── src/
│   │   ├── App.jsx     # Chat & Upload UI
│   │   └── main.jsx    # React Entry Point
│   └── vite.config.js  # Vite Proxy Configuration
└── README.md
```

## Setup Instructions

### 1. Prerequisites
-   Python 3.8+
-   Node.js & npm
-   MongoDB Atlas Cluster (Free Tier)
-   Google Gemini API Key

### 2. Backend Setup
1.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Configure Environment (`.env`):
    ```ini
    MONGO_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
    DB_NAME=vector_poc_db
    COLLECTION_NAME=documents
    GOOGLE_API_KEY=your_gemini_api_key
    ```
4.  Run Server:
    ```bash
    python backend/server.py
    ```

### 3. Frontend Setup
1.  Navigate to frontend:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run Dev Server:
    ```bash
    npm run dev
    ```

## Usage

1.  Open **http://localhost:5173**.
2.  **Upload**: Drag & Drop a PDF to add knowledge.
3.  **Chat**: Ask questions. The agent will check your docs first, then the web.
4.  **Follow-up**: Ask conversational follow-ups like "Tell me more".
