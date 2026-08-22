# app.py - ANTARANG: Judicial Triage System & Legal AI Portal
import streamlit as st
import os
import sys

# Page Configuration
st.set_page_config(
    page_title="ANTARANG - Justice Decoded",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Luxury Black & Gold Theme
st.markdown("""
<style>
    .stApp {
        background-color: #0a0a0a;
        color: #f5f5f5;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .gold-glow {
        background: radial-gradient(ellipse at 50% 0%, rgba(212,175,55,0.12) 0%, transparent 70%);
        position: fixed; top: 0; left: 0; right: 0; height: 500px;
        pointer-events: none; z-index: 0;
    }
    
    .hero-container {
        padding: 3rem 1rem 2rem 1rem;
        text-align: center;
        position: relative;
        z-index: 1;
    }
    
    .brand-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #D4AF37 0%, #FFF2B2 50%, #D4AF37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 6px;
        text-transform: uppercase;
        margin-bottom: 0.2rem;
    }
    
    .brand-tagline {
        color: #D4AF37;
        font-size: 1.1rem;
        letter-spacing: 6px;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }
    
    .brand-sub {
        color: rgba(255,255,255,0.65);
        font-size: 1rem;
        max-width: 750px;
        margin: 0 auto 1.5rem auto;
        line-height: 1.6;
    }
    
    .gold-line {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #D4AF37 20%, #D4AF37 80%, transparent 100%);
        width: 60%;
        margin: 1.5rem auto 2.5rem auto;
        opacity: 0.4;
    }
    
    .feature-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(212,175,55,0.2);
        border-radius: 16px;
        padding: 2rem 1.5rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .feature-card:hover {
        transform: translateY(-6px);
        border-color: #D4AF37;
        box-shadow: 0 12px 30px rgba(212,175,55,0.15);
        background: rgba(212,175,55,0.04);
    }
    
    .card-icon {
        font-size: 2.8rem;
        margin-bottom: 1rem;
    }
    
    .card-title {
        color: #D4AF37;
        font-size: 1.35rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        letter-spacing: 1px;
    }
    
    .card-desc {
        color: rgba(255,255,255,0.7);
        font-size: 0.92rem;
        line-height: 1.5;
        margin-bottom: 1.5rem;
    }
    
    .stats-container {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(212,175,55,0.12);
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 3rem;
        text-align: center;
    }
    
    .stat-num {
        font-size: 2rem;
        font-weight: 700;
        color: #D4AF37;
    }
    
    .stat-label {
        font-size: 0.75rem;
        color: rgba(255,255,255,0.5);
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 0.3rem;
    }
    
    .footer {
        text-align: center;
        padding: 3rem 0 2rem 0;
        border-top: 1px solid rgba(212,175,55,0.1);
        color: rgba(255,255,255,0.4);
        font-size: 0.8rem;
        letter-spacing: 2px;
        margin-top: 3rem;
    }
    
    .footer span {
        color: #D4AF37;
    }
</style>

<div class="gold-glow"></div>

<div class="hero-container">
    <div style="font-size: 3.5rem; color: #D4AF37; margin-bottom: 0.5rem;">⚖️</div>
    <div class="brand-title">ANTARANG</div>
    <div class="brand-tagline">⚜️ JUSTICE DECODED · JUDICIAL TRIAGE SYSTEM ⚜️</div>
    <p class="brand-sub">
        An intelligent AI-powered legal triage suite designed to evaluate ADR dispute suitability, 
        streamline mandatory document readiness, and match citizens with verified domain-specialist advocates.
    </p>
    <div class="gold-line"></div>
</div>
""", unsafe_allow_html=True)

# Main Grid Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="card-icon">⚖️</div>
            <div class="card-title">Mediation Predictor</div>
            <div class="card-desc">
                Evaluate whether your legal dispute is eligible for Alternative Dispute Resolution (ADR) & Mediation using predictive intelligence trained across 26 case categories.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_⚖️_Mediation_Predictor.py", label="Launch Mediation Predictor →", icon="⚖️", use_container_width=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="card-icon">📋</div>
            <div class="card-title">Documents Checklist</div>
            <div class="card-desc">
                Instant statutory checklist of mandatory filings, optional annexures, notarization rules, stamp duties, and court presentation standards.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_📋_Documents_Checklist.py", label="Open Documents Checklist →", icon="📋", use_container_width=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div>
            <div class="card-icon">👨‍⚖️</div>
            <div class="card-title">Find My Advocate</div>
            <div class="card-desc">
                Intelligent matchmaking engine connecting litigators with verified legal advocates filtered by jurisdiction, language, years of experience, and historical success rates.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_👨‍⚖️_Find_My_Advocate.py", label="Find Legal Advocate →", icon="👨‍⚖️", use_container_width=True)

# System Metrics Bar
st.markdown("""
<div class="stats-container">
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 1rem;">
        <div>
            <div class="stat-num">26</div>
            <div class="stat-label">Legal Dispute Categories</div>
        </div>
        <div>
            <div class="stat-num">100+</div>
            <div class="stat-label">Verified Document Checklists</div>
        </div>
        <div>
            <div class="stat-num">5,000+</div>
            <div class="stat-label">Trained Mediation Scenarios</div>
        </div>
        <div>
            <div class="stat-num">14+</div>
            <div class="stat-label">States & Jurisdictions</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <span>⚜️</span> ANTARANG · Judicial Triage System · Antarang Project <span>⚜️</span><br>
    Select any module from the left sidebar navigation to begin
</div>
""", unsafe_allow_html=True)

def main():
    print("Welcome to the Judicial Triage System - ANTARANG")

if __name__ == "__main__":
    main()
