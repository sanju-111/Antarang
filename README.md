# ⚖️ ANTARANG — Justice Decoded
### Next-Gen AI Judicial Triage & Legal Intelligence Suite

Antarang is an end-to-end AI-powered legal triage suite designed to evaluate ADR dispute suitability, predict court case resolution lifecycles, streamline mandatory statutory document filings, balance judicial pendency loads, and match citizens with verified domain-specialist advocates.

---

## 🌟 Modules & Features

1. **⚖️ 1. Mediation Predictor**
   - Evaluates whether a dispute is eligible for Alternative Dispute Resolution (ADR) & Pre-litigation Mediation.
   - Evaluates willingness, legal complexity, financial impact, and intensity level.

2. **⏱️ 2. Duration Predictor**
   - Forecasts case resolution timelines (days, months, years) using a trained Random Forest Regressor.
   - Incorporates backlog risk factors, filing month/day patterns, and court hierarchy levels.

3. **📋 3. Documents Checklist**
   - Instant statutory checklist of mandatory petitions, optional annexures, notarization rules, stamp duty requirements, and court format standards across 26 legal categories.

4. **🏛️ 4. Court Load & Pendency Indicator**
   - Real-time analytics on case processing velocities across High Courts and District Courts.
   - Categorizes courts into *High Pendency*, *Moderate*, and *Fast Track* benchmarks with CSV export.

5. **👨‍⚖️ 5. Find My Advocate**
   - Smart recommendation engine matching litigants with top domain-specialist advocates filtered by state jurisdiction, language, minimum experience, and historical win rate.

6. **📊 6. Model Analytics & Explainable AI (XAI)**
   - Transparent feature importance rankings (Gini importance), regression diagnostics, actual vs. predicted performance plots, and dataset distributions.

---

## 📁 Complete Project Structure

```
antarang sanjana/
├── data/
│   ├── cleaned_cases_antarang.csv     # 3,296 cleaned case records for duration modeling
│   ├── docs.csv                       # Legal document definitions
│   ├── documents_mapping_complete.csv # Statutory checklist mapping across case types
│   ├── feature_importance.csv         # Computed feature importance data
│   ├── lawyer_dataset.csv             # Verified advocate directory and performance records
│   └── mediation_dataset_20cols.csv   # 5,000+ synthetic/historical mediation scenarios
├── models/
│   ├── duration_predictor_model.pkl   # Trained Random Forest Regressor for duration
│   ├── encoders.pkl                   # Categorical LabelEncoders for case duration
│   ├── feature_names.pkl              # Feature definition list
│   ├── lawyer_recommendation.py       # Advocate matchmaking and ranking engine
│   ├── model_performance.png          # Duration regression diagnostic plot
│   ├── predict_documents.py           # Statutory document requirements engine
│   ├── predict_simple.py              # Mediation eligibility scoring & rule engine
│   ├── simple_model.pkl               # Mediation eligibility trained model
│   ├── train_duration_model.py        # Duration predictor ML training pipeline
│   ├── train_mediation_model.py       # Mediation classifier ML training pipeline
│   └── train_model_simple.py          # Simple mediation model trainer
├── pages/
│   ├── 1_⚖️_Mediation_Predictor.py      # Streamlit Page: ADR & Mediation Suitability
│   ├── 2_⏱️_Duration_Predictor.py       # Streamlit Page: Case Duration Prediction
│   ├── 3_📋_Documents_Checklist.py      # Streamlit Page: Statutory Document Checklist
│   ├── 4_🏛️_Court_Load_Indicator.py    # Streamlit Page: Court Pendency & Load Analytics
│   ├── 5_👨‍⚖️_Find_My_Advocate.py        # Streamlit Page: Specialist Advocate Finder
│   └── 6_📊_Model_Analytics.py         # Streamlit Page: Model Explainability & Metrics
├── utils/
│   ├── check_data.py                  # Dataset inspection utility
│   ├── generate_5000_rows_final.py    # Mediation data synthesis utility
│   └── helpers.py                     # Path resolvers, loaders, UI styling & constants
├── tests/
│   └── test_lawyer_recommendation.py  # Standalone test script for lawyer recommendation
├── app.py                             # Master Streamlit Portal & Executive Command Center
├── requirements.txt                   # Dependency definitions
├── .gitignore                         # Standard Git ignore configuration
└── README.md                          # Project documentation
```

---

## 🚀 Quickstart Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. (Optional) Run ML Training Pipelines
```bash
# Train Case Duration Predictor
python models/train_duration_model.py

# Train Mediation Eligibility Model
python models/train_mediation_model.py
```

### 3. Launch the Master Streamlit Application
```bash
streamlit run app.py
```

---

## 🛠️ Technology Stack

- **Machine Learning**: `scikit-learn`, `joblib`, `pandas`, `numpy`
- **Application Framework**: `Streamlit` (Multi-Page App Architecture)
- **Data Visualizations**: `Plotly Express`, `Plotly Graph Objects`, `Matplotlib`, `Seaborn`

---

## 🏆 Hackathon
Built for **Malla Reddy Tech Fusion Hackathon 2026**.
