"""
Knowledge Serializer
"""

import json
from dataclasses import asdict
from pathlib import Path

from app.models.knowledge_record import KnowledgeRecord


class KnowledgeSerializer:

    @staticmethod
    def save(records, output_file):

        Path(output_file).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        data = [
            asdict(record)
            for record in records
        ]

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

        print(f"{len(records)} records saved.")