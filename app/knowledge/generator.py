"""
Enterprise Knowledge Generator
"""

import random

from app.models.knowledge_record import KnowledgeRecord
from app.knowledge.constants import BUSINESS_OBJECTS
from app.knowledge.templates import (
    REPLICATION_ISSUES,
    ROOT_CAUSES,
    DIAGNOSTIC_STEPS,
    RESOLUTIONS,
)

from app.knowledge.templates.workflow import (
    WORKFLOW_ISSUES,
    WORKFLOW_ROOT_CAUSES,
    WORKFLOW_DIAGNOSTICS,
    WORKFLOW_RESOLUTIONS,
    WORKFLOW_TRANSACTIONS,
)


class KnowledgeGenerator:

    def __init__(self):
        self.business_objects = BUSINESS_OBJECTS

    # --------------------------------------------------
    # Replication Record
    # --------------------------------------------------
    def create_replication_record(self, record_id, business_object):

        info = self.business_objects[business_object]

        issue = random.choice(REPLICATION_ISSUES[business_object])

        priority = random.choices(
            ["Low", "Medium", "High", "Critical"],
            weights=[10, 40, 35, 15]
        )[0]

        escalation = {
            "Low": "L1",
            "Medium": "L1",
            "High": "L2",
            "Critical": "L3"
        }[priority]

        resolution_time = {
            "Low": "2 Hours",
            "Medium": "8 Hours",
            "High": "24 Hours",
            "Critical": "48 Hours"
        }[priority]

        return KnowledgeRecord(
            id=record_id,
            module=info["module"],
            business_object=business_object,
            category="Replication",
            priority=priority,
            issue=issue,
            possible_root_causes=random.sample(ROOT_CAUSES, 2),
            diagnostic_steps=random.sample(DIAGNOSTIC_STEPS, 3),
            recommended_resolution=random.sample(RESOLUTIONS, 3),
            sap_transactions=["SM59", "SMQ1", "DRFOUT", "SLG1"],
            responsible_department=info["department"],
            support_team=info["support_team"],
            resolver_role=info["resolver_role"],
            complexity=priority,
            business_process=info["business_process"],
            affected_system=random.choice([
                "SAP ECC",
                "SAP S/4HANA",
                "SAP MDG Hub"
            ]),
            business_impact=f"{business_object} synchronization interrupted.",
            estimated_resolution_time=resolution_time,
            sla=resolution_time,
            escalation_level=escalation,
            change_required=random.choice([True, False]),
            keywords=[
                business_object,
                "Replication",
                "DRF",
                "RFC"
            ],
            references=["SAP Note Placeholder"]
        )

    # --------------------------------------------------
    # Workflow Record
    # --------------------------------------------------
    def create_workflow_record(self, record_id):

        priority = random.choice(
            ["Medium", "High", "Critical"]
        )

        escalation = {
            "Medium": "L1",
            "High": "L2",
            "Critical": "L3"
        }[priority]

        resolution_time = {
            "Medium": "8 Hours",
            "High": "24 Hours",
            "Critical": "48 Hours"
        }[priority]

        return KnowledgeRecord(
            id=record_id,
            module="MDG-BP",
            business_object="Business Partner",
            category="Workflow",
            priority=priority,
            issue=random.choice(WORKFLOW_ISSUES),
            possible_root_causes=random.sample(
                WORKFLOW_ROOT_CAUSES, 2
            ),
            diagnostic_steps=random.sample(
                WORKFLOW_DIAGNOSTICS, 3
            ),
            recommended_resolution=random.sample(
                WORKFLOW_RESOLUTIONS, 3
            ),
            sap_transactions=WORKFLOW_TRANSACTIONS,
            responsible_department="SAP Workflow Team",
            support_team="Workflow Support",
            resolver_role="SAP Workflow Consultant",
            complexity=priority,
            business_process="Master Data Governance",
            affected_system="SAP MDG Hub",
            business_impact="Approval workflow interrupted.",
            estimated_resolution_time=resolution_time,
            sla=resolution_time,
            escalation_level=escalation,
            change_required=False,
            keywords=[
                "Workflow",
                "Approval",
                "Business Partner"
            ],
            references=[
                "SAP Workflow Guide"
            ]
        )

    # --------------------------------------------------
    # Generate Records
    # --------------------------------------------------
    def generate(self, count=50):

        records = []

        objects = list(REPLICATION_ISSUES.keys())

        for i in range(1, count + 1):

            if random.random() < 0.5:

                obj = random.choice(objects)

                records.append(
                    self.create_replication_record(
                        i,
                        obj
                    )
                )

            else:

                records.append(
                    self.create_workflow_record(i)
                )

        return records