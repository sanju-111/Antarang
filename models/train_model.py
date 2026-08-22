# models/train_model.py
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib

print("=" * 60)
print("🤖 TRAINING MEDIATION PREDICTION MODEL")
print("=" * 60)

base_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(base_dir, '..'))
data_path = os.path.join(project_root, 'data', 'mediation_dataset_20cols.csv')

if not os.path.exists(data_path):
    data_path = 'data/mediation_dataset_20cols.csv'

print(f"\n📁 Loading: {data_path}")

if not os.path.exists(data_path):
    print(f"❌ File '{data_path}' not found!")
    exit()

df = pd.read_csv(data_path)
print(f"✅ Loaded {len(df):,} cases with {len(df.columns):,} columns")

# Target
target = 'mediation_eligible'
if target not in df.columns:
    for col in ['eligible', 'eligibility', 'target', 'result']:
        if col in df.columns:
            target = col
            break

print(f"\n✅ Target column: {target}")

# Features
exclude = ['case_id', 'id', 'sl_no', 'serial', target, 'eligibility_score']
features = [col for col in df.columns if col not in exclude]

print(f"\n📊 Feature columns ({len(features)}): {features}")

# Prepare data
X = df[features].copy()
y = df[target]

if X.isnull().sum().sum() > 0:
    X = X.fillna(X.mode().iloc[0])

# Encode
encoders = {}
for col in X.columns:
    if X[col].dtype == 'object' or X[col].dtype.name == 'category':
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        encoders[col] = le

joblib.dump(encoders, os.path.join(base_dir, 'encoders.pkl'))

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Model Accuracy: {accuracy*100:.2f}%")
print(classification_report(y_test, y_pred))

joblib.dump(model, os.path.join(base_dir, 'mediation_model.pkl'))
with open(os.path.join(base_dir, 'features.txt'), 'w') as f:
    for feat in features:
        f.write(f"{feat}\n")

print("✅ Training complete and models saved.")
