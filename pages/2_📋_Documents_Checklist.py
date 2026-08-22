# pages/2_📋_Documents_Checklist.py - ANTARANG Documents Checklist
import streamlit as st
import pandas as pd
import sys
import os

# Ensure root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.predict_documents import DocumentPredictor

# Page Configuration
st.set_page_config(
    page_title="ANTARANG - Documents Checklist",
    page_icon="📋",
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
    
    .doc-item {
        padding: 0.8rem 1.2rem;
        margin-bottom: 0.6rem;
        background: rgba(255,255,255,0.04);
        border-left: 4px solid #D4AF37;
        border-radius: 6px;
        color: rgba(255,255,255,0.9);
        transition: all 0.2s ease;
    }
    
    .doc-item:hover {
        background: rgba(212,175,55,0.08);
        border-left-color: #F4E4A0;
        padding-left: 1.5rem;
    }
    
    .info-box {
        background: rgba(212,175,55,0.05);
        border: 1px solid rgba(212,175,55,0.15);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1.5rem 0;
        color: rgba(255,255,255,0.85);
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
    <div style="font-size: 2.8rem; color: #D4AF37;">📋</div>
    <div class="brand-title">ANTARANG</div>
    <div class="brand-subtitle">⚜️ CASE DOCUMENTS CHECKLIST ⚜️</div>
    <div class="gold-line"></div>
</div>
""", unsafe_allow_html=True)

# Load predictor
@st.cache_resource
def load_predictor():
    return DocumentPredictor()

try:
    predictor = load_predictor()
    predictor_loaded = True
except Exception as e:
    predictor_loaded = False
    st.error(f"⚠️ Could not load document mappings: {e}")

col1, col2, col3 = st.columns([1, 10, 1])

with col2:
    if predictor_loaded:
        # Search Section
        with st.container():
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.markdown('<p class="section-title">⚜️ Select Case Type</p>', unsafe_allow_html=True)
            
            selected_case = st.selectbox(
                "Choose the legal dispute category",
                predictor.case_types,
                help="Select your case category to see all mandatory and optional legal documents"
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Documents Display
        doc_data = predictor.get_documents(selected_case)
        
        if doc_data:
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.markdown('<p class="section-title">⚜️ Document Requirements</p>', unsafe_allow_html=True)
            
            # Case Info
            st.markdown(f"""
            <div style="display: flex; flex-wrap: wrap; gap: 2rem; margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid rgba(212,175,55,0.1);">
                <div>
                    <span style="color: rgba(255,255,255,0.4); font-size: 0.75rem; text-transform: uppercase;">Case Type</span>
                    <div style="color: #D4AF37; font-size: 1.25rem; font-weight: 600;">{selected_case}</div>
                </div>
                <div>
                    <span style="color: rgba(255,255,255,0.4); font-size: 0.75rem; text-transform: uppercase;">Domain</span>
                    <div style="color: rgba(255,255,255,0.9); font-size: 1.1rem;">{doc_data['domain']}</div>
                </div>
                <div>
                    <span style="color: rgba(255,255,255,0.4); font-size: 0.75rem; text-transform: uppercase;">Category</span>
                    <div style="color: rgba(255,255,255,0.9); font-size: 1.1rem;">{doc_data['category']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Required Documents
            st.markdown('<p style="color: #D4AF37; font-size: 1rem; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 0.8rem; font-weight: 600;">Mandatory Documents</p>', unsafe_allow_html=True)
            
            for doc in doc_data['required_documents']:
                st.markdown(f'<div class="doc-item">📌 {doc}</div>', unsafe_allow_html=True)
            
            # Optional Documents
            if doc_data['optional_documents']:
                st.markdown('<p style="color: rgba(255,255,255,0.5); font-size: 0.9rem; letter-spacing: 1px; text-transform: uppercase; margin-top: 1.5rem; margin-bottom: 0.8rem; font-weight: 600;">Supporting / Optional Documents</p>', unsafe_allow_html=True)
                for doc in doc_data['optional_documents']:
                    st.markdown(f'<div class="doc-item" style="opacity: 0.8; border-left-color: rgba(212,175,55,0.4);">📎 {doc}</div>', unsafe_allow_html=True)
            
            # Requirements
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            
            col_info1, col_info2, col_info3 = st.columns(3)
            with col_info1:
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="color: rgba(255,255,255,0.4); font-size: 0.7rem; text-transform: uppercase;">Time Validity</div>
                    <div style="color: #D4AF37; font-size: 1rem; font-weight: 600;">{doc_data['time_validity']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_info2:
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="color: rgba(255,255,255,0.4); font-size: 0.7rem; text-transform: uppercase;">Submission Deadline</div>
                    <div style="color: #D4AF37; font-size: 1rem; font-weight: 600;">{doc_data['submission_deadline']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_info3:
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="color: rgba(255,255,255,0.4); font-size: 0.7rem; text-transform: uppercase;">Number of Copies</div>
                    <div style="color: #D4AF37; font-size: 1rem; font-weight: 600;">{doc_data['number_of_copies']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            col_info4, col_info5 = st.columns(2)
            with col_info4:
                st.markdown(f"""
                <div style="text-align: center; margin-top: 1rem;">
                    <div style="color: rgba(255,255,255,0.4); font-size: 0.7rem; text-transform: uppercase;">Stamp Duty Required</div>
                    <div style="color: {'#D4AF37' if doc_data['stamp_duty_required'] == 'Yes' else 'rgba(255,255,255,0.5)'}; font-weight: 600;">{doc_data['stamp_duty_required']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_info5:
                st.markdown(f"""
                <div style="text-align: center; margin-top: 1rem;">
                    <div style="color: rgba(255,255,255,0.4); font-size: 0.7rem; text-transform: uppercase;">Notarization Required</div>
                    <div style="color: {'#D4AF37' if doc_data['notarization_required'] == 'Yes' else 'rgba(255,255,255,0.5)'}; font-weight: 600;">{doc_data['notarization_required']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Format Requirements
            st.markdown(f"""
            <div style="margin-top: 1rem; padding: 1.2rem; background: rgba(255,255,255,0.02); border-radius: 8px; border-left: 3px solid #D4AF37;">
                <div style="color: #D4AF37; font-size: 0.75rem; text-transform: uppercase; font-weight: 600;">Format & Presentation Requirements</div>
                <div style="color: rgba(255,255,255,0.85); font-size: 0.95rem; margin-top: 0.4rem;">{doc_data['format_requirements']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Download Checklist
            st.markdown('<div style="margin-top: 1.5rem;">', unsafe_allow_html=True)
            checklist_data = []
            for doc in doc_data['required_documents']:
                checklist_data.append({'Document': doc, 'Type': 'Mandatory', 'Status': 'Pending'})
            for doc in doc_data['optional_documents']:
                checklist_data.append({'Document': doc, 'Type': 'Optional', 'Status': 'Pending'})
            
            checklist_df = pd.DataFrame(checklist_data)
            csv_data = checklist_df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Download Case Documents Checklist (CSV)",
                data=csv_data,
                file_name=f"{selected_case.replace(' ', '_')}_checklist.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <span>⚜️</span> ANTARANG · Documents Checklist Module <span>⚜️</span><br>
    All Indian Jurisdictions & Case Categories Covered
</div>
""", unsafe_allow_html=True)
