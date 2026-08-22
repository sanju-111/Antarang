# check_data.py
import pandas as pd
import os

print("=" * 60)
print("📊 CHECKING YOUR DATASET")
print("=" * 60)

# Find all CSV files
csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
print(f"\n📁 CSV files found: {csv_files}")

# Ask user which file to check
if len(csv_files) == 0:
    print("❌ No CSV files found in current folder!")
    exit()
elif len(csv_files) == 1:
    filename = csv_files[0]
else:
    print("\nSelect file:")
    for i, f in enumerate(csv_files, 1):
        print(f"  {i}. {f}")
    choice = int(input("Enter number: ")) - 1
    filename = csv_files[choice]

print(f"\n📁 Loading: {filename}")
df = pd.read_csv(filename)

print(f"\n✅ Rows: {len(df):,}")
print(f"✅ Columns: {len(df.columns):,}")

print("\n📋 COLUMN LIST:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2}. {col}")

print("\n📊 DATA TYPES:")
print(df.dtypes)

print("\n📈 FIRST 5 ROWS:")
print(df.head())

print("\n📊 MISSING VALUES:")
print(df.isnull().sum())

print("\n🎯 TARGET COLUMN (mediation_eligible) - IF EXISTS:")
if 'mediation_eligible' in df.columns:
    print(df['mediation_eligible'].value_counts())
else:
    print("⚠️ 'mediation_eligible' column not found!")

print("\n" + "=" * 60)