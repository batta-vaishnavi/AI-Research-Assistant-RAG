
import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "chroma_db"

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path=str(DB_DIR))

collection = client.get_collection(
    name="ai_ml_documents"
)


def retrieve_documents(question, top_k=3):
    """Retrieve the most relevant document chunks."""
    question_embedding = model.encode(
        question,
        convert_to_numpy=True
    )

    results = collection.query(
        query_embeddings=[question_embedding.tolist()],
        n_results=min(top_k, collection.count())
    )

    retrieved_chunks = []

    for i, document in enumerate(results["documents"][0]):
        metadata = results["metadatas"][0][i]
        distance = results["distances"][0][i]

        retrieved_chunks.append({
            "text": document,
            "source": metadata["source"],
            "page": metadata["page"],
            "distance": distance
        })

    return retrieved_chunks


if __name__ == "__main__":
    question = input("\nEnter your question: ")

    results = retrieve_documents(question)

    print("\n--- RETRIEVED DOCUMENTS ---")

    for i, result in enumerate(results, start=1):
        print(f"\nResult {i}")
        print(f"Source: {result['source']}")
        print(f"Page: {result['page']}")
        print(f"Distance: {result['distance']:.4f}")
        print(f"Content:\n{result['text'][:1000]}")
        print("-" * 60)
