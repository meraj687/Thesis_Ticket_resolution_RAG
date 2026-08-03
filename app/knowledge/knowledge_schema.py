from dataclasses import dataclass
from typing import List


@dataclass
class KnowledgeRecord:

    id: int

    module: str

    business_object: str

    category: str

    priority: str

    issue: str

    possible_root_causes: List[str]

    diagnostic_steps: List[str]

    recommended_resolution: List[str]

    sap_transactions: List[str]

    responsible_department: str

    support_team: str

    resolver_role: str

    complexity: str

    business_impact: str

    sla: str

    keywords: List[str]

    references: List[str]