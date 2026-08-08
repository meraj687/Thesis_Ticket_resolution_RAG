"""
Semantic Retriever

Hybrid retrieval using:

1. Sentence Transformers
2. FAISS semantic similarity
3. SAP technical keyword matching
4. Business-object matching
5. Transaction matching
6. Hybrid re-ranking
"""

import re
import numpy as np

from sentence_transformers import SentenceTransformer

from app.repositories.embedding_repository import EmbeddingRepository
from app.retriever.faiss_index import FaissIndex


class SemanticRetriever:
    """
    Performs hybrid semantic retrieval for SAP MDG incidents.

    Semantic similarity is combined with exact SAP technical
    term matching to improve retrieval of technically specific
    incidents such as SMQ1, SM59, DRFOUT and RFC issues.
    """

    def __init__(self):

        print("Loading Sentence Transformer model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Loading knowledge records...")

        self.records = EmbeddingRepository.load_records()

        print(
            f"Loaded {len(self.records)} knowledge records."
        )

        print("Loading FAISS index...")

        self.faiss = FaissIndex()

        self.faiss.load()

        print("FAISS index loaded.")

    # =====================================================
    # TEXT NORMALIZATION
    # =====================================================

    @staticmethod
    def normalize_text(text):
        """
        Normalize text for reliable keyword matching.
        """

        if text is None:
            return ""

        text = str(text).lower()

        text = re.sub(
            r"[^a-z0-9]+",
            " ",
            text
        )

        return text.strip()

    # =====================================================
    # EXTRACT SAP TECHNICAL TERMS
    # =====================================================

    @staticmethod
    def extract_technical_terms(query):
        """
        Extract important SAP technical terms from
        the submitted ticket.
        """

        query_lower = query.lower()

        known_terms = [
            "smq1",
            "smq2",
            "sm59",
            "drfout",
            "drf",
            "rfc",
            "slg1",
            "replication",
            "outbound",
            "inbound",
            "queue",
            "workflow",
            "change request",
            "activation",
            "validation",
            "timeout",
            "connection",
            "configuration",
            "business partner",
            "customer",
            "vendor",
            "material"
        ]

        found_terms = []

        for term in known_terms:

            if term in query_lower:

                found_terms.append(term)

        return found_terms

    # =====================================================
    # RECORD TEXT
    # =====================================================

    @staticmethod
    def build_record_text(record):
        """
        Combine important knowledge-record fields into
        searchable text.
        """

        fields = [

            getattr(
                record,
                "issue",
                ""
            ),

            getattr(
                record,
                "module",
                ""
            ),

            getattr(
                record,
                "business_object",
                ""
            ),

            getattr(
                record,
                "category",
                ""
            ),

            getattr(
                record,
                "business_process",
                ""
            ),

            getattr(
                record,
                "possible_root_causes",
                ""
            ),

            getattr(
                record,
                "diagnostic_steps",
                ""
            ),

            getattr(
                record,
                "recommended_resolution",
                ""
            ),

            getattr(
                record,
                "responsible_department",
                ""
            ),

            getattr(
                record,
                "support_team",
                ""
            ),

            getattr(
                record,
                "resolver_role",
                ""
            ),

            getattr(
                record,
                "sap_transactions",
                ""
            ),

            getattr(
                record,
                "keywords",
                ""
            )

        ]

        text_parts = []

        for field in fields:

            if isinstance(field, list):

                text_parts.extend(
                    str(item)
                    for item in field
                )

            else:

                text_parts.append(
                    str(field)
                )

        return " ".join(
            text_parts
        )

    # =====================================================
    # TECHNICAL MATCH SCORE
    # =====================================================

    def calculate_keyword_score(
        self,
        query,
        record
    ):
        """
        Calculate exact technical-term overlap.

        Stronger weight is given to SAP transaction codes
        and technical terms.
        """

        query_terms = self.extract_technical_terms(
            query
        )

        if not query_terms:
            return 0.0

        record_text = self.normalize_text(
            self.build_record_text(record)
        )

        matched = 0

        for term in query_terms:

            normalized_term = self.normalize_text(
                term
            )

            if normalized_term in record_text:

                matched += 1

        return matched / len(
            query_terms
        )

    # =====================================================
    # BUSINESS OBJECT MATCH
    # =====================================================

    def calculate_business_object_score(
        self,
        query,
        record
    ):
        """
        Check whether the ticket and record refer to
        the same SAP business object.
        """

        query_lower = query.lower()

        business_objects = [
            "business partner",
            "customer",
            "vendor",
            "material",
            "master data"
        ]

        record_object = self.normalize_text(
            getattr(
                record,
                "business_object",
                ""
            )
        )

        if not record_object:
            return 0.0

        for obj in business_objects:

            if (
                obj in query_lower
                and obj in record_object
            ):

                return 1.0

        return 0.0

    # =====================================================
    # CATEGORY / PROCESS MATCH
    # =====================================================

    def calculate_category_score(
        self,
        query,
        record
    ):
        """
        Give additional weight when the ticket contains
        concepts matching the record category/process.
        """

        query_text = self.normalize_text(
            query
        )

        category = self.normalize_text(
            getattr(
                record,
                "category",
                ""
            )
        )

        process = self.normalize_text(
            getattr(
                record,
                "business_process",
                ""
            )
        )

        score = 0.0

        if category:

            category_words = category.split()

            if any(
                word in query_text
                for word in category_words
                if len(word) > 2
            ):

                score += 0.5

        if process:

            process_words = process.split()

            if any(
                word in query_text
                for word in process_words
                if len(word) > 2
            ):

                score += 0.5

        return min(
            score,
            1.0
        )

    # =====================================================
    # HYBRID SEARCH
    # =====================================================

    def search(
        self,
        query: str,
        top_k: int = 5
    ):
        """
        Perform hybrid retrieval.

        FAISS retrieves a wider candidate pool first.
        Candidates are then re-ranked using:

        Semantic similarity
        +
        Technical term matching
        +
        Business-object matching
        +
        Category/process matching
        """

        if not query or not query.strip():

            return []

        # -------------------------------------------------
        # STEP 1
        # Generate normalized query embedding
        # -------------------------------------------------

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        query_embedding = np.asarray(
            query_embedding,
            dtype=np.float32
        )

        # -------------------------------------------------
        # STEP 2
        # Retrieve wider FAISS candidate pool
        # -------------------------------------------------

        candidate_k = min(
            max(top_k * 5, 15),
            len(self.records)
        )

        similarities, indices = (
            self.faiss.index.search(
                query_embedding,
                candidate_k
            )
        )

        candidates = []

        # -------------------------------------------------
        # STEP 3
        # Build hybrid score
        # -------------------------------------------------

        for similarity, index in zip(
            similarities[0],
            indices[0]
        ):

            if index == -1:
                continue

            record = self.records[index]

            semantic_score = float(
                similarity
            )

            semantic_score = max(
                0.0,
                min(
                    semantic_score,
                    1.0
                )
            )

            keyword_score = (
                self.calculate_keyword_score(
                    query,
                    record
                )
            )

            business_object_score = (
                self.calculate_business_object_score(
                    query,
                    record
                )
            )

            category_score = (
                self.calculate_category_score(
                    query,
                    record
                )
            )

            # -------------------------------------------------
            # HYBRID WEIGHTING
            # -------------------------------------------------

            hybrid_score = (

                0.60 * semantic_score

                + 0.25 * keyword_score

                + 0.10 * business_object_score

                + 0.05 * category_score

            )

            hybrid_score = max(
                0.0,
                min(
                    hybrid_score,
                    1.0
                )
            )

            candidates.append({

                "similarity": round(
                    hybrid_score,
                    4
                ),

                "semantic_similarity": round(
                    semantic_score,
                    4
                ),

                "keyword_score": round(
                    keyword_score,
                    4
                ),

                "business_object_score": round(
                    business_object_score,
                    4
                ),

                "category_score": round(
                    category_score,
                    4
                ),

                "record": record

            })

        # -------------------------------------------------
        # STEP 4
        # Sort by hybrid score
        # -------------------------------------------------

        candidates.sort(
            key=lambda item: item["similarity"],
            reverse=True
        )

        # -------------------------------------------------
        # STEP 5
        # Return Top-K
        # -------------------------------------------------

        results = candidates[:top_k]

        # -------------------------------------------------
        # DEBUG INFORMATION
        # -------------------------------------------------

        print(
            "\n========== HYBRID RETRIEVAL =========="
        )

        print(
            f"Query: {query}"
        )

        print(
            f"Technical terms: "
            f"{self.extract_technical_terms(query)}"
        )

        for i, result in enumerate(
            results,
            start=1
        ):

            record = result["record"]

            print(
                f"\n#{i}"
            )

            print(
                f"Issue: {record.issue}"
            )

            print(
                f"Hybrid Score: "
                f"{result['similarity']}"
            )

            print(
                f"Semantic: "
                f"{result['semantic_similarity']}"
            )

            print(
                f"Keyword: "
                f"{result['keyword_score']}"
            )

            print(
                f"Business Object: "
                f"{result['business_object_score']}"
            )

            print(
                f"Category: "
                f"{result['category_score']}"
            )

        print(
            "=======================================\n"
        )

        return results