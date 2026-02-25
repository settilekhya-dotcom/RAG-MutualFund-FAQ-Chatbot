import json
import os
import chromadb
from chromadb.utils import embedding_functions
from static_knowledge import STATIC_DOCS

DB_PATH = "chroma_db"
COLLECTION_NAME = "icici_mf_facts"

def load_chunks(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def initialize_vector_store(chunks):
    # Initialize Persistent Client - delete existing collection to rebuild clean
    client = chromadb.PersistentClient(path=DB_PATH)
    
    # Delete and recreate to avoid stale data
    try:
        client.delete_collection(name=COLLECTION_NAME)
        print("Deleted existing collection.")
    except Exception:
        pass

    model_name = "all-MiniLM-L6-v2"
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)
    
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=emb_fn,
        metadata={"hnsw:space": "cosine"}
    )
    
    # Add scraped chunks
    ids = [c["chunk_id"] for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    
    # Add static knowledge docs
    for doc in STATIC_DOCS:
        ids.append(doc["id"])
        documents.append(doc["text"])
        metadatas.append({"source": doc["source"], "title": doc["title"]})
    
    print(f"Upserting {len(ids)} total items ({len(chunks)} scraped + {len(STATIC_DOCS)} curated)...")
    collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
    print(f"Successfully stored {collection.count()} items in collection '{COLLECTION_NAME}'.")

def main():
    chunks_file = "data/processed_chunks.json"
    if not os.path.exists(chunks_file):
        print(f"Error: {chunks_file} not found. Run processor.py first.")
        return
    chunks = load_chunks(chunks_file)
    initialize_vector_store(chunks)

if __name__ == "__main__":
    main()
