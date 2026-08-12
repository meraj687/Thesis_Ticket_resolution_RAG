"""
Automated Evaluation Script
SAP MDG Intelligent Support Assistant

Purpose
-------
Evaluates the existing FastAPI recommendation system
using the 10-case pilot evaluation dataset.

The application itself is NOT modified.
This script only sends test tickets to the API
and records the returned results.

Output
------
evaluation/results/pilot_evaluation_results.csv
"""

import csv
import os
import time

import requests


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000/analyze-ticket"

OUTPUT_DIR = os.path.join(
    "evaluation",
    "results"
)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "pilot_evaluation_results.csv"
)

REQUEST_TIMEOUT = 180


# ============================================================
# PILOT EVALUATION DATASET
# ============================================================

TEST_CASES = [

    # --------------------------------------------------------
    # SAP MDG RELEVANT CASES
    # --------------------------------------------------------

    {
        "id": "A01",
        "group": "SAP MDG",
        "ticket": (
            "Material master replication failed "
            "after DRF execution."
        )
    },

    {
        "id": "A02",
        "group": "SAP MDG",
        "ticket": (
            "Vendor replication failed because "
            "the RFC destination is unavailable."
        )
    },

    {
        "id": "A03",
        "group": "SAP MDG",
        "ticket": (
            "MDG outbound messages are stuck "
            "in the SMQ1 queue."
        )
    },

    {
        "id": "A04",
        "group": "SAP MDG",
        "ticket": (
            "Business Partner synchronization "
            "failed after DRF execution."
        )
    },

    {
        "id": "A05",
        "group": "SAP MDG",
        "ticket": (
            "Material replication stopped unexpectedly "
            "after outbound processing."
        )
    },

    {
        "id": "A06",
        "group": "SAP MDG",
        "ticket": (
            "Vendor synchronization failed because "
            "the RFC connection timed out."
        )
    },

    {
        "id": "A07",
        "group": "SAP MDG",
        "ticket": (
            "MDG replication failed and errors "
            "are visible in SLG1."
        )
    },

    # --------------------------------------------------------
    # NON-SAP / UNRELATED CASES
    # --------------------------------------------------------

    {
        "id": "C01",
        "group": "Non-SAP",
        "ticket": (
            "What is an LLM model?"
        )
    },

    {
        "id": "C02",
        "group": "Non-SAP",
        "ticket": (
            "The office printer is not working."
        )
    },

    {
        "id": "C03",
        "group": "Non-SAP",
        "ticket": (
            "I need help booking a flight to Berlin."
        )
    }
]


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# RESULT STORAGE
# ============================================================

results = []


# ============================================================
# START EVALUATION
# ============================================================

print("=" * 80)
print("SAP MDG INTELLIGENT SUPPORT ASSISTANT")
print("AUTOMATED PILOT EVALUATION")
print("=" * 80)

print()

print(
    f"Total test cases: {len(TEST_CASES)}"
)

print(
    f"API endpoint: {API_URL}"
)

print()


# ============================================================
# RUN EACH TEST CASE
# ============================================================

for index, test in enumerate(
    TEST_CASES,
    start=1
):

    test_id = test["id"]

    group = test["group"]

    ticket = test["ticket"]

    print("-" * 80)

    print(
        f"[{index}/{len(TEST_CASES)}] "
        f"{test_id} | {group}"
    )

    print(
        f"Ticket: {ticket}"
    )

    start_time = time.time()

    try:

        # ----------------------------------------------------
        # API REQUEST
        # ----------------------------------------------------

        response = requests.post(

            API_URL,

            json={
                "ticket": ticket
            },

            timeout=REQUEST_TIMEOUT
        )

        elapsed = round(
            time.time() - start_time,
            3
        )

        response.raise_for_status()

        data = response.json()

        # ----------------------------------------------------
        # BASIC RESPONSE INFORMATION
        # ----------------------------------------------------

        status = data.get(
            "status",
            ""
        )

        response_time = data.get(
            "response_time",
            elapsed
        )

        retrieved_records = data.get(
            "retrieved_records",
            0
        )

        # ----------------------------------------------------
        # RECOMMENDATION
        # ----------------------------------------------------

        recommendation = data.get(
            "recommendation",
            {}
        )

        if not isinstance(
            recommendation,
            dict
        ):
            recommendation = {}

        confidence = recommendation.get(
            "confidence",
            data.get(
                "similarity_score",
                0
            )
        )

        confidence_level = recommendation.get(
            "confidence_level",
            ""
        )

        # ----------------------------------------------------
        # SIMILAR INCIDENTS
        # ----------------------------------------------------

        similar_incidents = data.get(
            "similar_incidents",
            []
        )

        if not isinstance(
            similar_incidents,
            list
        ):
            similar_incidents = []

        # ----------------------------------------------------
        # TOP SIMILARITY
        #
        # Accepted tickets:
        #     similarity comes from similar_incidents[0]
        #
        # Rejected tickets:
        #     similar_incidents is empty
        #     so use data["similarity_score"]
        # ----------------------------------------------------

        top_similarity = data.get(
            "similarity_score",
            ""
        )

        top_issue = ""

        top_module = ""

        top_category = ""

        top_business_object = ""

        top_department = ""

        top_resolver = ""

        if similar_incidents:

            top_incident = similar_incidents[0]

            if isinstance(
                top_incident,
                dict
            ):

                top_similarity = top_incident.get(
                    "similarity",
                    top_similarity
                )

                top_issue = top_incident.get(
                    "issue",
                    ""
                )

                top_module = top_incident.get(
                    "module",
                    ""
                )

                top_category = top_incident.get(
                    "category",
                    ""
                )

                top_business_object = top_incident.get(
                    "business_object",
                    ""
                )

                top_department = top_incident.get(
                    "department",
                    ""
                )

                top_resolver = top_incident.get(
                    "resolver_role",
                    ""
                )

        # ----------------------------------------------------
        # REJECTION INFORMATION
        # ----------------------------------------------------

        rejection_reason = data.get(
            "rejection_reason",
            ""
        )

        rejection_message = data.get(
            "rejection_message",
            ""
        )

        # ----------------------------------------------------
        # RECOMMENDATION CONTENT
        # ----------------------------------------------------

        issue_summary = recommendation.get(
            "issue_summary",
            ""
        )

        root_cause = recommendation.get(
            "root_cause",
            []
        )

        diagnostic_steps = recommendation.get(
            "diagnostic_steps",
            []
        )

        recommended_resolution = recommendation.get(
            "recommended_resolution",
            []
        )

        # ----------------------------------------------------
        # NORMALIZE LISTS FOR CSV
        # ----------------------------------------------------

        if isinstance(
            root_cause,
            list
        ):

            root_cause = " | ".join(
                str(item)
                for item in root_cause
            )

        else:

            root_cause = str(
                root_cause
            )

        if isinstance(
            diagnostic_steps,
            list
        ):

            diagnostic_steps = " | ".join(
                str(item)
                for item in diagnostic_steps
            )

        else:

            diagnostic_steps = str(
                diagnostic_steps
            )

        if isinstance(
            recommended_resolution,
            list
        ):

            recommended_resolution = " | ".join(
                str(item)
                for item in recommended_resolution
            )

        else:

            recommended_resolution = str(
                recommended_resolution
            )

        # ----------------------------------------------------
        # EXPECTED BEHAVIOR
        # ----------------------------------------------------

        if group == "Non-SAP":

            expected_behavior = "Rejected"

            if status == "rejected":

                actual_behavior = "Rejected"

                evaluation_result = "PASS"

            else:

                actual_behavior = "Accepted"

                evaluation_result = "FAIL"

        else:

            expected_behavior = "Accepted"

            if status == "rejected":

                actual_behavior = "Rejected"

                evaluation_result = "FAIL"

            else:

                actual_behavior = "Accepted"

                evaluation_result = "PASS"

        # ----------------------------------------------------
        # STORE RESULT
        # ----------------------------------------------------

        results.append({

            "test_id": test_id,

            "group": group,

            "ticket": ticket,

            "expected_behavior": expected_behavior,

            "actual_behavior": actual_behavior,

            "evaluation_result": evaluation_result,

            "status": status,

            "confidence": confidence,

            "confidence_level": confidence_level,

            "retrieved_records": retrieved_records,

            "top_similarity": top_similarity,

            "top_issue": top_issue,

            "top_business_object": top_business_object,

            "top_module": top_module,

            "top_category": top_category,

            "top_department": top_department,

            "top_resolver": top_resolver,

            "response_time": response_time,

            "issue_summary": issue_summary,

            "root_cause": root_cause,

            "diagnostic_steps": diagnostic_steps,

            "recommended_resolution": recommended_resolution,

            "rejection_reason": rejection_reason,

            "rejection_message": rejection_message

        })

        # ----------------------------------------------------
        # TERMINAL OUTPUT
        # ----------------------------------------------------

        print(
            f"Status: {status}"
        )

        print(
            f"Confidence: {confidence}%"
        )

        print(
            f"Top similarity: {top_similarity}%"
        )

        print(
            f"Retrieved records: {retrieved_records}"
        )

        print(
            f"Response time: {response_time}s"
        )

        print(
            f"Evaluation: {evaluation_result}"
        )

    # ========================================================
    # API / CONNECTION ERROR
    # ========================================================

    except requests.exceptions.RequestException as error:

        elapsed = round(
            time.time() - start_time,
            3
        )

        print(
            f"ERROR: {error}"
        )

        results.append({

            "test_id": test_id,

            "group": group,

            "ticket": ticket,

            "expected_behavior": (
                "Rejected"
                if group == "Non-SAP"
                else "Accepted"
            ),

            "actual_behavior": "ERROR",

            "evaluation_result": "ERROR",

            "status": "ERROR",

            "confidence": "",

            "confidence_level": "",

            "retrieved_records": "",

            "top_similarity": "",

            "top_issue": "",

            "top_business_object": "",

            "top_module": "",

            "top_category": "",

            "top_department": "",

            "top_resolver": "",

            "response_time": elapsed,

            "issue_summary": "",

            "root_cause": "",

            "diagnostic_steps": "",

            "recommended_resolution": "",

            "rejection_reason": "",

            "rejection_message": ""

        })


# ============================================================
# CSV COLUMNS
# ============================================================

fieldnames = [

    "test_id",

    "group",

    "ticket",

    "expected_behavior",

    "actual_behavior",

    "evaluation_result",

    "status",

    "confidence",

    "confidence_level",

    "retrieved_records",

    "top_similarity",

    "top_issue",

    "top_business_object",

    "top_module",

    "top_category",

    "top_department",

    "top_resolver",

    "response_time",

    "issue_summary",

    "root_cause",

    "diagnostic_steps",

    "recommended_resolution",

    "rejection_reason",

    "rejection_message"

]


# ============================================================
# SAVE RESULTS
# ============================================================

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as csv_file:

    writer = csv.DictWriter(
        csv_file,
        fieldnames=fieldnames
    )

    writer.writeheader()

    writer.writerows(
        results
    )


# ============================================================
# CALCULATE BASIC SUMMARY
# ============================================================

total = len(results)

passed = sum(
    1
    for item in results
    if item["evaluation_result"] == "PASS"
)

failed = sum(
    1
    for item in results
    if item["evaluation_result"] == "FAIL"
)

errors = sum(
    1
    for item in results
    if item["evaluation_result"] == "ERROR"
)


# ============================================================
# ACCEPTED / REJECTED COUNTS
# ============================================================

accepted_results = [
    item
    for item in results
    if item["group"] == "SAP MDG"
    and item["evaluation_result"] != "ERROR"
]

rejected_results = [
    item
    for item in results
    if item["group"] == "Non-SAP"
    and item["evaluation_result"] != "ERROR"
]


# ============================================================
# ACCEPTANCE RATE
# ============================================================

if accepted_results:

    accepted_correct = sum(
        1
        for item in accepted_results
        if item["actual_behavior"] == "Accepted"
    )

    acceptance_rate = (
        accepted_correct
        / len(accepted_results)
    ) * 100

else:

    acceptance_rate = 0


# ============================================================
# REJECTION ACCURACY
# ============================================================

if rejected_results:

    rejected_correct = sum(
        1
        for item in rejected_results
        if item["actual_behavior"] == "Rejected"
    )

    rejection_accuracy = (
        rejected_correct
        / len(rejected_results)
    ) * 100

else:

    rejection_accuracy = 0


# ============================================================
# AVERAGE CONFIDENCE
# ============================================================

confidence_values = []

for item in accepted_results:

    try:

        value = float(
            item["confidence"]
        )

        confidence_values.append(
            value
        )

    except (
        TypeError,
        ValueError
    ):

        pass


if confidence_values:

    average_confidence = (
        sum(confidence_values)
        / len(confidence_values)
    )

else:

    average_confidence = 0


# ============================================================
# AVERAGE RESPONSE TIME
# ============================================================

response_times = []

for item in results:

    try:

        value = float(
            item["response_time"]
        )

        response_times.append(
            value
        )

    except (
        TypeError,
        ValueError
    ):

        pass


if response_times:

    average_response_time = (
        sum(response_times)
        / len(response_times)
    )

else:

    average_response_time = 0


# ============================================================
# MIN / MAX RESPONSE TIME
# ============================================================

if response_times:

    minimum_response_time = min(
        response_times
    )

    maximum_response_time = max(
        response_times
    )

else:

    minimum_response_time = 0

    maximum_response_time = 0


# ============================================================
# FINAL TERMINAL SUMMARY
# ============================================================

print()

print("=" * 80)

print(
    "AUTOMATED PILOT EVALUATION SUMMARY"
)

print("=" * 80)

print(
    f"Total cases              : {total}"
)

print(
    f"Passed                   : {passed}"
)

print(
    f"Failed                   : {failed}"
)

print(
    f"Errors                   : {errors}"
)

print(
    f"Overall pass rate        : "
    f"{(passed / total * 100) if total else 0:.2f}%"
)

print()

print(
    f"SAP MDG accepted cases   : "
    f"{len(accepted_results)}"
)

print(
    f"SAP MDG acceptance rate  : "
    f"{acceptance_rate:.2f}%"
)

print()

print(
    f"Non-SAP rejected cases   : "
    f"{len(rejected_results)}"
)

print(
    f"Rejection accuracy      : "
    f"{rejection_accuracy:.2f}%"
)

print()

print(
    f"Average confidence      : "
    f"{average_confidence:.2f}%"
)

print(
    f"Average response time   : "
    f"{average_response_time:.3f}s"
)

print(
    f"Minimum response time   : "
    f"{minimum_response_time:.3f}s"
)

print(
    f"Maximum response time   : "
    f"{maximum_response_time:.3f}s"
)

print()

print(
    "Results saved to:"
)

print(
    OUTPUT_FILE
)

print("=" * 80)