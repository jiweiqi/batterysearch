# search.py

import numpy as np
import pickle
from rank_bm25 import BM25Okapi
from typing import List, Dict
import os
from dotenv import load_dotenv
import ollama
import unittest
from utils import preprocess_text

# Load environment variables
load_dotenv()

# Load the index
with open(os.getenv("INDEX_PATH", "index/index.pkl"), "rb") as f:
    index = pickle.load(f)

documents = index["documents"]
embeddings = index["embeddings"]
metadata = index["metadata"]
bm25 = index["bm25"]

# Initialize the model
model_name = os.getenv("EMBEDDING_MODEL", "mxbai-embed-large")


def hybrid_search(bm25_query: str, vector_query: str, top_k: int = 5) -> tuple[List[Dict], List[Dict]]:
    # BM25 Search
    tokenized_query = preprocess_text(bm25_query)
    bm25_scores = bm25.get_scores(tokenized_query)
    top_bm25_results = np.argsort(bm25_scores)[::-1][:top_k]

    bm25_results = []
    for idx in top_bm25_results:
        bm25_results.append(
            {
                "score": bm25_scores[idx],
                "file_name": metadata[idx]["file_name"],
                "chunk_number": metadata[idx]["chunk_number"],
                "total_chunks": metadata[idx]["total_chunks"],
                "content": documents[idx],
            }
        )

    # Vector Search
    response = ollama.embed(model=model_name, input=[vector_query])
    query_embedding = np.array(response["embeddings"][0])

    cos_scores = np.dot(embeddings, query_embedding) / (np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding))
    top_vector_results = np.argsort(cos_scores)[::-1][:top_k]

    vector_results = []
    for idx in top_vector_results:
        vector_results.append(
            {
                "score": cos_scores[idx],
                "file_name": metadata[idx]["file_name"],
                "chunk_number": metadata[idx]["chunk_number"],
                "total_chunks": metadata[idx]["total_chunks"],
                "content": documents[idx],
            }
        )

    return bm25_results, vector_results


class TestHybridSearch(unittest.TestCase):
    def test_hybrid_search(self):
        bm25_query = "What's TOT?"
        vector_query = "sample vector query"
        top_k = 3

        bm25_results, vector_results = hybrid_search(bm25_query, vector_query, top_k)

        # print bm25_results nicely
        for result in bm25_results:
            print(result)

        self.assertLessEqual(len(bm25_results), top_k, f"Expected at most {top_k} BM25 results")
        self.assertLessEqual(len(vector_results), top_k, f"Expected at most {top_k} vector results")


if __name__ == "__main__":
    unittest.main()
