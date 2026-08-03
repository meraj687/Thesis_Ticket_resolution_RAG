"""
Knowledge Templates
"""

REPLICATION_ISSUES = {

    "Vendor": [

        "Vendor replication failed after DRF execution.",

        "Vendor synchronization failed due to RFC timeout.",

        "Vendor master data not replicated to ECC.",

        "Vendor replication queue blocked."

    ],

    "Material": [

        "Material replication failed.",

        "Material master synchronization failed.",

        "Material replication stopped unexpectedly."

    ],

    "Customer": [

        "Customer replication failed.",

        "Customer synchronization unsuccessful."

    ],

    "Business Partner": [

        "Business Partner replication failed.",

        "Business Partner synchronization timeout."

    ]
}

ROOT_CAUSES = [

    "RFC destination unavailable.",

    "Outbound queue blocked.",

    "SOA service unavailable.",

    "Incorrect DRF configuration."

]

DIAGNOSTIC_STEPS = [

    "Check SM59 connection.",

    "Review SMQ1 queue.",

    "Check DRFOUT configuration.",

    "Review SLG1 application logs."

]

RESOLUTIONS = [

    "Restart DRF replication.",

    "Clear outbound queue.",

    "Correct RFC destination.",

    "Retry synchronization."

]