"""
SAP MDG Domain Constants
"""

BUSINESS_OBJECTS = {

    "Vendor": {
        "module": "MDG-S",
        "business_process": "Procurement",
        "department": "SAP Master Data Integration",
        "support_team": "MDG Integration Support",
        "resolver_role": "SAP MDG Technical Consultant"
    },

    "Supplier": {
        "module": "MDG-S",
        "business_process": "Procurement",
        "department": "SAP Master Data Integration",
        "support_team": "MDG Integration Support",
        "resolver_role": "SAP MDG Technical Consultant"
    },

    "Customer": {
        "module": "MDG-C",
        "business_process": "Sales",
        "department": "SAP Customer Master Team",
        "support_team": "Customer Master Support",
        "resolver_role": "SAP Functional Consultant"
    },

    "Business Partner": {
        "module": "MDG-BP",
        "business_process": "Master Data Governance",
        "department": "SAP MDG Functional Team",
        "support_team": "Business Partner Support",
        "resolver_role": "SAP MDG Functional Consultant"
    },

    "Material": {
        "module": "MDG-MM",
        "business_process": "Manufacturing",
        "department": "SAP Material Master Team",
        "support_team": "Material Master Support",
        "resolver_role": "SAP Material Master Consultant"
    }
}


CATEGORY_OWNER = {

    "Replication": {

        "department":"SAP Master Data Integration",

        "resolver":"SAP MDG Technical Consultant"

    },

    "Workflow": {

        "department":"SAP Workflow Team",

        "resolver":"SAP Workflow Consultant"

    }

}