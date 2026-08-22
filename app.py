# ============================================================
# ANTARANG - AI-POWERED JUDICIAL TRIAGE SYSTEM
# Master Portal & Executive Command Center
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Page Configuration
st.set_page_config(
    page_title="ANTARANG - Justice Decoded",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Luxury Black, Gold & Platinum Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
    }

    .hero-glow {
        background: radial-gradient(ellipse at 50% -20%, rgba(212, 175, 55, 0.15) 0%, rgba(99, 102, 241, 0.08) 50%, transparent 80%);
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 600px;
        pointer-events: none;
        z-index: 0;
    }

    .hero-container {
        padding: 2.5rem 1rem 2rem 1rem;
        text-align: center;
        position: relative;
        z-index: 1;
    }

    .brand-title {
        font-size: 3.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #D4AF37 0%, #FFF2B2 50%, #D4AF37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-bottom: 0.2rem;
    }

    .brand-tagline {
        color: #D4AF37;
        font-size: 1.05rem;
        letter-spacing: 5px;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }

    .brand-sub {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1.05rem;
        max-width: 800px;
        margin: 0 auto 1.5rem auto;
        line-height: 1.6;
    }

    .gold-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #D4AF37 25%, #D4AF37 75%, transparent 100%);
        width: 60%;
        margin: 1.5rem auto 2.5rem auto;
        opacity: 0.4;
    }

    .feature-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 18px;
        padding: 1.8rem 1.4rem;
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .feature-card:hover {
        transform: translateY(-5px);
        border-color: #D4AF37;
        box-shadow: 0 12px 30px rgba(212, 175, 55, 0.15);
        background: rgba(212, 175, 55, 0.04);
    }

    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 0.8rem;
    }

    .card-title {
        color: #D4AF37;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.6rem;
    }

    .card-desc {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
        line-height: 1.5;
        margin-bottom: 1.2rem;
    }

    .stats-bar {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(212, 175, 55, 0.15);
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 2.5rem;
        text-align: center;
    }

    .stat-val {
        font-size: 2rem;
        font-weight: 800;
        color: #D4AF37;
    }

    .stat-label {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.6);
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 0.3rem;
    }

    .footer {
        text-align: center;
        padding: 3rem 0 2rem 0;
        border-top: 1px solid rgba(212, 175, 55, 0.1);
        color: rgba(255, 255, 255, 0.4);
        font-size: 0.8rem;
        letter-spacing: 2px;
        margin-top: 3rem;
    }
</style>

<div class="hero-glow"></div>

<div class="hero-container">
    <div style="font-size: 3.2rem; margin-bottom: 0.3rem;">⚖️</div>
    <div class="brand-title">ANTARANG</div>
    <div class="brand-tagline">⚜️ JUSTICE DECODED · JUDICIAL TRIAGE SUITE ⚜️</div>
    <p class="brand-sub">
        An end-to-end AI judicial intelligence system built to evaluate ADR mediation suitability, 
        predict case resolution lifecycles, audit statutory document filings, balance court loads, 
        and match litigants with verified domain-specialist advocates.
    </p>
    <div class="gold-divider"></div>
</div>
""", unsafe_allow_html=True)

# Grid Layout of All 6 Modules
r1_c1, r1_c2, r1_c3 = st.columns(3)

with r1_c1:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="card-icon">⚖️</div>
            <div class="card-title">1. Mediation Predictor</div>
            <div class="card-desc">
                Evaluate legal dispute suitability for Alternative Dispute Resolution (ADR) & Mediation using AI trained on 26 distinct case categories.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_⚖️_Mediation_Predictor.py", label="Open Mediation Predictor →", icon="⚖️", use_container_width=True)

with r1_c2:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="card-icon">⏱️</div>
            <div class="card-title">2. Duration Predictor</div>
            <div class="card-desc">
                Forecast case resolution timeline (days, months, years) using Random Forest regression across case types, filing dates, and judicial tiers.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_⏱️_Duration_Predictor.py", label="Open Duration Predictor →", icon="⏱️", use_container_width=True)

with r1_c3:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="card-icon">📋</div>
            <div class="card-title">3. Documents Checklist</div>
            <div class="card-desc">
                Instant statutory checklist of mandatory petitions, annexures, notarization requirements, stamp duties, and court compliance guidelines.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_📋_Documents_Checklist.py", label="Open Documents Checklist →", icon="📋", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

r2_c1, r2_c2, r2_c3 = st.columns(3)

with r2_c1:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="card-icon">🏛️</div>
            <div class="card-title">4. Court Load Indicator</div>
            <div class="card-desc">
                Real-time court capacity & pendency analytics. Identify overloaded vs fast-track benches against national disposal benchmarks with CSV export.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/4_🏛️_Court_Load_Indicator.py", label="Open Court Load Indicator →", icon="🏛️", use_container_width=True)

with r2_c2:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="card-icon">👨‍⚖️</div>
            <div class="card-title">5. Find My Advocate</div>
            <div class="card-desc">
                Intelligent lawyer recommendation engine matching litigants with top advocates filtered by jurisdiction, language, experience, and win rate.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/5_👨‍⚖️_Find_My_Advocate.py", label="Find Legal Advocate →", icon="👨‍⚖️", use_container_width=True)

with r2_c3:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="card-icon">📊</div>
            <div class="card-title">6. Model Analytics & XAI</div>
            <div class="card-desc">
                Inspect machine learning model performance, feature importance rankings, regression diagnostics, and training dataset distributions.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/6_📊_Model_Analytics.py", label="View Model Analytics →", icon="📊", use_container_width=True)

# System Metrics Bar
st.markdown("""
<div class="stats-bar">
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 1rem;">
        <div>
            <div class="stat-val">5,000+</div>
            <div class="stat-label">Mediation Scenarios</div>
        </div>
        <div>
            <div class="stat-val">3,296</div>
            <div class="stat-label">Historical Case Records</div>
        </div>
        <div>
            <div class="stat-val">100+</div>
            <div class="stat-label">Document Checklists</div>
        </div>
        <div>
            <div class="stat-val">19</div>
            <div class="stat-label">States & Jurisdictions</div>
        </div>
        <div>
            <div class="stat-val">77.8%</div>
            <div class="stat-label">ML Prediction R² Score</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <span>⚜️</span> ANTARANG · Judicial Triage System · Tech Fusion 2026 <span>⚜️</span><br>
    Select any module from the sidebar navigation or click the cards above to begin
</div>
""", unsafe_allow_html=True)

def main():
    print("Welcome to the Judicial Triage System - ANTARANG")

if __name__ == "__main__":
    main()