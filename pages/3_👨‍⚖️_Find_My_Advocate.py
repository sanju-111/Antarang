# pages/3_👨‍⚖️_Find_My_Advocate.py - ANTARANG Lawyer Recommendation Engine
import streamlit as st
import pandas as pd
import sys
import os

# Ensure root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.lawyer_recommendation import LawyerRecommendationEngine

st.set_page_config(
    page_title="ANTARANG - Find My Advocate",
    page_icon="👨‍⚖️",
    layout="wide"
)

# Custom CSS - Black, White & Gold Theme
st.markdown("""
<style>
    .stApp { background-color: #0a0a0a; color: #f5f5f5; }
    
    .gold-glow {
        background: radial-gradient(ellipse at 50% 0%, rgba(212,175,55,0.08) 0%, transparent 70%);
        position: fixed; top: 0; left: 0; right: 0; height: 400px;
        pointer-events: none; z-index: 0;
    }
    
    .header-container {
        padding: 2rem 0 1rem 0;
        border-bottom: 1px solid rgba(212,175,55,0.15);
        position: relative; z-index: 1;
        text-align: center;
    }
    
    .brand-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #D4AF37 0%, #F4E4A0 50%, #D4AF37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 4px;
        text-transform: uppercase;
    }
    
    .brand-subtitle {
        color: rgba(255,255,255,0.6);
        font-size: 0.9rem;
        letter-spacing: 6px;
        margin-top: -8px;
    }
    
    .gold-line {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #D4AF37 20%, #D4AF37 80%, transparent 100%);
        width: 60%;
        margin: 0.8rem auto;
        opacity: 0.3;
    }
    
    .card-container {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(212,175,55,0.15);
        border-radius: 16px;
        padding: 2rem;
        backdrop-filter: blur(10px);
        margin-bottom: 2rem;
    }
    
    .section-title {
        color: #D4AF37;
        font-size: 1.5rem;
        font-weight: 500;
        letter-spacing: 2px;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid rgba(212,175,55,0.15);
        padding-bottom: 0.8rem;
    }
    
    .footer {
        text-align: center;
        padding: 2rem 0;
        border-top: 1px solid rgba(212,175,55,0.1);
        color: rgba(255,255,255,0.4);
        font-size: 0.75rem;
        letter-spacing: 2px;
    }
    
    .footer span {
        color: #D4AF37;
    }
</style>

<div class="gold-glow"></div>
<div class="header-container">
    <div style="font-size: 2.8rem; color: #D4AF37;">👨‍⚖️</div>
    <div class="brand-title">ANTARANG</div>
    <div class="brand-subtitle">⚜️ FIND MY ADVOCATE ⚜️</div>
    <div class="gold-line"></div>
</div>
""", unsafe_allow_html=True)

# Initialize engine
@st.cache_resource
def load_engine():
    try:
        return LawyerRecommendationEngine()
    except Exception as e:
        st.error(f"⚠️ Error loading advocate database: {e}")
        return None

engine = load_engine()

col1, col2, col3 = st.columns([1, 10, 1])

with col2:
    if engine:
        with st.container():
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.markdown('<p class="section-title">⚜️ Advocate Search Filters</p>', unsafe_allow_html=True)
            
            col_f1, col_f2 = st.columns(2)
            
            with col_f1:
                specializations = engine.get_specializations()
                case_type = st.selectbox('Select Case Type / Specialization', specializations)
                location = st.text_input('Enter City / Location (e.g. Mumbai, Delhi)', '')
                languages = st.text_input('Languages (comma separated)', 'English, Hindi')
            
            with col_f2:
                min_experience = st.slider('Minimum Years of Experience', 0, 30, 5)
                min_success_rate = st.slider('Minimum Success Rate (%)', 0, 100, 70)
                max_results = st.slider('Number of Lawyers to Recommend', 5, 50, 10)
                sorting = st.radio('Sort By:', ['Relevance', 'Experience', 'Success Rate'], horizontal=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

        # Get recommendations
        if languages:
            languages_list = [lang.strip() for lang in languages.split(',') if lang.strip()]
        else:
            languages_list = None

        sort_map = {'experience': 'experience', 'success rate': 'success', 'relevance': 'relevance'}

        with st.spinner('🔍 Searching for matching legal advocates...'):
            results = engine.recommend_lawyers(
                case_type=case_type,
                location=location if location else None,
                languages=languages_list,
                min_experience=min_experience,
                min_success=min_success_rate,
                max_results=max_results,
                sort_by=sort_map.get(sorting.lower(), 'relevance')
            )

        # Display results
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.markdown('<p class="section-title">⚜️ Matching Advocates</p>', unsafe_allow_html=True)
        
        if len(results) > 0:
            st.success(f"✅ Found {len(results)} verified legal advocates matching your criteria!")
            
            display_cols = ['lawyer_name', 'specialization', 'location', 'years_experience', 'success_rate']
            if 'relevance_score' in results.columns:
                display_cols.append('relevance_score')
                
            df_display = results[display_cols].copy()
            rename_map = {
                'lawyer_name': 'Advocate Name',
                'specialization': 'Specialization',
                'location': 'Location',
                'years_experience': 'Experience (Yrs)',
                'success_rate': 'Success Rate (%)',
                'relevance_score': 'Relevance Match (%)'
            }
            df_display = df_display.rename(columns=rename_map)
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        else:
            st.warning("⚠️ No lawyers found matching the exact criteria. Try adjusting your location or filter thresholds.")
            
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <span>⚜️</span> ANTARANG · Find My Advocate <span>⚜️</span><br>
    Empowering Citizens · Connecting Verified Legal Counsel
</div>
""", unsafe_allow_html=True)
