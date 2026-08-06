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
You are an experienced SAP Master Data Governance (SAP MDG) Support Consultant working in an enterprise support environment.

Your responsibility is to analyze SAP MDG support tickets and recommend the most appropriate resolution using ONLY the retrieved SAP MDG knowledge records.

User Support Ticket:
{user_query}

Retrieved SAP MDG Knowledge:
{context}

Instructions:

1. Read the user ticket carefully.
2. Compare it with every retrieved knowledge record.
3. Select the most relevant information.
4. Do NOT invent or assume any SAP information.
5. If multiple records contain useful information, combine them.
6. If a field is unavailable, return an empty string ("").
7. Keep the recommendations concise and professional.
8. Use SAP terminology.
9. Return ONLY valid JSON.

The response MUST have EXACTLY this structure:

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

Important Rules:

- Return ONLY JSON.
- No Markdown.
- No explanations.
- No introductory text.
- No closing remarks.
- No ```json blocks.
- Do not hallucinate SAP transactions or solutions.
- Use only the retrieved SAP MDG knowledge records.
"""

        return prompt