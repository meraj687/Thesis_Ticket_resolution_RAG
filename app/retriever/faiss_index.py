"""
FAISS Vector Index

Builds and loads a FAISS vector index using
Cosine Similarity (Inner Product).

Author: Mohammad Aryaan
Project: SAP MDG Intelligent Support Assistant
"""

from pathlib import Path

import faiss
import numpy as np


class FaissIndex:
    """
    Handles creation, saving, and loading
    of the FAISS vector index.
    """

    INDEX_PATH = Path("models/faiss/faiss.index")

    def __init__(self):

        self.index = None

    def build(self, embeddings):
        """
        Build a FAISS index using
        Cosine Similarity.

        Parameters
        ----------
        embeddings : numpy.ndarray
            Sentence Transformer embeddings.

        Returns
        -------
        faiss.Index
        """

        if embeddings is None or len(embeddings) == 0:
            raise ValueError(
                "No embeddings were provided to build the FAISS index."
            )

        embeddings = np.asarray(
            embeddings,
            dtype=np.float32
        )

        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)

        dimension = embeddings.shape[1]

        # Inner Product on normalized vectors = Cosine Similarity
        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(embeddings)

        print(
            f"FAISS index created successfully with {self.index.ntotal} vectors."
        )

        return self.index

    def save(self):
        """
        Save the FAISS index to disk.
        """

        if self.index is None:
            raise ValueError(
                "FAISS index has not been created yet."
            )

        self.INDEX_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            str(self.INDEX_PATH)
        )

        print(
            f"FAISS index saved successfully at:\n{self.INDEX_PATH}"
        )

    def load(self):
        """
        Load the FAISS index from disk.
        """

        if not self.INDEX_PATH.exists():
            raise FileNotFoundError(
                f"FAISS index not found:\n{self.INDEX_PATH}"
            )

        self.index = faiss.read_index(
            str(self.INDEX_PATH)
        )

        print(
            f"FAISS index loaded successfully ({self.index.ntotal} vectors)."
        )

        return self.index