"""
Embedding Service

Creates sentence embeddings for SAP MDG knowledge documents.
"""

from sentence_transformers import SentenceTransformer
import numpy as np
import joblib
from pathlib import Path


class EmbeddingService:
    """
    Generates and saves semantic embeddings.
    """

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Embedding model loaded successfully.")

    def encode(self, documents):

        embeddings = self.model.encode(

            documents,

            convert_to_numpy=True,

            show_progress_bar=True

        )

        return embeddings

    @staticmethod
    def save_embeddings(
        embeddings,
        output_file
    ):

        Path(output_file).parent.mkdir(

            parents=True,

            exist_ok=True

        )

        joblib.dump(

            embeddings,

            output_file

        )

        print(f"Embeddings saved to {output_file}")