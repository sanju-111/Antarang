# ============================================================
# ANTARANG - UTILS & HELPERS
# Path resolvers, cached loaders, and styling utilities
# ============================================================

import os
import joblib
import pandas as pd
import streamlit as st

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Case types and metadata mapping
CASE_TYPES = ["BA", "WP_C", "CS", "CRL_A", "MACA"]
CASE_NAMES = {
    "BA": "Bail Application",
    "WP_C": "Writ Petition (Civil)",
    "CS": "Civil Suit",
    "CRL_A": "Criminal Appeal",
    "MACA": "Motor Accident Claims Appeal"
}

STATES = [
    "Andhra Pradesh", "Bihar", "Chhattisgarh", "Delhi", "Goa",
    "Gujarat", "Haryana", "Karnataka", "Kerala", "Madhya Pradesh",
    "Maharashtra", "Meghalaya", "Odisha", "Punjab", "Rajasthan",
    "Tamil Nadu", "Telangana", "Uttar Pradesh", "West Bengal"
]

COURT_TIERS = ["district", "hc"]
TIER_LABELS = {
    "district": "District Court",
    "hc": "High Court"
}

def resolve_path(*subpaths):
    """
    Finds a file by checking multiple potential locations:
    1. Direct subpath from BASE_DIR
    2. In data/ directory
    3. In models/ directory
    4. In root directory
    """
    filename = subpaths[-1] if subpaths else ""
    candidates = [
        os.path.join(BASE_DIR, *subpaths),
        os.path.join(DATA_DIR, filename),
        os.path.join(MODELS_DIR, filename),
        os.path.join(BASE_DIR, filename),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return candidates[0]

@st.cache_resource
def load_model_artifacts():
    """Load machine learning model, encoders, and feature names with caching."""
    model_path = resolve_path('models', 'duration_predictor_model.pkl')
    encoders_path = resolve_path('models', 'encoders.pkl')
    features_path = resolve_path('models', 'feature_names.pkl')

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    if not os.path.exists(encoders_path):
        raise FileNotFoundError(f"Encoders file not found at {encoders_path}")
    if not os.path.exists(features_path):
        raise FileNotFoundError(f"Feature names file not found at {features_path}")

    model = joblib.load(model_path)
    encoders = joblib.load(encoders_path)
    features = joblib.load(features_path)
    return model, encoders, features

@st.cache_data
def load_cases_dataset():
    """Load cleaned case dataset."""
    data_path = resolve_path('data', 'cleaned_cases_antarang.csv')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")
    return pd.read_csv(data_path)

@st.cache_data
def load_feature_importance():
    """Load feature importance data."""
    path = resolve_path('data', 'feature_importance.csv')
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

def inject_custom_css():
    """Inject custom modern CSS styling across all pages."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
        }
        
        .main-header {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
            border-radius: 20px;
            padding: 2.2rem 2.5rem;
            color: #ffffff;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.15), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
        }
        
        .main-header::after {
            content: '';
            position: absolute;
            top: -50%;
            right: -20%;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.25) 0%, rgba(0,0,0,0) 70%);
            pointer-events: none;
        }

        .main-header h1 {
            font-size: 2.4rem;
            font-weight: 800;
            color: #ffffff;
            margin: 0;
            letter-spacing: -0.5px;
        }

        .main-header p {
            color: #cbd5e1;
            font-size: 1.05rem;
            margin: 0.5rem 0 0 0;
            font-weight: 400;
        }

        .hero-badge {
            display: inline-block;
            background: rgba(99, 102, 241, 0.25);
            border: 1px solid rgba(165, 180, 252, 0.4);
            color: #e0e7ff;
            font-size: 0.8rem;
            font-weight: 600;
            padding: 0.3rem 0.8rem;
            border-radius: 9999px;
            margin-bottom: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .kpi-card {
            background: #ffffff;
            border-radius: 14px;
            padding: 1.3rem;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            transition: all 0.2s ease-in-out;
        }
        
        .kpi-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
            border-color: #cbd5e1;
        }

        .prediction-hero-card {
            background: linear-gradient(135deg, #1e1b4b 0%, #312e81 60%, #4338ca 100%);
            border-radius: 20px;
            padding: 2.2rem;
            text-align: center;
            color: white;
            box-shadow: 0 12px 24px -4px rgba(49, 46, 129, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.15);
            margin-bottom: 1.5rem;
        }

        .prediction-hero-card .number {
            font-size: 4rem;
            font-weight: 800;
            font-family: 'Outfit', sans-serif;
            line-height: 1;
            margin: 0.8rem 0;
            color: #f8fafc;
        }

        .prediction-hero-card .subtitle {
            font-size: 1.15rem;
            color: #c7d2fe;
            font-weight: 500;
        }

        .badge-fast {
            background-color: #ecfdf5;
            color: #065f46;
            border: 1px solid #a7f3d0;
            font-weight: 600;
            padding: 6px 14px;
            border-radius: 20px;
            display: inline-block;
        }
        
        .badge-moderate {
            background-color: #fffbeb;
            color: #92400e;
            border: 1px solid #fde68a;
            font-weight: 600;
            padding: 6px 14px;
            border-radius: 20px;
            display: inline-block;
        }
        
        .badge-high {
            background-color: #fef2f2;
            color: #991b1b;
            border: 1px solid #fecaca;
            font-weight: 600;
            padding: 6px 14px;
            border-radius: 20px;
            display: inline-block;
        }
        
        .footer-note {
            text-align: center;
            color: #94a3b8;
            font-size: 0.85rem;
            padding-top: 2rem;
            border-top: 1px solid #e2e8f0;
            margin-top: 3rem;
        }
    </style>
    """, unsafe_allow_html=True)
