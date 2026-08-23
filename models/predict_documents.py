# models/predict_documents.py - ANTARANG Document Requirements Engine
import os
import pandas as pd

class DocumentPredictor:
    """ANTARANG - Document Requirements Predictor"""
    
    def __init__(self, data_path=None):
        if data_path is None:
            # Check data/documents_mapping_complete.csv relative to project root or file
            base_dir = os.path.dirname(os.path.abspath(__file__))
            candidate1 = os.path.join(base_dir, '..', 'data', 'documents_mapping_complete.csv')
            candidate2 = os.path.join(os.getcwd(), 'data', 'documents_mapping_complete.csv')
            candidate3 = os.path.join(os.getcwd(), 'documents_mapping_complete.csv')
            candidate4 = os.path.join(base_dir, 'documents_mapping_complete.csv')
            
            for candidate in [candidate1, candidate2, candidate3, candidate4]:
                if os.path.exists(candidate):
                    data_path = candidate
                    break
            if data_path is None:
                data_path = 'data/documents_mapping_complete.csv'
        
        # Load documents mapping
        self.documents_df = pd.read_csv(data_path)
        
        # Get all case types
        self.case_types = sorted(self.documents_df['case_type'].unique())
        
        # Get all domains
        self.domains = sorted(self.documents_df['domain'].unique())
        
        # Build case type to details mapping
        self.case_type_map = {}
        for _, row in self.documents_df.iterrows():
            self.case_type_map[row['case_type']] = {
                'domain': row['domain'],
                'sub_category': row.get('sub_category', ''),
                'category': row.get('category', ''),
                'required_documents': row['required_documents'].split('; ') if isinstance(row.get('required_documents'), str) else [],
                'optional_documents': row['optional_documents'].split('; ') if isinstance(row.get('optional_documents'), str) else [],
                'time_validity': row.get('time_validity', 'N/A'),
                'submission_deadline': row.get('submission_deadline', 'N/A'),
                'format_requirements': row.get('format_requirements', 'N/A'),
                'number_of_copies': row.get('number_of_copies', 1),
                'stamp_duty_required': row.get('stamp_duty_required', 'No'),
                'notarization_required': row.get('notarization_required', 'No')
            }
    
    def get_documents(self, case_type):
        """Get all document requirements for a case type"""
        if case_type in self.case_type_map:
            return self.case_type_map[case_type]
        return None
    
    def get_required_documents(self, case_type):
        """Get required documents only"""
        data = self.get_documents(case_type)
        if data:
            return data['required_documents']
        return []
    
    def get_optional_documents(self, case_type):
        """Get optional documents only"""
        data = self.get_documents(case_type)
        if data:
            return data['optional_documents']
        return []
    
    def get_all_domains(self):
        """Get all unique domains"""
        return self.domains
    
    def get_all_categories(self):
        """Get all unique categories"""
        return sorted(self.documents_df['category'].dropna().unique())
