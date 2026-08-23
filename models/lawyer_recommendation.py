# models/lawyer_recommendation.py - ANTARANG Lawyer Recommendation Engine
import os
import pandas as pd
import numpy as np

class LawyerRecommendationEngine:
    def __init__(self, data_path=None):
        """Load the CSV and clean it."""
        if data_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            candidate1 = os.path.join(base_dir, '..', 'data', 'lawyer_dataset.csv')
            candidate2 = os.path.join(os.getcwd(), 'data', 'lawyer_dataset.csv')
            candidate3 = os.path.join(os.getcwd(), 'lawyer_dataset.csv')
            
            for candidate in [candidate1, candidate2, candidate3]:
                if os.path.exists(candidate):
                    data_path = candidate
                    break
            if data_path is None:
                data_path = 'data/lawyer_dataset.csv'
        
        self.df = pd.read_csv(data_path)
        self.df[['lang2','lang3']] = self.df[['lang2','lang3']].fillna('')
        # Convert success_rate to numeric
        self.df['success_rate'] = pd.to_numeric(self.df['success_rate'], errors='coerce').fillna(0)
    
    def get_specializations(self):
        """Return the list of all categories for dropdowns."""
        return sorted(self.df['specialization'].unique().tolist())
    
    def recommend_lawyers(self, 
                         case_type,          # Required: e.g., "Civil Suits"
                         location=None,      # Optional: "Hyderabad"
                         languages=None,     # Optional: ["English", "Telugu"]
                         min_experience=0,   # Optional: 5
                         min_success=0,      # Optional: 70
                         max_results=10,     # Optional: how many to show
                         sort_by='relevance' # 'experience', 'success', 'relevance'
                         ):
        """
        Core filtering and scoring logic.
        """
        results = self.df.copy()
        
        # 1. Filter by specialization (case type)
        results = results[results['specialization'] == case_type]
        
        # 2. Filter by location (if provided)
        if location:
            results = results[results['location'].str.contains(location, case=False, na=False)]
        
        # 3. Filter by languages (if provided)
        if languages:
            # Check if lawyer speaks ANY of the requested languages
            mask = (
                results['lang1'].isin(languages) |
                results['lang2'].isin(languages) |
                results['lang3'].isin(languages)
            )
            results = results[mask]
        
        # 4. Filter by experience and success rate
        results = results[results['years_experience'] >= min_experience]
        results = results[results['success_rate'] >= min_success]
        
        # 5. Calculate relevance score
        if len(results) > 0:
            # Normalize experience (max 20 years)
            results['exp_score'] = results['years_experience'] / 20.0
            # Normalize success rate (max 100)
            results['success_score'] = results['success_rate'] / 100.0
            # Weighted score: 60% experience, 40% success
            results['relevance_score'] = (0.6 * results['exp_score']) + (0.4 * results['success_score'])
            results['relevance_score'] = results['relevance_score'] * 100
            
            # Sort
            if sort_by == 'experience':
                results = results.sort_values('years_experience', ascending=False)
            elif sort_by == 'success':
                results = results.sort_values('success_rate', ascending=False)
            else:  # relevance
                results = results.sort_values('relevance_score', ascending=False)
        
        return results.head(max_results)