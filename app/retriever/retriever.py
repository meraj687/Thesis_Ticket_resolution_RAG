"""
Semantic Retriever

Uses Sentence Transformers + FAISS
to retrieve the most semantically similar
SAP MDG support incidents.
"""

import numpy as np
from sentence_transformers import SentenceTransformer

from app.repositories.embedding_repository import EmbeddingRepository
from app.retriever.faiss_index import FaissIndex


class SemanticRetriever:
    """
    Performs semantic search using
    Sentence Transformers and FAISS.
    """

    def __init__(self):

        print("Loading Sentence Transformer model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Loading knowledge records...")

        self.records = EmbeddingRepository.load_records()

        print("Loading FAISS index...")

        self.faiss = FaissIndex()

        self.faiss.load()

    def search(
        self,
        query: str,
        top_k: int = 5
    ):
        """
        Search the FAISS vector database
        and return the Top-K most similar
        SAP incidents.
        """

        # Generate normalized embedding
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        query_embedding = np.asarray(
            query_embedding,
            dtype=np.float32
        )

        # Search FAISS
        similarities, indices = self.faiss.index.search(
            query_embedding,
            top_k
        )

        results = []

        for similarity, index in zip(
            similarities[0],
            indices[0]
        ):

            # Skip invalid FAISS results
            if index == -1:
                continue

            results.append({

                "similarity": round(
                    float(similarity),
                    4
                ),

                "record": self.records[index]

            })

        return results