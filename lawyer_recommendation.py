import pandas as pd
import random

# Load existing data
df = pd.read_csv('lawyer_recommendation_csv (1).csv')
df[['lang1','lang2','lang3']] = df[['lang1','lang2','lang3']].fillna('')

# Count current per category
counts = df['specialization'].value_counts()
target = 15
missing = {spec: max(0, target - counts.get(spec, 0)) for spec in df['specialization'].unique()}

# Pools for new data (same as before)
FIRST_NAMES = ["Aarav","Advik","Ananya","Arjun","Arnav","Aryan","Ayaan","Bhavya","Chaitanya","Darsh",
               "Devansh","Devika","Dhruv","Diya","Eshan","Harshita","Ishaan","Ishita","Kabir","Karan",
               "Kavish","Kavya","Krish","Lakshay","Lavanya","Mahira","Meera","Myra","Neha","Nia",
               "Nikhil","Nivan","Pooja","Pranav","Priya","Raghav","Rahul","Reyansh","Rhea","Riya",
               "Rohan","Rudra","Saanvi","Samaira","Samarth","Sara","Shaurya","Sia","Siddharth","Tanvi",
               "Trisha","Viaan","Vihaan","Vivaan","Yash","Zara"]
LAST_NAMES = ["Sharma","Verma","Reddy","Nair","Singh","Patel","Kumar","Gupta","Joshi","Menon",
              "Iyer","Desai","Khan","Rao","Bose","Chatterjee","Mishra","Agarwal","Pillai","Sinha",
              "Mehta","Choudhary","Saxena","Das","Malhotra","Bhatt","Trivedi","Nayar","Gandhi","Sethi"]
COURTS = ["District Court Delhi","District Court Mumbai","District Court Hyderabad","District Court Chennai",
          "District Court Bangalore","District Court Ahmedabad","District Court Pune","High Court of Delhi",
          "High Court of Bombay","High Court of Calcutta","High Court of Madras","High Court of Karnataka",
          "Supreme Court of India","Consumer Forum Delhi","Labour Court Bangalore","Debt Recovery Tribunal Delhi",
          "GST Appellate Tribunal Delhi","National Green Tribunal Delhi","CBI Special Court Delhi","NCLT Delhi",
          "RERA Tribunal Delhi NCR","Arbitration Centre Mumbai"]
CITIES = ["Delhi","Mumbai","Hyderabad","Chennai","Bangalore","Ahmedabad","Pune","Kolkata","Lucknow","Jaipur","Chandigarh"]
LANG_COMBOS = [["English","Hindi"],["English","Marathi","Hindi"],["English","Telugu","Hindi"],["English","Tamil"],
               ["English","Kannada","Hindi"],["English","Malayalam"],["English","Gujarati","Hindi"],
               ["English","Bengali","Hindi"],["English","Punjabi","Hindi"],["English","Odia","Hindi"]]

new_rows = []
used_names = set(df['lawyer_name'])

for spec, need in missing.items():
    for _ in range(need):
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
        lang1 = langs[0] if len(langs)>0 else "English"
        lang2 = langs[1] if len(langs)>1 else ""
        lang3 = langs[2] if len(langs)>2 else ""
        new_rows.append([name, spec, court, exp, location, success, phone, email, lang1, lang2, lang3])

# Combine
df_new = pd.DataFrame(new_rows, columns=df.columns)
df_final = pd.concat([df, df_new], ignore_index=True)

# Fill NaN again (just in case)
df_final[['lang1','lang2','lang3']] = df_final[['lang1','lang2','lang3']].fillna('')

# Save
df_final.to_csv('lawyer_dataset_final.csv', index=False)
print(f"✅ Final dataset has {len(df_final)} lawyers. Specialization counts:\n{df_final['specialization'].value_counts().sort_index()}")
