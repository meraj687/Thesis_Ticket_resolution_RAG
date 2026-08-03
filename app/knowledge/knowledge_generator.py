import json
from pathlib import Path


class KnowledgeGenerator:

    def __init__(self):

        self.records = [

            {
                "category": "Replication",
                "issue": "Vendor replication failed after DRF execution.",
                "root_cause": "RFC destination unavailable.",
                "resolution": "Verify RFC destination and restart DRF replication.",
                "sap_transactions": ["SM59", "DRFOUT", "SMQ1"],
                "priority": "High",
                "keywords": [
                    "Vendor",
                    "Replication",
                    "DRF",
                    "RFC"
                ]
            },

            {
                "category": "Workflow",
                "issue": "Workflow approval stuck.",
                "root_cause": "Approval agent missing.",
                "resolution": "Assign workflow agent and restart workflow.",
                "sap_transactions": ["SWIA", "SWDD"],
                "priority": "Medium",
                "keywords": [
                    "Workflow",
                    "Approval",
                    "Agent"
                ]
            },

            {
                "category": "Validation",
                "issue": "Business Partner validation failed.",
                "root_cause": "Mandatory field missing.",
                "resolution": "Fill mandatory fields and reprocess the request.",
                "sap_transactions": ["USMD_CREQUEST"],
                "priority": "Medium",
                "keywords": [
                    "Validation",
                    "Business Partner"
                ]
            }

        ]

    def save(self):

        Path("data/knowledge").mkdir(
            parents=True,
            exist_ok=True
        )

        output = Path(
            "data/knowledge/sap_mdg_knowledge.json"
        )

        with open(output, "w", encoding="utf-8") as file:

            json.dump(
                self.records,
                file,
                indent=4
            )

        print(f"Knowledge base saved to {output}")