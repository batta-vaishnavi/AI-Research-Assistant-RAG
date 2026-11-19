# AI Research Assistant using Retrieval-Augmented Generation (RAG)

## Project Overview

The AI Research Assistant is a document-based question-answering application built using Retrieval-Augmented Generation (RAG).

It allows users to ask questions about research papers and receive context-aware answers generated using Google's Gemini API. The system retrieves relevant information from a document database before generating answers.

## Features

- Upload and process research papers in PDF format.
- Extract and chunk document text.
- Generate embeddings using Sentence Transformers.
- Store and retrieve document embeddings using ChromaDB.
- Generate research-based answers using Google Gemini.
- Display retrieved document sources and page numbers.
- Handle questions that cannot be answered using the available research papers.
- Compare RAG-based answers with Non-RAG answers.

## Technologies Used

- Python 3.12
- Streamlit
- ChromaDB
- Sentence Transformers
- Google Gemini API
- PyPDF
- Python-dotenv

## Research Papers Included

1. Attention Is All You Need
2. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
3. LoRA: Low-Rank Adaptation of Large Language Models

## Project Structure

```text
rag-ai-assistant/
│
├── data/
│   ├── attention.pdf
│   ├── bert.pdf
│   └── lora.pdf
│
├── src/
│   ├── ingest.py
│   ├── retrieve.py
│   └── generate.py
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd rag-ai-assistant
```

### 2. Create a virtual environment

```bash
py -3.12 -m venv .venv312
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\.venv312\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure the Gemini API key

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_gemini_api_key
```

Do not upload your `.env` file or share your API key publicly.

### 6. Ingest research papers

```bash
python src/ingest.py
```

### 7. Run the application

```bash
streamlit run app.py
```

## Application Sections

### Research Assistant

Users can ask questions about the included research papers. The application retrieves relevant document chunks and generates answers grounded in the retrieved context.

### RAG vs Non-RAG Comparison

This section compares:
- Non-RAG: Answers generated using the LLM's general knowledge.
- RAG: Answers generated using retrieved research-paper content.

## Testing

The application was tested using questions related to:

- Self-attention mechanisms in Transformers.
- Masked Language Modeling in BERT.
- Low-Rank Adaptation (LoRA).
- Questions outside the available document knowledge base.

The system successfully retrieved relevant sources and identified questions that could not be answered using the provided research papers.

## Future Improvements

- Improve document chunking and retrieval accuracy.
- Add support for more document formats.
- Implement advanced retrieval techniques.
- Add response evaluation metrics.
- Improve the user interface.

## Author

AI/ML Project Submission