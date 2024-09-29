# indexing.py

import os
import glob
import pickle
from bs4 import BeautifulSoup
import ollama
import numpy as np
from dotenv import load_dotenv
from typing import List
from rank_bm25 import BM25Okapi
from utils import preprocess_text


def create_chunks(text: str, chunk_size: int) -> List[str]:
    words = text.split()
    return [" ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)]


def create_embeddings(texts: List[str]) -> np.ndarray:
    response = ollama.embed(model=model_name, input=texts)
    return np.array(response["embeddings"])


# Load environment variables
load_dotenv()

# Initialize the model
model_name = os.getenv("EMBEDDING_MODEL", "mxbai-embed-large")

# Get chunk size from environment variable, default to 200
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 200))

# Path to data
data_path = "data/*.html"

# Lists to store data
documents = []
embeddings = []
metadata = []

# Loop over HTML files
for file_path in glob.glob(data_path):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        chunks = create_chunks(text, CHUNK_SIZE)
        documents.extend(chunks)

        # Create detailed chunk metadata
        base_name = os.path.basename(file_path)
        chunk_metadata = [{"file_name": base_name, "chunk_number": i + 1, "total_chunks": len(chunks)} for i in range(len(chunks))]
        metadata.extend(chunk_metadata)

        # Generate embeddings for chunks (now using batch embedding)
        chunk_embeddings = create_embeddings(chunks)
        embeddings.extend(chunk_embeddings)

# Print the dimension of the embedding vector
if embeddings:
    print(f"Embedding vector dimension: {len(embeddings[0])}")

# Preprocess documents for BM25
tokenized_corpus = [preprocess_text(doc) for doc in documents]
bm25 = BM25Okapi(tokenized_corpus)

# Convert embeddings to numpy array
embeddings = np.array(embeddings)
# Ensure the index directory exists
os.makedirs("index", exist_ok=True)

# Save the index
index_path = os.getenv("INDEX_PATH", "index/index.pkl")
with open(index_path, "wb") as f:
    pickle.dump({"documents": documents, "embeddings": embeddings, "metadata": metadata, "bm25": bm25}, f)

# print the number of documents, embeddings, metadata, and bm25 and file size in MB
print(f"Number of documents: {len(documents)}")
print(f"Number of embeddings: {len(embeddings)}")
print(f"File size: {os.path.getsize(index_path) / 1024 / 1024:.2f} MB")
