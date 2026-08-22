# ============================================================
# ANTARANG - MODEL ANALYTICS & EXPLAINABILITY
# Inspect model metrics, training details, and diagnostic visual plots
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Ensure utils can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import (
    load_model_artifacts,
    load_cases_dataset,
    load_feature_importance,
    resolve_path,
    inject_custom_css
)

st.set_page_config(
    page_title="Model Analytics & Explainability | Antarang",
    page_icon="📊",
    layout="wide"
)

inject_custom_css()

st.markdown("""
<div class="main-header">
    <div class="hero-badge">Explainable AI (XAI)</div>
    <h1>📊 Model Analytics & Diagnostic Insights</h1>
    <p>Understand the Random Forest Regressor architecture, accuracy metrics, and feature significance</p>
</div>
""", unsafe_allow_html=True)

# Load data and artifacts
try:
    model, encoders, features = load_model_artifacts()
    df = load_cases_dataset()
    importance_df = load_feature_importance()
except Exception as e:
    st.error(f"❌ Error loading artifacts: {e}")
    st.stop()

# Key metrics
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(label="Model Architecture", value="Random Forest", delta="100 Estimators")
with m2:
    st.metric(label="R² Score (Test Set)", value="0.758", delta="75.8% Variance Explained")
with m3:
    st.metric(label="Mean Absolute Error", value="308 Days", delta="±10 Months")
with m4:
    st.metric(label="Total Dataset Size", value=f"{len(df):,} Cases", delta="Pre-processed")

st.markdown("---")

# Visual Diagnostic Tabs
tab1, tab2, tab3 = st.tabs(["🔑 Feature Importance", "📈 Model Diagnostic Plot", "📂 Dataset Distribution"])

with tab1:
    st.markdown("### 🔑 Relative Feature Importance")
    st.markdown("Quantifying the relative impact of each predictor on estimated duration:")

    if importance_df is not None:
        c1, c2 = st.columns([1.6, 1.1])
        with c1:
            fig = px.bar(
                importance_df.sort_values('Importance', ascending=True),
                x='Importance',
                y='Feature',
                orientation='h',
                color='Importance',
                color_continuous_scale='Blues',
                text=importance_df.sort_values('Importance', ascending=True)['Importance'].apply(lambda x: f'{x*100:.1f}%'),
                title="Gini Feature Importance"
            )
            fig.update_layout(height=380, margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig, width='stretch')

        with c2:
            st.markdown("#### Feature Explanations")
            st.markdown("""
            - **`is_old_case` & `is_very_old_case`**: Historical backlogs and year of registration dominate resolution timelines.
            - **`caseType_encoded`**: Bail Applications (`BA`) vs Civil Suits (`CS`) have completely distinct statutory urgency timelines.
            - **`stateName_encoded`**: Captures differences in state-level judicial vacancy and infrastructure.
            - **`tier_encoded`**: High Court vs District Court procedural stages.
            - **`filing_month` & `filing_day`**: Captures judicial vacation periods (e.g. summer/winter recesses).
            """)

with tab2:
    st.markdown("### 📈 Actual vs. Predicted Diagnostic Visualization")
    plot_path = resolve_path('models', 'model_performance.png')
    if os.path.exists(plot_path):
        st.image(plot_path, caption="Random Forest Test Set Performance & Actual vs Predicted Correlation", use_container_width=True)
    else:
        st.info("Visual performance plot not found. Run `python models/train_model.py` to regenerate.")

with tab3:
    st.markdown("### 📂 Training Data Exploration")
    col_d1, col_d2 = st.columns(2)

    with col_d1:
        fig_hist = px.histogram(
            df,
            x='duration_days',
            nbins=40,
            title="Case Duration Distribution (Days)",
            color_discrete_sequence=['#4338ca']
        )
        fig_hist.update_layout(height=320)
        st.plotly_chart(fig_hist, width='stretch')

    with col_d2:
        case_counts = df['caseType'].value_counts().reset_index()
        case_counts.columns = ['Case Type', 'Count']
        fig_cases = px.pie(
            case_counts,
            names='Case Type',
            values='Count',
            title="Breakdown by Case Type",
            hole=0.4
        )
        fig_cases.update_layout(height=320)
        st.plotly_chart(fig_cases, width='stretch')

st.markdown("""
<div class="footer-note">
    📊 <b>Antarang Model Analytics</b> • Built with Scikit-Learn, Plotly & Streamlit.
</div>
""", unsafe_allow_html=True)
