# pages/3_Find_My_Advocate.py - ANTARANG Lawyer Recommendation Engine
import streamlit as st
import pandas as pd
import sys
import os

# Ensure root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models')))

try:
    from models.lawyer_recommendation import LawyerRecommendationEngine
except ImportError:
    from lawyer_recommendation import LawyerRecommendationEngine

from utils.helpers import inject_custom_css

st.set_page_config(
    page_title="ANTARANG - Find My Advocate",
    page_icon="👨‍⚖️",
    layout="wide"
)

inject_custom_css()

try:
    st.page_link("app.py", label="← Back to Portal", icon="🏛️")
except Exception:
    pass

st.markdown("""
<div class="main-header">
    <div class="hero-badge">Advocate Discovery Engine</div>
    <h1>👨‍⚖️ Find My Advocate & Specialist Match</h1>
    <p>Intelligent lawyer matching algorithm tailored by legal domain expertise, court jurisdiction, fee budget, and language</p>
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

if engine:
    with st.container(border=True):
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
    with st.container(border=True):
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
            
            st.dataframe(df_display, width=1200, hide_index=True)
        else:
            st.error("⚠️ No advocates found matching your criteria. Try adjusting the filters.")

# Footer
st.markdown("""
<div class="footer">
    <span>⚜️</span> ANTARANG · Find My Advocate <span>⚜️</span><br>
    Empowering Citizens · Connecting Verified Legal Counsel
</div>
""", unsafe_allow_html=True)
