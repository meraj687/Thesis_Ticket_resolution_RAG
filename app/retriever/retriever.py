"""
Semantic Retriever
Cosine Similarity Retrieval
"""

import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

from app.repositories.embedding_repository import EmbeddingRepository
from app.retriever.faiss_index import FaissIndex


class SemanticRetriever:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.records = EmbeddingRepository.load_records()

        self.faiss = FaissIndex()

        self.faiss.load()

    def search(
        self,
        query: str,
        top_k: int = 5
    ):

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )

        query_embedding = np.asarray(
            query_embedding,
            dtype=np.float32
        )

        # Normalize query
        faiss.normalize_L2(query_embedding)

        scores, indices = self.faiss.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            results.append({

                "score": float(score),

                "similarity": float(score),

                "distance": float(score),

                "record": self.records[index]

            })

        return results