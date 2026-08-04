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

        if not recommendation.get("diagnostic_steps"):

            recommendation["diagnostic_steps"] = (
                best_record.diagnostic_steps
            )

        # Recommended Resolution

        if not recommendation.get("recommended_resolution"):

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
        # STEP 5 : Convert Strings to Lists
        # =====================================================

        if isinstance(
            recommendation["root_cause"],
            str
        ):

            recommendation["root_cause"] = [

                item.strip()

                for item in recommendation[
                    "root_cause"
                ].split(",")

                if item.strip()

            ]

        if isinstance(
            recommendation["diagnostic_steps"],
            str
        ):

            recommendation["diagnostic_steps"] = [

                item.strip()

                for item in recommendation[
                    "diagnostic_steps"
                ].split(",")

                if item.strip()

            ]

        if isinstance(
            recommendation["recommended_resolution"],
            str
        ):

            recommendation["recommended_resolution"] = [

                item.strip()

                for item in recommendation[
                    "recommended_resolution"
                ].split(",")

                if item.strip()

            ]

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

        if confidence >= 95:

            recommendation["confidence_level"] = "Very High"

        elif confidence >= 85:

            recommendation["confidence_level"] = "High"

        elif confidence >= 70:

            recommendation["confidence_level"] = "Medium"

        else:

            recommendation["confidence_level"] = "Low"

        # =====================================================
        # STEP 7 : Similar Incidents
        # =====================================================

        similar_incidents = []

        seen = set()

        for item in results:

            record = item["record"]

            if record.issue in seen:

                continue

            seen.add(record.issue)

            similar_incidents.append({

                "issue": record.issue,

                "business_object": record.business_object,

                "module": record.module,

                "category": record.category,

                "department": record.responsible_department,

                "resolver_role": record.resolver_role,

                "similarity": round(
                    item["similarity"] * 100,
                    2
                )

            })

        # =====================================================
        # STEP 8 : Final Response
        # =====================================================

        reasoning = f"""
The submitted SAP ticket was converted into embeddings.

The FAISS vector database retrieved {len(records)} similar incidents.

The recommendation was generated using the retrieved SAP MDG knowledge base.

Confidence is based on semantic similarity between the submitted ticket and retrieved incidents.
"""

        recommendation["reasoning"] = reasoning

        response_time = round(time.time() - start_time,2)

        return {

            "ticket": ticket,
            "response_time": response_time,

            "retrieved_records": len(records),

            "recommendation": recommendation,

            "similar_incidents": similar_incidents

        }