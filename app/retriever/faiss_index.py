"""
FAISS Vector Index
Using Cosine Similarity (Inner Product)
"""

from pathlib import Path

import faiss
import numpy as np


class FaissIndex:

    INDEX_PATH = Path("models/faiss/faiss.index")

    def __init__(self):

        self.index = None

    def build(self, embeddings):

        dimension = embeddings.shape[1]

        # Normalize embeddings
        embeddings = np.asarray(
            embeddings,
            dtype=np.float32
        )

        faiss.normalize_L2(embeddings)

        # Inner Product = Cosine Similarity
        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(embeddings)

        return self.index

    def save(self):

        self.INDEX_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            str(self.INDEX_PATH)
        )

        print("FAISS index saved successfully.")

    def load(self):

        self.index = faiss.read_index(
            str(self.INDEX_PATH)
        )

        return self.index