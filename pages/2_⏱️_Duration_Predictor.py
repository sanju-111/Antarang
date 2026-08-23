# ============================================================
# ANTARANG - DURATION PREDICTOR PAGE
# AI-Powered Judiciary Case Timeline & Duration Forecast
# ============================================================

import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Ensure utils can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import (
    load_model_artifacts,
    load_feature_importance,
    inject_custom_css,
    CASE_TYPES,
    CASE_NAMES,
    STATES,
    COURT_TIERS,
    TIER_LABELS
)

st.set_page_config(
    page_title="Case Duration Predictor | Antarang",
    page_icon="⏱️",
    layout="wide"
)

inject_custom_css()

try:
    st.page_link("app.py", label="← Back to Portal", icon="🏛️")
except Exception:
    pass

# Header Banner
st.markdown("""
<div class="main-header">
    <div class="hero-badge">AI Predictive Engine</div>
    <h1>⏱️ Case Duration Predictor</h1>
    <p>Forecast expected judicial lifecycle, analyze timeline drivers, and assess delay probabilities</p>
</div>
""", unsafe_allow_html=True)

# Load Model
try:
    model, encoders, features = load_model_artifacts()
except Exception as e:
    st.error(f"❌ Could not load AI Model artifacts: {e}")
    st.info("💡 Run `python models/train_model.py` to generate the model artifacts.")
    st.stop()

# Layout: 2 Columns (Input Form on Left, Output & Insights on Right)
col_input, col_output = st.columns([1.1, 1.9], gap="large")

with col_input:
    st.markdown("### 📋 Case Parameters")
    with st.container(border=True):
        case_type = st.selectbox(
            "Case Type / Category",
            CASE_TYPES,
            format_func=lambda x: f"{x} - {CASE_NAMES.get(x, x)}",
            help="Select the category of the legal suit/petition"
        )

        state = st.selectbox(
            "State Jurisdiction",
            STATES,
            index=2,  # Default to Delhi or Andhra
            help="State where the case is filed"
        )

        tier = st.selectbox(
            "Court Hierarchy Level",
            COURT_TIERS,
            format_func=lambda x: TIER_LABELS.get(x, x),
            help="District Court or High Court level"
        )

        filing_date = st.date_input(
            "Case Filing Date",
            value=datetime.today(),
            help="Date when the petition/case was officially registered"
        )

        priority_level = st.radio(
            "Case Priority Flag",
            ["Standard", "Urgent / Senior Citizen / Commercial"],
            index=0,
            horizontal=True
        )

        predict_btn = st.button("🔮 Forecast Duration", type="primary", width="stretch")

# Process Prediction
filing_month = filing_date.month
filing_day = filing_date.day
filing_dayofweek = filing_date.weekday()
filing_year = filing_date.year
is_old_case = 1 if filing_year < 2024 else 0
is_very_old_case = 1 if filing_year < 2020 else 0

try:
    case_encoded = encoders['caseType'].transform([case_type])[0]
    state_encoded = encoders['stateName'].transform([state])[0]
    tier_encoded = encoders['tier'].transform([tier])[0]
except ValueError as e:
    st.error(f"Encoding Error: {e}")
    st.stop()

user_features = [
    case_encoded,
    state_encoded,
    tier_encoded,
    filing_month,
    filing_day,
    filing_dayofweek,
    is_old_case,
    is_very_old_case
]

# Run prediction
pred_log = model.predict([user_features])[0]
pred_days = max(1.0, np.exp(pred_log) - 1)

# Apply priority reduction heuristic for estimation display
if "Urgent" in priority_level:
    pred_days = pred_days * 0.75

with col_output:
    st.markdown("### 📊 Prediction & Timeline Analysis")

    # Main Hero Prediction Card
    months_val = pred_days / 30.4
    years_val = pred_days / 365.25

    if pred_days < 120:
        badge_html = '<span class="badge-fast">⚡ Fast Track Timeline (< 4 Months)</span>'
    elif pred_days < 365:
        badge_html = '<span class="badge-moderate">⏳ Moderate Timeline (4-12 Months)</span>'
    else:
        badge_html = '<span class="badge-high">⚠️ Extended Pendency Timeline (> 1 Year)</span>'

    st.markdown(f"""
    <div class="prediction-hero-card">
        <div class="subtitle">ESTIMATED CASE LIFECYCLE</div>
        <div class="number">{pred_days:.0f} <span style="font-size: 2rem; font-weight: 500;">Days</span></div>
        <div style="font-size: 1.25rem; font-weight: 600; color: #e0e7ff; margin-bottom: 0.8rem;">
            ≈ {months_val:.1f} Months &nbsp;•&nbsp; ≈ {years_val:.2f} Years
        </div>
        <div>{badge_html}</div>
    </div>
    """, unsafe_allow_html=True)

    # 3 Summary Metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Model Confidence (R²)", "75.8%", delta="High Reliability")
    with m2:
        st.metric("Expected Error Margin", "± 10 Months", delta_color="off")
    with m3:
        target_est_date = filing_date + pd.Timedelta(days=int(pred_days))
        st.metric("Est. Resolution Date", target_est_date.strftime("%b %Y"))

    # Case Summary Details
    with st.expander("📋 Detailed Case Profile & Risk Factors", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**Case Category:** {CASE_NAMES.get(case_type, case_type)} (`{case_type}`)")
            st.write(f"**Jurisdiction:** {state}")
            st.write(f"**Court Level:** {TIER_LABELS.get(tier, tier)}")
        with c2:
            st.write(f"**Filing Date:** {filing_date.strftime('%d %B %Y')}")
            st.write(f"**Legacy Status:** {'Pre-2024 Backlog' if is_old_case else 'Active New Case'}")
            st.write(f"**Critical Delay Risk:** {'High (>5 yrs legacy)' if is_very_old_case else 'Low/Normal'}")

    # Visual Gauge / Comparison
    st.markdown("#### ⏱️ Timeline Benchmarking")
    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pred_days,
        title={'text': "Predicted Duration vs National Benchmarks (Days)", 'font': {'size': 14}},
        gauge={
            'axis': {'range': [None, 1200]},
            'bar': {'color': "#4338ca"},
            'steps': [
                {'range': [0, 180], 'color': "#dcfce7"},
                {'range': [180, 500], 'color': "#fef9c3"},
                {'range': [500, 1200], 'color': "#fee2e2"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 730
            }
        }
    ))
    gauge_fig.update_layout(height=230, margin=dict(l=20, r=20, t=30, b=10))
    st.plotly_chart(gauge_fig, width='stretch')

# Feature Importance Breakdown
st.markdown("---")
st.markdown("### 🔑 Key Drivers Influencing This Prediction")

importance_df = load_feature_importance()
if importance_df is not None:
    f_col1, f_col2 = st.columns([1.5, 1])
    with f_col1:
        fig = px.bar(
            importance_df,
            x='Importance',
            y='Feature',
            orientation='h',
            labels={'Importance': 'Relative Contribution (%)', 'Feature': 'Feature Name'},
            color='Importance',
            color_continuous_scale='Blues',
            text=importance_df['Importance'].apply(lambda x: f'{x*100:.1f}%')
        )
        fig.update_layout(height=280, showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, width='stretch')
    with f_col2:
        st.info("""
        **💡 Triage Observations:**
        - **Filing year & backlog age** represent the strongest predictors of prolonged duration.
        - **Case Type (e.g. Bail vs Civil Suit)** significantly determines hearing frequency and prioritization.
        - **State jurisdiction capacity** creates systematic differences in average throughput.
        """)

st.markdown("""
<div class="footer-note">
    ⚖️ <b>Disclaimer</b>: Antarang is an AI-powered triage and workflow optimization assistant built for research and judicial administration.
</div>
""", unsafe_allow_html=True)
