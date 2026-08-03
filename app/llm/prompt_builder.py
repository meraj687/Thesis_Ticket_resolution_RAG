"""
Prompt Builder

Builds structured prompts for the local LLM.
"""

from typing import List
from app.models.knowledge_record import KnowledgeRecord


class PromptBuilder:

    @staticmethod
    def build(
        user_query: str,
        retrieved_records: List[KnowledgeRecord]
    ) -> str:

        context = ""

        for i, record in enumerate(retrieved_records, start=1):

            context += f"""
==========================
Knowledge Record {i}
==========================

Issue:
{record.issue}

Business Object:
{record.business_object}

SAP Module:
{record.module}

Category:
{record.category}

Possible Root Causes:
{", ".join(record.possible_root_causes)}

Diagnostic Steps:
{", ".join(record.diagnostic_steps)}

Recommended Resolution:
{", ".join(record.recommended_resolution)}

Responsible Department:
{record.responsible_department}

Support Team:
{record.support_team}

Resolver Role:
{record.resolver_role}

Business Process:
{record.business_process}

Business Impact:
{record.business_impact}
"""

        prompt = f"""
You are a Senior SAP MDG Support Consultant.

Analyze the SAP support ticket using ONLY the retrieved SAP MDG knowledge.

User Ticket:
{user_query}

Retrieved Knowledge:
{context}

Return ONLY valid JSON.

The JSON must have EXACTLY the following structure:

{{
    "issue_summary": "",
    "root_cause": "",
    "diagnostic_steps": [
        "",
        "",
        ""
    ],
    "recommended_resolution": "",
    "responsible_department": "",
    "resolver_role": "",
    "business_impact": "",
    "confidence": ""
}}

Rules:
- Return ONLY valid JSON.
- Do NOT use Markdown.
- Do NOT add explanations.
- Do NOT wrap the JSON in ```json blocks.
- Do NOT add any text before or after the JSON.
- Use ONLY the retrieved SAP MDG knowledge.
- If information is unavailable, return an empty string ("") for that field.
"""

        return prompt