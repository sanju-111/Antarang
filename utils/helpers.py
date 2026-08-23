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
    """Inject custom luxury Black, Gold & Marble CSS styling across all pages."""
    try:
        from styles import inject_luxury_css
        inject_luxury_css()
    except Exception:
        pass


