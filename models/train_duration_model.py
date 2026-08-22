# ============================================================
# ANTARANG - DURATION PREDICTOR MODEL TRAINING
# Trains Random Forest Regressor on cleaned case data
# ============================================================

import os
import sys

# Ensure UTF-8 output on Windows terminals
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.preprocessing import LabelEncoder
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

# Determine base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

def train_duration_model():
    print("=" * 70)
    print("ANTARANG - DURATION PREDICTOR MODEL TRAINING")
    print("=" * 70)

    # 1. Load Data
    data_path = os.path.join(DATA_DIR, 'cleaned_cases_antarang.csv')
    if not os.path.exists(data_path):
        data_path = os.path.join(BASE_DIR, 'cleaned_cases_antarang.csv')
    
    if not os.path.exists(data_path):
        print(f"[ERROR] cleaned_cases_antarang.csv not found in {DATA_DIR} or {BASE_DIR}")
        sys.exit(1)

    print(f"\n[STEP 1] Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    print(f"[OK] Loaded {len(df)} cases")

    # 2. Encode Categorical Features
    print("\n[STEP 2] Encoding categorical data...")
    encoders = {}

    le_case = LabelEncoder()
    df['caseType_encoded'] = le_case.fit_transform(df['caseType'])
    encoders['caseType'] = le_case
    print(f"  [OK] Case types encoded: {dict(zip(le_case.classes_, range(len(le_case.classes_))))}")

    le_state = LabelEncoder()
    df['stateName_encoded'] = le_state.fit_transform(df['stateName'])
    encoders['stateName'] = le_state
    print(f"  [OK] States encoded: {dict(zip(le_state.classes_, range(len(le_state.classes_))))}")

    le_tier = LabelEncoder()
    df['tier_encoded'] = le_tier.fit_transform(df['tier'])
    encoders['tier'] = le_tier
    print(f"  [OK] Tier encoded: {dict(zip(le_tier.classes_, range(len(le_tier.classes_))))}")

    encoders_path = os.path.join(MODELS_DIR, 'encoders.pkl')
    joblib.dump(encoders, encoders_path)
    print(f"  [OK] Encoders saved to: {encoders_path}")

    # 3. Prepare Features & Target
    print("\n[STEP 3] Preparing features and target...")
    features = [
        'caseType_encoded',
        'stateName_encoded',
        'tier_encoded',
        'filing_month',
        'filing_day',
        'filing_dayofweek',
        'is_old_case',
        'is_very_old_case'
    ]

    target = 'duration_days_log'

    X = df[features]
    y = df[target]

    print(f"[OK] Features ({len(features)} total): {features}")
    print(f"[OK] Target: {target} (Mean: {y.mean():.2f}, Min: {y.min():.2f}, Max: {y.max():.2f})")

    # 4. Split Data
    print("\n[STEP 4] Splitting into training (80%) and testing (20%) sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 5. Train Random Forest Model
    print("\n[STEP 5] Training Random Forest Regressor...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    print("[OK] Model training complete!")

    # 6. Evaluate Performance
    print("\n[STEP 6] Evaluating model performance...")
    y_pred = model.predict(X_test)
    y_test_days = np.exp(y_test) - 1
    y_pred_days = np.exp(y_pred) - 1

    mae = mean_absolute_error(y_test_days, y_pred_days)
    rmse = np.sqrt(mean_squared_error(y_test_days, y_pred_days))
    r2 = r2_score(y_test, y_pred)

    print(f"   ─────────────────────────────────────")
    print(f"   Mean Absolute Error (MAE):  {mae:>8,.0f} days")
    print(f"   Root Mean Squared Error:    {rmse:>8,.0f} days")
    print(f"   R2 Score:                   {r2:>8.3f}")
    print(f"   ─────────────────────────────────────")

    # 7. Feature Importance
    print("\n[STEP 7] Calculating feature importance...")
    importance = pd.DataFrame({
        'Feature': features,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)

    for _, row in importance.iterrows():
        bar = "#" * int(row['Importance'] * 40)
        print(f"   {row['Feature']:25s} {row['Importance']*100:>5.1f}%  {bar}")

    # 8. Save Artifacts
    print("\n[STEP 8] Saving artifacts...")
    model_path = os.path.join(MODELS_DIR, 'duration_predictor_model.pkl')
    features_path = os.path.join(MODELS_DIR, 'feature_names.pkl')
    importance_path = os.path.join(DATA_DIR, 'feature_importance.csv')
    plot_path = os.path.join(MODELS_DIR, 'model_performance.png')

    joblib.dump(model, model_path)
    joblib.dump(features, features_path)
    importance.to_csv(importance_path, index=False)

    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    axes[0].scatter(y_test_days, y_pred_days, alpha=0.4, s=15, c='blue')
    axes[0].plot([0, y_test_days.max() * 1.1], [0, y_test_days.max() * 1.1], 'r--', alpha=0.7, linewidth=2)
    axes[0].set_xlabel('Actual Duration (days)', fontsize=12)
    axes[0].set_ylabel('Predicted Duration (days)', fontsize=12)
    axes[0].set_title('Actual vs Predicted Case Duration', fontsize=14, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    axes[0].text(0.05, 0.95, f'R2 = {r2:.3f}\nMAE = {mae:.0f} days', 
                 transform=axes[0].transAxes, fontsize=11, verticalalignment='top',
                 bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(importance)))[::-1]
    axes[1].barh(importance['Feature'], importance['Importance'], color=colors)
    axes[1].set_xlabel('Importance', fontsize=12)
    axes[1].set_title('Feature Importance', fontsize=14, fontweight='bold')
    axes[1].grid(True, alpha=0.3, axis='x')

    for i, (_, row) in enumerate(importance.iterrows()):
        axes[1].text(row['Importance'] + 0.01, i, f"{row['Importance']*100:.1f}%", 
                     va='center', fontsize=10)

    plt.tight_layout()
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"[OK] Model saved: {model_path}")
    print(f"[OK] Feature names saved: {features_path}")
    print(f"[OK] Feature importance saved: {importance_path}")
    print(f"[OK] Performance plot saved: {plot_path}")
    print("\n" + "=" * 70)
    print("DURATION MODEL TRAINING PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    train_duration_model()
