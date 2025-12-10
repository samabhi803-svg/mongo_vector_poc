# MongoDB Vector Store PoC

This project is a Proof of Concept (PoC) demonstrating how to store and query vector embeddings using MongoDB and Python. It utilizes the `sentence-transformers` library to generate embeddings and MongoDB Atlas Vector Search for semantic similarity searches.

## Prerequisites

- Python 3.8+
- A MongoDB Atlas account (M0 Sandbox is sufficient).
- A MongoDB Atlas Cluster deployed.

## Setup and Installation

1.  **Clone the repository** (if applicable) or navigate to the project directory.

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment**:
    - **Windows**:
      ```bash
      .\venv\Scripts\activate
      ```
    - **macOS/Linux**:
      ```bash
      source venv/bin/activate
      ```

4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **Environment Variables**:
    Create a `.env` file in the root directory of the project. A template is provided below:

    ```env
    MONGO_URI=your_mongodb_connection_string
    DB_NAME=vector_poc_db
    COLLECTION_NAME=documents
    ```
    Replace `your_mongodb_connection_string` with your actual connection string from MongoDB Atlas.

2.  **MongoDB Atlas Vector Search Index (CRITICAL)**:
    Before you can perform searches, you **MUST** create a Vector Search Index on your MongoDB Atlas collection.

    - Go to your cluster in the MongoDB Atlas UI.
    - Click on the **"Atlas Search"** tab.
    - Click **"Create Search Index"**.
    - Select **"JSON Editor"**.
    - Select your Database (`vector_poc_db`) and Collection (`documents`).
    - Name the index: `vector_index` (This name matches the code in `vector_store.py`).
    - Paste the following JSON configuration:

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
    *Note: `384` is the dimension size for the `all-MiniLM-L6-v2` model used in this project.*

## Usage

Run the main application:

```bash
python main.py
```

### Application Flow

1.  **Configuration Check**: The app checks if it can connect to MongoDB.
2.  **Ingestion Step**: You will be prompted to ingest sample documents.
    - Type `y` to insert sample text data into your MongoDB collection. The app will generate embeddings for them automatically.
3.  **Search Step**: You can enter natural language queries.
    - Example: "programming languages for AI"
    - The app will convert your query into a vector and find the most semantically similar documents in the database using the Atlas Vector Search index.

## File Overview

- `main.py`: The entry point script that orchestrates the user interaction (ingestion and search).
- `vector_store.py`: Contains the core logic for connecting to MongoDB, generating embeddings using `sentence-transformers`, inserting documents, and executing vector search queries.
