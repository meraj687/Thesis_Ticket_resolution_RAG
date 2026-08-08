"""
SAP MDG Intelligent Support Assistant
Knowledge Base Embedding + FAISS Index Builder

This script:
1. Loads the current SAP MDG knowledge base
2. Generates embeddings using all-MiniLM-L6-v2
3. Saves the embeddings
4. Builds a new FAISS index
5. Saves the FAISS index
6. Verifies the number of records
"""

from pathlib import Path

import joblib
import numpy as np
from sentence_transformers import SentenceTransformer

from app.repositories.embedding_repository import EmbeddingRepository
from app.retriever.faiss_index import FaissIndex


# =====================================================
# PATHS
# =====================================================

EMBEDDING_PATH = Path(
    "models/embeddings/knowledge_embeddings.pkl"
)

KNOWLEDGE_PATH = Path(
    "data/knowledge/sap_mdg_knowledge.json"
)


# =====================================================
# BUILD TEXT FOR EMBEDDING
# =====================================================

def build_record_text(record):

    fields = [

        getattr(record, "issue", ""),

        getattr(record, "module", ""),

        getattr(record, "business_object", ""),

        getattr(record, "category", ""),

        getattr(record, "possible_root_causes", []),

        getattr(record, "diagnostic_steps", []),

        getattr(record, "recommended_resolution", []),

        getattr(record, "responsible_department", ""),

        getattr(record, "support_team", ""),

        getattr(record, "resolver_role", ""),

        getattr(record, "business_process", ""),

        getattr(record, "business_impact", ""),

        getattr(record, "sap_transactions", []),

        getattr(record, "keywords", [])

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
# MAIN
# =====================================================

def main():

    print("\n")
    print("=" * 70)
    print("SAP MDG KNOWLEDGE BASE REBUILD")
    print("=" * 70)
    print("\n")

    # =================================================
    # STEP 1 : LOAD KNOWLEDGE RECORDS
    # =================================================

    print(
        "STEP 1: Loading knowledge records..."
    )

    records = EmbeddingRepository.load_records()

    print(
        f"Loaded {len(records)} knowledge records."
    )

    if len(records) == 0:

        raise ValueError(
            "Knowledge base is empty."
        )

    # =================================================
    # STEP 2 : SHOW LAST RECORDS
    # =================================================

    print("\nLast knowledge records:")

    for record in records[-5:]:

        print(
            f"ID: {record.id} | "
            f"Issue: {record.issue}"
        )

    # =================================================
    # STEP 3 : BUILD EMBEDDING TEXT
    # =================================================

    print("\n")
    print(
        "STEP 2: Preparing embedding text..."
    )

    documents = [

        build_record_text(record)

        for record in records

    ]

    print(
        f"Prepared {len(documents)} documents."
    )

    # =================================================
    # STEP 4 : LOAD SENTENCE TRANSFORMER
    # =================================================

    print("\n")
    print(
        "STEP 3: Loading Sentence Transformer..."
    )

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    print(
        "Embedding model loaded."
    )

    # =================================================
    # STEP 5 : GENERATE EMBEDDINGS
    # =================================================

    print("\n")
    print(
        "STEP 4: Generating embeddings..."
    )

    embeddings = model.encode(

        documents,

        convert_to_numpy=True,

        normalize_embeddings=True,

        show_progress_bar=True

    )

    embeddings = np.asarray(
        embeddings,
        dtype=np.float32
    )

    print(
        f"Generated embeddings shape: "
        f"{embeddings.shape}"
    )

    # =================================================
    # STEP 6 : SAVE EMBEDDINGS
    # =================================================

    print("\n")
    print(
        "STEP 5: Saving embeddings..."
    )

    EMBEDDING_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        embeddings,
        EMBEDDING_PATH
    )

    print(
        f"Embeddings saved to:\n"
        f"{EMBEDDING_PATH}"
    )

    # =================================================
    # STEP 7 : BUILD FAISS INDEX
    # =================================================

    print("\n")
    print(
        "STEP 6: Building FAISS index..."
    )

    faiss_index = FaissIndex()

    faiss_index.build(
        embeddings
    )

    # =================================================
    # STEP 8 : SAVE FAISS INDEX
    # =================================================

    print("\n")
    print(
        "STEP 7: Saving FAISS index..."
    )

    faiss_index.save()

    # =================================================
    # STEP 9 : VERIFY
    # =================================================

    print("\n")
    print("=" * 70)
    print("REBUILD VERIFICATION")
    print("=" * 70)

    print(
        f"Knowledge records : {len(records)}"
    )

    print(
        f"Embedding vectors : {len(embeddings)}"
    )

    print(
        f"FAISS vectors     : "
        f"{faiss_index.index.ntotal}"
    )

    print(
        f"Embedding file    : "
        f"{EMBEDDING_PATH}"
    )

    print(
        f"FAISS file        : "
        f"{FaissIndex.INDEX_PATH}"
    )

    print("=" * 70)

    if (
        len(records)
        ==
        len(embeddings)
        ==
        faiss_index.index.ntotal
    ):

        print(
            "\nSUCCESS: Knowledge base, embeddings "
            "and FAISS index are synchronized."
        )

    else:

        raise RuntimeError(
            "\nERROR: Record count, embedding count "
            "and FAISS vector count do not match."
        )

    print("\n")


if __name__ == "__main__":
    main()