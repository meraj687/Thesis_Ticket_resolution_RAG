"""
Recommendation Service

Orchestrates the complete AI pipeline.
"""

import json

from app.retriever.retriever import SemanticRetriever
from app.llm.prompt_builder import PromptBuilder
from app.llm.ollama_client import OllamaClient


class RecommendationService:

    def __init__(self):

        self.retriever = SemanticRetriever()

        self.llm = OllamaClient()

    def analyze_ticket(self, ticket: str):

        # --------------------------------------------------
        # Retrieve Similar Incidents
        # --------------------------------------------------

        results = self.retriever.search(
            ticket,
            top_k=3
        )

        records = [
            item["record"]
            for item in results
        ]

        # --------------------------------------------------
        # Build Prompt
        # --------------------------------------------------

        prompt = PromptBuilder.build(
            ticket,
            records
        )

        # --------------------------------------------------
        # Generate AI Recommendation
        # --------------------------------------------------

        answer = self.llm.generate(prompt)

        try:

            recommendation = json.loads(answer)

        except json.JSONDecodeError:

            recommendation = {}

        # --------------------------------------------------
        # Fallback using Best Retrieved Record
        # --------------------------------------------------

        best_record = records[0]

        recommendation.setdefault(
            "issue_summary",
            best_record.issue
        )

        if not recommendation.get("root_cause"):

            recommendation["root_cause"] = (
                best_record.possible_root_causes
            )

        if not recommendation.get("diagnostic_steps"):

            recommendation["diagnostic_steps"] = (
                best_record.diagnostic_steps
            )

        if not recommendation.get("recommended_resolution"):

            recommendation["recommended_resolution"] = (
                best_record.recommended_resolution
            )

        if not recommendation.get("responsible_department"):

            recommendation["responsible_department"] = (
                best_record.responsible_department
            )

        if not recommendation.get("resolver_role"):

            recommendation["resolver_role"] = (
                best_record.resolver_role
            )

        if not recommendation.get("business_impact"):

            recommendation["business_impact"] = (
                best_record.business_impact
            )

        # --------------------------------------------------
        # Convert Strings into Lists
        # --------------------------------------------------

        if isinstance(
            recommendation["root_cause"],
            str
        ):

            recommendation["root_cause"] = [

                x.strip()

                for x in recommendation[
                    "root_cause"
                ].split(",")

                if x.strip()

            ]

        if isinstance(
            recommendation["recommended_resolution"],
            str
        ):

            recommendation["recommended_resolution"] = [

                x.strip()

                for x in recommendation[
                    "recommended_resolution"
                ].split(",")

                if x.strip()

            ]

        if isinstance(
            recommendation["diagnostic_steps"],
            str
        ):

            recommendation["diagnostic_steps"] = [

                x.strip()

                for x in recommendation[
                    "diagnostic_steps"
                ].split(",")

                if x.strip()

            ]

        # --------------------------------------------------
        # Confidence Calculation
        # --------------------------------------------------

        best_distance = results[0]["distance"]

        confidence = round(
            (1 - best_distance) * 100
        )

        confidence = max(
            0,
            min(
                confidence,
                100
            )
        )

        recommendation["confidence"] = f"{confidence}%"

        # --------------------------------------------------
        # Similar Incidents
        # --------------------------------------------------

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

                "distance": round(
                    item["distance"],
                    4
                )

            })

        # --------------------------------------------------
        # Final Response
        # --------------------------------------------------

        return {

            "ticket": ticket,

            "retrieved_records": len(records),

            "similar_incidents": similar_incidents,

            "recommendation": recommendation

        }