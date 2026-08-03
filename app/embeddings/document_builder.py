"""
Document Builder

Converts KnowledgeRecord into a semantic document.
"""

from app.models.knowledge_record import KnowledgeRecord


class DocumentBuilder:

    @staticmethod
    def build(record: KnowledgeRecord) -> str:

        return f"""
Business Object:
{record.business_object}

SAP Module:
{record.module}

Category:
{record.category}

Priority:
{record.priority}

Issue:
{record.issue}

Possible Root Causes:
{"; ".join(record.possible_root_causes)}

Diagnostic Steps:
{"; ".join(record.diagnostic_steps)}

Recommended Resolution:
{"; ".join(record.recommended_resolution)}

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

Keywords:
{"; ".join(record.keywords)}
"""