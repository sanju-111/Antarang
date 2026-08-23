# ============================================================
# COURT LOAD INDICATOR - BACKEND LOGIC ONLY
# No Streamlit, no UI - pure data processing functions
# ============================================================

import pandas as pd
import numpy as np

def calculate_court_load(df):
    """
    Calculate court load status for each court
    
    Parameters:
    df: DataFrame with 'courtName', 'duration_days', 'stateName', 'tier' columns
    
    Returns:
    court_stats: DataFrame with court load metrics
    national_avg: float, national average duration
    """
    
    # Check required columns
    required_cols = ['courtName', 'duration_days']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    
    # Group by court
    court_stats = df.groupby('courtName').agg({
        'duration_days': ['mean', 'count', 'std', 'min', 'max']
    }).round(0)
    
    # Flatten column names
    court_stats.columns = ['avg_duration', 'case_count', 'std_duration', 'min_duration', 'max_duration']
    court_stats = court_stats.reset_index()
    court_stats = court_stats.rename(columns={'courtName': 'court'})
    
    # Add state and tier if available
    if 'stateName' in df.columns:
        state_map = df.groupby('courtName')['stateName'].first()
        court_stats['state'] = court_stats['court'].map(state_map)
    
    if 'tier' in df.columns:
        tier_map = df.groupby('courtName')['tier'].first()
        court_stats['tier'] = court_stats['court'].map(tier_map)
    
    # Calculate national average
    national_avg = df['duration_days'].mean()
    
    # Determine load status
    def get_load_status(avg):
        if avg > national_avg * 1.5:
            return "High Pendency"
        elif avg < national_avg * 0.7:
            return "Fast Track"
        else:
            return "Moderate"
    
    court_stats['load_status'] = court_stats['avg_duration'].apply(get_load_status)
    
    # Add percentage difference from national average
    court_stats['pct_diff'] = ((court_stats['avg_duration'] - national_avg) / national_avg * 100).round(1)
    
    # Add status color coding
    def get_status_color(status):
        if status == "High Pendency":
            return "red"
        elif status == "Fast Track":
            return "green"
        else:
            return "orange"
    
    court_stats['status_color'] = court_stats['load_status'].apply(get_status_color)
    
    # Sort by average duration (highest first)
    court_stats = court_stats.sort_values('avg_duration', ascending=False)
    
    return court_stats, national_avg


def get_high_pendency_courts(court_stats, top_n=5):
    """Get top N high pendency courts"""
    high_courts = court_stats[court_stats['load_status'] == "High Pendency"].head(top_n)
    return high_courts


def get_fast_track_courts(court_stats, top_n=5):
    """Get top N fast track courts"""
    fast_courts = court_stats[court_stats['load_status'] == "Fast Track"].head(top_n)
    return fast_courts


def get_court_load_summary(court_stats, national_avg):
    """Get summary statistics for court load"""
    
    total_courts = len(court_stats)
    high_count = len(court_stats[court_stats['load_status'] == "High Pendency"])
    moderate_count = len(court_stats[court_stats['load_status'] == "Moderate"])
    fast_count = len(court_stats[court_stats['load_status'] == "Fast Track"])
    
    summary = {
        'total_courts': total_courts,
        'high_pendency': high_count,
        'moderate': moderate_count,
        'fast_track': fast_count,
        'national_avg': round(national_avg, 0),
        'high_pendency_pct': round(high_count / total_courts * 100, 1) if total_courts > 0 else 0,
        'fast_track_pct': round(fast_count / total_courts * 100, 1) if total_courts > 0 else 0
    }
    
    return summary


def get_court_performance(court_stats):
    """Get performance metrics for each court"""
    
    performance = {}
    for _, row in court_stats.iterrows():
        performance[row['court']] = {
            'avg_duration': row['avg_duration'],
            'case_count': row['case_count'],
            'status': row['load_status'],
            'status_color': row['status_color'],
            'pct_diff': row['pct_diff']
        }
    
    return performance


def generate_recommendations(court_stats):
    """Generate recommendations based on court load data"""
    
    recommendations = []
    
    high_courts = court_stats[court_stats['load_status'] == "High Pendency"]
    fast_courts = court_stats[court_stats['load_status'] == "Fast Track"]
    
    if len(high_courts) > 0:
        recommendations.append({
            'type': 'warning',
            'message': f"{len(high_courts)} courts are in High Pendency",
            'details': high_courts['court'].tolist()[:5]
        })
    
    if len(fast_courts) > 0:
        recommendations.append({
            'type': 'success',
            'message': f"{len(fast_courts)} courts are Fast Track",
            'details': fast_courts['court'].tolist()[:5]
        })
    
    # Check if any court is extremely slow (>3x national avg)
    extreme_courts = court_stats[court_stats['avg_duration'] > court_stats['avg_duration'].mean() * 2]
    if len(extreme_courts) > 0:
        recommendations.append({
            'type': 'critical',
            'message': f"{len(extreme_courts)} courts are extremely slow (>2x average)",
            'details': extreme_courts['court'].tolist()[:3]
        })
    
    return recommendations


def export_court_load_csv(court_stats):
    """Export court load data to CSV format"""
    return court_stats.to_csv(index=False)


def get_court_load_for_state(court_stats, state):
    """Filter court load data by state"""
    if 'state' in court_stats.columns:
        return court_stats[court_stats['state'] == state]
    return court_stats


def get_court_load_for_tier(court_stats, tier):
    """Filter court load data by tier"""
    if 'tier' in court_stats.columns:
        return court_stats[court_stats['tier'] == tier]
    return court_stats


def calculate_overall_efficiency_score(court_stats):
    """Calculate overall efficiency score (0-100)"""
    high_count = len(court_stats[court_stats['load_status'] == "High Pendency"])
    total = len(court_stats)
    
    if total == 0:
        return 0
    
    efficiency_score = (1 - (high_count / total)) * 100
    return round(efficiency_score, 1)


# ---------- EXAMPLE USAGE ----------
if __name__ == "__main__":
    
    # Load data
    try:
        df = pd.read_csv('cleaned_cases_antarang.csv')
        print(f"✅ Loaded {len(df)} cases")
    except FileNotFoundError:
        print("❌ Cleaned data file not found")
        exit()
    
    # Calculate court load
    court_stats, national_avg = calculate_court_load(df)
    
    # Get summary
    summary = get_court_load_summary(court_stats, national_avg)
    print("\n📊 Summary:")
    print(f"  Total Courts: {summary['total_courts']}")
    print(f"  High Pendency: {summary['high_pendency']} ({summary['high_pendency_pct']}%)")
    print(f"  Fast Track: {summary['fast_track']} ({summary['fast_track_pct']}%)")
    print(f"  National Average: {summary['national_avg']:.0f} days")
    
    # Get top high pendency courts
    high_courts = get_high_pendency_courts(court_stats)
    print("\n🔴 High Pendency Courts:")
    for _, row in high_courts.iterrows():
        print(f"  {row['court']}: {row['avg_duration']:.0f} days ({row['case_count']} cases)")
    
    # Get recommendations
    recommendations = generate_recommendations(court_stats)
    print("\n💡 Recommendations:")
    for rec in recommendations:
        print(f"  {rec['type'].upper()}: {rec['message']}")
    
    # Get efficiency score
    score = calculate_overall_efficiency_score(court_stats)
    print(f"\n🏆 Overall Efficiency Score: {score}/100")