import os
import faiss
import pickle
import requests
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer


load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")


if not api_key:
    raise ValueError("OPENROUTER_API_KEY is not set in .env file")


index = faiss.read_index("../data/vector_db/index.faiss")
with open("../data/vector_db/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

embedder = SentenceTransformer("all-MiniLM-L6-v2")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def ask_chatbot(query: str):

    query_embedding = embedder.encode([query])
    _, I = index.search(query_embedding, k=3)
    context = "\n\n".join([metadata[i]["text"] for i in I[0]])


    prompt = f"""Answer the question clearly and directly using the context below if helpful.

Question: {query}

Context:
{context}

Answer:"""

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f" Error: {str(e)}"

if __name__ == "__main__":
    print(" Welcome to the Changi Airport Chatbot \n")
    while True:
        user_input = input("Ask a question (or type 'exit'): ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break
        print("\nAnswer:\n", ask_chatbot(user_input), "\n")
