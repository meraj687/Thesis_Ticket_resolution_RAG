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

# st.title("🤖 SAP MDG Intelligent Support Assistant")

# st.markdown(
#     "### AI-powered SAP MDG Support Ticket Classification and Resolution Recommendation"
# )
st.title("🤖 SAP MDG Intelligent Support Assistant")

st.caption(
    "AI-powered SAP Support Ticket Classification and Resolution Recommendation using Retrieval-Augmented Generation (RAG)"
)

st.markdown(
    """
**Technology Stack**

FastAPI • FAISS • Sentence Transformers • Llama 3.2 • Streamlit
"""
)

st.divider()

ticket = st.text_area(
    "Enter SAP Support Ticket",
    height=120,
    placeholder="Example: Vendor replication failed because RFC timeout"
)

if st.button("🚀 Analyze Ticket", use_container_width=True):

    if ticket.strip() == "":
        st.warning("Please enter a support ticket.")
        st.stop()

    with st.spinner(
    "Retrieving similar SAP incidents and generating AI recommendation..."
    ):

        try:

            response = requests.post(
                API_URL,
                json={
                    "ticket": ticket
                },
                timeout=120
            )

            response.raise_for_status()

        except requests.RequestException as e:

            st.error(f"API Error: {e}")

            st.stop()

    result = response.json()

    recommendation = result["recommendation"]

    similar = result.get("similar_incidents", [])

    if not similar:
        st.error("No similar incidents found.")
        st.stop()

    # st.success("Analysis Completed Successfully")
    
    st.subheader("⚙ AI Processing Workflow")

    workflow = [
        "Ticket Received",
        "Embedding Generated",
        "Semantic Search (FAISS)",
        "Top Similar Incidents Retrieved",
        "Llama 3.2 Analysis",
        "Recommendation Generated"
    ]

    for step in workflow:
        st.success(f"✔ {step}")

    st.divider()

    st.divider()

    # =====================================================
    # KPI CARDS
    # =====================================================

    first = similar[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.info(f"**Business Object**\n\n{first['business_object']}")

    with col2:
        st.info(f"**Module**\n\n{first['module']}")

    with col3:
        st.info(f"**Category**\n\n{first['category']}")

    with col4:
        st.info(f"**Department**\n\n{first['department']}")

    # col1.metric(
    #     "Business Object",
    #     first["business_object"]
    # )

    # col2.metric(
    #     "Category",
    #     first["category"]
    # )

    # col3.metric(
    #     "Department",
    #     first["department"]
    # )

    # col4.metric(
    #     "Resolver",
    #     first["resolver_role"]
    # )

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

                # st.write("•", cause)
                st.warning(cause)

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
        st.subheader("🧠 AI Reasoning")

        st.info(recommendation.get("reasoning",""))

        st.error(
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

                # st.checkbox(
                #     step,
                #     value=True,
                #     disabled=True
                # )
                # st.markdown(f"✅ {step}")
                st.info(f"Step {steps.index(step)+1}")

                st.success(step)

        else:

            st.write(steps)

        st.subheader("✅ Recommended Resolution")

        resolutions = recommendation.get(
            "recommended_resolution",
            []
        )

        if isinstance(resolutions, list):

            # for item in resolutions:

            #     st.success(item)
            for i, item in enumerate(resolutions, start=1):

                st.success(f"Resolution {i}\n\n{item}"
    )

        else:

            st.success(resolutions)

        # st.subheader("📈 Confidence Score")

        # confidence = recommendation.get(
        #     "confidence",
        #     "0%"
        # )
        # confidence_level = recommendation.get("confidence_level", "Unknown")

        # try:

        #     value = int(
        #         confidence.replace(
        #             "%",
        #             ""
        #         )
        #     )

        # except:

        #     value = 0

        # st.progress(value / 100)

        # st.write(f"### {confidence}")

    # =====================================================
    # AI Match Score
    # =====================================================

    st.subheader("📈 AI Match Score")

    confidence = recommendation.get("confidence", 0)
    confidence_level = recommendation.get(
        "confidence_level",
        "Unknown"
    )

    # Support both int and string confidence values
    if isinstance(confidence, str):

        confidence = confidence.replace("%", "").strip()

        try:
            confidence = int(confidence)
        except ValueError:
            confidence = 0

    st.progress(confidence / 100)

    metric1, metric2 = st.columns(2)

    with metric1:

        st.metric(
            "Score",
            f"{confidence}%"
        )

    with metric2:

        st.metric(
            "Level",
            confidence_level
        )

    st.divider()

    # =====================================================
    # Processing Summary
    # =====================================================

    st.subheader("📊 Processing Summary")

    c1, c2, c3, c4, c5 = st.columns(4)

    with c1:
        st.metric(
            "Retrieved Records",
            result["retrieved_records"]
        )

    with c2:
        st.metric(
            "Embedding Model",
            "MiniLM-L6-v2"
        )

    with c3:
        st.metric(
            "Vector Database",
            "FAISS"
        )

    with c4:
        st.metric(
            "LLM",
            "Llama 3.2"
        )

    with c5:
        st.metric(
            "Response Time",
            f"{result['response_time']} sec"
        )

    st.divider()

    # =====================================================
    # SIMILAR INCIDENTS
    # =====================================================

    st.subheader("📚 Similar SAP Incidents")

    for i, incident in enumerate(similar, start=1):

        with st.expander(
            f"📄 Similar SAP Incident #{i}"
        ):
            # Show the issue at the top
            st.write("### Issue")
            st.info(incident["issue"])

            st.info(incident["issue"])

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

                # st.write("**Distance:**")
                # similarity = incident.get("similarity", 0)

                # st.metric(
                #     "AI Match Score",
                #     f"{similarity:.2f}%"
                # )
                # st.progress(similarity / 100)
                similarity = incident.get("similarity", 0)

                st.metric(
                    "Semantic Match",
                    f"{similarity:.2f}%"
                )

                st.progress(
                    similarity / 100
                )

    st.divider()

    # =====================================================
    # RAW JSON (Optional)
    # =====================================================

    # with st.expander("🔍 View Complete JSON Response"):

    #     st.json(result)
    st.divider()

    st.caption("Developed for MSc Artificial Intelligence Thesis | SAP MDG Intelligent Support Assistant")