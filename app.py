import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Customer Segmentation & Churn Pattern Analytics in European Banking",
    page_icon="🏦",
    layout="wide"
)
st.markdown("""
<style>

/* ==========================
   GLOBAL
========================== */

:root {
    --app-bg: #050A18;
    --container-bg: #0F172A;
    --panel-bg: #111827;
    --sidebar-bg: #08142a;
    --sidebar-border: rgba(96,165,250,.25);
    --sidebar-text: #E2E8F0;
    --sidebar-accent: rgba(96,165,250,.14);
    --panel-border: #1E293B;
    --panel-border-soft: rgba(59,130,246,.25);
    --text-primary: #FFFFFF;
    --text-secondary: #94A3B8;
    --card-bg: linear-gradient(145deg, #1E293B, #0F172A);
    --hero-bg: linear-gradient(135deg, #2563EB, #1E40AF);
    --hero-text: #FFFFFF;
    --tab-bg: #111827;
    --tab-border: #1F2937;
    --tab-active-bg: linear-gradient(135deg, #2563EB, #1D4ED8);
    --metric-bg: #111827;
    --metric-border: #334155;
    --scrollbar-track: #111827;
    --scrollbar-thumb: #2563EB;
}

@media (prefers-color-scheme: light) {
    :root {
        --app-bg: #F1F5F9;
        --container-bg: #FFFFFF;
        --panel-bg: #FFFFFF;
        --sidebar-bg: #F8FAFC;
        --sidebar-border: rgba(59,130,246,.24);
        --sidebar-text: #0F172A;
        --sidebar-accent: rgba(59,130,246,.12);
        --panel-border: #CBD5E1;
        --panel-border-soft: rgba(96,165,250,.18);
        --text-primary: #0F172A;
        --text-secondary: #475569;
        --card-bg: linear-gradient(145deg, #FFFFFF, #E2E8F0);
        --hero-bg: linear-gradient(135deg, #60A5FA, #D9E8FE);
        --hero-text: #0F172A;
        --tab-bg: #F8FAFC;
        --tab-border: #E2E8F0;
        --tab-active-bg: linear-gradient(135deg, #60A5FA, #7DD3FC);
        --metric-bg: #F8FAFC;
        --metric-border: #E2E8F0;
        --scrollbar-track: #E2E8F0;
        --scrollbar-thumb: #2563EB;
    }
}

.main{
    background: var(--app-bg);
}
            
.block-container{
    max-width:1600px;
    margin:auto;
    padding-top:1rem;
    padding-left:1.5rem;
    padding-right:1.5rem;
}
section[data-testid="stSidebar"]{
    width:340px !important;
    padding: 1.2rem 1rem 1.2rem 1rem;
}

/* ==========================
   SIDEBAR
========================== */

[data-testid="stSidebar"]{
    background: var(--sidebar-bg);
    border-right: 1px solid var(--sidebar-border);
    box-shadow: inset 0 0 45px rgba(0,0,0,.15);
    border-radius: 28px;
    padding: 1rem 0;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label{
    color: var(--sidebar-text) !important;
}

[data-testid="stSidebar"] .sidebar-title {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 1.25rem;
    padding: 0.95rem 1rem;
    background: var(--sidebar-accent);
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,.08);
    box-shadow: 0 10px 35px rgba(0,0,0,.15);
    font-size: 1.2rem;
    font-weight: 800;
    letter-spacing: 0.01em;
    color: var(--sidebar-text) !important;
}

[data-testid="stSidebar"] .sidebar-title span {
    font-size: 1.1rem;
}

[data-testid="stSidebar"] .sidebar-section-title {
    margin: 0 0 0.75rem;
    padding: 0.8rem 1rem;
    border-radius: 16px;
    background: rgba(255,255,255,.04);
    color: var(--sidebar-text) !important;
    font-size: 0.95rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    border: 1px solid rgba(255,255,255,.08);
}

[data-testid="stSidebar"] .sidebar-divider {
    height: 1px;
    width: 100%;
    background: rgba(255,255,255,.08);
    margin: 1rem 0;
}

[data-testid="stSidebar"] .css-1d391kg {
    background: rgba(255,255,255,.07);
    border-radius: 18px;
    padding: 12px 14px;
    margin-bottom: 18px;
}

[data-testid="stSidebar"] .stTextInput>div>div>input,
[data-testid="stSidebar"] .stSelectbox>div>div>div,
[data-testid="stSidebar"] .stMultiSelect>div>div>div{
    background: rgba(255,255,255,.08);
}

/* ==========================
   TITLE
========================== */

.dashboard-title{
    font-size:2.6rem;
    font-weight:800;

    background: linear-gradient(90deg, #FFFFFF, #60A5FA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-bottom:4px;
}

.dashboard-subtitle{
    font-size:1rem;
    color: var(--text-secondary);
    margin-bottom:15px;
}
/* ==========================
   PAGE SEPARATORS
========================== */

hr{
    border:none;
    height:1px;
    background: var(--panel-border);
    margin-top:20px;
    margin-bottom:20px;
}
/* ==========================
   HERO SECTION
========================== */

.hero-banner{
    background: var(--hero-bg);
    padding:25px;
    border-radius:20px;
    margin-bottom:25px;
    box-shadow:0 10px 30px rgba(14,30,60,.12);
}

.hero-title{
    color: var(--hero-text);
    font-size:30px;
    font-weight:700;
}

.hero-text{
    color: var(--hero-text);
    font-size:16px;
    margin-top:10px;
}

/* ==========================
   KPI CARDS
========================== */

.kpi-card{
    border-radius:24px;
    padding:14px;
    min-height:100px;
    text-align:center;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    background: var(--card-bg);
    border:1px solid var(--panel-border-soft);
    box-shadow:
        0 10px 35px rgba(14,30,60,.08);
    transition:all .30s ease;
}

.kpi-card:hover{
    transform:
        translateY(-8px)
        scale(1.01);
    border:1px solid rgba(37,99,235,.9);
    box-shadow:
        0 0 25px rgba(37,99,235,.35),
        0 12px 40px rgba(0,0,0,.20);
    cursor:pointer;
}

.kpi-label{
    color: var(--text-secondary);
    font-size:13px;
    font-weight:800;
    letter-spacing:0.8px;
    text-transform:uppercase;
    line-height:1.35;
    margin-bottom:10px;
    min-height:34px;
}

.kpi-value{
    color: var(--text-primary);
    font-size:1.75rem;
    font-weight:800;
    line-height:1.05;
    text-shadow:
        0 0 12px rgba(255,255,255,.15);
}
/* ==========================
   KPI COLOR THEMES
========================== */

.churn-card{
    border-top:5px solid #EF4444;
}

.segment-card{
    border-top:5px solid #F59E0B;
}

.highvalue-card{
    border-top:5px solid #10B981;
}

.geographic-card{
    border-top:5px solid #8B5CF6;
}

.engagement-card{
    border-top:5px solid #06B6D4;
}

/* ==========================
   KPI HOVER GLOW
========================== */

.churn-card:hover{
    box-shadow:
        0 0 30px rgba(239,68,68,.60),
        0 10px 40px rgba(0,0,0,.40);
}

.segment-card:hover{
    box-shadow:
        0 0 30px rgba(245,158,11,.60),
        0 10px 40px rgba(0,0,0,.40);
}

.highvalue-card:hover{
    box-shadow:
        0 0 30px rgba(16,185,129,.60),
        0 10px 40px rgba(0,0,0,.40);
}

.geographic-card:hover{
    box-shadow:
        0 0 30px rgba(139,92,246,.60),
        0 10px 40px rgba(0,0,0,.40);
}

.engagement-card:hover{
    box-shadow:
        0 0 30px rgba(6,182,212,.60),
        0 10px 40px rgba(0,0,0,.40);
}

/* ==========================
   SECTION HEADERS
========================== */

.section-header{
    color: var(--text-primary);
    font-size:2rem;
    font-weight:700;
    margin-top:10px;
    margin-bottom:20px;
}

/* ==========================
   TABS
========================== */

.stTabs [data-baseweb="tab-list"]{
    gap:8px;
    overflow-x:auto;
    padding-bottom:5px;
}

.stTabs [data-baseweb="tab"]{
    background: var(--panel-bg);
    border:1px solid var(--tab-border);
    border-radius:12px;
    padding:10px 18px;
    height:55px;
    white-space:nowrap;
    color: var(--text-primary);
    font-weight:600;
    flex-shrink:0;
}

.stTabs [aria-selected="true"]{
    background: var(--tab-active-bg) !important;
    color: var(--text-primary) !important;
}

/* ==========================
   TABS
========================== */

div[data-testid="stTabs"]{
    background: var(--container-bg);
    border:1px solid var(--panel-border);
    border-radius:18px;
    padding:10px;
    margin-top:20px;
    margin-bottom:20px;
}

.stTabs [data-baseweb="tab-list"]{
    gap:8px;
}

.stTabs [data-baseweb="tab"]{
    height:56px;
    border-radius:14px;
    background: var(--panel-bg);
    border:1px solid var(--tab-border);
    color: var(--text-primary);
    font-weight:600;
    padding:0 22px;
    transition:all .25s ease;
}

.stTabs [data-baseweb="tab"]:hover{
    border-color: rgba(37,99,235,.75);
}

.stTabs [aria-selected="true"]{
    background: var(--tab-active-bg) !important;
    color: var(--text-primary) !important;
    box-shadow:
        0 0 15px rgba(37,99,235,.35);
}
/* ==========================
   CHART CONTAINERS
========================== */

[data-testid="stPlotlyChart"]{
    background: var(--container-bg);
    border:1px solid var(--panel-border);
    border-radius:20px;
    padding:8px;
    margin-top:5px;
    margin-bottom:8px;
    box-shadow:
        0 8px 25px rgba(0,0,0,.12);
}
/* ==========================
   DATAFRAMES
========================== */

[data-testid="stDataFrame"]{
    border:1px solid var(--panel-border);
    border-radius:15px;
    overflow:hidden;
}

/* ==========================
   METRICS
========================== */

[data-testid="stMetric"]{
    background: var(--metric-bg);
    border:1px solid var(--metric-border);
    border-radius:15px;
    padding:15px;
}

/* ==========================
   ALERTS
========================== */

.stAlert{
    border-radius:15px;
}

/* ==========================
   SCROLLBAR
========================== */

::-webkit-scrollbar{
    width:8px;
}

::-webkit-scrollbar-track{
    background: var(--scrollbar-track);
}

::-webkit-scrollbar-thumb{
    background: var(--scrollbar-thumb);
    border-radius:10px;
}

/* ==========================
   STREAMLIT CHROME
========================== */

[data-testid="stMetric"]{
    background: var(--metric-bg);
    border:1px solid var(--metric-border);
    border-radius:12px;
    padding:10px;
    text-align:center;
}

[data-testid="stMetricValue"]{
    font-size:1.4rem !important;
}

[data-testid="stMetricLabel"]{
    font-size:0.8rem !important;
}
.section-header{
    color: var(--text-primary) !important;
    font-size:2rem;
    font-weight:700;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    data_path = Path(__file__).resolve().parent / "Data" / "European_Bank_Cleaned.csv"
    return pd.read_csv(data_path)

df = load_data()

# ==========================================
# DERIVED COLUMNS
# ==========================================

df["Age_Group"] = pd.cut(
    df["Age"],
    bins=[0, 30, 45, 60, 100],
    labels=["<30", "30-45", "46-60", "60+"]
)

df["Credit_Band"] = pd.cut(
    df["CreditScore"],
    bins=[0, 500, 700, 1000],
    labels=["Low", "Medium", "High"]
)

df["Tenure_Group"] = pd.cut(
    df["Tenure"],
    bins=[-1, 3, 7, 10],
    labels=["New", "Mid-Term", "Long-Term"]
)

df["Balance_Group"] = pd.cut(
    df["Balance"],
    bins=[-1, 1, 100000, float("inf")],
    labels=["Zero Balance", "Low Balance", "High Balance"]
)

df["High_Value_Customer"] = np.where(
    df["Balance"] >= 100000,
    1,
    0
)

# =====================================================
# TITLE
# =====================================================

st.markdown("""
<div style='text-align:center; margin-bottom:20px;'>
    <h1 class='hero-title'>
        🏦 Customer Segmentation & Churn Pattern Analytics in European Banking
    </h1>
</div>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.markdown(
    """
    <div class='sidebar-title'>
        <span>🏦</span>
        Customer Analytics Filters
    </div>
    """,
    unsafe_allow_html=True
)

# Geography
selected_geo = st.sidebar.multiselect(
    "🌍 Geography",
    sorted(df["Geography"].unique()),
    default=sorted(df["Geography"].unique())
)

# Gender
selected_gender = st.sidebar.multiselect(
    "👤 Gender",
    sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)

st.sidebar.markdown(
    """
    <div class='sidebar-section-title'>
        📊 Segmentation Dimensions
    </div>
    """,
    unsafe_allow_html=True
)
selected_age = st.sidebar.multiselect(
    "📅 Age Segment",
    options=list(df["Age_Group"].dropna().unique()),
    default=list(df["Age_Group"].dropna().unique())
)

selected_credit = st.sidebar.multiselect(
    "💳 Credit Score Band",
    options=list(df["Credit_Band"].dropna().unique()),
    default=list(df["Credit_Band"].dropna().unique())
)

selected_tenure = st.sidebar.multiselect(
    "⏳ Customer Tenure",
    options=list(df["Tenure_Group"].dropna().unique()),
    default=list(df["Tenure_Group"].dropna().unique())
)

selected_balance = st.sidebar.multiselect(
    "💰 Balance Segment",
    options=list(df["Balance_Group"].dropna().unique()),
    default=list(df["Balance_Group"].dropna().unique())
)

st.sidebar.markdown("---")
# ==========================================
# BASE DATASET (ONLY GEO + GENDER FILTERS)
# ==========================================

filtered_df = df[
    (df["Geography"].isin(selected_geo))
    &
    (df["Gender"].isin(selected_gender))
    &
    (df["Age_Group"].isin(selected_age))
    &
    (df["Credit_Band"].isin(selected_credit))
    &
    (df["Tenure_Group"].isin(selected_tenure))
    &
    (df["Balance_Group"].isin(selected_balance))
].copy()

if filtered_df.empty:
    st.warning(
        "No data available for selected filters. Please adjust the sidebar filters."
    )
    st.stop()

# Custom churn risk score for customer prioritization
filtered_df["RiskScore"] = (
    filtered_df["Age"] * 0.25
    + filtered_df["Balance"] * 0.00003
    + (1 - filtered_df["IsActiveMember"]) * 20
    + filtered_df["NumOfProducts"] * 5
)

# =====================================================
# KPI CALCULATIONS
# =====================================================

# 1. Overall Churn Rate
overall_churn_rate = (
    filtered_df ["Exited"].mean() * 100
)

# 2. Segment Churn Rate
segment_churn_rate = (
    filtered_df.groupby("Age_Group")["Exited"]
    .mean()
    .max() * 100
)

# 3. High-Value Churn Ratio
high_value_churn_ratio = (
    filtered_df[
        filtered_df["High_Value_Customer"] == 1
    ]["Exited"]
    .mean() * 100
)

# 4. Geographic Risk Index
geographic_risk_index = (
    filtered_df.groupby("Geography")["Exited"]
    .mean()
    .max() * 100
)

# 5. Engagement Drop Indicator

inactive_churn = (
    filtered_df[
        filtered_df["IsActiveMember"] == 0
    ]["Exited"]
    .mean() * 100
)

active_churn = (
    filtered_df[
        filtered_df["IsActiveMember"] == 1
    ]["Exited"]
    .mean() * 100
)

engagement_drop_indicator = (
    inactive_churn - active_churn
)

# =====================================================
# KPI DASHBOARD
# =====================================================

st.markdown("## 📊 Key Performance Indicators")

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
    <div class='kpi-card churn-card'>
        <div class='kpi-label'>Overall Churn Rate</div>
        <div class='kpi-value'>{overall_churn_rate:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='kpi-card segment-card'>
        <div class='kpi-label'>Highest Segment Churn Rate</div>
        <div class='kpi-value'>{segment_churn_rate:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='kpi-card highvalue-card'>
        <div class='kpi-label'>High-Value Churn Ratio</div>
        <div class='kpi-value'>{high_value_churn_ratio:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class='kpi-card geographic-card'>
        <div class='kpi-label'>Highest Regional Churn Rate</div>
        <div class='kpi-value'>{geographic_risk_index:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class='kpi-card engagement-card'>
        <div class='kpi-label'>Engagement Drop Indicator</div>
        <div class='kpi-value'>{engagement_drop_indicator:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
# =====================================================
# DASHBOARD TABS
# =====================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Project Overview",
    "👥 Customer Segmentation",
    "📉 Churn Distribution Analysis",
    "⭐ High-Value Customer Analysis",
    "🎯 Strategic Recommendations"
])
with tab1:
    st.markdown(
        """<h3 class='section-header'>
        📋 Executive Banking Overview
        </h3>""",
        unsafe_allow_html=True
    )

    geo_churn = (
        filtered_df.groupby("Geography")["Exited"]
        .mean()
        .mul(100)
        .reset_index()
    )

    gender_churn = (
        filtered_df.groupby("Gender")["Exited"]
        .mean()
        .mul(100)
        .reset_index()
    )
    if filtered_df.empty:
        st.warning("No data available for selected filters.")
    else:

        col1, col2 = st.columns(2)

        with col1:

            fig = px.bar(
                geo_churn,
                x="Geography",
                y="Exited",
                color="Geography",
                text_auto=".1f",
                title="Geography-wise Churn Rate"
            )

            fig.update_layout(height=450)
            st.plotly_chart(fig, use_container_width=True)
            highest_geo = geo_churn.loc[geo_churn["Exited"].idxmax(), "Geography"]
            highest_rate = geo_churn["Exited"].max()

            lowest_geo = geo_churn.loc[geo_churn["Exited"].idxmin(), "Geography"]
            lowest_rate = geo_churn["Exited"].min()

            if lowest_rate > 0:
                ratio_text = f"{(highest_rate/lowest_rate):.1f}x"
            else:
                ratio_text = "significantly"

            st.info(
                f"""
                📌 Business Insight

                {highest_geo} records the highest customer churn rate at
                {highest_rate:.1f}%, compared with only {lowest_rate:.1f}%
                in {lowest_geo}.

                Customers in {highest_geo} are {ratio_text} more likely
                to churn.

                This indicates a need for targeted retention strategies
                in this region.
                """
            ) 

        with col2:

            fig = px.bar(
                gender_churn,
                x="Gender",
                y="Exited",
                color="Gender",
                text_auto=".1f",
                title="Gender-wise Churn Rate"
            )

            fig.update_layout(height=450)
            st.plotly_chart(fig, use_container_width=True)
            female_data = gender_churn[
                gender_churn["Gender"]=="Female"
            ]

            male_data = gender_churn[
                gender_churn["Gender"]=="Male"
            ]

            female_rate = (
                female_data["Exited"].iloc[0]
                if len(female_data)>0
                else 0
            )

            male_rate = (
                male_data["Exited"].iloc[0]
                if len(male_data)>0
                else 0
            )

            gap = female_rate - male_rate

            st.info(
            f"""
            📌 Business Insight

            Female customers show a churn rate of {female_rate:.1f}%
            versus {male_rate:.1f}% for male customers.

            The churn gap of {gap:.1f} percentage points suggests
            different engagement patterns across genders. Tailored
            customer experience and personalized offers could help
            reduce attrition.
            """
            )     

with tab2:
    st.markdown("""<h3 class='section-header'>👥 Customer Segmentation Analysis</h3>""", unsafe_allow_html=True)
    st.caption("Age, Tenure, Credit Score and Balance Segment Analysis")

    col1, col2 = st.columns(2)

    # Age Group Analysis
    with col1:

        age_churn = (
            filtered_df.groupby("Age_Group")["Exited"]
            .mean()
            .mul(100)
            .reset_index()
        )

        fig = px.bar(
            age_churn,
            x="Age_Group",
            y="Exited",
            color="Age_Group",
            text_auto=".1f",
            title="Age Group Churn Analysis"
        )
        fig.update_layout(height=450)
        st.plotly_chart(
            fig,
            use_container_width=True
        )
        
        if not age_churn["Exited"].dropna().empty:
            top_age = age_churn.loc[
                age_churn["Exited"].idxmax(),
                "Age_Group"
            ]
            top_rate = age_churn["Exited"].max()

            st.warning(
            f"""
            📌 Business Insight

            Customers aged {top_age} exhibit the highest churn rate
            at {top_rate:.1f}%.

            This segment represents the most vulnerable customer group.
            Dedicated retention initiatives, relationship management,
            and targeted offers should be focused on these customers.
            """
            )
        else:
            st.info(
                "No age churn insight is available for the selected filters."
            )

    # Tenure Analysis
    with col2:

        tenure_churn = (
            filtered_df.groupby("Tenure_Group")["Exited"]
            .mean()
            .mul(100)
            .reset_index()
        )

        fig = px.bar(
            tenure_churn,
            x="Tenure_Group",
            y="Exited",
            color="Tenure_Group",
            text_auto=".1f",
            title="Tenure Group Churn Analysis"
        )
        fig.update_layout(height=450)
        st.plotly_chart(
            fig,
            use_container_width=True
        )
        if not tenure_churn["Exited"].dropna().empty:
            top_tenure = tenure_churn.loc[
                tenure_churn["Exited"].idxmax(),
                "Tenure_Group"
            ]

            top_tenure_rate = tenure_churn["Exited"].max()

            st.info(
            f"""
            📌 Business Insight

            {top_tenure} customers demonstrate the highest churn rate
            at {top_tenure_rate:.1f}%.

            This indicates that churn risk is concentrated within this
            stage of the customer lifecycle. Improved onboarding and
            engagement strategies may significantly improve retention.
            """
            )
        else:
            st.info(
                "No tenure churn insight is available for the selected filters."
            )

    col3, col4 = st.columns(2)

    # Credit Score Band
    with col3:

        credit_churn = (
            filtered_df.groupby("Credit_Band", observed=False)["Exited"]
            .mean()
            .mul(100)
            .reset_index()
        )

        fig = px.bar(
            credit_churn,
            x="Credit_Band",
            y="Exited",
            color="Credit_Band",
            text_auto=".1f",
            title="Credit Score Band Churn"
        )
        fig.update_layout(height=450)
        st.plotly_chart(
            fig,
            use_container_width=True
        )
        if not credit_churn["Exited"].dropna().empty:
            risk_band = credit_churn.loc[
                credit_churn["Exited"].idxmax(),
                "Credit_Band"
            ]

            risk_rate = credit_churn["Exited"].max()

            st.info(
            f"""
            📌 Business Insight

            Customers in the {risk_band} credit band show the highest
            churn rate at {risk_rate:.1f}%.

            Creditworthiness appears closely associated with retention
            behavior. Proactive support and personalized banking
            solutions could reduce customer attrition.
            """
            )
        else:
            st.info(
                "No credit band churn insight is available for the selected filters."
            )

    # Balance Segment
    with col4:

        balance_churn = (
            filtered_df.groupby("Balance_Group")["Exited"]
            .mean()
            .mul(100)
            .reset_index()
        )

        fig = px.bar(
            balance_churn,
            x="Balance_Group",
            y="Exited",
            color="Balance_Group",
            text_auto=".1f",
            title="Balance Segment Churn"
        )
        fig.update_layout(height=450)
        st.plotly_chart(
            fig,
            use_container_width=True
        )
        if not balance_churn["Exited"].dropna().empty:
            top_balance = balance_churn.loc[
                balance_churn["Exited"].idxmax(),
                "Balance_Group"
            ]

            top_balance_rate = balance_churn["Exited"].max()

            st.warning(
            f"""
            📌 Business Insight

            {top_balance} customers have the highest churn rate at
            {top_balance_rate:.1f}%.

            Since these customers represent significant account value,
            their departure creates substantial revenue exposure.
            Retention efforts should focus heavily on this segment.
            """
            )
        else:
            st.info(
                "No balance segment churn insight is available for the selected filters."
            )

    st.subheader("🌳 Customer Segmentation Treemap")

    treemap_df = filtered_df.copy()
    treemap_df["Balance"] = treemap_df["Balance"].fillna(0).clip(lower=0.0001)

    fig = px.treemap(
        treemap_df,
        path=[
            "Geography",
            "Gender",
            "Age_Group"
        ],
        values="Balance",
        color="Exited",
        color_continuous_scale="RdYlGn_r"
    )

    fig.update_layout(height=450)

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    fig.update_layout(height=450)
    st.subheader("📋 Segment Summary")

    segment_summary = pd.DataFrame({

        "Metric":[
            "Total Customers",
            "High Value Customers",
            "Average Credit Score",
            "Average Balance"
        ],

        "Value":[
            len(filtered_df),
            len(
                filtered_df[
                    filtered_df["High_Value_Customer"] == 1
                ]
            ),
            round(
                filtered_df["CreditScore"].mean(),
                2
            ),
            round(
                filtered_df["Balance"].mean(),
                2
            )
        ]
    })

    fig = px.bar(
        segment_summary,
        x="Metric",
        y="Value",
        color="Metric",
        text_auto=".2s",
        title="Customer Segment Summary"
    )

    fig.update_layout(
        height=450,
        showlegend=False,
        xaxis_title="",
        yaxis_title="Value"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    with st.expander("📋 View Detailed Segment Summary"):
        st.dataframe(
            segment_summary,
            use_container_width=True
        )
    if len(filtered_df) > 0:
        premium_pct = (
            len(
                filtered_df[
                    filtered_df["High_Value_Customer"] == 1
                ]
            ) / len(filtered_df)
        ) * 100
    else:
        premium_pct = 0
    st.info(
    f"""
    📌 Business Insight

    High-value customers represent
    {premium_pct:.1f}% of the customer base.

    Protecting this segment is essential because it
    contributes a significant share of deposits,
    balances, and future revenue.
    """
    )
with tab3:
    st.markdown("""<h3 class='section-header'>📉 Churn Distribution Dashboard</h3>""", unsafe_allow_html=True)
    filtered_df = filtered_df.copy()

    # ==========================================
    # AGE × GEOGRAPHY HEATMAP
    # ==========================================

    st.markdown("### 🔥 Geography vs Age Group Churn Heatmap")

    heatmap_data = pd.pivot_table(
        filtered_df,
        values="Exited",
        index="Age_Group",
        columns="Geography",
        aggfunc="mean"
    ) * 100

    fig = px.imshow(
        heatmap_data,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Reds"
    )
    fig.update_layout(height=450)
    st.plotly_chart(
        fig,
        use_container_width=True
    )
    max_value = heatmap_data.max().max()

    row,col = np.where(
        heatmap_data.values == max_value
    )

    top_age = heatmap_data.index[row[0]]
    top_geo = heatmap_data.columns[col[0]]

    st.warning(
    f"""
    📌 Business Insight

    The highest churn concentration occurs among
    {top_age} customers in {top_geo},
    with a churn rate of {max_value:.1f}%.

    This customer segment should be considered the
    highest-risk demographic group.
    """
    )
    # ==========================================
    # RISK SCORE
    # ==========================================

    st.markdown("### ⚠️ Customer Risk Distribution")

    fig = px.histogram(
        filtered_df,
        x="RiskScore",
        color="Exited",
        nbins=40,
        barmode="overlay",
        title="Customer Risk Score Distribution"
    )
    fig.update_layout(height=450)
    st.plotly_chart(
        fig,
        use_container_width=True
    )
    high_risk = len(
        filtered_df[
            filtered_df["RiskScore"] > 40
        ]
    )

    high_risk_pct = (
        high_risk / len(filtered_df)
    ) * 100

    st.warning(
    f"""
    📌 Business Insight

    Approximately {high_risk_pct:.1f}% of customers
    fall into the high-risk category (Risk Score > 40).

    These customers require immediate retention attention
    as they have a significantly higher probability of churn.
    """
    )
    # ==========================================
    # REVENUE RISK
    # ==========================================

    st.markdown("### 💰 Revenue Risk by Geography")

    revenue_by_country = (
        filtered_df[
            filtered_df["Exited"] == 1
        ]
        .groupby("Geography")["Balance"]
        .sum()
        .reset_index()
    )

    if revenue_by_country.empty:

        st.warning(
            """
            No churned customers found for the selected filters.

            Revenue risk cannot be calculated.
            """
        )

    else:

        fig = px.bar(
            revenue_by_country,
            x="Geography",
            y="Balance",
            color="Geography",
            text_auto=".2s",
            title="Revenue Exposure Due to Churn"
        )

        fig.update_layout(height=450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        risk_geo = revenue_by_country.loc[
            revenue_by_country["Balance"].idxmax(),
            "Geography"
        ]

        risk_amount = revenue_by_country["Balance"].max()

        st.error(
            f"""
            📌 Business Insight

            {risk_geo} contributes the largest revenue exposure,
            with approximately ${risk_amount:,.0f} at risk due
            to customer churn.

            Reducing churn in this geography could significantly
            improve profitability and revenue stability.
            """
        )
    # ==========================================
    # CHURN FUNNEL
    # ==========================================

    st.markdown("### 📊 Customer Portfolio Overview")

    funnel_df = pd.DataFrame({

        "Stage":[
            "Total Customers",
            "Active Members",
            "High Value Customers",
            "Churned Customers"
        ],

        "Count":[
            len(filtered_df),
            filtered_df["IsActiveMember"].sum(),
            len(
                filtered_df[
                    filtered_df["High_Value_Customer"] == 1
                ]
            ),
            filtered_df["Exited"].sum()
        ]
    })

    fig = px.funnel(
        funnel_df,
        x="Count",
        y="Stage"
    )
    fig.update_layout(height=450)
    st.plotly_chart(
        fig,
        use_container_width=True
    )
    active_pct = (
        filtered_df["IsActiveMember"].mean()
    ) * 100

    churn_pct = (
        filtered_df["Exited"].mean()
    ) * 100

    st.info(
    f"""
    📌 Business Insight

    Out of {len(filtered_df):,} customers,
    {active_pct:.1f}% remain active while
    {churn_pct:.1f}% have already churned.

    Customer engagement remains one of the strongest
    drivers of retention performance.
    """
    )
    # ==========================================
    # CHURNED VS RETAINED
    # ==========================================

    st.markdown("### 📈 Churned vs Retained Customer Comparison")

    comparison = (
        filtered_df.groupby("Exited")[
            [
                "Balance",
                "EstimatedSalary",
                "CreditScore",
                "Age"
            ]
        ]
        .mean()
        .round(2)
    )

    comparison.rename(
        index={
            0:"Retained",
            1:"Churned"
        },
        inplace=True
    )
    comparison_chart = comparison.reset_index()

    comparison_melt = comparison_chart.melt(
        id_vars="Exited",
        var_name="Metric",
        value_name="Value"
    )

    fig = px.bar(
        comparison_melt,
        x="Metric",
        y="Value",
        color="Exited",
        barmode="group",
        text_auto=".0f",
        title="Churned vs Retained Customer Metrics",
        color_discrete_sequence=["#3B82F6", "#EF4444"]
    )

    fig.update_layout(
        height=500,
        xaxis_title="Customer Metrics",
        yaxis_title="Average Value",
        legend_title="Customer Type"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    if (
        "Churned" in comparison.index
        and
        "Retained" in comparison.index
    ):

        balance_gap = (
            comparison.loc["Churned","Balance"]
            -
            comparison.loc["Retained","Balance"]
        )

        st.info(
            f"""
            📌 Business Insight

            Churned customers hold an average balance that is
            ${balance_gap:,.0f} higher than retained customers.

            This indicates that the bank is losing valuable
            customers, making retention efforts financially critical.
            """
        )

    else:

        st.warning(
            """
            Insufficient data available for comparison.

            Both churned and retained customers must be present
            in the selected filters.
            """
        )
with tab4:
    st.markdown("""<h3 class='section-header'>⭐ High-Value Customer Churn Analysis</h3>""", unsafe_allow_html=True)
    
    premium_customers = filtered_df[
        filtered_df["High_Value_Customer"] == 1
    ]
    if premium_customers.empty:
        st.warning(
            "No high-value customers available for selected filters."
        )
    else:
    # ==========================================
    # PREMIUM KPIs
    # ==========================================

        premium_count = len(premium_customers)

        premium_churn = (
            premium_customers["Exited"].mean()
            * 100
        )

        premium_balance = (
            premium_customers["Balance"].sum()
        )

        premium_salary = (
            premium_customers["EstimatedSalary"].mean()
        )

        revenue_risk = (
            premium_customers[
                premium_customers["Exited"] == 1
            ]["Balance"].sum()
        )

        p1, p2, p3, p4, p5 = st.columns(5)

        p1.metric(
            "High-Value Customers",
            f"{premium_count:,}"
        )

        p2.metric(
            "High-Value Churn Rate",
            f"{premium_churn:.2f}%"
        )

        p3.metric(
            "High-Value Deposits",
            f"${premium_balance/1_000_000:.1f}M"
        )

        p4.metric(
            "Average Customer Salary",
            f"${premium_salary:,.0f}"
        )

        p5.metric(
            "Deposit Risk Exposure",
            f"${revenue_risk/1_000_000:.1f}M"
        )

        st.divider()
        # ==========================================
        # SALARY VS BALANCE
        # ==========================================

        st.markdown(
            "### 💰 Salary vs Balance Churn Analysis"
        )

        fig = px.scatter(
            premium_customers,
            x="EstimatedSalary",
            y="Balance",
            color="Exited",
            size="CreditScore",
            hover_data=[
                "Age",
                "Geography"
            ],
            title="High-Value Customer Portfolio Analysis"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
        avg_balance = premium_customers["Balance"].mean()

        high_balance_churn = (
            premium_customers[
                premium_customers["Balance"] > avg_balance
            ]["Exited"].mean() * 100
        )

        st.warning(
        f"""
        📌 Business Insight

        High-value customers with balances above
        ${avg_balance:,.0f} show a churn rate of
        {high_balance_churn:.1f}%.

        Losing these customers may result in substantial
        revenue leakage because they represent the bank's
        most valuable accounts.
        """
        )
        # ==========================================
        # PREMIUM CHURN BY GEOGRAPHY
        # ==========================================

        st.markdown(
            "### 🌍 High-Value Customer Churn by Geography"
        )

        premium_geo = (
            premium_customers
            .groupby("Geography")["Exited"]
            .mean()
            .mul(100)
            .reset_index()
        )

        if premium_geo.empty:

            st.warning(
                "No high-value customer data available for selected filters."
            )

        else:

            fig = px.bar(
                premium_geo,
                x="Geography",
                y="Exited",
                color="Geography",
                text_auto=".1f"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            top_geo = premium_geo.loc[
                premium_geo["Exited"].idxmax(),
                "Geography"
            ]

            top_rate = premium_geo["Exited"].max()

            st.error(
                f"""
                📌 Business Insight

                High-value customers in {top_geo}
                show the highest churn rate at
                {top_rate:.1f}%.
                """
            )    
            # ==========================================
            # TOP RISK CUSTOMERS
            # ==========================================

            st.markdown(
                "### 📊 High-Value Customer Risk Ranking"
            )

            top_risk = (
                premium_customers
                .sort_values(
                    "RiskScore",
                    ascending=False
                )
                .head(10)
            )


            with st.expander("📋 View Top 10 High-Risk Customers"):
                st.dataframe(
                    top_risk[
                        [
                            "Geography",
                            "Gender",
                            "Age",
                            "Balance",
                            "EstimatedSalary",
                            "CreditScore",
                            "RiskScore",
                            "Exited"
                        ]
                    ],
                    use_container_width=True
                )
            avg_risk = top_risk["RiskScore"].mean()

            dominant_geo = (
                top_risk["Geography"]
                .value_counts()
                .idxmax()
            )

            st.success(
                f"""
                📌 Portfolio Risk Summary

                Average Risk Score: {avg_risk:.1f}

                Highest Risk Geography: {dominant_geo}

                The bank's highest-risk customers are primarily concentrated
                in {dominant_geo}. This segment should be prioritized for
                retention campaigns, proactive outreach, and relationship
                management initiatives.
                """
            )
        # ==========================================
        # CUSTOMER DRILL DOWN
        # ==========================================

        st.markdown(
            "### 🔍 Customer Profile Drill-Down"
        )

        customer_index = st.selectbox(
            "Select High-Value Customer",
            premium_customers.index
        )

        customer = premium_customers.loc[[customer_index]]

        customer_risk = customer["RiskScore"].iloc[0]

        # ==========================================
        # CUSTOMER PROFILE
        # ==========================================

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Age",
            int(customer["Age"].iloc[0])
        )

        col2.metric(
            "Credit Score",
            int(customer["CreditScore"].iloc[0])
        )

        col3.metric(
            "Balance",
            f"${customer['Balance'].iloc[0]:,.0f}"
        )

        col4.metric(
            "Salary",
            f"${customer['EstimatedSalary'].iloc[0]:,.0f}"
        )

        col5, col6, col7, col8 = st.columns(4)

        col5.metric(
            "Geography",
            customer["Geography"].iloc[0]
        )

        col6.metric(
            "Gender",
            customer["Gender"].iloc[0]
        )

        col7.metric(
            "Products",
            int(customer["NumOfProducts"].iloc[0])
        )

        col8.metric(
            "Active Member",
            "Yes" if customer["IsActiveMember"].iloc[0] else "No"
        )

        st.divider()

        # ==========================================
        # RISK GAUGE
        # ==========================================

        if customer_risk > 40:
            risk_level = "High Risk"
            bar_color = "red"
        elif customer_risk > 25:
            risk_level = "Moderate Risk"
            bar_color = "orange"
        else:
            risk_level = "Low Risk"
            bar_color = "green"

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=customer_risk,
                title={
                    "text": f"Customer Churn Risk Score — {risk_level}"
                },
                gauge={
                    "axis":{
                        "range":[0,60],
                        "tickmode":"array",
                        "tickvals":[0,25,40,60],
                        "ticktext":["Low","Medium","High",""]
                    },
                    "bar":{
                        "color": bar_color
                    },
                    "steps":[
                        {
                            "range":[0,25],
                            "color":"#10B981"
                        },
                        {
                            "range":[25,40],
                            "color":"#F59E0B"
                        },
                        {
                            "range":[40,60],
                            "color":"#EF4444"
                        }
                    ],
                    "threshold":{
                        "line":{
                            "color":"#444444",
                            "width":4
                        },
                        "thickness":0.75,
                        "value": customer_risk
                    }
                }
            )
        )

        fig.update_layout(
            height=350
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.warning(
        f"""
        📌 Customer Insight

        This customer belongs to
        {customer['Geography'].iloc[0]}
        and is classified as {risk_level}.

        Current Risk Score:
        {customer_risk:.1f}

        Relationship managers can use this information
        to determine whether proactive retention efforts
        are required.
        """
        )

        # ==========================================
        # COMPLETE RECORD
        # ==========================================

        with st.expander("📋 View Complete Customer Record"):
            st.dataframe(
                customer,
                use_container_width=True
            )
with tab5:

    st.markdown(
        """<h3 class='section-header'>
        🎯 Strategic Recommendations & Business Impact
        </h3>""",
        unsafe_allow_html=True
    )

    # ==========================================
    # EXECUTIVE SUMMARY
    # ==========================================

    st.info(
        """
        📌 Executive Summary

        Customer churn is primarily concentrated among high-value,
        inactive, and Germany-based customer segments.

        Strategic retention initiatives focused on these groups
        can significantly improve customer lifetime value,
        reduce revenue leakage, and strengthen long-term
        business performance.
        """
    )

    st.divider()

    # ==========================================
    # STRATEGIC ACTION PRIORITIES
    # ==========================================

    st.subheader("📊 Strategic Action Priorities")

    recommendations = pd.DataFrame({

        "Priority":[
            "High",
            "High",
            "Medium",
            "Medium",
            "Low"
        ],

        "Recommendation":[
            "Retain High-Value Customers",
            "Reduce Germany Churn",
            "Increase Customer Engagement",
            "Improve Product Adoption",
            "Strengthen Loyalty Programs"
        ],

        "Impact Score":[
            95,
            90,
            80,
            70,
            60
        ]
    })

    fig = px.bar(
        recommendations,
        x="Impact Score",
        y="Recommendation",
        color="Priority",
        orientation="h",
        text="Impact Score",
        title="Business Impact Prioritization",
        color_discrete_map={
            "High":"#EF4444",
            "Medium":"#F59E0B",
            "Low":"#10B981"
        }
    )

    fig.update_layout(
        height=450,
        xaxis_title="Expected Business Impact",
        yaxis_title="",
        legend_title="Priority"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ==========================================
    # KEY RECOMMENDATIONS
    # ==========================================

    st.subheader("🎯 Key Recommendations")

    st.success(
        """
        1️⃣ Prioritize retention campaigns in Germany.

        2️⃣ Develop engagement programs for inactive customers.

        3️⃣ Protect high-value customers through loyalty benefits
        and personalized relationship management.

        4️⃣ Create targeted offers for high-risk age segments.

        5️⃣ Increase multi-product adoption to improve customer
        stickiness and retention.
        """
    )

    st.divider()

    # ==========================================
    # EXECUTIVE CONCLUSION
    # ==========================================

    st.subheader("📌 Executive Conclusion")

    st.markdown(
        """
        ### Key Findings

        ✅ Germany exhibits the highest churn exposure.

        ✅ High-value customers contribute significant revenue risk.

        ✅ Inactive customers are substantially more likely to churn.

        ✅ Customer age and tenure strongly influence churn behaviour.

        ✅ Geography and demographic segments require targeted retention strategies.

        ---

        ### Strategic Business Impact

        ✅ Reduce customer attrition.

        ✅ Improve customer lifetime value.

        ✅ Minimize revenue leakage.

        ✅ Support data-driven decision making.

        ✅ Enable targeted customer retention programs.

        ---
        
        ### Final Recommendation

        The bank should adopt a segmentation-driven retention strategy
        focused on geography, customer value, engagement level,
        and demographic characteristics to reduce churn and improve
        long-term profitability.
        """
    )