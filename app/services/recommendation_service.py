"""
Recommendation Service

Handles:
1. Semantic Retrieval
2. Prompt Generation
3. LLM Recommendation
4. Fallback Logic
5. Confidence Calculation
"""

import json
import time

from app.retriever.retriever import SemanticRetriever
from app.llm.prompt_builder import PromptBuilder
from app.llm.ollama_client import OllamaClient


class RecommendationService:

    def __init__(self):

        self.retriever = SemanticRetriever()

        self.llm = OllamaClient()

    def analyze_ticket(self, ticket: str):
        start_time = time.time()

        # =====================================================
        # STEP 1 : Retrieve Similar Incidents
        # =====================================================

        results = self.retriever.search(
            ticket,
            top_k=3
        )

        if not results:
            return {
                "ticket": ticket,
                "response_time": round(time.time() - start_time, 2),
                "retrieved_records": 0,
                "recommendation": {
                    "issue_summary": "No similar SAP incidents found.",
                    "root_cause": [],
                    "diagnostic_steps": [],
                    "recommended_resolution": [],
                    "responsible_department": "",
                    "resolver_role": "",
                    "business_impact": "",
                    "confidence": 0,
                    "confidence_level": "Unknown",
                    "reasoning": "The knowledge base did not contain any similar incidents."
                },
                "similar_incidents": []
            }

        records = [
            item["record"]
            for item in results
        ]

        # =====================================================
        # STEP 2 : Build Prompt
        # =====================================================

        prompt = PromptBuilder.build(
            ticket,
            records
        )

        # =====================================================
        # STEP 3 : Generate AI Recommendation
        # =====================================================

        answer = self.llm.generate(prompt)

        try:

            recommendation = json.loads(answer)

        except json.JSONDecodeError:

            recommendation = {}

        # =====================================================
        # STEP 4 : Fallback using Best Retrieved Record
        # =====================================================

        best_record = records[0]

        # Issue Summary

        if not recommendation.get("issue_summary"):

            recommendation["issue_summary"] = best_record.issue

        # Root Cause

        if not recommendation.get("root_cause"):

            recommendation["root_cause"] = (
                best_record.possible_root_causes
            )

        # Diagnostic Steps

        # if not recommendation.get("diagnostic_steps"):

        #     recommendation["diagnostic_steps"] = (
        #         best_record.diagnostic_steps
        #     )

        steps = recommendation.get("diagnostic_steps")

        if(
            not steps
            or (
                isinstance(steps , list)
                and all(
                    str(step).strip() == ""
                    for step in steps
                )
            )
        ):

            recommendation["diagnostic_steps"] = (
                best_record.diagnostic_steps    
            )   

        # Recommended Resolution

        # if not recommendation.get("recommended_resolution"):

        #     recommendation["recommended_resolution"] = (
        #         best_record.recommended_resolution
        #     )

        resolution = recommendation.get("recommended_resolution")

        if(
            not resolution
            or (
                isinstance(resolution , list)
                and all(
                    str(res).strip() == ""
                    for res in resolution
                )
            )
        ):
        
            recommendation["recommended_resolution"] = (
                best_record.recommended_resolution    
            )

        # Department

        if not recommendation.get("responsible_department"):

            recommendation["responsible_department"] = (
                best_record.responsible_department
            )

        # Resolver

        if not recommendation.get("resolver_role"):

            recommendation["resolver_role"] = (
                best_record.resolver_role
            )

        # Business Impact

        if not recommendation.get("business_impact"):

            recommendation["business_impact"] = (
                best_record.business_impact
            )

        # =====================================================
        # STEP 5 : Normalize Recommendation Fields
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
            # Missing or None value
            # -------------------------------------------------

            if value is None:

                recommendation[field] = []

            # -------------------------------------------------
            # LLM returned a string
            # -------------------------------------------------

            elif isinstance(value, str):

                recommendation[field] = [
                    item.strip()
                    for item in value.split(",")
                    if item.strip()
                ]

            # -------------------------------------------------
            # LLM returned a list
            # -------------------------------------------------

            elif isinstance(value, list):

                recommendation[field] = [
                    str(item).strip()
                    for item in value
                    if str(item).strip()
                ]

            # -------------------------------------------------
            # Unexpected data type
            # -------------------------------------------------

            else:

                recommendation[field] = []

        # =====================================================
        # STEP 6 : Confidence Calculation
        # (Cosine Similarity)
        # =====================================================

        similarity = results[0]["similarity"]

        confidence = round(similarity * 100)

        confidence = max(
            0,
            min(
                confidence,
                100
            )
        )

        recommendation["confidence"] = confidence

        if confidence >= 90:

            recommendation["confidence_level"] = "Excellent"

        elif confidence >= 75:

            recommendation["confidence_level"] = "High"

        elif confidence >= 60:

            recommendation["confidence_level"] = "Moderate"

        elif confidence >= 40:

            recommendation["confidence_level"] = "Fair"

        else:

            recommendation["confidence_level"] = "Low"

        # =====================================================
        # STEP 7 : Similar Incidents
        # =====================================================

        similar_incidents = []

        for item in results:

            record = item["record"]
            similarity = min(item["similarity"], 1.0)  # Ensure similarity does not exceed 1.0

            similar_incidents.append({
                "issue": record.issue,
                "business_object": record.business_object,
                "module": record.module,
                "category": record.category,
                "department": record.responsible_department,
                "resolver_role": record.resolver_role,
                "similarity": round(
                    similarity * 100,
                    2
                )
            })

        # =====================================================
        # STEP 8 : Final Response
        # =====================================================

        reasoning = f"""
The submitted SAP support ticket was converted into semantic embeddings using the Sentence Transformer model.

FAISS searched the vector database and retrieved {len(records)} similar SAP MDG incidents.

The retrieved incidents were supplied to the Llama 3.2 language model using Retrieval-Augmented Generation (RAG).

The recommendation was generated only from the retrieved SAP knowledge records.

The confidence score is derived from the semantic similarity between the submitted ticket and the closest matching incident.
"""

        recommendation["reasoning"] = reasoning

        # Add these new fields here
        recommendation["retrieval_method"] = "Semantic Search (Sentence Transformers + FAISS)"

        recommendation["llm"] = "Llama 3.2"

        recommendation["embedding_model"] = "all-MiniLM-L6-v2"

        recommendation["retrieved_records"] = len(records)

        response_time = round(time.time() - start_time, 3)

        return {
            "version": "1.0.0",
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "ticket": ticket,
            "response_time": response_time,
            "retrieved_records": len(records),
            "recommendation": recommendation,
            "similar_incidents": similar_incidents
        }