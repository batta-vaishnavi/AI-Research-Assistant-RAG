
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from retrieve import retrieve_documents

# Load API key from the project's .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Please check your .env file."
    )

# Initialize Gemini
client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.5-flash-lite"


def generate_with_retry(prompt, max_attempts=3):
    """Retry Gemini requests when the server is temporarily unavailable."""

    for attempt in range(max_attempts):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
            return response.text

        except Exception as error:
            error_message = str(error)

            is_temporary_error = (
                "503" in error_message
                or "UNAVAILABLE" in error_message
            )

            if is_temporary_error and attempt < max_attempts - 1:
                wait_time = 2 ** (attempt + 1)

                print(
                    f"Gemini is busy. Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:
                raise


def generate_answer(question):
    """Generate an answer grounded in retrieved research papers."""

    documents = retrieve_documents(question, top_k=3)

    if not documents:
        return "I could not find relevant information in the research papers."

    context = "\n\n".join([
        f"Source: {doc['source']}, Page: {doc['page']}\n"
        f"{doc['text']}"
        for doc in documents
    ])

    prompt = f"""
You are an AI research assistant.

Answer the user's question using ONLY the research paper
information provided in the context below.

If the answer is not available in the context, clearly say:
"I could not find this information in the provided research papers."

Do not invent facts or unsupported information.

RESEARCH PAPER CONTEXT:
{context}

USER QUESTION:
{question}

Provide a clear, structured and easy-to-understand answer.
"""

    return generate_with_retry(prompt)



def generate_without_rag(question):
    """Generate an answer using Gemini without retrieving documents."""

    prompt = f"""
You are a helpful AI assistant.

Answer the following question using your general knowledge.
Do not retrieve or refer to the research paper database.

Question:
{question}

Provide a clear and structured explanation.
"""

    return generate_with_retry(prompt)
