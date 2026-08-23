# models/predict_simple.py - ANTARANG Mediation Predictor Engine
import os
import pickle
import pandas as pd

class SimpleModel:
    """Simple rule-based model for mediation prediction"""
    def predict(self, data):
        predictions = []
        for idx, row in data.iterrows():
            score = 0
            if row.get('mediation_willingness', 5) >= 7:
                score += 20
            elif row.get('mediation_willingness', 5) >= 4:
                score += 10
            
            intensity = row.get('intensity_level', 'Medium')
            if intensity == 'Low':
                score += 15
            elif intensity == 'Medium':
                score += 5
            else:
                score -= 10
            
            if row.get('settlement_possibility', 5) >= 7:
                score += 15
            elif row.get('settlement_possibility', 5) >= 4:
                score += 5
            
            complexity = row.get('legal_complexity', 5)
            if complexity <= 4:
                score += 10
            elif complexity >= 8:
                score -= 10
            
            if row.get('state', '') in ['Kerala', 'Maharashtra', 'Delhi']:
                score += 5
            
            finance = row.get('financial_impact', 5)
            if finance <= 3:
                score += 5
            elif finance >= 8:
                score -= 5
            
            if score >= 40:
                predictions.append('Yes')
            elif score >= 20:
                predictions.append('Conditional')
            else:
                predictions.append('No')
        return predictions

class SimpleMediationPredictor:
    """ANTARANG - Simple Mediation Predictor"""
    
    def __init__(self, model_path=None):
        if model_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            candidate1 = os.path.join(base_dir, 'simple_model.pkl')
            candidate2 = os.path.join(os.getcwd(), 'models', 'simple_model.pkl')
            candidate3 = os.path.join(os.getcwd(), 'simple_model.pkl')
            if os.path.exists(candidate1):
                model_path = candidate1
            elif os.path.exists(candidate2):
                model_path = candidate2
            elif os.path.exists(candidate3):
                model_path = candidate3
            else:
                model_path = candidate1

        # Load the model or fallback to SimpleModel
        self.model = SimpleModel()
        if model_path and os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    loaded = pickle.load(f)
                    if hasattr(loaded, 'predict'):
                        self.model = loaded
            except Exception:
                # Use standard SimpleModel instance
                self.model = SimpleModel()
        
        # Define all options
        self.case_types = [
            'NI Act / Cheque Bounce', 'Civil Suits', 'Writ Petitions', 'Bail Applications',
            'Motor Accident Claims', 'Criminal Appeals', 'Family Disputes', 'Property Disputes',
            'Consumer Protection', 'Labour & Employment Disputes', 'Corporate & Commercial Law',
            'Banking & Debt Recovery', 'Intellectual Property', 'Tax Law (Direct & Indirect)',
            'Cyber Crime & IT Act', 'Insurance Claims', 'Environmental Law', 'Human Rights & PIL',
            'Arbitration & Mediation', 'Real Estate & RERA', 'Immigration & Passport Matters',
            'Medical Negligence', 'Constitutional Law', 'POCSO & Juvenile Justice',
            'Anti-Corruption & Vigilance', 'Company / Insolvency (NCLT-NCLAT)'
        ]
        
        self.states = ['Maharashtra', 'Delhi', 'Tamil Nadu', 'Karnataka', 'Uttar Pradesh',
                      'West Bengal', 'Rajasthan', 'Kerala', 'Punjab', 'Bihar',
                      'Madhya Pradesh', 'Gujarat', 'Haryana', 'Assam']
        
        self.districts = {
            'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Thane', 'Navi Mumbai'],
            'Delhi': ['New Delhi', 'South Delhi', 'North Delhi', 'East Delhi'],
            'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Salem'],
            'Karnataka': ['Bangalore', 'Mysore', 'Hubli', 'Mangalore'],
            'Uttar Pradesh': ['Lucknow', 'Agra', 'Varanasi', 'Kanpur'],
            'West Bengal': ['Kolkata', 'Howrah', 'Siliguri', 'Asansol'],
            'Rajasthan': ['Jaipur', 'Jodhpur', 'Udaipur', 'Kota'],
            'Kerala': ['Thiruvananthapuram', 'Kochi', 'Kozhikode', 'Thrissur'],
            'Punjab': ['Amritsar', 'Ludhiana', 'Chandigarh', 'Jalandhar'],
            'Bihar': ['Patna', 'Gaya', 'Bhagalpur', 'Muzaffarpur'],
            'Madhya Pradesh': ['Bhopal', 'Indore', 'Jabalpur', 'Gwalior'],
            'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot'],
            'Haryana': ['Gurugram', 'Faridabad', 'Hisar', 'Rohtak'],
            'Assam': ['Guwahati', 'Silchar', 'Dibrugarh', 'Jorhat']
        }
    
    def predict(self, case_data):
        """Predict mediation eligibility"""
        # Calculate score based on rules
        score = self._calculate_score(case_data)
        
        try:
            df = pd.DataFrame([case_data])
            pred_val = self.model.predict(df)[0]
        except Exception:
            if score >= 40:
                pred_val = 'Yes'
            elif score >= 20:
                pred_val = 'Conditional'
            else:
                pred_val = 'No'
        
        # Calculate confidence
        if pred_val == 'Yes':
            confidence = 70 + min(25, max(0, (score - 40) * 1.5))
        elif pred_val == 'Conditional':
            confidence = 50 + max(0, min(35, (score - 20) * 1.5))
        else:
            confidence = 70 - min(40, max(0, (20 - score) * 1.5))
        
        confidence = min(95, max(50, confidence))
        
        return {
            'prediction': pred_val,
            'confidence': confidence,
            'probabilities': self._get_probabilities(pred_val, confidence),
            'recommendations': self.get_recommendations(pred_val)
        }
    
    def _calculate_score(self, case_data):
        """Calculate score based on rules"""
        score = 0
        
        # Rule 1: Mediation willingness
        willingness = case_data.get('mediation_willingness', 5)
        if willingness >= 7:
            score += 20
        elif willingness >= 4:
            score += 10
        
        # Rule 2: Intensity
        intensity = case_data.get('intensity_level', 'Medium')
        if intensity == 'Low':
            score += 15
        elif intensity == 'Medium':
            score += 5
        else:
            score -= 10
        
        # Rule 3: Settlement possibility
        settlement = case_data.get('settlement_possibility', 5)
        if settlement >= 7:
            score += 15
        elif settlement >= 4:
            score += 5
        
        # Rule 4: Legal complexity
        complexity = case_data.get('legal_complexity', 5)
        if complexity <= 4:
            score += 10
        elif complexity >= 8:
            score -= 10
        
        # Rule 5: State factor
        state = case_data.get('state', '')
        if state in ['Kerala', 'Maharashtra', 'Delhi']:
            score += 5
        
        # Rule 6: Financial impact
        finance = case_data.get('financial_impact', 5)
        if finance <= 3:
            score += 5
        elif finance >= 8:
            score -= 5
        
        return score
    
    def _get_probabilities(self, prediction, confidence):
        """Create probability distribution"""
        if prediction == 'Yes':
            return {'Yes': round(confidence, 1), 'Conditional': round((100-confidence)*0.6, 1), 'No': round((100-confidence)*0.4, 1)}
        elif prediction == 'Conditional':
            return {'Yes': round((100-confidence)*0.3, 1), 'Conditional': round(confidence, 1), 'No': round((100-confidence)*0.7, 1)}
        else:
            return {'Yes': round((100-confidence)*0.2, 1), 'Conditional': round((100-confidence)*0.3, 1), 'No': round(confidence, 1)}
    
    def get_recommendations(self, prediction):
        """Get recommendations based on prediction"""
        recommendations = {
            'Yes': {
                'title': 'Eligible for Mediation',
                'color': '#D4AF37',
                'message': 'Your case is suitable for Alternative Dispute Resolution & Mediation.',
                'actions': [
                    'Proceed with mediation immediately',
                    'Find a certified mediator in your area',
                    'Prepare all relevant documents from the checklist',
                    'Schedule a preliminary mediation meeting'
                ]
            },
            'Conditional': {
                'title': 'Conditionally Eligible',
                'color': '#C0A030',
                'message': 'Your case may be eligible for mediation subject to specific pre-conditions.',
                'actions': [
                    'Address specific contention issues first',
                    'Consider preliminary expert assistance',
                    'Try pre-mediation counseling',
                    'Reassess after addressing underlying concerns'
                ]
            },
            'No': {
                'title': 'Not Eligible for Mediation',
                'color': '#DC3545',
                'message': 'Your case requires direct court intervention / litigation.',
                'actions': [
                    'Proceed with litigation',
                    'File your case in the appropriate court',
                    'Consider arbitration as an alternative if contractual',
                    'Seek immediate legal counsel via Find My Advocate'
                ]
            }
        }
        return recommendations.get(prediction, recommendations['No'])
