# pages/1_Mediation_Predictor.py - ANTARANG Mediation Eligibility Predictor
import streamlit as st
import pandas as pd
import sys
import os

# Ensure root and models are in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models')))

try:
    from models.predict_simple import SimpleMediationPredictor
except ImportError:
    from predict_simple import SimpleMediationPredictor

st.set_page_config(
    page_title="ANTARANG - Mediation Predictor",
    page_icon="⚖️",
    layout="wide"
)

# Custom CSS - Black, White & Gold Theme
st.markdown("""
<style>
    .stApp { background-color: #0a0a0a; color: #f5f5f5; }
    
    .header-container {
        padding: 2rem 0 1rem 0;
        border-bottom: 1px solid rgba(212,175,55,0.15);
        text-align: center;
    }
    
    .brand-title {
        font-size: 3rem;
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
        font-size: 1.4rem;
        font-weight: 500;
        letter-spacing: 2px;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid rgba(212,175,55,0.15);
        padding-bottom: 0.8rem;
    }
    
    .form-label {
        color: rgba(255,255,255,0.8);
        font-size: 0.85rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    
    .result-card {
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(212,175,55,0.2);
    }
    
    .result-eligible {
        border-color: #D4AF37;
        background: rgba(212,175,55,0.08);
    }
    
    .result-conditional {
        border-color: #C0A030;
        background: rgba(192,160,48,0.08);
    }
    
    .result-not-eligible {
        border-color: rgba(220,53,69,0.6);
        background: rgba(220,53,69,0.08);
    }
    
    .confidence-bar {
        background: rgba(255,255,255,0.08);
        border-radius: 50px;
        height: 10px;
        overflow: hidden;
        margin-top: 0.5rem;
    }
    
    .confidence-fill {
        height: 100%;
        background: linear-gradient(90deg, #D4AF37, #F4E4A0);
        border-radius: 50px;
        transition: width 1s ease;
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

<div style="text-align: center; padding: 1rem 0;">
    <div style="font-size: 3rem; color: #D4AF37;">⚖️</div>
    <div class="brand-title">ANTARANG</div>
    <div class="brand-subtitle">⚜️ MEDIATION ELIGIBILITY PREDICTOR ⚜️</div>
    <div class="gold-line"></div>
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
col1, col2, col3 = st.columns([1, 10, 1])

with col2:
    if predictor:
        # Case Type Selection
        with st.container():
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.markdown('<p class="section-title">⚜️ Case Type Selection</p>', unsafe_allow_html=True)
            
            case_type = st.selectbox(
                "Select the type of case",
                predictor.case_types,
                help="Choose the category that best describes your legal dispute"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Case Details
        with st.container():
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.markdown('<p class="section-title">⚜️ Case Details</p>', unsafe_allow_html=True)
            
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.markdown('<p class="form-label">📍 Location</p>', unsafe_allow_html=True)
                state = st.selectbox("State", predictor.states, label_visibility="collapsed")
                district = st.selectbox("District", predictor.districts.get(state, ['']), label_visibility="collapsed")
                
                st.markdown('<p class="form-label">⚡ Intensity Level</p>', unsafe_allow_html=True)
                intensity = st.select_slider(
                    "Intensity", 
                    options=['Low', 'Medium', 'High'], 
                    value='Medium',
                    label_visibility="collapsed"
                )
                
                st.markdown('<p class="form-label">🤝 Mediation Willingness (1-10)</p>', unsafe_allow_html=True)
                willingness = st.slider("Willingness", 1, 10, 7, label_visibility="collapsed")
                
                st.markdown('<p class="form-label">📊 Settlement Possibility (1-10)</p>', unsafe_allow_html=True)
                settlement = st.slider("Settlement", 1, 10, 7, label_visibility="collapsed")
            
            with col_right:
                st.markdown('<p class="form-label">⚖️ Legal Complexity (1-10)</p>', unsafe_allow_html=True)
                complexity = st.slider("Complexity", 1, 10, 5, label_visibility="collapsed")
                
                st.markdown('<p class="form-label">📅 Time to Resolve (Days)</p>', unsafe_allow_html=True)
                time_days = st.number_input(
                    "Days", 
                    min_value=30, 
                    max_value=730, 
                    value=180, 
                    step=30,
                    label_visibility="collapsed"
                )
                
                st.markdown('<p class="form-label">💰 Financial Impact (1-10)</p>', unsafe_allow_html=True)
                finance = st.slider("Finance", 1, 10, 6, label_visibility="collapsed")
                
                st.markdown('<p class="form-label">📋 Number of Parties</p>', unsafe_allow_html=True)
                parties = st.number_input(
                    "Parties", 
                    min_value=2, 
                    max_value=10, 
                    value=2, 
                    step=1,
                    label_visibility="collapsed"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Advanced Options
        with st.expander("⚜️ Advanced Details", expanded=False):
            col_adv1, col_adv2 = st.columns(2)
            with col_adv1:
                urgency = st.slider("Urgency Level (1-10)", 1, 10, 5)
                power = st.slider("Power Imbalance (1-10)", 1, 10, 4)
                legal_awareness = st.slider("Legal Awareness (1-10)", 1, 10, 6)
            with col_adv2:
                access = st.slider("Access to Justice (1-10)", 1, 10, 7)
                past_litigation = st.radio("Past Litigation History?", ['No', 'Yes'], horizontal=True)
                income = st.selectbox("Income Level", ['Low', 'Middle', 'High'])
        
        # Predict Button
        st.markdown('<div style="text-align: center; padding: 1rem 0;">', unsafe_allow_html=True)
        
        if st.button("⚜️ PREDICT ELIGIBILITY", type="primary", use_container_width=True):
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
            
            with st.spinner("🔮 Analyzing your case..."):
                result = predictor.predict(case_data)
            
            # Display Results
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.markdown('<p class="section-title">⚜️ Prediction Results</p>', unsafe_allow_html=True)
            
            rec = result['recommendations']
            result_class = "result-eligible" if result['prediction'] == 'Yes' else "result-conditional" if result['prediction'] == 'Conditional' else "result-not-eligible"
            
            st.markdown(f"""
            <div class="result-card {result_class}">
                <h2 style="color: {rec['color']}; font-size: 2.2rem; margin-bottom: 0.5rem;">
                    {rec['title']}
                </h2>
                <p style="color: rgba(255,255,255,0.85); font-size: 1.1rem;">
                    {rec['message']}
                </p>
                <div style="margin: 1.5rem 0;">
                    <div style="color: rgba(255,255,255,0.5); font-size: 0.8rem; letter-spacing: 1px;">
                        CONFIDENCE
                    </div>
                    <div style="font-size: 2.5rem; color: #D4AF37; font-weight: 700;">
                        {result['confidence']:.1f}%
                    </div>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: {result['confidence']}%;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Probability Distribution
            st.markdown('<p style="color: rgba(255,255,255,0.7); margin-top: 1.5rem; font-weight: 600;">Probability Distribution</p>', unsafe_allow_html=True)
            
            prob_df = pd.DataFrame({
                'Eligibility': list(result['probabilities'].keys()),
                'Probability': list(result['probabilities'].values())
            })
            
            st.bar_chart(prob_df.set_index('Eligibility'))
            
            st.dataframe(
                prob_df,
                column_config={
                    "Eligibility": "Eligibility",
                    "Probability": st.column_config.NumberColumn(
                        "Probability (%)",
                        format="%.1f %%"
                    )
                },
                hide_index=True,
                use_container_width=True
            )
            
            # Recommendations
            st.markdown(f"""
            <div style="margin-top: 1.5rem; padding: 1.5rem; background: rgba(255,255,255,0.02); border-radius: 12px; border-left: 4px solid {rec['color']};">
                <p style="color: #D4AF37; font-size: 0.9rem; letter-spacing: 1px; font-weight: 600;">RECOMMENDED NEXT STEPS</p>
                <ul style="color: rgba(255,255,255,0.85); list-style: none; padding-left: 0;">
                    {''.join([f'<li style="padding: 0.4rem 0;">▸ {action}</li>' for action in rec['actions']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("⚠️ Could not load the predictor. Please check the models folder.")

# Footer
st.markdown("""
<div class="footer">
    <span>⚜️</span> ANTARANG · Mediation Eligibility Predictor <span>⚜️</span><br>
    Powered by AI Triage Engine · 26 Case Categories
</div>
""", unsafe_allow_html=True)
