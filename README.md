# ANTARANG — JUSTICE DECODED
### AI-Powered Judicial Triage System

ANTARANG is an intelligent judicial triage suite engineered to streamline case processing, dispute resolution assessment, document completeness, and legal advocate matching.

---

## 🏛️ System Architecture & Modules

The repository follows a clean, modular structure:

```
antarang_project/
├── app.py                          # Unified ANTARANG Landing Portal & Multi-Page Hub
├── data/                           # Verified Datasets
│   ├── docs.csv
│   ├── documents_mapping_complete.csv
│   ├── lawyer_dataset.csv
│   └── mediation_dataset_20cols.csv
├── models/                         # Predictive ML & Rule Engines
│   ├── lawyer_recommendation.py    # Advocate Matchmaking Engine
│   ├── predict_documents.py        # Statutory Document Requirements Engine
│   ├── predict_simple.py           # Mediation Suitability Predictor Engine
│   ├── simple_model.pkl            # Trained Mediation Model
│   ├── train_model.py              # Random Forest Classifier Trainer
│   └── train_model_simple.py       # Rule-Based Model Trainer
├── pages/                          # Multi-Page Streamlit Applications
│   ├── 1_⚖️_Mediation_Predictor.py   # Mediation Suitability Assessment UI
│   ├── 2_📋_Documents_Checklist.py   # Court Document Requirements & Export UI
│   └── 3_👨‍⚖️_Find_My_Advocate.py      # Precision Advocate Finder UI
└── utils/                          # Dataset Utilities & Verification
    ├── check_data.py               # Dataset Validation Utility
    └── generate_5000_rows_final.py # Case Data Generator
```

---

## 🚀 Running the Application

### 1. Install Dependencies
```bash
pip install streamlit pandas numpy scikit-learn joblib
```

### 2. Launch the Multi-Page Streamlit App
```bash
streamlit run app.py
```
This launches the central portal with full multi-page navigation across all three triage modules.

---

## 👥 Branch Information
- **`Trial`**: Integration baseline branch.
- **`geeta`**: Mediation prediction & document checklist features integrated into standard project structure.
