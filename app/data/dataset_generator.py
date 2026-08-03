import random
import pandas as pd
from pathlib import Path


class SAPMDGDatasetGenerator:

    def __init__(self):

        self.categories = {

            "Data Quality": [
                ("Business partner duplicate record found",
                 "Merge duplicate business partners"),

                ("Duplicate supplier record created",
                 "Run duplicate check process"),

                ("Duplicate customer detected",
                 "Merge duplicate customer records"),

                ("Incomplete business partner data",
                 "Update mandatory attributes")
            ],

            "Replication": [
                ("Vendor replication failed",
                 "Verify SOA services"),

                ("Material master not replicated to ECC",
                 "Check DRF configuration"),

                ("Customer replication failed",
                 "Restart replication service"),

                ("Replication queue blocked",
                 "Clear outbound queue")
            ],

            "Workflow": [
                ("Workflow approval stuck",
                 "Restart workflow"),

                ("Change request activation failed",
                 "Activate change request manually"),

                ("Approval agent not assigned",
                 "Update workflow configuration"),

                ("Workflow timeout occurred",
                 "Review workflow logs")
            ],

            "Validation": [
                ("Customer validation failed",
                 "Review BRF+ rules"),

                ("Material type validation error",
                 "Correct validation rule"),

                ("Mandatory field missing",
                 "Provide mandatory values"),

                ("Invalid business rule detected",
                 "Review validation logic")
            ],

            "Search": [
                ("Business partner search returns no results",
                 "Rebuild search index"),

                ("Search performance is slow",
                 "Optimize HANA indexes"),

                ("Search index corrupted",
                 "Recreate search index"),

                ("Search returns incorrect results",
                 "Synchronize search index")
            ]
        }

        self.priorities = [
            "Low",
            "Medium",
            "High",
            "Critical"
        ]

    def generate(self, records=1000):

        data = []

        ticket_id = 1

        for _ in range(records):

            category = random.choice(list(self.categories.keys()))

            description, resolution = random.choice(
                self.categories[category]
            )

            priority = random.choice(self.priorities)

            data.append({

                "ticket_id": ticket_id,
                "description": description,
                "category": category,
                "priority": priority,
                "resolution": resolution

            })

            ticket_id += 1

        return pd.DataFrame(data)

    def save(self, dataframe):

        output = Path("data/raw/mdg_tickets.csv")

        dataframe.to_csv(output, index=False)

        print(f"Dataset saved to {output}")