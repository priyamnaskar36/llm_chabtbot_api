
import json
import os
import faiss
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import pickle


DATA_PATH = "../data/changi_cleaned_chunks.json"
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)


texts = [item["content"] for item in data]


model = SentenceTransformer("all-MiniLM-L6-v2")


print("[INFO] Generating embeddings...")
embeddings = model.encode(texts, show_progress_bar=True)


dimension = embeddings[0].shape[0]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

print(f"[SUCCESS] FAISS index created with {index.ntotal} vectors")

# Save index and metadata
os.makedirs("../data/vector_db", exist_ok=True)
faiss.write_index(index, "../data/vector_db/index.faiss")


metadata = [
    {"text": data[i]["content"], "url": data[i]["url"]}
    for i in range(len(data))
]

with open("../data/vector_db/metadata.pkl", "wb") as f:
    pickle.dump(metadata, f)

print("Embeddings and metadata saved to /data/vector_db/")
