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

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🤖 SAP MDG AI")

    st.markdown("---")

    st.subheader("System Status")

    st.success("🟢 FastAPI Connected")
    st.success("🟢 FAISS Loaded")
    st.success("🟢 Sentence Transformer Ready")
    st.success("🟢 Llama 3.2 Ready")

    st.markdown("---")

    st.subheader("Technology")

    st.info("FastAPI")
    st.info("Sentence Transformers")
    st.info("FAISS")
    st.info("Llama 3.2")
    st.info("Streamlit")

    st.markdown("---")

    st.caption("Version 1.0")

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.block-container{
    padding-top:1.8rem;
    padding-bottom:2rem;
}

div[data-testid="metric-container"]{
    border-radius:12px;
    padding:18px;
    border:1px solid #404040;
    background:#1E1E1E;
}

div.stAlert{
    border-radius:12px;
}

hr{
    margin-top:20px;
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<div style="
padding:25px;
border-radius:15px;
background:linear-gradient(90deg,#0f2027,#203a43,#2c5364);
color:white;
">

<h1 style="margin-bottom:0;">
🤖 SAP MDG Intelligent Support Assistant
</h1>

<h3 style="margin-top:8px;">
Enterprise AI Recommendation System
</h3>

<p style="font-size:18px;">
AI-powered SAP Support Ticket Classification and Resolution Recommendation
using <b>Retrieval-Augmented Generation (RAG)</b>.
</p>

<hr>

<b>Technology Stack</b>

<br>

FastAPI • Sentence Transformers • FAISS • Ollama • Llama 3.2 • Streamlit

</div>
""", unsafe_allow_html=True)

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

    recommendation = result.get("recommendation", {})

    similar = result.get("similar_incidents", [])

    if not similar:
        st.error("No similar incidents found.")
        st.stop()

st.subheader("⚙ AI Processing Workflow")

workflow_steps = [
    "📩 Ticket Received",
    "🧠 Sentence Embedding Generated",
    "🔎 FAISS Semantic Search",
    "📚 Top 3 Similar Incidents Retrieved",
    "🤖 Llama 3.2 Analysis",
    "✅ AI Recommendation Generated"
]

cols = st.columns(len(workflow_steps))

for col, step in zip(cols, workflow_steps):
    with col:
        st.success(step)

    st.divider()

    # =====================================================
    # KPI CARDS
    # =====================================================

    first = similar[0]

    col1, col2, col3, col4 , col5 , col6 = st.columns(6)

    with col1:
        st.metric(
    "Business Object",
    first["business_object"]
)

    with col2:
        st.metric(
    "Module",
    first["module"]
)

    with col3:
        st.metric(
    "Category",
    first["category"]
)

    with col4:
        st.metric(
    "Department",
    first["department"]
)

    with col5:
        st.metric(
    "Resolver",
    first["resolver_role"]
)

    with col6:
        st.metric(
    "Records",
    result['retrieved_records']
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
                st.warning(cause)

        else:
            st.write(root_causes)


    with right:

        st.subheader("🔧 Diagnostic Steps")

        steps = recommendation.get(
            "diagnostic_steps",
            []
        )

        if isinstance(steps, list):

            for i, step in enumerate(steps, start=1):
                st.info(f"Step {i}")
                st.success(step)

        else:
            st.write(steps)

        st.subheader("✅ Recommended Resolution")

        resolutions = recommendation.get(
            "recommended_resolution",
            []
        )

        if isinstance(resolutions, list):

            for i, item in enumerate(resolutions, start=1):
                st.success(f"✅ Resolution {i}")
                st.write(item)

        else:
            st.success(resolutions)

    st.divider()

    # =====================================================
    # BUSINESS INFORMATION
    # =====================================================

    st.subheader("🏢 Business Information")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### Responsible Department")
        st.success(
            recommendation.get(
                "responsible_department",
                ""
            )
        )

        st.markdown("### Business Impact")
        st.error(
            recommendation.get(
                "business_impact",
                ""
            )
        )

    with c2:
        st.markdown("### Resolver Role")
        st.success(
            recommendation.get(
                "resolver_role",
                ""
            )
        )

    reasoning = recommendation.get("reasoning")

    if reasoning:
        st.divider()
        st.subheader("🧠 AI Reasoning")
        st.info(reasoning)

    # =====================================================
    # AI Match Score
    # =====================================================

    st.subheader("📈 AI Match Score")

    confidence = recommendation.get("confidence", 0)
    confidence_level = recommendation.get(
        "confidence_level",
        "Unknown"
    )

    if isinstance(confidence, str):
        confidence = confidence.replace("%", "").strip()
        try:
            confidence = int(confidence)
        except ValueError:
            confidence = 0

    st.progress(confidence / 100)

    metric1, metric2 = st.columns(2)
    with metric1:
        st.metric("Score", f"{confidence}%")
    with metric2:
        st.metric("Level", confidence_level)

    st.divider()

    # =====================================================
    # Processing Summary
    # =====================================================

    st.subheader("📊 Processing Summary")

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    with c1:
        st.metric("Retrieved Records", result["retrieved_records"])
    with c2:
        st.metric("Embedding Model", "MiniLM-L6-v2")
    with c3:
        st.metric("Vector Database", "FAISS")
    with c4:
        st.metric("LLM", "Llama 3.2")
    with c5:
        st.metric("Response Time", f"{result['response_time']} sec")
    with c6:
        st.metric("Similarity", "Cosine")

    st.divider()

    # =====================================================
    # SIMILAR INCIDENTS
    # =====================================================

    st.subheader("📚 Similar SAP Incidents")

    for i, incident in enumerate(similar, start=1):
        with st.expander(f"📄 Similar SAP Incident #{i}"):
            st.write("### Issue")
            st.info(incident["issue"])

            c1, c2 = st.columns(2)

            with c1:
                st.write("**Business Object:**", incident["business_object"])
                st.write("**Module:**", incident["module"])
                st.write("**Category:**", incident["category"])

            with c2:
                st.write("**Department:**", incident["department"])
                st.write("**Resolver:**", incident["resolver_role"])

                similarity = incident.get("similarity", 0)
                st.metric("Semantic Match", f"{similarity:.2f}%")
                st.progress(min(max(similarity / 100, 0), 1))

    st.divider()

    # =====================================================
    # RAW JSON (Optional)
    # =====================================================

    # with st.expander("🔍 View Complete JSON Response"):
    #     st.json(result)

    st.divider()

    st.caption(
        "Developed by Mohammad Aryaan | "
        "MSc Artificial Intelligence | "
        "IU International University | "
        "Master Thesis 2026"
    )





#     """
# ====================================================
# SAP MDG Intelligent Support Assistant
# Enterprise Dashboard V2
# ====================================================
# """

# import requests
# import streamlit as st

# # =====================================================
# # CONFIGURATION
# # =====================================================

# API_URL = "http://127.0.0.1:8000/analyze-ticket"

# st.set_page_config(
#     page_title="SAP MDG Intelligent Support Assistant",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # =====================================================
# # CUSTOM CSS
# # =====================================================


# st.markdown("""
# <style>

# /* Main container */
# .block-container{
#     max-width:1400px;
#     padding-top:1.2rem;
#     padding-bottom:2rem;
# }

# /* Metric cards */
# div[data-testid="metric-container"]{
#     background:#FFFFFF;
#     border:1px solid #E5E7EB;
#     border-radius:14px;
#     padding:18px;
#     box-shadow:0 2px 8px rgba(0,0,0,.08);
# }

# /* Streamlit alerts */
# div.stAlert{
#     border-radius:12px;
# }

# /* Button */
# .stButton>button{
#     width:100%;
#     height:52px;
#     border-radius:12px;
#     font-size:18px;
#     font-weight:600;
# }

# /* Text Area */
# textarea{
#     font-size:16px;
# }

# /* Custom Card */

# .card{
#       background:#1E2D42;

#     border:1px solid #2F4158;

#     border-radius:15px;

#     padding:18px;

#     height:150px;

#     display:flex;

#     flex-direction:column;

#     justify-content:space-between;

#     transition:.3s;

#     cursor:pointer;
# }

# .card:hover{
#      transform:translateY(-5px);

#     box-shadow:0 10px 20px rgba(0,0,0,.25);

#     border:1px solid #4EA1FF;
# }

# .card-icon{

#     font-size:30px;

# }

# .card-title{

#     color:#55A3FF;

#     font-size:18px;

#     font-weight:700;

# }

# .card-value{

#     color:white;

#     font-size:30px;

#     font-weight:700;

# }




# </style>
# """, unsafe_allow_html=True)

# # =====================================================
# # REUSABLE DASHBOARD CARD
# # =====================================================

# def dashboard_card(icon, title, value):

#     st.markdown(f"""
# <div class="card">

# <div class="card-icon">
# {icon}
# </div>

# <div class="card-title">
# {title}
# </div>

# <div class="card-value">
# {value}
# </div>

# </div>
# """, unsafe_allow_html=True)


# # =====================================================
# # SIDEBAR
# # =====================================================

# with st.sidebar:

#     st.title("🤖 SAP MDG AI")

#     st.markdown("---")

#     st.subheader("System Status")

#     st.success("🟢 FastAPI Connected")
#     st.success("🟢 FAISS Loaded")
#     st.success("🟢 Embedding Model Ready")
#     st.success("🟢 Llama 3.2 Connected")

#     st.markdown("---")

#     st.subheader("Project")

#     st.write("📘 SAP MDG Intelligent Support Assistant")
#     st.write("🎓 MSc Artificial Intelligence")
#     st.write("🏫 IU International University")
#     st.write("👨‍💻 Mohammad Aryaan")

#     st.markdown("---")

#     st.caption("Version 2.0")

# # =====================================================
# # HEADER
# # =====================================================

# st.title("🤖 SAP MDG Intelligent Support Assistant")

# st.markdown("""
# ### Enterprise AI Recommendation System

# AI-powered SAP Support Ticket Classification and Resolution Recommendation using **Retrieval-Augmented Generation (RAG)**.
# """)

# st.divider()

# # =====================================================
# # USER INPUT
# # =====================================================

# ticket = st.text_area(
#     "📩 Enter SAP Support Ticket",
#     height=140,
#     placeholder="Example: Vendor replication failed because RFC timeout..."
# )

# analyze = st.button(
#     "🚀 Analyze Ticket",
#     use_container_width=True
# )

# # =====================================================
# # API CALL
# # =====================================================

# if analyze:

#     if ticket.strip() == "":
#         st.warning("Please enter a SAP support ticket.")
#         st.stop()

#     with st.spinner(
#         "Analyzing SAP support ticket..."
#     ):

#         try:

#             response = requests.post(
#                 API_URL,
#                 json={
#                     "ticket": ticket
#                 },
#                 timeout=120
#             )

#             response.raise_for_status()

#         except requests.RequestException as e:

#             st.error(f"API Error : {e}")

#             st.stop()

#     result = response.json()

#     recommendation = result.get(
#         "recommendation",
#         {}
#     )

#     similar = result.get(
#         "similar_incidents",
#         []
#     )

#     if len(similar) == 0:

#         st.warning(
#             "No similar incidents were found."
#         )

#         st.stop()

#    # =====================================================

#     # =====================================================
#     # AI PROCESSING WORKFLOW
#     # =====================================================

#     st.subheader("⚙ AI Processing Workflow")

#     workflow_col1, workflow_col2, workflow_col3, workflow_col4, workflow_col5, workflow_col6 = st.columns(6)

#     with workflow_col1:
#         st.info("📩\n\n**Ticket**")

#     with workflow_col2:
#         st.info("🧠\n\n**Embedding**")

#     with workflow_col3:
#         st.info("🔎\n\n**FAISS Search**")

#     with workflow_col4:
#         st.info("📚\n\n**Top-3 Results**")

#     with workflow_col5:
#         st.info("🤖\n\n**Llama 3.2**")

#     with workflow_col6:
#         st.info("✅\n\n**Recommendation**")

#     st.divider()

#     # =====================================================
#     # TICKET & AI ANALYSIS SUMMARY
#     # =====================================================

#     first = similar[0]

#     st.subheader("📊 Ticket & AI Analysis Summary")

#     left_summary, right_summary = st.columns(2)

#     # -------------------------------------------------
#     # LEFT SIDE
#     # -------------------------------------------------

#     with left_summary:

#         st.markdown("### 📋 Ticket Information")

#         st.write(f"**Business Object:** {first['business_object']}")
#         st.write(f"**SAP Module:** {first['module']}")
#         st.write(f"**Category:** {first['category']}")
#         st.write(f"**Department:** {first['department']}")
#         st.write(f"**Resolver:** {first['resolver_role']}")

#     # -------------------------------------------------
#     # RIGHT SIDE
#     # -------------------------------------------------

#     with right_summary:

#         confidence = recommendation.get("confidence", 0)

#         if isinstance(confidence, str):

#             confidence = confidence.replace("%", "").strip()

#             try:
#                 confidence = int(confidence)
#             except ValueError:
#                 confidence = 0

#         confidence = max(0, min(confidence, 100))

#         st.markdown("### 🤖 AI Analysis")

#         st.metric(
#             "Confidence",
#             f"{confidence}%"
#         )

#         st.progress(confidence / 100)

#         st.write(
#             "**Confidence Level:**",
#             recommendation.get(
#                 "confidence_level",
#                 "Unknown"
#             )
#         )

#         st.write(
#             "**Retrieved Records:**",
#             result["retrieved_records"]
#         )

#         st.write(
#             "**Response Time:**",
#             f"{result['response_time']} sec"
#         )

#         st.write(
#             "**Similarity Method:**",
#             "Cosine Similarity"
#         )

#     st.divider()

  
#     # =====================================================
#     # AI RECOMMENDATION
#     # =====================================================

#     st.subheader("🤖 AI Recommendation")

#     left, right = st.columns(2)

#     # -------------------------------------------------
#     # LEFT PANEL
#     # -------------------------------------------------

#     with left:

#         st.markdown("### 📋 Issue Summary")

#         st.info(
#             recommendation.get(
#                 "issue_summary",
#                 "No summary available."
#             )
#         )

#         st.markdown("### ⚠ Root Cause")

#         root_causes = recommendation.get(
#             "root_cause",
#             []
#         )

#         if isinstance(root_causes, list):

#             for cause in root_causes:

#                 st.warning(cause)

#         else:

#             st.warning(root_causes)

#     # -------------------------------------------------
#     # RIGHT PANEL
#     # -------------------------------------------------

#     with right:

#         st.markdown("### 🔧 Diagnostic Steps")

#         steps = recommendation.get(
#             "diagnostic_steps",
#             []
#         )

#         if isinstance(steps, list):

#             for i, step in enumerate(steps, start=1):

#                 st.success(f"Step {i}")

#                 st.write(step)

#         else:

#             st.write(steps)

#         st.markdown("### ✅ Recommended Resolution")

#         resolutions = recommendation.get(
#             "recommended_resolution",
#             []
#         )

#         if isinstance(resolutions, list):

#             for i, item in enumerate(resolutions, start=1):

#                 st.success(f"Resolution {i}")

#                 st.write(item)

#         else:

#             st.success(resolutions)

#     st.divider()

#     # =====================================================
#     # AI REASONING
#     # =====================================================

#     reasoning = recommendation.get(
#         "reasoning",
#         ""
#     )

#     if reasoning:

#         st.subheader("🧠 AI Reasoning")

#         st.info(reasoning)

#         st.divider()

    
#     # =====================================================
#     # PROCESSING SUMMARY
#     # =====================================================

#     st.subheader("📊 Processing Summary")

#     c1, c2, c3, c4, c5 = st.columns(5)

#     with c1:
#         dashboard_card(
#             "📚",
#             "Records",
#             result["retrieved_records"]
#         )

#     with c2:
#         dashboard_card(
#             "🧠",
#             "Embedding",
#             "MiniLM-L6-v2"
#         )

#     with c3:
#         dashboard_card(
#             "🔎",
#             "Vector DB",
#             "FAISS"
#         )

#     with c4:
#         dashboard_card(
#             "🤖",
#             "LLM",
#             "Llama 3.2"
#         )

#     with c5:
#         dashboard_card(
#             "⏱",
#             "Response",
#             f"{result['response_time']} sec"
#         )

#     st.divider()

#     # =====================================================
#     # SIMILAR INCIDENTS
#     # =====================================================

#     st.subheader("📚 Similar SAP Incidents")

#     for i, incident in enumerate(similar, start=1):

#         with st.expander(
#             f"📄 Similar Incident #{i}"
#         ):

#             st.markdown("### Issue")

#             st.info(
#                 incident.get(
#                     "issue",
#                     ""
#                 )
#             )

#             c1, c2 = st.columns(2)

#             with c1:

#                 st.write(
#                     "**Business Object:**",
#                     incident.get(
#                         "business_object",
#                         ""
#                     )
#                 )

#                 st.write(
#                     "**SAP Module:**",
#                     incident.get(
#                         "module",
#                         ""
#                     )
#                 )

#                 st.write(
#                     "**Category:**",
#                     incident.get(
#                         "category",
#                         ""
#                     )
#                 )

#             with c2:

#                 st.write(
#                     "**Department:**",
#                     incident.get(
#                         "department",
#                         ""
#                     )
#                 )

#                 st.write(
#                     "**Resolver:**",
#                     incident.get(
#                         "resolver_role",
#                         ""
#                     )
#                 )

#                 similarity = incident.get(
#                     "similarity",
#                     0
#                 )

#                 similarity = max(
#                     0,
#                     min(similarity, 100)
#                 )

#                 st.metric(
#                     "Semantic Match",
#                     f"{similarity:.2f}%"
#                 )

#                 st.progress(
#                     similarity / 100
#                 )

#     st.divider()

#     st.caption(
#         "Developed by Mohammad Aryaan | "
#         "MSc Artificial Intelligence | "
#         "IU International University | "
#         "Master Thesis 2026"
#     )



# """
# ====================================================
# SAP MDG Intelligent Support Assistant
# Enterprise Dashboard V2
# ====================================================
# """

# import requests
# import streamlit as st

# # =====================================================
# # CONFIGURATION
# # =====================================================

# API_URL = "http://127.0.0.1:8000/analyze-ticket"

# st.set_page_config(
#     page_title="SAP MDG Intelligent Support Assistant",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # =====================================================
# # CUSTOM CSS
# # =====================================================


# st.markdown("""
# <style>

# /* Main container */
# .block-container{
#     max-width:1400px;
#     padding-top:1.2rem;
#     padding-bottom:2rem;
# }

# /* Metric cards */
# div[data-testid="metric-container"]{
#     background:#FFFFFF;
#     border:1px solid #E5E7EB;
#     border-radius:14px;
#     padding:18px;
#     box-shadow:0 2px 8px rgba(0,0,0,.08);
# }

# /* Streamlit alerts */
# div.stAlert{
#     border-radius:12px;
# }

# /* Button */
# .stButton>button{
#     width:100%;
#     height:52px;
#     border-radius:12px;
#     font-size:18px;
#     font-weight:600;
# }

# /* Text Area */
# textarea{
#     font-size:16px;
# }

# /* Custom Card */

# .card{
#       background:#1E2D42;

#     border:1px solid #2F4158;

#     border-radius:15px;

#     padding:18px;

#     height:150px;

#     display:flex;

#     flex-direction:column;

#     justify-content:space-between;

#     transition:.3s;

#     cursor:pointer;
# }

# .card:hover{
#      transform:translateY(-5px);

#     box-shadow:0 10px 20px rgba(0,0,0,.25);

#     border:1px solid #4EA1FF;
# }

# .card-icon{

#     font-size:30px;

# }

# .card-title{

#     color:#55A3FF;

#     font-size:18px;

#     font-weight:700;

# }

# .card-value{

#     color:white;

#     font-size:30px;

#     font-weight:700;

# }




# </style>
# """, unsafe_allow_html=True)

# # =====================================================
# # REUSABLE DASHBOARD CARD
# # =====================================================

# def dashboard_card(icon, title, value):

#     st.markdown(f"""
# <div class="card">

# <div class="card-icon">
# {icon}
# </div>

# <div class="card-title">
# {title}
# </div>

# <div class="card-value">
# {value}
# </div>

# </div>
# """, unsafe_allow_html=True)


# # =====================================================
# # SIDEBAR
# # =====================================================

# with st.sidebar:

#     st.title("🤖 SAP MDG AI")

#     st.markdown("---")

#     st.subheader("System Status")

#     st.success("🟢 FastAPI Connected")
#     st.success("🟢 FAISS Loaded")
#     st.success("🟢 Embedding Model Ready")
#     st.success("🟢 Llama 3.2 Connected")

#     st.markdown("---")

#     st.subheader("Project")

#     st.write("📘 SAP MDG Intelligent Support Assistant")
#     st.write("🎓 MSc Artificial Intelligence")
#     st.write("🏫 IU International University")
#     st.write("👨‍💻 Mohammad Aryaan")

#     st.markdown("---")

#     st.caption("Version 2.0")

# # =====================================================
# # HEADER
# # =====================================================

# st.title("🤖 SAP MDG Intelligent Support Assistant")

# st.markdown("""
# ### Enterprise AI Recommendation System

# AI-powered SAP Support Ticket Classification and Resolution Recommendation using **Retrieval-Augmented Generation (RAG)**.
# """)

# st.divider()

# # =====================================================
# # USER INPUT
# # =====================================================

# ticket = st.text_area(
#     "📩 Enter SAP Support Ticket",
#     height=140,
#     placeholder="Example: Vendor replication failed because RFC timeout..."
# )

# analyze = st.button(
#     "🚀 Analyze Ticket",
#     use_container_width=True
# )

# # =====================================================
# # API CALL
# # =====================================================

# if analyze:

#     if ticket.strip() == "":
#         st.warning("Please enter a SAP support ticket.")
#         st.stop()

#     with st.spinner(
#         "Analyzing SAP support ticket..."
#     ):

#         try:

#             response = requests.post(
#                 API_URL,
#                 json={
#                     "ticket": ticket
#                 },
#                 timeout=120
#             )

#             response.raise_for_status()

#         except requests.RequestException as e:

#             st.error(f"API Error : {e}")

#             st.stop()

#     result = response.json()

#     recommendation = result.get(
#         "recommendation",
#         {}
#     )

#     similar = result.get(
#         "similar_incidents",
#         []
#     )

#     if len(similar) == 0:

#         st.warning(
#             "No similar incidents were found."
#         )

#         st.stop()

#    # =====================================================

#     # =====================================================
#     # AI PROCESSING WORKFLOW
#     # =====================================================

#     st.subheader("⚙ AI Processing Workflow")

#     workflow_col1, workflow_col2, workflow_col3, workflow_col4, workflow_col5, workflow_col6 = st.columns(6)

#     with workflow_col1:
#         st.info("📩\n\n**Ticket**")

#     with workflow_col2:
#         st.info("🧠\n\n**Embedding**")

#     with workflow_col3:
#         st.info("🔎\n\n**FAISS Search**")

#     with workflow_col4:
#         st.info("📚\n\n**Top-3 Results**")

#     with workflow_col5:
#         st.info("🤖\n\n**Llama 3.2**")

#     with workflow_col6:
#         st.info("✅\n\n**Recommendation**")

#     st.divider()

#     # =====================================================
#     # TICKET & AI ANALYSIS SUMMARY
#     # =====================================================

#     first = similar[0]

#     st.subheader("📊 Ticket & AI Analysis Summary")

#     left_summary, right_summary = st.columns(2)

#     # -------------------------------------------------
#     # LEFT SIDE
#     # -------------------------------------------------

#     with left_summary:

#         st.markdown("### 📋 Ticket Information")

#         st.write(f"**Business Object:** {first['business_object']}")
#         st.write(f"**SAP Module:** {first['module']}")
#         st.write(f"**Category:** {first['category']}")
#         st.write(f"**Department:** {first['department']}")
#         st.write(f"**Resolver:** {first['resolver_role']}")

#     # -------------------------------------------------
#     # RIGHT SIDE
#     # -------------------------------------------------

#     with right_summary:

#         confidence = recommendation.get("confidence", 0)

#         if isinstance(confidence, str):

#             confidence = confidence.replace("%", "").strip()

#             try:
#                 confidence = int(confidence)
#             except ValueError:
#                 confidence = 0

#         confidence = max(0, min(confidence, 100))

#         st.markdown("### 🤖 AI Analysis")

#         st.metric(
#             "Confidence",
#             f"{confidence}%"
#         )

#         st.progress(confidence / 100)

#         st.write(
#             "**Confidence Level:**",
#             recommendation.get(
#                 "confidence_level",
#                 "Unknown"
#             )
#         )

#         st.write(
#             "**Retrieved Records:**",
#             result["retrieved_records"]
#         )

#         st.write(
#             "**Response Time:**",
#             f"{result['response_time']} sec"
#         )

#         st.write(
#             "**Similarity Method:**",
#             "Cosine Similarity"
#         )

#     st.divider()

  
#     # =====================================================
#     # AI RECOMMENDATION
#     # =====================================================

#     st.subheader("🤖 AI Recommendation")

#     left, right = st.columns(2)

#     # -------------------------------------------------
#     # LEFT PANEL
#     # -------------------------------------------------

#     with left:

#         st.markdown("### 📋 Issue Summary")

#         st.info(
#             recommendation.get(
#                 "issue_summary",
#                 "No summary available."
#             )
#         )

#         st.markdown("### ⚠ Root Cause")

#         root_causes = recommendation.get(
#             "root_cause",
#             []
#         )

#         if isinstance(root_causes, list):

#             for cause in root_causes:

#                 st.warning(cause)

#         else:

#             st.warning(root_causes)

#     # -------------------------------------------------
#     # RIGHT PANEL
#     # -------------------------------------------------

#     with right:

#         st.markdown("### 🔧 Diagnostic Steps")

#         steps = recommendation.get(
#             "diagnostic_steps",
#             []
#         )

#         if isinstance(steps, list):

#             for i, step in enumerate(steps, start=1):

#                 st.success(f"Step {i}")

#                 st.write(step)

#         else:

#             st.write(steps)

#         st.markdown("### ✅ Recommended Resolution")

#         resolutions = recommendation.get(
#             "recommended_resolution",
#             []
#         )

#         if isinstance(resolutions, list):

#             for i, item in enumerate(resolutions, start=1):

#                 st.success(f"Resolution {i}")

#                 st.write(item)

#         else:

#             st.success(resolutions)

#     st.divider()

#     # =====================================================
#     # AI REASONING
#     # =====================================================

#     reasoning = recommendation.get(
#         "reasoning",
#         ""
#     )

#     if reasoning:

#         st.subheader("🧠 AI Reasoning")

#         st.info(reasoning)

#         st.divider()

    
#     # =====================================================
#     # PROCESSING SUMMARY
#     # =====================================================

#     st.subheader("📊 Processing Summary")

#     c1, c2, c3, c4, c5 = st.columns(5)

#     with c1:
#         dashboard_card(
#             "📚",
#             "Records",
#             result["retrieved_records"]
#         )

#     with c2:
#         dashboard_card(
#             "🧠",
#             "Embedding",
#             "MiniLM-L6-v2"
#         )

#     with c3:
#         dashboard_card(
#             "🔎",
#             "Vector DB",
#             "FAISS"
#         )

#     with c4:
#         dashboard_card(
#             "🤖",
#             "LLM",
#             "Llama 3.2"
#         )

#     with c5:
#         dashboard_card(
#             "⏱",
#             "Response",
#             f"{result['response_time']} sec"
#         )

#     st.divider()

#     # =====================================================
#     # SIMILAR INCIDENTS
#     # =====================================================

#     st.subheader("📚 Similar SAP Incidents")

#     for i, incident in enumerate(similar, start=1):

#         with st.expander(
#             f"📄 Similar Incident #{i}"
#         ):

#             st.markdown("### Issue")

#             st.info(
#                 incident.get(
#                     "issue",
#                     ""
#                 )
#             )

#             c1, c2 = st.columns(2)

#             with c1:

#                 st.write(
#                     "**Business Object:**",
#                     incident.get(
#                         "business_object",
#                         ""
#                     )
#                 )

#                 st.write(
#                     "**SAP Module:**",
#                     incident.get(
#                         "module",
#                         ""
#                     )
#                 )

#                 st.write(
#                     "**Category:**",
#                     incident.get(
#                         "category",
#                         ""
#                     )
#                 )

#             with c2:

#                 st.write(
#                     "**Department:**",
#                     incident.get(
#                         "department",
#                         ""
#                     )
#                 )

#                 st.write(
#                     "**Resolver:**",
#                     incident.get(
#                         "resolver_role",
#                         ""
#                     )
#                 )

#                 similarity = incident.get(
#                     "similarity",
#                     0
#                 )

#                 similarity = max(
#                     0,
#                     min(similarity, 100)
#                 )

#                 st.metric(
#                     "Semantic Match",
#                     f"{similarity:.2f}%"
#                 )

#                 st.progress(
#                     similarity / 100
#                 )

#     st.divider()

#     st.caption(
#         "Developed by Mohammad Aryaan | "
#         "MSc Artificial Intelligence | "
#         "IU International University | "
#         "Master Thesis 2026"
#     )