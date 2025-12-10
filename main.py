import sys
import vector_store

def main():
    print("=== MongoDB Vector Store PoC ===")
    
    # 1. Check Config
    try:
        vector_store.get_db_collection()
    except Exception as e:
        print(f"Configuration Error: {e}")
        print("Please update your .env file with your MongoDB Atlas URI.")
        sys.exit(1)

    # 2. Sample Data
    documents = [
        {"content": "MongoDB is a document database with the scalability and flexibility that you want with the querying and indexing that you need."},
        {"content": "Vector search allows you to find similar items based on their semantic meaning rather than exact text matches."},
        {"content": "Python is a powerful programming language widely used for data science and AI."},
        {"content": "Machine learning models transform data into vectors (embeddings) to capture numerical representations of features."},
        {"content": "Atlas Vector Search indexes your vector embeddings for fast approximate k-nearest neighbor search."}
    ]

    # 3. Ingest
    print("\n--- Ingestion Step ---")
    user_input = input("Do you want to ingest sample documents? (y/n): ")
    if user_input.lower() == 'y':
        vector_store.ingest_documents(documents)
    else:
        print("Skipping ingestion.")

    # 4. Search
    print("\n--- Search Step ---")
    while True:
        query = input("\nEnter a search query (or 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        
        results = vector_store.vector_search(query, limit=3)
        print(f"\nTop 3 results for '{query}':")
        if not results:
            print("No results found. (Did you create the vector index in Atlas?)")
        
        for res in results:
            print(f"- [Score: {res.get('score', 0):.4f}] {res.get('content')}")

if __name__ == "__main__":
    main()
