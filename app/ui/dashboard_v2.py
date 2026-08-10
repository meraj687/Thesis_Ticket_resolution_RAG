"""
====================================================
SAP MDG Intelligent Support Assistant
Enterprise Dashboard V2
====================================================
"""

import json
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import requests
import streamlit as st

# from app.utils.report_generator import generate_pdf
import app.utils.report_generator as report_generator



# =====================================================
# CONFIGURATION
# =====================================================

API_URL = "http://127.0.0.1:8000/analyze-ticket"

st.set_page_config(
    page_title="SAP MDG Intelligent Support Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================


st.markdown("""
<style>

/* Main container */
.block-container{
    max-width:1400px;
    padding-top:1.2rem;
    padding-bottom:2rem;
}

/* Metric cards */
div[data-testid="metric-container"]{
    background:#FFFFFF;
    border:1px solid #E5E7EB;
    border-radius:14px;
    padding:18px;
    box-shadow:0 2px 8px rgba(0,0,0,.08);
}

/* Streamlit alerts */
div.stAlert{
    border-radius:12px;
}

/* Button */
.stButton>button{
    width:100%;
    height:52px;
    border-radius:12px;
    font-size:18px;
    font-weight:600;
}

/* Text Area */
textarea{
    font-size:16px;
}

/* Custom Card */

.card{
    background:#1E2D42;
    border:1px solid #2F4158;
    border-radius:15px;
    padding:20px;
    min-height:150px;
    width:100%;
    box-sizing:border-box;
    display:flex;
    flex-direction:column;
    justify-content:space-between;
    transition:.3s;
    cursor:pointer;
    margin-bottom:18px;
}

.card:hover{
    transform:translateY(-4px);
    box-shadow:0 10px 20px rgba(0,0,0,.25);
    border:1px solid #4EA1FF;
}

# .card:hover{
#      transform:translateY(-5px);

#     box-shadow:0 10px 20px rgba(0,0,0,.25);

#     border:1px solid #4EA1FF;
# }

.card-icon{

    font-size:30px;

}

.card-title{

    color:#55A3FF;

    font-size:18px;

    font-weight:700;

}

.card-value{

    color:white;

    font-size:30px;

    font-weight:700;

}



/* ==========================================
Recommendation Card
========================================== */

.rec-card{

    background:#1E2D42;

    border:1px solid #2F4158;

    border-radius:14px;

    padding:18px;

    margin-bottom:15px;

    transition:.3s;

}

.rec-card:hover{

    border:1px solid #4EA1FF;

    transform:translateY(-3px);

}

.rec-header{

    display:flex;

    align-items:center;

    gap:10px;

    font-size:20px;

    font-weight:700;

    color:#55A3FF;

    margin-bottom:10px;

}

.rec-body{

    color:white;

    font-size:17px;

    line-height:1.7;

}


</style>
""", unsafe_allow_html=True)

# =====================================================
# REUSABLE DASHBOARD CARD
# =====================================================

def dashboard_card(icon, title, value):

    st.markdown(f"""
<div class="card">

<div class="card-icon">
{icon}
</div>

<div class="card-title">
{title}
</div>

<div class="card-value">
{value}
</div>

</div>
""", unsafe_allow_html=True)

# =====================================================
# RECOMMENDATION CARD
# =====================================================

def recommendation_card(icon, title, body):

    st.markdown(f"""
<div class="rec-card">

<div class="rec-header">

<span>{icon}</span>

<span>{title}</span>

</div>

<div class="rec-body">

{body}

</div>

</div>
""", unsafe_allow_html=True)

# =====================================================
# SIMILAR INCIDENT CARD
# =====================================================

def similar_incident_card(incident, index):

    # similarity = incident.get("similarity", 0)

    similarity = float(
    incident.get("similarity", 0)
    )

    # Keep similarity between 0 and 100
    similarity = max(
        0,
        min(similarity, 100)
    )

    st.markdown(
        f"""
<div class="rec-card">

<div class="rec-header">

<span>📄</span>

<span>Similar Incident #{index}</span>

</div>

<div class="rec-body">

<b>Issue</b><br>
{incident.get("issue","")}<br><br>

<table style="width:100%;border-collapse:collapse;">

<tr>
<td><b>Business Object</b></td>
<td>{incident.get("business_object","")}</td>
</tr>

<tr>
<td><b>SAP Module</b></td>
<td>{incident.get("module","")}</td>
</tr>

<tr>
<td><b>Category</b></td>
<td>{incident.get("category","")}</td>
</tr>

<tr>
<td><b>Department</b></td>
<td>{incident.get("department","")}</td>
</tr>

<tr>
<td><b>Resolver</b></td>
<td>{incident.get("resolver_role","")}</td>
</tr>

<tr>
<td><b>Semantic Match</b></td>
<td>{similarity:.2f}%</td>
</tr>

</table>

</div>

</div>
""",
        unsafe_allow_html=True
    )

    similarity = max(0,min(similarity,100))

    st.progress(similarity / 100)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🤖 SAP MDG AI")

    st.markdown("---")

    st.subheader("System Status")

    st.success("🟢 FastAPI Connected")
    st.success("🟢 FAISS Loaded")
    st.success("🟢 Embedding Model Ready")
    st.success("🟢 Llama 3.2 Connected")

    st.markdown("---")

    st.subheader("Project")

    st.write("📘 SAP MDG Intelligent Support Assistant")
    st.write("🎓 MSc Artificial Intelligence")
    st.write("🏫 IU International University")
    st.write("👨‍💻 Mohammad Aryaan")

    st.markdown("---")

    st.caption("Version 2.0")

# =====================================================
# HEADER
# =====================================================

st.title("🤖 SAP MDG Intelligent Support Assistant")

st.markdown("""
### Enterprise AI Recommendation System

AI-powered SAP Support Ticket Classification and Resolution Recommendation using **Retrieval-Augmented Generation (RAG)**.
""")

st.divider()

# =====================================================
# USER INPUT
# =====================================================

ticket = st.text_area(
    "📩 Enter SAP Support Ticket",
    height=140,
    placeholder="Example: Vendor replication failed because RFC timeout..."
)

analyze = st.button(
    "🚀 Analyze Ticket",
    use_container_width=True
)

# =====================================================
# API CALL
# =====================================================

if analyze:

    if ticket.strip() == "":
        st.warning("Please enter a SAP support ticket.")
        st.stop()

    with st.spinner(
        "Analyzing SAP support ticket..."
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

            st.error(f"API Error : {e}")

            st.stop()

    result = response.json()

    recommendation = result.get(
        "recommendation",
        {}
    )

    # =====================================================
    # GENERATE PDF REPORT
    # =====================================================

    # pdf_file = generate_pdf(
    #     recommendation=recommendation,
    #     ticket=ticket,
    #     similar_incidents=similar,
    #     response_time=result["response_time"]
    # )

    similar = result.get(
        "similar_incidents",
        []
    )

    if len(similar) == 0:

        st.warning(
            "No similar incidents were found."
        )

        st.stop()

# =====================================================
# PREPARE ANALYTICS DATA
# =====================================================

    import pandas as pd

    analytics_df = pd.DataFrame(similar)

    if not analytics_df.empty:

        analytics_df["similarity"] = pd.to_numeric(
            analytics_df["similarity"],
            errors="coerce"
        ).fillna(0)

        analytics_df["similarity"] = (
            analytics_df["similarity"]
            .clip(0, 100)
        )

        analytics_df["chart_label"] = (
            analytics_df["issue"]
            .fillna("Unknown incident")
            .astype(str)
            .str.replace("\n", " ", regex=False)
            .str.slice(0, 50)
        )

    # =====================================================
    # GENERATE PDF REPORT
    # =====================================================

    # pdf_file = generate_pdf(
    #     recommendation=recommendation,
    #     ticket=ticket,
    #     similar_incidents=similar,
    #     response_time=result["response_time"]
    # )
    pdf_file = report_generator.generate_pdf(
        recommendation=recommendation,
        ticket=ticket,
        similar_incidents=similar,
        response_time=result["response_time"]
    )

    # =====================================================
    # AI PROCESSING WORKFLOW
    # =====================================================

    st.subheader("⚙ AI Processing Workflow")

    workflow_col1, workflow_col2, workflow_col3, workflow_col4, workflow_col5, workflow_col6 = st.columns(6)

    with workflow_col1:
        st.info("📩\n\n**Ticket**")

    with workflow_col2:
        st.info("🧠\n\n**Embedding**")

    with workflow_col3:
        st.info("🔎\n\n**FAISS Search**")

    with workflow_col4:
        st.info("📚\n\n**Top-3 Results**")

    with workflow_col5:
        st.info("🤖\n\n**Llama 3.2**")

    with workflow_col6:
        st.info("✅\n\n**Recommendation**")

    st.divider()

    # =====================================================
    # TICKET & AI ANALYSIS SUMMARY
    # =====================================================

    first = similar[0]

    st.subheader("📊 Ticket & AI Analysis Summary")

    left_summary, right_summary = st.columns(2)

    # -------------------------------------------------
    # LEFT SIDE
    # -------------------------------------------------

    with left_summary:

        st.markdown("### 📋 Ticket Information")

        st.write(f"**Business Object:** {first['business_object']}")
        st.write(f"**SAP Module:** {first['module']}")
        st.write(f"**Category:** {first['category']}")
        st.write(f"**Department:** {first['department']}")
        st.write(f"**Resolver:** {first['resolver_role']}")

    # -------------------------------------------------
    # RIGHT SIDE
    # -------------------------------------------------

    with right_summary:

        confidence = recommendation.get("confidence", 0)

        if isinstance(confidence, str):

            confidence = confidence.replace("%", "").strip()

            try:
                confidence = int(confidence)
            except ValueError:
                confidence = 0

        confidence = max(0, min(confidence, 100))

        st.markdown("### 🤖 AI Analysis")

        st.metric(
            "Confidence",
            f"{confidence}%"
        )

        st.progress(confidence / 100)

        st.write(
            "**Confidence Level:**",
            recommendation.get(
                "confidence_level",
                "Unknown"
            )
        )

        st.write(
            "**Retrieved Records:**",
            result["retrieved_records"]
        )

        st.write(
            "**Response Time:**",
            f"{result['response_time']} sec"
        )

        st.write(
            "**Similarity Method:**",
            "Hybrid Semantic Retrieval"
        )

    st.divider()

  
    # =====================================================
    # AI RECOMMENDATION
    # =====================================================

    st.subheader("🤖 AI Recommendation")

    left, right = st.columns(2)

    # -------------------------------------------------
    # LEFT PANEL
    # -------------------------------------------------

    with left:

        st.markdown("### 📋 Issue Summary")

        st.info(
            recommendation.get(
                "issue_summary",
                "No summary available."
            )
        )

        st.markdown("### ⚠ Root Cause")

        root_causes = recommendation.get(
            "root_cause",
            []
        )

        if isinstance(root_causes, list):

            for cause in root_causes:

                st.warning(cause)

        else:

            st.warning(root_causes)

    # -------------------------------------------------
    # RIGHT PANEL
    # -------------------------------------------------

    with right:

        st.markdown("### 🔧 Diagnostic Steps")

        steps = recommendation.get(
            "diagnostic_steps",
            []
        )

        if isinstance(steps, list):
            steps = [
                step.strip()
                for step in steps
                if str(step).strip()
            ]

        # st.write("Diagnostic steps:", steps)

        if isinstance(steps, list):
            for i, step in enumerate(steps, start=1):
                recommendation_card(
                    "🔧",
                    f"Step {i}",
                    step
                )

        else:
            recommendation_card(
                "🔧",
                "Diagnostic",
                steps
            )

        # =====================================================
        # RECOMMENDED RESOLUTION
        # =====================================================

        st.markdown("## ✅ Recommended Resolution")

        resolutions = recommendation.get(
            "recommended_resolution",
            []
        )

        if isinstance(resolutions, list):

            for i, item in enumerate(resolutions, start=1):

                recommendation_card(
                    "✅",
                    f"Resolution {i}",
                    item
                )

        else:

            recommendation_card(
                "✅",
                "Resolution",
                resolutions
            )

    st.divider()


    # =====================================================
    # AI REASONING
    # =====================================================

    reasoning = recommendation.get(
        "reasoning",
        ""
    )

    if reasoning:

        st.subheader("🧠 AI Reasoning")

        st.info(reasoning)

        st.divider()

    
    # =====================================================
    # PROCESSING SUMMARY
    # =====================================================

    st.subheader("📊 Processing Summary")

    # -----------------------------
    # ROW 1
    # -----------------------------

    row1 = st.columns(2)

    with row1[0]:

        dashboard_card(
            "📚",
            "Records",
            len(similar)
        )

    with row1[1]:

        dashboard_card(
            "🧠",
            "Embedding",
            "MiniLM-L6-v2"
        )


    # -----------------------------
    # ROW 2
    # -----------------------------

    row2 = st.columns(2)

    with row2[0]:

        dashboard_card(
            "🔎",
            "Vector DB",
            "FAISS"
        )

    with row2[1]:

        dashboard_card(
            "🤖",
            "LLM",
            "Llama 3.2"
        )


    # -----------------------------
    # ROW 3
    # -----------------------------

    row3 = st.columns(2)

    with row3[0]:

        dashboard_card(
            "⏱",
            "Response Time",
            f"{result['response_time']} sec"
        )

    st.divider()

    # =====================================================
    # KNOWLEDGE BASE ANALYTICS
    # =====================================================

    # =====================================================
    # RETRIEVAL ANALYTICS
    # =====================================================

    st.subheader("📊 Retrieval & AI Performance Analytics")

#     import pandas as pd

#     analytics_df = pd.DataFrame(similar)

# if not analytics_df.empty:

#     # -------------------------------------------------
#     # PREPARE DATA
#     # -------------------------------------------------

#     analytics_df["similarity"] = pd.to_numeric(
#         analytics_df["similarity"],
#         errors="coerce"
#     ).fillna(0)

#     analytics_df["similarity"] = (
#         analytics_df["similarity"]
#         .clip(0, 100)
#     )

#     # Short labels for chart readability
#     analytics_df["chart_label"] = [
#         f"Incident #{i}"
#         for i in range(1, len(analytics_df) + 1)
#     ]

    # -------------------------------------------------
    # SUMMARY METRICS
    # -------------------------------------------------

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:

        st.metric(
            "Top-1 Similarity",
            f"{analytics_df.iloc[0]['similarity']:.2f}%"
        )

    with metric2:

        st.metric(
            "Average Similarity",
            f"{analytics_df['similarity'].mean():.2f}%"
        )

    with metric3:

        st.metric(
            "Top-3 Retrieved",
            len(analytics_df)
        )

    with metric4:

        st.metric(
            "Response Time",
            f"{float(result['response_time']):.2f} sec"
        )

    st.divider()

    # =================================================
    # CHART 1
    # TOP RETRIEVED INCIDENTS
    # =================================================

    st.markdown(
        "### 🎯 Semantic Similarity of Retrieved Incidents"
    )

    similarity_chart = analytics_df[
        ["chart_label", "similarity"]
    ].copy()

    similarity_chart = similarity_chart.set_index(
        "chart_label"
    )

    st.bar_chart(
        similarity_chart,
        y="similarity",
        y_label="Similarity (%)",
        x_label="Retrieved SAP MDG Incident",
        use_container_width=True
    )

    st.caption(
        "Higher similarity indicates stronger semantic alignment "
        "between the submitted SAP MDG ticket and the retrieved incident."
    )

    st.divider()

    # =================================================
    # CHART 2
    # RETRIEVAL RANKING
    # =================================================

    st.markdown(
        "### 🏆 Retrieval Ranking"
    )

    ranking_df = analytics_df[
        [
            "chart_label",
            "similarity",
            "business_object",
            "module"
        ]
    ].copy()

    ranking_df["Rank"] = range(
        1,
        len(ranking_df) + 1
    )

    ranking_df = ranking_df[
        [
            "Rank",
            "chart_label",
            "similarity",
            "business_object",
            "module"
        ]
    ]

    ranking_df.columns = [
        "Rank",
        "Incident",
        "Similarity (%)",
        "Business Object",
        "SAP Module"
    ]

    st.dataframe(
        ranking_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # =================================================
    # CHART 3
    # TECHNICAL RELEVANCE
    # =================================================

    st.markdown(
        "### 🔎 Retrieved Incident Technical Context"
    )

    technical_df = analytics_df[
        [
            "chart_label",
            "business_object",
            "module",
            "category"
        ]
    ].copy()

    technical_df.columns = [
        "Incident",
        "Business Object",
        "SAP Module",
        "Category"
    ]

    st.dataframe(
        technical_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # =================================================
    # CHART 4
    # CONFIDENCE
    # =================================================

    # st.markdown(
    #     "### 🤖 AI Recommendation Confidence"
    # )

    # confidence_chart = pd.DataFrame({
    #     "Metric": ["AI Recommendation"],
    #     "Confidence": [confidence]
    # })

    # confidence_chart = confidence_chart.set_index(
    #     "Metric"
    # )

    # st.bar_chart(
    #     confidence_chart,
    #     y="Confidence",
    #     y_label="Confidence (%)",
    #     x_label="",
    #     use_container_width=True
    # )

    # st.caption(
    #     "The confidence score represents the system's confidence "
    #     "in the generated recommendation based on the retrieved knowledge."
    # )

    st.divider()

    # =================================================
    # INTERPRETATION
    # =================================================

    st.markdown(
        "### 📝 Retrieval Interpretation"
    )

    top_similarity = analytics_df.iloc[0]["similarity"]

    if top_similarity >= 80:

        st.success(
            f"Strong retrieval match: the top incident has "
            f"a similarity score of {top_similarity:.2f}%."
        )

    elif top_similarity >= 65:

        st.info(
            f"Moderate-to-strong retrieval match: the top incident "
            f"has a similarity score of {top_similarity:.2f}%."
        )

    else:

        st.warning(
            f"Low retrieval similarity: the top incident has "
            f"a similarity score of {top_similarity:.2f}%. "
            f"Manual verification is recommended."
        )
        st.divider()

        # chart1, chart2 = st.columns(2)

        # with chart1:

        #     st.markdown("### 📦 Business Object Distribution")

        #     business_counts = (
        #         analytics_df["business_object"]
        #         .value_counts()
        #     )

        #     st.bar_chart(business_counts)

        # with chart2:

        #     st.markdown("### ⚙ SAP Module Distribution")

        #     module_counts = (
        #         analytics_df["module"]
        #         .value_counts()
        #     )

        #     st.bar_chart(module_counts)

        # chart3, chart4 = st.columns(2)

        # with chart3:

        #     st.markdown("### 🏢 Department Distribution")

        #     dept_counts = (
        #         analytics_df["department"]
        #         .value_counts()
        #     )

        #     st.bar_chart(dept_counts)

        # with chart4:

        #     st.markdown("### 🎯 Similarity Score")

        #     similarity_chart = analytics_df.set_index(
        #         "issue"
        #     )["similarity"]

        #     st.bar_chart(similarity_chart)

    # st.divider()

    # =====================================================
    # SIMILAR INCIDENTS
    # =====================================================

    st.subheader("📚 Similar SAP Incidents")

    for i, incident in enumerate(similar, start=1):

        similar_incident_card(
            incident,
            i
        )

    st.divider()

    # =====================================================
    # EXPORT REPORTS
    # =====================================================

    st.divider()

    st.subheader("📥 Export Reports")

    col1, col2 = st.columns(2)

    # =====================================================
    # GENERATE PDF
    # =====================================================

    pdf_file = report_generator.generate_pdf(
        recommendation=recommendation,
        ticket=ticket,
        similar_incidents=similar,
        response_time=result["response_time"]
    )

    # =====================================================
    # PDF DOWNLOAD
    # =====================================================

    with col1:

        with open(pdf_file, "rb") as pdf:

            st.download_button(
                label="📄 Download Enterprise PDF Report",
                data=pdf,
                file_name="SAP_MDG_AI_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    # =====================================================
    # JSON DOWNLOAD
    # =====================================================

    with col2:

        st.download_button(
            label="📜 Download Analysis JSON",
            data=json.dumps(result, indent=4),
            file_name="SAP_MDG_AI_Report.json",
            mime="application/json",
            use_container_width=True
        )

    st.divider()

    st.success("✅ Analysis completed successfully. Reports are ready for download.")

    st.caption(
        "SAP MDG Intelligent Support Assistant | "
        "Master Thesis | "
        "MSc Artificial Intelligence | "
        "IU International University | "
        "Developed by Mohammad Aryaan"
    )