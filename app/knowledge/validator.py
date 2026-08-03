"""
Knowledge Record Validator
"""

from app.models.knowledge_record import KnowledgeRecord


class KnowledgeValidator:
    """
    Validates KnowledgeRecord objects.
    """

    REQUIRED_LIST_FIELDS = [
        "possible_root_causes",
        "diagnostic_steps",
        "recommended_resolution",
        "sap_transactions",
        "keywords",
        "references",
    ]

    @classmethod
    def validate(cls, record: KnowledgeRecord):

        if not record.issue.strip():
            raise ValueError("Issue cannot be empty.")

        if not record.category.strip():
            raise ValueError("Category cannot be empty.")

        if not record.module.strip():
            raise ValueError("Module cannot be empty.")

        if not record.business_object.strip():
            raise ValueError("Business Object cannot be empty.")

        for field in cls.REQUIRED_LIST_FIELDS:

            value = getattr(record, field)

            if not isinstance(value, list):

                raise TypeError(f"{field} must be a list.")

            if len(value) == 0:

                raise ValueError(f"{field} cannot be empty.")

        return True