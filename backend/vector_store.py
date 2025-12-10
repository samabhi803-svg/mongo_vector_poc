import os
import pymongo
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Explicitly load .env from the same directory as this script
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(env_path)

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "vector_poc_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "documents")

# Initialize model once
print("Loading model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
# class MockModel:
#     def encode(self, text):
#         return [0.1] * 384
# model = MockModel()
print("Model loaded.")

def get_db_collection():
    if not MONGO_URI or "example" in MONGO_URI:
        raise ValueError("Please set a valid MONGO_URI in .env")
    
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    try:
        # Ping to check connection
        client.admin.command('ping')
        print("Connected to MongoDB successfully.")
    except Exception as e:
        raise ConnectionError(f"Failed to connect to MongoDB: {e}")

    return db[COLLECTION_NAME]

def get_embedding(text):
    return model.encode(text).tolist()

def ingest_documents(documents):
    """
    documents: List of dicts, e.g., [{"content": "text...", "metadata": "..."}]
    """
    collection = get_db_collection()
    
    operations = []
    print(f"Generating embeddings for {len(documents)} documents...")
    
    docs_to_insert = []
    for doc in documents:
        text = doc.get("content", "")
        if text:
            vector = get_embedding(text)
            doc["embedding"] = vector
            docs_to_insert.append(doc)
    
    if docs_to_insert:
        result = collection.insert_many(docs_to_insert)
        print(f"Inserted {len(result.inserted_ids)} documents.")
    else:
        print("No documents to insert.")

def vector_search(query_text, limit=5):
    collection = get_db_collection()
    query_vector = get_embedding(query_text)
    
    # Note: This pipeline assumes an Atlas Vector Search index exists.
    # We will print the instruction to create one if it doesn't work, 
    # but strictly speaking we can't 'create' the index from here easily 
    # without using Atlas Admin API or GUI.
    
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_vector,
                "numCandidates": limit * 10,
                "limit": limit
            }
        },
        {
            "$project": {
                "_id": 0,
                "content": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]
    
    try:
        results = list(collection.aggregate(pipeline))
        return results
    except pymongo.errors.OperationFailure as e:
        print(f"Error executing vector search: {e}")
        print("Ensure you have created a Vector Search index named 'vector_index' on the 'embedding' field on MongoDB Atlas.")
        return []


def get_history_collection():
    if not MONGO_URI:
         raise ValueError("Please set a valid MONGO_URI in .env")
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db["chat_history"]

def get_chat_history(limit=50):
    collection = get_history_collection()
    cursor = collection.find({}, {'_id': 0}).sort('_id', 1).limit(limit)
    return list(cursor)

def save_chat_message(role, content):
    collection = get_history_collection()
    collection.insert_one({
        "role": role,
        "content": content
    })

def clear_chat_history():
    collection = get_history_collection()
    collection.delete_many({})
