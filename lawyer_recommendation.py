import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
import random   # Remove if not in Colab

# ---------- CONFIG ----------
TARGET_TOTAL = 900          # Approximate total lawyers

# ---------- DATA POOLS ----------
FIRST_NAMES = [
    "Aarav","Advik","Ananya","Arjun","Arnav","Aryan","Ayaan","Bhavya","Chaitanya","Darsh",
    "Devansh","Devika","Dhruv","Diya","Eshan","Harshita","Ishaan","Ishita","Kabir","Karan",
    "Kavish","Kavya","Krish","Lakshay","Lavanya","Mahira","Meera","Myra","Neha","Nia",
    "Nikhil","Nivan","Pooja","Pranav","Priya","Raghav","Rahul","Reyansh","Rhea","Riya",
    "Rohan","Rudra","Saanvi","Samaira","Samarth","Sara","Shaurya","Sia","Siddharth","Tanvi",
    "Trisha","Viaan","Vihaan","Vivaan","Yash","Zara"
]

LAST_NAMES = [
    "Sharma","Verma","Reddy","Nair","Singh","Patel","Kumar","Gupta","Joshi","Menon",
    "Iyer","Desai","Khan","Rao","Bose","Chatterjee","Mishra","Agarwal","Pillai","Sinha",
    "Mehta","Choudhary","Saxena","Das","Malhotra","Bhatt","Trivedi","Nayar","Gandhi","Sethi"
]

SPECIALIZATIONS = [
    "NI Act / Cheque Bounce", "Civil Suits", "Writ Petitions", "Bail Applications",
    "Motor Accident Claims", "Criminal Appeals", "Family Disputes", "Property Disputes",
    "Consumer Protection", "Labour & Employment Disputes", "Corporate & Commercial Law",
    "Banking & Debt Recovery", "Intellectual Property", "Tax Law (Direct & Indirect)",
    "Cyber Crime & IT Act", "Insurance Claims", "Environmental Law",
    "Human Rights & Public Interest Litigation", "Arbitration & Mediation",
    "Real Estate & RERA", "Immigration & Passport Matters", "Medical Negligence",
    "Constitutional Law", "POCSO & Juvenile Justice", "Anti-Corruption & Vigilance",
    "Company / Insolvency (NCLT-NCLAT)"
]

COURTS = [
    "District Court Delhi","District Court Mumbai","District Court Hyderabad",
    "District Court Chennai","District Court Bangalore","District Court Ahmedabad",
    "District Court Pune","District Court Kolkata","District Court Lucknow",
    "District Court Jaipur","District Court Chandigarh","District Court Kochi",
    "District Court Madurai","District Court Surat","District Court Nagpur",
    "District Court Patna","District Court Bhopal","District Court Indore",
    "High Court of Delhi","High Court of Bombay","High Court of Calcutta",
    "High Court of Madras","High Court of Karnataka","High Court of Kerala",
    "High Court of Telangana","High Court of Andhra Pradesh","High Court of Rajasthan",
    "High Court of Gujarat","Supreme Court of India","Consumer Forum Delhi",
    "Consumer Forum Hyderabad","Labour Court Bangalore","Labour Court Pune",
    "Industrial Tribunal Mumbai","Commercial Court Mumbai","Debt Recovery Tribunal Delhi",
    "Debt Recovery Tribunal Chennai","Debt Recovery Tribunal Hyderabad",
    "GST Appellate Tribunal Delhi","Income Tax Appellate Tribunal Mumbai",
    "Income Tax Appellate Tribunal Hyderabad","National Green Tribunal Delhi",
    "National Green Tribunal Chennai","CBI Special Court Delhi","CBI Special Court Mumbai",
    "CBI Special Court Hyderabad","NCLT Delhi","NCLT Hyderabad","NCLAT Delhi",
    "RERA Tribunal Delhi NCR","RERA Tribunal Karnataka","RERA Tribunal Maharashtra",
    "Arbitration Centre Mumbai","Arbitration Centre Bangalore","Motor Accident Claims Tribunal",
    "Insurance Ombudsman Mumbai","Cyber Crime Cell Hyderabad","Cyber Crime Cell Delhi",
    "Cyber Crime Cell Bangalore","Foreigners Regional Registration Office Delhi"
]

CITIES = [
    "Delhi","Mumbai","Hyderabad","Chennai","Bangalore","Ahmedabad",
    "Pune","Kolkata","Lucknow","Jaipur","Chandigarh","Kochi",
    "Madurai","Surat","Nagpur","Patna","Bhopal","Indore",
    "Vijayawada","Visakhapatnam","Coimbatore","Guwahati","Cuttack","Goa"
]

# Language combinations: lang1 is always English, lang2 and lang3 optional
LANG_COMBOS = [
    ["English","Hindi"], ["English","Marathi","Hindi"], ["English","Telugu","Hindi"],
    ["English","Tamil"], ["English","Kannada","Hindi"], ["English","Malayalam"],
    ["English","Gujarati","Hindi"], ["English","Bengali","Hindi"],
    ["English","Punjabi","Hindi"], ["English","Odia","Hindi"],
    ["English","Marathi"], ["English","Telugu"], ["English","Kannada"],
    ["English","Tamil","Hindi"], ["English","Malayalam","Hindi"],
    ["English","Hindi","Marathi"], ["English","Hindi","Telugu"],
    ["English","Hindi","Tamil"], ["English","Hindi","Kannada"],
    ["English","Hindi","Gujarati"], ["English","Hindi","Bengali"],
    ["English","Hindi","Punjabi"]
]

# ---------- GENERATE ----------
data = []
used_names = set()
num_specs = len(SPECIALIZATIONS)
lawyers_per_spec = TARGET_TOTAL // num_specs   # ~34 per category

for spec in SPECIALIZATIONS:
    for _ in range(lawyers_per_spec):
        while True:
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            name = f"Adv. {first} {last}"
            if name not in used_names:
                used_names.add(name)
                break
        court = random.choice(COURTS)
        location = random.choice(CITIES)
        exp = random.randint(2, 20)
        success = random.randint(60, 95)
        phone = ''.join([str(random.randint(0,9)) for _ in range(10)])
        email = f"{first.lower()}.{last.lower()}@legaldemo.in"
        langs = random.choice(LANG_COMBOS)
        lang1 = langs[0]
        lang2 = langs[1] if len(langs) > 1 else np.nan
        lang3 = langs[2] if len(langs) > 2 else np.nan
        data.append([name, spec, court, exp, location, success, phone, email, lang1, lang2, lang3])

df = pd.DataFrame(data, columns=[
    "lawyer_name","specialization","court","years_experience",
    "location","success_rate","contact_phone","contact_email",
    "lang1","lang2","lang3"
])

# ---------- SAVE WITH 'NaN' STRING ----------
filename = 'lawyer_dataset_900_with_NaN.csv'
df.to_csv(filename, index=False, na_rep='NaN')   # <-- This writes 'NaN' in the CSV

print(f"✅ Generated {len(df)} lawyers. Missing languages are written as 'NaN'.")
print("📊 Per-specialization counts:\n", df['specialization'].value_counts().sort_index())

# Show first few rows to verify
print("\n🔍 Preview (first 5 rows):")
print(df.head())

# Download (if in Colab)
try:
    files.download(filename)
except:
    print(f"File saved locally as '{filename}'")