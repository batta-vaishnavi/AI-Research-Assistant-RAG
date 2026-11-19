
import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "chroma_db"

# Chunk settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 80

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path=str(DB_DIR))

collection = client.get_or_create_collection(
    name="ai_ml_documents",
    metadata={"hnsw:space": "cosine"}
)


def extract_pdf_text(pdf_path):
    """Extract text page by page from a PDF."""
    reader = PdfReader(str(pdf_path))
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            pages.append({
                "text": text,
                "page": page_number
            })

    return pages


def chunk_text(text, chunk_size=CHUNK_SIZE,
               overlap=CHUNK_OVERLAP):
    """Split text into overlapping word-based chunks."""
    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap

    return chunks


def ingest_documents():
    all_chunks = []
    all_metadata = []
    all_ids = []

    pdf_files = list(DATA_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in the data folder!")
        return

    for pdf_path in pdf_files:
        print(f"\nReading: {pdf_path.name}")

        pages = extract_pdf_text(pdf_path)

        for page_data in pages:
            chunks = chunk_text(page_data["text"])

            for chunk_index, chunk in enumerate(chunks):
                chunk_id = (
                    f"{pdf_path.stem}_"
                    f"page_{page_data['page']}_"
                    f"chunk_{chunk_index}"
                )

                all_chunks.append(chunk)

                all_metadata.append({
                    "source": pdf_path.name,
                    "page": page_data["page"],
                    "chunk_index": chunk_index
                })

                all_ids.append(chunk_id)

        print(f"Extracted {len(pages)} pages")

    if not all_chunks:
        print("No readable text found in PDFs.")
        return

    print(f"\nTotal chunks: {len(all_chunks)}")
    print("Generating embeddings...")

    embeddings = model.encode(
        all_chunks,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    print("Storing chunks in ChromaDB...")

    collection.upsert(
        ids=all_ids,
        documents=all_chunks,
        metadatas=all_metadata,
        embeddings=embeddings.tolist()
    )

    print("\nINGESTION COMPLETED!")
    print("Total chunks stored:", collection.count())


if __name__ == "__main__":
    ingest_documents()
