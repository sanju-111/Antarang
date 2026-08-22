# pages/test_lawyer_recommendation.py
import streamlit as st
import pandas as pd
import sys
import os

# Ensure root and models are in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models')))

try:
    from models.lawyer_recommendation import LawyerRecommendationEngine
except ImportError:
    from lawyer_recommendation import LawyerRecommendationEngine

# Initialize the engine
engine = LawyerRecommendationEngine()

# Title
st.set_page_config(page_title="FindMyAdvocate - Your Personal Lawyer Finder", layout="wide")
st.title("FindMyAdvocate")
st.subheader("Empowering Citizens, Empowering Lawyers")

# Sidebar for input parameters
with st.sidebar:
    st.header("Search Filters")
    specializations = engine.get_specializations()
    case_type = st.selectbox('Select Case Type', specializations)
    location = st.text_input('Enter Location', '')
    languages = st.text_input('Languages (comma separated)', 'English')
    min_experience = st.slider('Minimum Years of Experience', 0, 30, 5)
    min_success_rate = st.slider('Minimum Success Rate (%)', 0, 100, 70)
    max_results = st.slider('Number of Lawyers to Recommend', 5, 50, 10)
    sorting = st.radio('Sort By:', ['Experience', 'Success Rate', 'Relevance'])

# Display search filters summary
col1, col2 = st.columns(2)
with col1:
    st.write(f"**Case Type:** {case_type}")
    st.write(f"**Location:** {location if location else 'Any'}")
    st.write(f"**Languages:** {languages if languages else 'Any'}")
    st.write(f"**Experience:** {min_experience}+ years")
    st.write(f"**Success Rate:** {min_success_rate}%+")
with col2:
    st.write(f"**Results:** Showing top {max_results}")
    st.write(f"**Sorted By:** {sorting}")
    st.markdown("---")

# Get recommendations
if languages:
    languages_list = [lang.strip() for lang in languages.split(',') if lang.strip()]
else:
    languages_list = None

sort_map = {'experience': 'experience', 'success rate': 'success', 'relevance': 'relevance'}

with st.spinner('Searching for matching lawyers...'):
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
if len(results) > 0:
    st.success(f"Found {len(results)} matching lawyers!")
    df = results[['lawyer_name', 'specialization', 'location', 'years_experience', 'success_rate']]
    df.columns = ['Name', 'Specialization', 'Location', 'Experience (Years)', 'Success Rate (%)']
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No lawyers found matching the criteria. Try adjusting your filters.")
