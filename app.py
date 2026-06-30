import streamlit as st
import pandas as pd
from ranking.search_candidates import search_candidates

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="TalentIQ AI Recruiter",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>

header{
    visibility:hidden;
}

.block-container{
    padding-top:0rem !important;
    margin-top:0rem !important;
}

section.main > div{
    padding-top:0rem !important;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# SESSION STATE
# ----------------------------------------------------

if "searched" not in st.session_state:
    st.session_state.searched = False

if "results_df" not in st.session_state:
    st.session_state.results_df = pd.DataFrame()

if "top_candidates" not in st.session_state:
    st.session_state.top_candidates = []

# ----------------------------------------------------
# DARK THEME
# ----------------------------------------------------

st.markdown("""
<style>

.stApp{
background:#0E1117;
color:white;
}

section[data-testid="stSidebar"]{
background:#161B22;
}

h1,h2,h3,h4,h5{
color:white !important;
}

p,label{
color:#D1D5DB !important;
}

textarea{
background:#1E1E1E !important;
color:white !important;
border-radius:10px !important;
}

.stButton>button{
background:#2563EB;
color:white;
font-size:18px;
font-weight:bold;
height:50px;
border-radius:10px;
width:100%;
}

.stButton>button:hover{
background:#1D4ED8;
}

div[data-testid="metric-container"]{
background:#161B22;
border:1px solid #30363D;
border-radius:12px;
padding:18px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

st.sidebar.title("🤖 TalentIQ")

st.sidebar.markdown("---")

st.sidebar.success("AI Recruiter Dashboard")

st.sidebar.markdown("### Modules")

st.sidebar.write("🏠 Dashboard")
st.sidebar.write("📊 Candidate Ranking")
st.sidebar.write("🧠 Explainability")
st.sidebar.write("📄 Semantic Search")

st.sidebar.markdown("---")

st.sidebar.info("""
AI Powered Recruitment

✔ Semantic Search

✔ FAISS Ranking

✔ Explainability
""")

# ----------------------------------------------------
# TITLE
# ----------------------------------------------------

st.title("🤖 TalentIQ AI Recruiter")

st.caption(
"AI Powered Intelligent Candidate Discovery"
)

st.divider()

# ----------------------------------------------------
# JOB DESCRIPTION
# ----------------------------------------------------

st.subheader("📄 Job Description")

job_description = st.text_area(
"Paste Job Description",
height=250,
placeholder="""
We are looking for an AI Engineer.

Required Skills

Python
Machine Learning
TensorFlow
SQL
Git
Docker

Responsibilities

Develop AI Models

Deploy ML Pipelines

Collaborate with Data Scientists
"""
)

search = st.button(
"🔍 Search Candidates",
use_container_width=True
)
# ----------------------------------------------------
# SEARCH CANDIDATES
# ----------------------------------------------------

if search:

    if job_description.strip() == "":

        st.warning("⚠ Please enter the Job Description.")

        st.stop()

    with st.spinner("Searching candidates..."):

        top_candidates = search_candidates(job_description)

    if len(top_candidates) == 0:

        st.error("No candidates found.")

        st.stop()

    st.session_state.searched = True
    st.session_state.top_candidates = top_candidates
    st.session_state.results_df = pd.DataFrame(top_candidates)

# ----------------------------------------------------
# DISPLAY RESULTS
# ----------------------------------------------------

if st.session_state.searched:

    results_df = st.session_state.results_df
    top_candidates = st.session_state.top_candidates

    st.divider()

    st.header("📊 Search Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Candidates",
            len(results_df)
        )

    with col2:
        average = round(
            results_df["Similarity_Score"].mean() * 100,
            2
        )

        st.metric(
            "Average Similarity",
            f"{average}%"
        )

    with col3:
        highest = round(
            results_df["Similarity_Score"].max() * 100,
            2
        )

        st.metric(
            "Best Match",
            f"{highest}%"
        )

    st.divider()

    st.subheader("🏆 Top Ranked Candidates")

    preview = results_df[
        [
            "Name",
            "Current_Title",
            "Similarity_Score"
        ]
    ].copy()

    preview["Similarity_Score"] = (
        preview["Similarity_Score"] * 100
    ).round(2)

    preview.columns = [
        "Candidate",
        "Current Title",
        "Similarity (%)"
    ]

    st.dataframe(
        preview,
        use_container_width=True,
        hide_index=True
    )

    st.divider()
    
    # ----------------------------------------------------
    # AI CANDIDATE RECOMMENDATIONS
    # ----------------------------------------------------

    st.header("🤖 AI Candidate Recommendations")

    rank = 1

    for candidate in top_candidates:

        similarity = round(
            float(candidate["Similarity_Score"]) * 100,
            2
        )

        github = float(candidate.get("Github_Score", 0))
        profile = float(candidate.get("Profile_Completeness", 0))
        response = float(candidate.get("Recruiter_Response_Rate", 0))
        notice = float(candidate.get("Notice_Period", 60))

        confidence = round(
            similarity * 0.60 +
            github * 0.10 +
            profile * 0.10 +
            response * 0.10 +
            max(0, (30 - notice)) * 0.33,
            2
        )

        if confidence >= 95:
            recommendation = "🟢 Excellent Match"
        elif confidence >= 80:
            recommendation = "🟢 Strong Match"
        elif confidence >= 70:
            recommendation = "🟡 Good Match"
        elif confidence >= 50:
            recommendation = "🟠 Average Match"
        else:
            recommendation = "🔴 Low Match"

        with st.container():

            st.markdown(f"""
<div style="
background:#161B22;
padding:20px;
border-radius:15px;
border:1px solid #30363D;
margin-bottom:20px;
">

<h2 style="color:#58A6FF;">🏅 Rank {rank}</h2>

<h3 style="color:white;">
{candidate['Name']}
</h3>

<p style="color:#D1D5DB;">
<b>Current Title:</b>
{candidate['Current_Title']}
</p>

<p style="color:#D1D5DB;">
<b>Similarity Score:</b>
{similarity:.2f}%
</p>

<p style="color:#D1D5DB;">
<b>Confidence Score:</b>
{confidence:.2f}%
</p>

<h4 style="color:#58A6FF;">
{recommendation}
</h4>

</div>
""", unsafe_allow_html=True)

            st.subheader("💻 Skills")

            st.write(candidate["Skills"])

            st.subheader("📊 Candidate Metrics")

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric("GitHub", github)

            with c2:
                st.metric("Profile", profile)

            with c3:
                st.metric("Response", response)

            with c4:
                st.metric("Notice", f"{int(notice)} Days")

            st.subheader("🧠 Why this Candidate?")

            reasons = []

            if similarity >= 75:
                reasons.append("✔ Excellent semantic match with the Job Description.")
            elif similarity >= 60:
                reasons.append("✔ Good semantic similarity.")
            else:
                reasons.append("✔ Moderate semantic relevance.")

            if github >= 80:
                reasons.append("✔ Strong GitHub activity.")

            if profile >= 80:
                reasons.append("✔ Highly complete professional profile.")

            if response >= 80:
                reasons.append("✔ Highly responsive to recruiters.")

            if notice <= 30:
                reasons.append("✔ Can join within 30 days.")

            for reason in reasons:
                st.success(reason)

            st.divider()

        rank += 1
    # ----------------------------------------------------
    # DOWNLOAD RESULTS
    # ----------------------------------------------------

    st.header("📥 Download Results")

    download_df = results_df.copy()

    download_df["Similarity_Score"] = (
        download_df["Similarity_Score"] * 100
    ).round(2)

    download_df.rename(
        columns={
            "Name": "Candidate",
            "Current_Title": "Current Title",
            "Similarity_Score": "Similarity (%)"
        },
        inplace=True
    )

    csv = download_df.to_csv(index=False).encode("utf-8")

    st.download_button(

        label="📄 Download Ranked Candidates (CSV)",

        data=csv,

        file_name="recommended_candidates.csv",

        mime="text/csv",

        use_container_width=True

    )

    st.success("✅ Candidate ranking completed successfully!")

    st.info("""
The recruiter can now:

• View ranked candidates

• Compare similarity scores

• Understand AI explainability

• Download candidate results
""")

    st.divider()

    st.markdown("""
<div style="
background:#161B22;
padding:20px;
border-radius:15px;
border:1px solid #30363D;
text-align:center;
">

<h3 style="color:#58A6FF;">
TalentIQ – Intelligent Candidate Discovery
</h3>

<p style="color:#D1D5DB;">
Built using
<b>Python</b> •
<b>Sentence Transformers</b> •
<b>FAISS</b> •
<b>Pandas</b> •
<b>Streamlit</b>
</p>

<p style="color:#8B949E;">
🚀 AI Powered Recruitment | Semantic Search | Explainable AI
</p>

</div>
""", unsafe_allow_html=True)