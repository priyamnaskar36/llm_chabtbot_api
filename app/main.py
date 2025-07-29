import os
import faiss
import pickle
import requests
import datetime
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY is missing in your .env file")

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Load vector DB and metadata
index = faiss.read_index("data/vector_db/index.faiss")
with open("data/vector_db/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

# Load embedder
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# FastAPI setup
app = FastAPI(title="Changi Airport Chatbot via OpenRouter")

# Pydantic schema
class QueryRequest(BaseModel):
    question: str

# Logging function
def log_interaction(question, answer, ip_address, model_name="mistralai/mistral-7b-instruct"):
    timestamp = datetime.datetime.now().isoformat()
    log_entry = f"[{timestamp}] IP: {ip_address} | Model: {model_name}\nQ: {question}\nA: {answer}\n---\n"
    with open("logs/conversations.log", "a", encoding="utf-8") as f:
        f.write(log_entry)

@app.post("/chat", response_class=PlainTextResponse)
async def chat_with_bot(payload: QueryRequest, request: Request):
    question = payload.question.strip()

    # Embed and search
    query_embedding = embedder.encode([question])
    _, I = index.search(query_embedding, k=3)
    context = "\n\n".join([metadata[i]["text"] for i in I[0]])

    # Prompt template
    prompt = f"""Answer the following question clearly using the context below if relevant.

Question: {question}

Context:
{context}

Answer:"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload_data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                                 headers=headers,
                                 json=payload_data,
                                 timeout=30)
        response_json = response.json()
        answer = response_json["choices"][0]["message"]["content"].strip()

        # Get client IP address
        client_ip = request.client.host
        log_interaction(question, answer, client_ip)

        return f"Question: {question}\nAnswer: {answer}\n\nContext:\n{context}"
    except Exception as e:
        return f" Error: {str(e)}"

@app.get("/")
async def root():
    return {"message": "Welcome to the Changi RAG Chatbot API via OpenRouter"}
