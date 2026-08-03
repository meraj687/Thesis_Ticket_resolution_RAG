"""
Embedding Repository

Loads embeddings and metadata used by the retrieval engine.
"""

import json
import joblib
from pathlib import Path

from app.models.knowledge_record import KnowledgeRecord


class EmbeddingRepository:

    EMBEDDING_PATH = Path("models/embeddings/knowledge_embeddings.pkl")
    KNOWLEDGE_PATH = Path("data/knowledge/sap_mdg_knowledge.json")

    @classmethod
    def load_embeddings(cls):

        if not cls.EMBEDDING_PATH.exists():
            raise FileNotFoundError(
                f"Embedding file not found: {cls.EMBEDDING_PATH}"
            )

        return joblib.load(cls.EMBEDDING_PATH)

    @classmethod
    def load_records(cls):

        if not cls.KNOWLEDGE_PATH.exists():
            raise FileNotFoundError(
                f"Knowledge file not found: {cls.KNOWLEDGE_PATH}"
            )

        with open(cls.KNOWLEDGE_PATH, encoding="utf-8") as file:

            data = json.load(file)

        return [

            KnowledgeRecord(**record)

            for record in data

        ]