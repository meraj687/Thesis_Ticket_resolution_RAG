"""
SAP MDG Intelligent Support Assistant
Streamlit Dashboard
"""

import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/analyze-ticket"

st.set_page_config(
    page_title="SAP MDG Intelligent Support Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 SAP MDG Intelligent Support Assistant")

st.markdown(
    "### AI-powered SAP MDG Support Ticket Classification and Resolution Recommendation"
)

ticket = st.text_area(
    "Enter SAP Support Ticket",
    height=120,
    placeholder="Example: Vendor replication failed because RFC timeout"
)

if st.button("🚀 Analyze Ticket", use_container_width=True):

    if ticket.strip() == "":
        st.warning("Please enter a support ticket.")
        st.stop()

    with st.spinner("Analyzing Ticket..."):

        response = requests.post(
            API_URL,
            json={
                "ticket": ticket
            }
        )

    if response.status_code != 200:

        st.error("Unable to connect to FastAPI.")
        st.stop()

    result = response.json()

    recommendation = result["recommendation"]

    similar = result["similar_incidents"]

    st.success("Analysis Completed Successfully")

    st.divider()

    # =====================================================
    # KPI CARDS
    # =====================================================

    first = similar[0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Business Object",
        first["business_object"]
    )

    col2.metric(
        "Category",
        first["category"]
    )

    col3.metric(
        "Department",
        first["department"]
    )

    col4.metric(
        "Resolver",
        first["resolver_role"]
    )

    st.divider()

    # =====================================================
    # MAIN CONTENT
    # =====================================================

    left, right = st.columns(2)

    with left:

        st.subheader("📋 Issue Summary")

        st.info(
            recommendation.get(
                "issue_summary",
                ""
            )
        )

        st.subheader("⚠ Root Cause")

        root_causes = recommendation.get(
            "root_cause",
            []
        )

        if isinstance(root_causes, list):

            for cause in root_causes:

                st.write("•", cause)

        else:

            st.write(root_causes)

        st.subheader("🏢 Responsible Department")

        st.success(
            recommendation.get(
                "responsible_department",
                ""
            )
        )

        st.subheader("👨‍💼 Resolver Role")

        st.success(
            recommendation.get(
                "resolver_role",
                ""
            )
        )

        st.subheader("💼 Business Impact")

        st.warning(
            recommendation.get(
                "business_impact",
                ""
            )
        )

    with right:

        st.subheader("🔧 Diagnostic Steps")

        steps = recommendation.get(
            "diagnostic_steps",
            []
        )

        if isinstance(steps, list):

            for step in steps:

                st.checkbox(
                    step,
                    value=True,
                    disabled=True
                )

        else:

            st.write(steps)

        st.subheader("✅ Recommended Resolution")

        resolutions = recommendation.get(
            "recommended_resolution",
            []
        )

        if isinstance(resolutions, list):

            for item in resolutions:

                st.success(item)

        else:

            st.success(resolutions)

        st.subheader("📈 Confidence Score")

        confidence = recommendation.get(
            "confidence",
            "0%"
        )

        try:

            value = int(
                confidence.replace(
                    "%",
                    ""
                )
            )

        except:

            value = 0

        st.progress(value / 100)

        st.write(f"### {confidence}")

    st.divider()

    # =====================================================
    # SIMILAR INCIDENTS
    # =====================================================

    st.subheader("📚 Similar SAP Incidents")

    for i, incident in enumerate(similar, start=1):

        with st.expander(
            f"{i}. {incident['issue']}"
        ):

            c1, c2 = st.columns(2)

            with c1:

                st.write(
                    "**Business Object:**",
                    incident["business_object"]
                )

                st.write(
                    "**Module:**",
                    incident["module"]
                )

                st.write(
                    "**Category:**",
                    incident["category"]
                )

            with c2:

                st.write(
                    "**Department:**",
                    incident["department"]
                )

                st.write(
                    "**Resolver:**",
                    incident["resolver_role"]
                )

                st.write(
                    "**Distance:**",
                    incident["distance"]
                )

    st.divider()

    # =====================================================
    # RAW JSON (Optional)
    # =====================================================

    with st.expander("🔍 View Complete JSON Response"):

        st.json(result)