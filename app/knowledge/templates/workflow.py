"""
Workflow Knowledge Templates
"""

WORKFLOW_ISSUES = [

    "Workflow approval is stuck in pending status.",

    "Approval workflow failed after submission.",

    "Workflow agent determination failed.",

    "Workflow was not triggered after change request creation.",

    "Business Partner workflow remains in process.",

    "Workflow terminated unexpectedly during approval.",

    "Change request approval failed.",

    "Workflow inbox is empty for approvers."
]

WORKFLOW_ROOT_CAUSES = [

    "Workflow configuration missing.",

    "Agent determination failed.",

    "Business rule configuration incorrect.",

    "Workflow template inactive.",

    "Approval step configuration missing.",

    "Background job not running."
]

WORKFLOW_DIAGNOSTICS = [

    "Check SWIA workflow log.",

    "Verify SWDD workflow definition.",

    "Check PFTC workflow task.",

    "Review workflow container.",

    "Review application log using SLG1.",

    "Verify background jobs."
]

WORKFLOW_RESOLUTIONS = [

    "Restart workflow instance.",

    "Correct agent determination.",

    "Activate workflow template.",

    "Correct business rule configuration.",

    "Restart workflow background job.",

    "Re-submit change request."
]

WORKFLOW_TRANSACTIONS = [

    "SWIA",

    "SWDD",

    "PFTC",

    "SBWP",

    "SLG1"
]