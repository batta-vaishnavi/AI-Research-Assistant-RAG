
from generate import client, generate_answer


def generate_without_rag(question):
    prompt = f"""
Answer the following question using your general knowledge.
Do not use any external documents.

Question: {question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":
    question = input("\nEnter a question about AI/ML: ")

    print("\n========== WITHOUT RAG ==========")
    answer_without_rag = generate_without_rag(question)
    print(answer_without_rag)

    print("\n========== WITH RAG ==========")
    answer_with_rag = generate_answer(question)
    print(answer_with_rag)
