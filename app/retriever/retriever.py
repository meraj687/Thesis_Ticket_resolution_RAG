"""
Semantic Retriever
"""

import numpy as np
from sentence_transformers import SentenceTransformer

from app.repositories.embedding_repository import EmbeddingRepository
from app.retriever import similarity
from app.retriever.faiss_index import FaissIndex


class SemanticRetriever:
    """
    Retrieves the most semantically similar knowledge records.
    """

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.records = EmbeddingRepository.load_records()

        self.faiss = FaissIndex()

        self.faiss.load()

    def search(self, query: str, top_k: int = 5):

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )

        distances, indices = self.faiss.index.search(
            np.asarray(query_embedding, dtype=np.float32),
            top_k
        )

        results = []

        for distance, index in zip(distances[0], indices[0]):

            results.append({

                "distance": float(distance),
                "similarity": similarity,
                "record": self.records[index]

            })

        return results