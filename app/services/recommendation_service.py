"""
Recommendation Service

Handles:

1. Semantic Retrieval
2. SAP MDG Relevance Validation
3. Prompt Generation
4. LLM Recommendation
5. Fallback Logic
6. Confidence Calculation
7. Similar Incident Preparation
"""

import json
import time

from app.retriever.retriever import SemanticRetriever
from app.llm.prompt_builder import PromptBuilder
from app.llm.ollama_client import OllamaClient


class RecommendationService:

    def __init__(self):

        # -------------------------------------------------
        # Initialize Retriever
        # -------------------------------------------------

        self.retriever = SemanticRetriever()

        # -------------------------------------------------
        # Initialize Local LLM
        # -------------------------------------------------

        self.llm = OllamaClient()

        # -------------------------------------------------
        # Minimum SAP MDG Relevance Threshold
        #
        # 0.40 = 40% similarity
        #
        # Tickets below this threshold will NOT
        # be sent to the LLM.
        # -------------------------------------------------

        self.MIN_RELEVANCE_THRESHOLD = 0.40


    def analyze_ticket(self, ticket: str):

        start_time = time.time()

        # =====================================================
        # STEP 1 : Retrieve Similar SAP MDG Incidents
        # =====================================================

        results = self.retriever.search(
            ticket,
            top_k=3
        )

        # =====================================================
        # NO RETRIEVAL RESULTS
        # =====================================================

        if not results:

            response_time = round(
                time.time() - start_time,
                3
            )

            return {

                "version": "1.0.0",

                "generated_at": time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

                "ticket": ticket,

                "response_time": response_time,

                "retrieved_records": 0,

                "status": "rejected",

                "rejection_reason": (
                    "No relevant SAP MDG knowledge "
                    "was found for the submitted ticket."
                ),

                "recommendation": {

                    "issue_summary": (
                        "No sufficiently relevant "
                        "SAP MDG incident was found."
                    ),

                    "root_cause": [],

                    "diagnostic_steps": [],

                    "recommended_resolution": [],

                    "responsible_department": "",

                    "resolver_role": "",

                    "business_impact": "",

                    "confidence": 0,

                    "confidence_level": "Rejected",

                    "reasoning": (
                        "The knowledge base did not "
                        "contain a sufficiently relevant "
                        "SAP MDG incident."
                    ),

                    "retrieval_method": (
                        "Semantic Search "
                        "(Sentence Transformers + FAISS)"
                    ),

                    "llm": "Llama 3.2",

                    "embedding_model": (
                        "all-MiniLM-L6-v2"
                    ),

                    "retrieved_records": 0
                },

                "similar_incidents": []
            }


        # =====================================================
        # STEP 2 : Extract Retrieved Records
        # =====================================================

        records = [

            item["record"]

            for item in results

        ]


        # =====================================================
        # STEP 3 : SAP MDG RELEVANCE CHECK
        # =====================================================

        top_similarity = float(
            results[0]["similarity"]
        )

        # -----------------------------------------------------
        # Reject unrelated / low-relevance tickets
        # -----------------------------------------------------

        if top_similarity < self.MIN_RELEVANCE_THRESHOLD:

            response_time = round(
                time.time() - start_time,
                3
            )

            similarity_percentage = round(
                top_similarity * 100,
                2
            )

            return {

                "version": "1.0.0",

                "generated_at": time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

                "ticket": ticket,

                "response_time": response_time,

                "retrieved_records": 0,

                "status": "rejected",

                "rejection_reason": (
                    "The submitted ticket does not "
                    "appear to be related to SAP MDG "
                    "based on the available knowledge base."
                ),

                "rejection_message": (
                    "Please submit an SAP MDG-related "
                    "support ticket and try again."
                ),

                "similarity_score": similarity_percentage,

                "recommendation": {

                    "issue_summary": (
                        "The submitted ticket could not "
                        "be matched sufficiently to SAP MDG "
                        "knowledge."
                    ),

                    "root_cause": [],

                    "diagnostic_steps": [],

                    "recommended_resolution": [],

                    "responsible_department": "",

                    "resolver_role": "",

                    "business_impact": "",

                    "confidence": similarity_percentage,

                    "confidence_level": "Rejected",

                    "reasoning": (

                        "The highest retrieved similarity "
                        f"was {similarity_percentage:.2f}%, "
                        "which is below the minimum SAP MDG "
                        "relevance threshold of "
                        f"{self.MIN_RELEVANCE_THRESHOLD * 100:.0f}%. "
                        "The LLM was not invoked."
                    ),

                    "retrieval_method": (
                        "Semantic Search "
                        "(Sentence Transformers + FAISS)"
                    ),

                    "llm": "Llama 3.2",

                    "embedding_model": (
                        "all-MiniLM-L6-v2"
                    ),

                    "retrieved_records": 0
                },

                "similar_incidents": []
            }


        # =====================================================
        # STEP 4 : Build RAG Prompt
        # =====================================================

        prompt = PromptBuilder.build(
            ticket,
            records
        )


        # =====================================================
        # STEP 5 : Generate AI Recommendation
        # =====================================================

        answer = self.llm.generate(
            prompt
        )


        # =====================================================
        # STEP 6 : Parse LLM JSON Response
        # =====================================================

        try:

            recommendation = json.loads(
                answer
            )

        except json.JSONDecodeError:

            recommendation = {}


        # =====================================================
        # STEP 7 : Fallback Using Best Retrieved Record
        # =====================================================

        best_record = records[0]


        # -------------------------------------------------
        # Issue Summary
        # -------------------------------------------------

        if not recommendation.get(
            "issue_summary"
        ):

            recommendation["issue_summary"] = (
                best_record.issue
            )


        # -------------------------------------------------
        # Root Cause
        # -------------------------------------------------

        if not recommendation.get(
            "root_cause"
        ):

            recommendation["root_cause"] = (
                best_record.possible_root_causes
            )


        # -------------------------------------------------
        # Diagnostic Steps
        # -------------------------------------------------

        steps = recommendation.get(
            "diagnostic_steps"
        )

        if (
            not steps
            or (
                isinstance(
                    steps,
                    list
                )
                and all(
                    str(step).strip() == ""
                    for step in steps
                )
            )
        ):

            recommendation[
                "diagnostic_steps"
            ] = (
                best_record.diagnostic_steps
            )


        # -------------------------------------------------
        # Recommended Resolution
        # -------------------------------------------------

        resolution = recommendation.get(
            "recommended_resolution"
        )

        if (
            not resolution
            or (
                isinstance(
                    resolution,
                    list
                )
                and all(
                    str(res).strip() == ""
                    for res in resolution
                )
            )
        ):

            recommendation[
                "recommended_resolution"
            ] = (
                best_record.recommended_resolution
            )


        # -------------------------------------------------
        # Responsible Department
        # -------------------------------------------------

        if not recommendation.get(
            "responsible_department"
        ):

            recommendation[
                "responsible_department"
            ] = (
                best_record.responsible_department
            )


        # -------------------------------------------------
        # Resolver Role
        # -------------------------------------------------

        if not recommendation.get(
            "resolver_role"
        ):

            recommendation[
                "resolver_role"
            ] = (
                best_record.resolver_role
            )


        # -------------------------------------------------
        # Business Impact
        # -------------------------------------------------

        if not recommendation.get(
            "business_impact"
        ):

            recommendation[
                "business_impact"
            ] = (
                best_record.business_impact
            )


        # =====================================================
        # STEP 8 : Normalize Recommendation Fields
        # =====================================================

        for field in [

            "root_cause",

            "diagnostic_steps",

            "recommended_resolution"

        ]:

            value = recommendation.get(
                field,
                []
            )


            # -------------------------------------------------
            # Missing or None
            # -------------------------------------------------

            if value is None:

                recommendation[field] = []


            # -------------------------------------------------
            # String
            # -------------------------------------------------

            elif isinstance(
                value,
                str
            ):

                recommendation[field] = [

                    item.strip()

                    for item in value.split(",")

                    if item.strip()

                ]


            # -------------------------------------------------
            # List
            # -------------------------------------------------

            elif isinstance(
                value,
                list
            ):

                recommendation[field] = [

                    str(item).strip()

                    for item in value

                    if str(item).strip()

                ]


            # -------------------------------------------------
            # Unexpected Type
            # -------------------------------------------------

            else:

                recommendation[field] = []


        # =====================================================
        # STEP 9 : Confidence Calculation
        # =====================================================

        similarity = float(
            results[0]["similarity"]
        )

        confidence = round(
            similarity * 100
        )

        confidence = max(
            0,
            min(
                confidence,
                100
            )
        )

        recommendation[
            "confidence"
        ] = confidence


        # -------------------------------------------------
        # Confidence Level
        # -------------------------------------------------

        if confidence >= 90:

            recommendation[
                "confidence_level"
            ] = "Excellent"

        elif confidence >= 75:

            recommendation[
                "confidence_level"
            ] = "High"

        elif confidence >= 60:

            recommendation[
                "confidence_level"
            ] = "Moderate"

        elif confidence >= 40:

            recommendation[
                "confidence_level"
            ] = "Fair"

        else:

            recommendation[
                "confidence_level"
            ] = "Low"


        # =====================================================
        # STEP 10 : Prepare Similar Incidents
        # =====================================================

        similar_incidents = []


        for item in results:

            record = item["record"]

            similarity = float(
                item["similarity"]
            )

            # Keep similarity between 0 and 1
            similarity = max(
                0.0,
                min(
                    similarity,
                    1.0
                )
            )

            similar_incidents.append({

                "issue": record.issue,

                "business_object": (
                    record.business_object
                ),

                "module": record.module,

                "category": record.category,

                "department": (
                    record.responsible_department
                ),

                "resolver_role": (
                    record.resolver_role
                ),

                "similarity": round(
                    similarity * 100,
                    2
                )

            })


        # =====================================================
        # STEP 11 : Reasoning
        # =====================================================

        reasoning = f"""
The submitted SAP support ticket was converted into
semantic embeddings using the Sentence Transformer model.

FAISS searched the vector database and retrieved
{len(records)} similar SAP MDG incidents.

The retrieved incidents were supplied to the Llama 3.2
language model using Retrieval-Augmented Generation (RAG).

The recommendation was generated only from the retrieved
SAP knowledge records.

The confidence score is derived from the semantic similarity
between the submitted ticket and the closest matching incident.

The minimum SAP MDG relevance threshold was
{self.MIN_RELEVANCE_THRESHOLD * 100:.0f}%.
"""


        recommendation[
            "reasoning"
        ] = reasoning


        # =====================================================
        # STEP 12 : System Metadata
        # =====================================================

        recommendation[
            "retrieval_method"
        ] = (
            "Semantic Search "
            "(Sentence Transformers + FAISS)"
        )


        recommendation[
            "llm"
        ] = "Llama 3.2"


        recommendation[
            "embedding_model"
        ] = "all-MiniLM-L6-v2"


        recommendation[
            "retrieved_records"
        ] = len(records)


        # =====================================================
        # STEP 13 : Final Response Time
        # =====================================================

        response_time = round(
            time.time() - start_time,
            3
        )


        # =====================================================
        # STEP 14 : Final Response
        # =====================================================

        return {

            "version": "1.0.0",

            "generated_at": time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "ticket": ticket,

            "response_time": response_time,

            "retrieved_records": len(records),

            "status": "success",

            "recommendation": recommendation,

            "similar_incidents": similar_incidents

        }