# pages/1_⚖️_Mediation_Predictor.py - ANTARANG Mediation Eligibility Predictor
import os
import sys
import pandas as pd
import streamlit as st

# Ensure root and models are in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models')))

# Page Configuration MUST be first Streamlit call
st.set_page_config(
    page_title="ANTARANG - Mediation Predictor",
    page_icon="⚖",
    layout="wide"
)

# Inject luxury styling from styles.py
from styles import inject_luxury_css
inject_luxury_css()

try:
    from models.predict_simple import SimpleMediationPredictor
except ImportError:
    from predict_simple import SimpleMediationPredictor

# Navigation link back to landing portal
try:
    st.page_link("app.py", label="← Back to Portal", icon="🏛️")
except Exception:
    pass

# Header Banner
st.markdown("""
<div class="main-header">
    <div class="hero-badge">ADR Judicial Suite</div>
    <h1>⚖️ Mediation Eligibility Predictor</h1>
    <p>Evaluate dispute suitability for Alternative Dispute Resolution (ADR), forecast settlement probability & audit statutory filings</p>
</div>
""", unsafe_allow_html=True)


# Load predictor
@st.cache_resource
def load_predictor():
    try:
        return SimpleMediationPredictor()
    except Exception as e:
        st.error(f"⚠️ Error loading predictor: {e}")
        return None

predictor = load_predictor()

# Main content
if predictor:
    # Case Type Selection
    with st.container(border=True):
        st.markdown('<p class="section-title">⚜️ Case Classification</p>', unsafe_allow_html=True)
        
        case_type = st.selectbox(
            "Select the type of case",
            predictor.case_types,
            help="Choose the category that best describes your legal dispute"
        )
    # Case Details
    with st.container(border=True):
        st.markdown('<p class="section-title">⚜️ Dispute Parameters</p>', unsafe_allow_html=True)
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown('<p class="form-label"><span class="glyph-icon">⟡</span> Jurisdiction & Location</p>', unsafe_allow_html=True)
            state = st.selectbox("State", predictor.states, label_visibility="collapsed")
            district = st.selectbox("District", predictor.districts.get(state, ['']), label_visibility="collapsed")
            
            st.markdown('<p class="form-label"><span class="glyph-icon">✦</span> Dispute Intensity Level</p>', unsafe_allow_html=True)
            intensity = st.select_slider(
                "Intensity", 
                options=['Low', 'Medium', 'High'], 
                value='Medium',
                label_visibility="collapsed"
            )
            
            st.markdown('<p class="form-label"><span class="glyph-icon">⚖</span> Mediation Willingness (1–10)</p>', unsafe_allow_html=True)
            willingness = st.slider("Willingness", 1, 10, 7, label_visibility="collapsed")
            
            st.markdown('<p class="form-label"><span class="glyph-icon">✧</span> Settlement Possibility (1–10)</p>', unsafe_allow_html=True)
            settlement = st.slider("Settlement", 1, 10, 7, label_visibility="collapsed")
        
        with col_right:
            st.markdown('<p class="form-label"><span class="glyph-icon">§</span> Legal Complexity (1–10)</p>', unsafe_allow_html=True)
            complexity = st.slider("Complexity", 1, 10, 5, label_visibility="collapsed")
            
            st.markdown('<p class="form-label"><span class="glyph-icon">⧗</span> Expected Resolution Time (Days)</p>', unsafe_allow_html=True)
            time_days = st.number_input(
                "Days", 
                min_value=30, 
                max_value=730, 
                value=180, 
                step=30,
                label_visibility="collapsed"
            )
            
            st.markdown('<p class="form-label"><span class="glyph-icon">❖</span> Financial Dispute Impact (1–10)</p>', unsafe_allow_html=True)
            finance = st.slider("Finance", 1, 10, 6, label_visibility="collapsed")
            
            st.markdown('<p class="form-label"><span class="glyph-icon">✦</span> Number of Litigant Parties</p>', unsafe_allow_html=True)
            parties = st.number_input(
                "Parties", 
                min_value=2, 
                max_value=10, 
                value=2, 
                step=1,
                label_visibility="collapsed"
            )
            
    # Advanced Options
    with st.expander("⚜️ Advanced Dispute Diagnostics", expanded=False):
        col_adv1, col_adv2 = st.columns(2)
        with col_adv1:
            urgency = st.slider("Urgency Level (1–10)", 1, 10, 5)
            power = st.slider("Power Imbalance (1–10)", 1, 10, 4)
            legal_awareness = st.slider("Legal Awareness (1–10)", 1, 10, 6)
        with col_adv2:
            access = st.slider("Access to Justice (1–10)", 1, 10, 7)
            past_litigation = st.radio("Past Litigation History?", ['No', 'Yes'], horizontal=True)
            income = st.selectbox("Income Level", ['Low', 'Middle', 'High'])
        
    # Predict Button (Hero Primary Action)
    st.markdown('<div style="text-align: center; padding: 1.2rem 0;">', unsafe_allow_html=True)
    
    if st.button("⚜️ PREDICT ELIGIBILITY", type="primary", width='stretch'):
        # Prepare data
        case_data = {
            'case_type': case_type,
            'state': state,
            'district': district,
            'intensity_level': intensity,
            'mediation_willingness': willingness,
            'settlement_possibility': settlement,
            'legal_complexity': complexity,
            'time_to_resolve_days': time_days,
            'financial_impact': finance,
            'number_of_parties': parties,
            'urgency_level': urgency if 'urgency' in locals() else 5,
            'power_imbalance': power if 'power' in locals() else 4,
            'past_litigation_history': past_litigation if 'past_litigation' in locals() else 'No',
            'legal_awareness': legal_awareness if 'legal_awareness' in locals() else 6,
            'access_to_justice': access if 'access' in locals() else 7,
            'income_level': income if 'income' in locals() else 'Middle',
            'residence_type': 'Urban'
        }
        
        with st.spinner("🔮 Evaluating dispute against ADR resolution matrix..."):
            result = predictor.predict(case_data)
            
        # Display Results
        with st.container(border=True):
            st.markdown('<p class="section-title">⚜️ Prediction Results & ADR Assessment</p>', unsafe_allow_html=True)
            
            rec = result['recommendations']
            result_class = "result-eligible" if result['prediction'] == 'Yes' else "result-conditional" if result['prediction'] == 'Conditional' else "result-not-eligible"
            
            st.markdown(f"""
            <div class="result-card {result_class}">
                <h2 style="color: {rec['color']}; font-size: 2.3rem; margin-bottom: 0.5rem; font-family: 'Cormorant Garamond', Georgia, serif;">
                    {rec['title']}
                </h2>
                <p style="color: #F3F0E7; font-size: 1.1rem; max-width: 750px; margin: 0 auto; line-height: 1.6;">
                    {rec['message']}
                </p>
                <div style="margin: 1.8rem auto 0 auto; max-width: 400px;">
                    <div style="color: #A69C86; font-size: 0.78rem; letter-spacing: 0.2em; text-transform: uppercase;">
                        Model Confidence
                    </div>
                    <div style="font-size: 2.8rem; color: #F0D67B; font-weight: 700; font-family: 'Cormorant Garamond', serif;">
                        {result['confidence']:.1f}%
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Probability Distribution
            st.markdown('<p style="color: #F0D67B; margin-top: 1.8rem; font-weight: 600; font-size: 0.9rem; letter-spacing: 0.1em; text-transform: uppercase;">Outcome Probability Distribution</p>', unsafe_allow_html=True)
            
            prob_df = pd.DataFrame({
                'Eligibility': list(result['probabilities'].keys()),
                'Probability': list(result['probabilities'].values())
            })
            
            st.dataframe(
                prob_df,
                column_config={
                    "Eligibility": "Eligibility Tier",
                    "Probability": st.column_config.NumberColumn(
                        "Probability (%)",
                        format="%.1f %%"
                    )
                },
                hide_index=True,
                width='stretch'
            )
            
            # Recommendations
            st.markdown(f"""
            <div style="margin-top: 1.5rem; padding: 1.5rem; background: #181818; border-radius: 12px; border-left: 4px solid {rec['color']}; border: 1px solid rgba(201,162,39,0.25);">
                <p style="color: #F0D67B; font-size: 0.85rem; letter-spacing: 0.15em; font-weight: 700; text-transform: uppercase;">RECOMMENDED NEXT STEPS</p>
                <ul style="color: #F3F0E7; list-style: none; padding-left: 0; margin-top: 0.8rem;">
                    {''.join([f'<li style="padding: 0.4rem 0; font-size: 0.95rem;">▸ {action}</li>' for action in rec['actions']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
else:
    st.error("⚠️ Could not load the predictor. Please check the models folder.")

# Footer
st.markdown("""
<div class="footer">
    <span>⚜️</span> ANTARANG · Mediation Eligibility Predictor <span>⚜️</span><br>
    Powered by AI Triage Engine · 26 Case Categories
</div>
""", unsafe_allow_html=True)
