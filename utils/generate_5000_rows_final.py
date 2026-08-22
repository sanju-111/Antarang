# generate_5000_rows_final.py
# Run this script to generate your complete 5,000 row dataset
# WITH ONLY 20 IMPORTANT COLUMNS

import pandas as pd
import random
from datetime import datetime, timedelta

print("🚀 Generating 5,000 Rows with 20 Important Columns...")
print("=" * 60)

# ============================================
# ALL 26 CASE TYPES MAPPED TO DOMAINS
# ============================================
case_type_mapping = {
    'NI Act / Cheque Bounce': {'domain': 'Criminal Law', 'sub_categories': ['IPC-Cheating', 'IPC-Criminal Breach of Trust']},
    'Civil Suits': {'domain': 'Civil Law', 'sub_categories': ['Contract-Breach', 'Property-Title', 'Torts-Motor Accident']},
    'Writ Petitions': {'domain': 'Constitutional Law', 'sub_categories': ['Writ-Habeas Corpus', 'Writ-Mandamus', 'Writ-Prohibition', 'Writ-Certiorari', 'Writ-Quo Warranto']},
    'Bail Applications': {'domain': 'Criminal Law', 'sub_categories': ['IPC-Murder', 'IPC-Hurt', 'IPC-Assault']},
    'Motor Accident Claims': {'domain': 'Civil Law', 'sub_categories': ['Torts-Motor Accident']},
    'Criminal Appeals': {'domain': 'Criminal Law', 'sub_categories': ['IPC-Murder', 'IPC-Hurt', 'IPC-Cheating']},
    'Family Disputes': {'domain': 'Family Law', 'sub_categories': ['Divorce-Mutual Consent', 'Divorce-Contested', 'Child Custody-Physical', 'Child Custody-Legal', 'Domestic Violence-Physical', 'Maintenance-Spousal', 'Inheritance-Intestate']},
    'Property Disputes': {'domain': 'Property Law', 'sub_categories': ['Land-Boundary', 'Land-Encroachment', 'Land-Title', 'Building-Construction', 'Housing-Society', 'Lease-Commercial', 'Mortgage-Dispute']},
    'Consumer Protection': {'domain': 'Consumer Law', 'sub_categories': ['Products-Electronic', 'Products-Vehicles', 'Services-Health', 'Services-Travel', 'Practices-Misleading Ads', 'Practices-E-commerce']},
    'Labour & Employment Disputes': {'domain': 'Labour Law', 'sub_categories': ['Industrial-Layoff', 'Industrial-Retrenchment', 'Wages-Minimum', 'Wages-Overtime', 'Termination-Wrongful', 'Termination-Retirement', 'Harassment-Sexual', 'Service-Promotion', 'Compensation-Accident']},
    'Corporate & Commercial Law': {'domain': 'Corporate Law', 'sub_categories': ['Director-Conflict', 'Shareholder-Issues', 'Oppression-Mismanagement', 'Arbitration-Enforcement', 'Arbitration-Challenge', 'Contract-Breach']},
    'Banking & Debt Recovery': {'domain': 'Corporate Law', 'sub_categories': ['Insolvency', 'Corporate-Fraud', 'Contract-Breach']},
    'Intellectual Property': {'domain': 'Civil Law', 'sub_categories': ['Copyright', 'Trade Mark', 'Patent', 'Design', 'Geographical Indication']},
    'Tax Law (Direct & Indirect)': {'domain': 'Administrative Law', 'sub_categories': ['Taxation-Property', 'Taxation-Service', 'Taxation-Professional']},
    'Cyber Crime & IT Act': {'domain': 'Criminal Law', 'sub_categories': ['Cyber Crime-Hacking', 'Cyber Crime-Identity Theft', 'Cyber Crime-Phishing', 'Cyber Crime-Cyber Stalking', 'IPC-Cheating']},
    'Insurance Claims': {'domain': 'Consumer Law', 'sub_categories': ['Services-Insurance', 'Torts-Motor Accident']},
    'Environmental Law': {'domain': 'Criminal Law', 'sub_categories': ['Environment-Pollution', 'Environment-Forest']},
    'Human Rights & PIL': {'domain': 'Constitutional Law', 'sub_categories': ['PIL-Public Interest', 'Fundamental Rights-Article 14', 'Fundamental Rights-Article 15', 'Fundamental Rights-Article 19', 'Fundamental Rights-Article 21']},
    'Arbitration & Mediation': {'domain': 'Corporate Law', 'sub_categories': ['Arbitration-Enforcement', 'Arbitration-Challenge', 'Arbitration-Appointment', 'Arbitration-International']},
    'Real Estate & RERA': {'domain': 'Property Law', 'sub_categories': ['Housing-Society', 'Lease-Commercial', 'Lease-Residential', 'Building-Construction']},
    'Immigration & Passport Matters': {'domain': 'Administrative Law', 'sub_categories': ['Licensing', 'Service-Transfer']},
    'Medical Negligence': {'domain': 'Civil Law', 'sub_categories': ['Torts-Medical Negligence', 'Services-Health']},
    'Constitutional Law': {'domain': 'Constitutional Law', 'sub_categories': ['Fundamental Rights-Article 14', 'Fundamental Rights-Article 15', 'Writ-Habeas Corpus', 'Writ-Mandamus']},
    'POCSO & Juvenile Justice': {'domain': 'Criminal Law', 'sub_categories': ['IPC-Rape', 'IPC-Gang Rape', 'IPC-Acid Attack']},
    'Anti-Corruption & Vigilance': {'domain': 'Criminal Law', 'sub_categories': ['IPC-Cheating', 'IPC-Criminal Breach of Trust']},
    'Company / Insolvency (NCLT-NCLAT)': {'domain': 'Corporate Law', 'sub_categories': ['Oppression-Mismanagement', 'Insolvency', 'Arbitration-Enforcement']}
}

# All states with districts
states = {
    'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Thane', 'Navi Mumbai', 'Aurangabad', 'Nashik', 'Solapur', 'Amravati'],
    'Delhi': ['New Delhi', 'South Delhi', 'North Delhi', 'East Delhi', 'West Delhi', 'Central Delhi'],
    'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli', 'Salem', 'Tirunelveli', 'Vellore', 'Erode'],
    'Karnataka': ['Bangalore', 'Mysore', 'Hubli', 'Mangalore', 'Belgaum', 'Gulbarga', 'Davangere'],
    'Uttar Pradesh': ['Lucknow', 'Agra', 'Varanasi', 'Kanpur', 'Allahabad', 'Meerut', 'Ghaziabad', 'Noida'],
    'West Bengal': ['Kolkata', 'Howrah', 'Durgapur', 'Siliguri', 'Asansol', 'Hooghly'],
    'Rajasthan': ['Jaipur', 'Jodhpur', 'Udaipur', 'Kota', 'Ajmer', 'Bikaner'],
    'Kerala': ['Thiruvananthapuram', 'Kochi', 'Kozhikode', 'Thrissur', 'Alappuzha', 'Kollam'],
    'Punjab': ['Amritsar', 'Ludhiana', 'Chandigarh', 'Jalandhar', 'Patiala', 'Bathinda'],
    'Bihar': ['Patna', 'Gaya', 'Bhagalpur', 'Muzaffarpur', 'Darbhanga', 'Munger'],
    'Madhya Pradesh': ['Bhopal', 'Indore', 'Jabalpur', 'Gwalior', 'Ujjain', 'Sagar'],
    'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Bhavnagar', 'Jamnagar'],
    'Haryana': ['Gurugram', 'Faridabad', 'Hisar', 'Rohtak', 'Panipat', 'Ambala'],
    'Assam': ['Guwahati', 'Silchar', 'Dibrugarh', 'Jorhat', 'Nagaon', 'Tinsukia']
}

# ============================================
# GENERATE 5,000 ROWS
# ============================================

def generate_eligibility_score(domain, intensity, willingness):
    """Generate realistic eligibility score"""
    base_scores = {
        'Family Law': 70,
        'Civil Law': 65,
        'Criminal Law': 40,
        'Labour Law': 55,
        'Administrative Law': 50,
        'Consumer Law': 60,
        'Corporate Law': 45,
        'Constitutional Law': 20,
        'Property Law': 55
    }
    
    base = base_scores.get(domain, 50)
    
    # Intensity adjustment
    intensity_adj = {'Low': 15, 'Medium': 0, 'High': -20}
    
    # Willingness adjustment
    willingness_adj = (willingness - 5) * 3
    
    score = base + intensity_adj.get(intensity, 0) + willingness_adj
    
    # Add some randomness
    score += random.randint(-5, 5)
    
    return max(0, min(100, score))

def determine_eligibility(score):
    """Determine eligibility based on score"""
    if score >= 60:
        return 'Yes'
    elif score >= 40:
        return 'Conditional'
    else:
        return 'No'

print("📊 Generating 5,000 cases with 20 columns...")
print("-" * 60)

all_rows = []
total_rows = 5000

case_types = list(case_type_mapping.keys())

for i in range(total_rows):
    # Progress indicator
    if (i + 1) % 1000 == 0:
        print(f"Generated {i + 1:,} cases...")
    
    # Select case type
    case_type = random.choice(case_types)
    mapping = case_type_mapping[case_type]
    domain = mapping['domain']
    sub_category = random.choice(mapping['sub_categories'])
    
    # Select state and district
    state = random.choice(list(states.keys()))
    district = random.choice(states[state])
    
    # Generate features (20 columns)
    intensity = random.choices(['Low', 'Medium', 'High'], weights=[0.3, 0.5, 0.2])[0]
    willingness = random.randint(1, 10)
    settlement_possibility = random.randint(1, 10)
    legal_complexity = random.randint(3, 9)
    time_to_resolve_days = random.randint(30, 400)
    financial_impact = random.randint(1, 10)
    number_of_parties = random.randint(2, 6)
    urgency_level = random.randint(1, 10)
    power_imbalance = random.randint(1, 10)
    past_litigation_history = 'Yes' if random.random() > 0.6 else 'No'
    legal_awareness = random.randint(1, 10)
    access_to_justice = random.randint(1, 10)
    income_level = random.choice(['Low', 'Middle', 'High'])
    residence_type = random.choice(['Urban', 'Semi-Urban', 'Rural'])
    
    # Calculate eligibility score
    eligibility_score = generate_eligibility_score(domain, intensity, willingness)
    
    # Adjust for high legal complexity
    if legal_complexity >= 8:
        eligibility_score = max(0, eligibility_score - 15)
    
    # State adjustment
    state_boost = {
        'Maharashtra': 1.05,
        'Delhi': 1.08,
        'Kerala': 1.10,
        'Tamil Nadu': 1.03,
        'Karnataka': 1.04,
        'Uttar Pradesh': 0.92,
        'Bihar': 0.88,
        'Rajasthan': 0.93
    }
    eligibility_score = min(100, max(0, eligibility_score * state_boost.get(state, 1.0)))
    eligibility_score = round(eligibility_score, 2)
    
    mediation_eligible = determine_eligibility(eligibility_score)
    
    # Create row with 20 columns
    row = {
        'case_id': f'CASE{i+1:05d}',
        'case_type': case_type,
        'domain': domain,
        'sub_category': sub_category,
        'state': state,
        'district': district,
        'intensity_level': intensity,
        'mediation_willingness': willingness,
        'settlement_possibility': settlement_possibility,
        'legal_complexity': legal_complexity,
        'time_to_resolve_days': time_to_resolve_days,
        'financial_impact': financial_impact,
        'number_of_parties': number_of_parties,
        'urgency_level': urgency_level,
        'power_imbalance': power_imbalance,
        'past_litigation_history': past_litigation_history,
        'legal_awareness': legal_awareness,
        'access_to_justice': access_to_justice,
        'income_level': income_level,
        'residence_type': residence_type,
        'eligibility_score': eligibility_score,
        'mediation_eligible': mediation_eligible
    }
    
    all_rows.append(row)

print("\n📊 Creating DataFrame...")
df = pd.DataFrame(all_rows)

print("💾 Saving to CSV...")
df.to_csv('mediation_dataset_20cols.csv', index=False)

print("\n" + "=" * 60)
print("✅ SUCCESS! COMPLETE 5,000 ROW DATASET CREATED!")
print("=" * 60)
print(f"\n📊 Total Rows: {len(df):,}")
print(f"📋 Total Columns: {len(df.columns):,}")

print("\n📋 COLUMN LIST (20 Columns):")
print("-" * 60)
for i, col in enumerate(df.columns, 1):
    print(f"{i:2}. {col}")

print("\n" + "=" * 60)
print("📈 STATISTICS")
print("=" * 60)

print(f"\nMediation Eligibility Distribution:")
print(df['mediation_eligible'].value_counts())

print(f"\nIntensity Levels:")
print(df['intensity_level'].value_counts())

print(f"\nTop 5 States:")
print(df['state'].value_counts().head(5))

print(f"\nAverage Eligibility Score: {df['eligibility_score'].mean():.2f}")

print("\n" + "=" * 60)
print("✅ File saved as: mediation_dataset_20cols.csv")