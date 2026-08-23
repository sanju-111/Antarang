# models/train_model_simple.py
import os
import pandas as pd
import pickle

print("=" * 60)
print("🤖 TRAINING SIMPLE MEDIATION MODEL")
print("=" * 60)

base_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(base_dir, '..'))
data_path = os.path.join(project_root, 'data', 'mediation_dataset_20cols.csv')

if not os.path.exists(data_path):
    data_path = 'data/mediation_dataset_20cols.csv'

# Load dataset
df = pd.read_csv(data_path)
print(f"✅ Loaded {len(df):,} cases from {data_path}")

# Define the model class
class SimpleModel:
    """Simple rule-based model for mediation prediction"""
    
    def predict(self, data):
        """Predict using simple rules"""
        predictions = []
        
        for idx, row in data.iterrows():
            score = 0
            
            # Rule 1: Mediation willingness
            if row.get('mediation_willingness', 5) >= 7:
                score += 20
            elif row.get('mediation_willingness', 5) >= 4:
                score += 10
            
            # Rule 2: Intensity
            if row.get('intensity_level', 'Medium') == 'Low':
                score += 15
            elif row.get('intensity_level', 'Medium') == 'Medium':
                score += 5
            else:
                score -= 10
            
            # Rule 3: Settlement possibility
            if row.get('settlement_possibility', 5) >= 7:
                score += 15
            elif row.get('settlement_possibility', 5) >= 4:
                score += 5
            
            # Rule 4: Legal complexity
            if row.get('legal_complexity', 5) <= 4:
                score += 10
            elif row.get('legal_complexity', 5) >= 8:
                score -= 10
            
            # Rule 5: State factor
            if row.get('state', '') in ['Kerala', 'Maharashtra', 'Delhi']:
                score += 5
            
            # Rule 6: Financial impact
            if row.get('financial_impact', 5) <= 3:
                score += 5
            elif row.get('financial_impact', 5) >= 8:
                score -= 5
            
            # Determine prediction
            if score >= 40:
                predictions.append('Yes')
            elif score >= 20:
                predictions.append('Conditional')
            else:
                predictions.append('No')
        
        return predictions

# Create model
print("\n📊 Training simple model...")
model = SimpleModel()

# Test accuracy on first 100 rows
test_df = df.head(100)
predictions = model.predict(test_df)
actual = test_df['mediation_eligible']

correct = sum(1 for p, a in zip(predictions, actual) if p == a)
accuracy = correct / len(test_df) * 100

print(f"✅ Accuracy on 100 samples: {accuracy:.1f}%")

# Create models folder if not present
os.makedirs(base_dir, exist_ok=True)
model_out = os.path.join(base_dir, 'simple_model.pkl')

with open(model_out, 'wb') as f:
    pickle.dump(model, f)
print(f"✅ Model saved to '{model_out}' using pickle")

print("\n" + "=" * 60)
print("✅ Model training complete! Now run: streamlit run app.py")
print("=" * 60)
