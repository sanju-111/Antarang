# ============================================================
# FAST-TRACK ORDER - BACKEND LOGIC ONLY
# Suggests optimal case processing order based on duration
# ============================================================

import pandas as pd
import numpy as np
from datetime import datetime

def calculate_fast_track_impact(df):
    """
    Calculate the impact of fast-tracking cases
    
    Parameters:
    df: DataFrame with 'duration_days', 'case_type', 'filing_date', 'court'
    
    Returns:
    dict: {
        'sorted_cases': DataFrame sorted by duration,
        'fifo_total': Total waiting time with FIFO,
        'fast_total': Total waiting time with Fast-Track,
        'time_saved': Time saved,
        'pct_saved': Percentage saved,
        'cases_in_month_fifo': Cases resolved in 30 days (FIFO),
        'cases_in_month_fast': Cases resolved in 30 days (Fast-Track),
        'cases_in_year_fifo': Cases resolved in 365 days (FIFO),
        'cases_in_year_fast': Cases resolved in 365 days (Fast-Track)
    }
    """
    
    sample_df = df.copy()
    
    # Remove cases with unknown duration
    sample_df = sample_df.dropna(subset=['duration_days'])
    
    # FIFO: Original order
    fifo_cases = sample_df.copy().reset_index(drop=True)
    
    # Fast-Track: Shortest first
    fast_cases = sample_df.sort_values('duration_days').copy().reset_index(drop=True)
    
    n = len(sample_df)
    
    # 1. Total waiting time (Cumulative sum)
    fifo_total = 0
    cumulative = 0
    for i in range(n):
        cumulative += fifo_cases.iloc[i]['duration_days']
        fifo_total += cumulative
    
    fast_total = 0
    cumulative = 0
    for i in range(n):
        cumulative += fast_cases.iloc[i]['duration_days']
        fast_total += cumulative
    
    time_saved = fifo_total - fast_total
    pct_saved = (time_saved / fifo_total * 100) if fifo_total > 0 else 0
    
    # 2. Time to clear 50% of cases
    half_index = max(n // 2, 1)
    fifo_half_time = fifo_cases.iloc[:half_index]['duration_days'].sum()
    fast_half_time = fast_cases.iloc[:half_index]['duration_days'].sum()
    
    # 3. Cases in first 30 days
    fifo_cumsum = fifo_cases['duration_days'].cumsum()
    fast_cumsum = fast_cases['duration_days'].cumsum()
    fifo_cases_in_month = len(fifo_cases[fifo_cumsum <= 30])
    fast_cases_in_month = len(fast_cases[fast_cumsum <= 30])
    
    # 4. Cases in first 365 days
    fifo_cases_in_year = len(fifo_cases[fifo_cumsum <= 365])
    fast_cases_in_year = len(fast_cases[fast_cumsum <= 365])
    
    # 5. Average wait for quick cases (bottom 50%)
    fifo_quick_wait = fifo_cases.iloc[half_index:]['duration_days'].mean() if n > half_index else 0
    fast_quick_wait = fast_cases.iloc[half_index:]['duration_days'].mean() if n > half_index else 0
    
    return {
        'sorted_cases': fast_cases,
        'fifo_total': fifo_total,
        'fast_total': fast_total,
        'time_saved': time_saved,
        'pct_saved': pct_saved,
        'fifo_half_time': fifo_half_time,
        'fast_half_time': fast_half_time,
        'fifo_cases_in_month': fifo_cases_in_month,
        'fast_cases_in_month': fast_cases_in_month,
        'fifo_cases_in_year': fifo_cases_in_year,
        'fast_cases_in_year': fast_cases_in_year,
        'fifo_quick_wait': fifo_quick_wait,
        'fast_quick_wait': fast_quick_wait,
        'total_cases': n
    }


def get_case_priority(duration_days):
    """
    Get priority tier based on duration
    """
    if duration_days < 30:
        return "🚀 IMMEDIATE"
    elif duration_days < 100:
        return "🟢 QUICK"
    elif duration_days < 365:
        return "🟡 MEDIUM"
    else:
        return "🔴 LONG"


def get_priority_color(duration_days):
    """
    Get color for priority tier
    """
    if duration_days < 30:
        return "#00e676"
    elif duration_days < 100:
        return "#66bb6a"
    elif duration_days < 365:
        return "#ffa726"
    else:
        return "#ef5350"


def get_case_type_name(case_type_code):
    """
    Convert case type code to readable name
    """
    mapping = {
        "BA": "Bail Application",
        "WP_C": "Writ Petition (Civil)",
        "CS": "Civil Suit",
        "CRL_A": "Criminal Appeal",
        "MACA": "Motor Accident Claims Appeal"
    }
    return mapping.get(case_type_code, case_type_code)


def get_case_summary(df):
    """
    Get summary of cases by priority tier
    """
    if 'duration_days' not in df.columns:
        return {}
    
    quick_cases = df[df['duration_days'] < 100]
    medium_cases = df[(df['duration_days'] >= 100) & (df['duration_days'] < 365)]
    long_cases = df[df['duration_days'] >= 365]
    
    return {
        'total_cases': len(df),
        'quick_count': len(quick_cases),
        'quick_total_days': quick_cases['duration_days'].sum(),
        'medium_count': len(medium_cases),
        'medium_total_days': medium_cases['duration_days'].sum(),
        'long_count': len(long_cases),
        'long_total_days': long_cases['duration_days'].sum(),
        'avg_duration': df['duration_days'].mean(),
        'median_duration': df['duration_days'].median(),
        'min_duration': df['duration_days'].min(),
        'max_duration': df['duration_days'].max()
    }


def generate_fast_track_recommendations(metrics):
    """
    Generate recommendations based on fast-track metrics
    """
    recommendations = []
    
    # Recommendation 1: Process quick cases first
    if metrics['fast_cases_in_month'] > metrics['fifo_cases_in_month']:
        recommendations.append({
            'type': 'success',
            'title': 'Process Quick Cases First',
            'message': f"Fast-tracking would resolve {metrics['fast_cases_in_month']} cases in first month vs {metrics['fifo_cases_in_month']} with FIFO.",
            'action': 'Process cases with duration < 30 days immediately.'
        })
    
    # Recommendation 2: Time to clear half
    if metrics['fast_half_time'] < metrics['fifo_half_time']:
        time_saved_half = metrics['fifo_half_time'] - metrics['fast_half_time']
        recommendations.append({
            'type': 'success',
            'title': 'Clear Half the Backlog Faster',
            'message': f"Fast-tracking clears 50% of cases in {metrics['fast_half_time']:.0f} days vs {metrics['fifo_half_time']:.0f} days.",
            'action': f'You would save {time_saved_half:.0f} days to clear half the backlog.'
        })
    
    # Recommendation 3: Overall impact
    if metrics['pct_saved'] > 10:
        recommendations.append({
            'type': 'success',
            'title': 'Significant Time Savings',
            'message': f"Fast-tracking saves {metrics['pct_saved']:.1f}% total waiting time.",
            'action': f"This saves {metrics['time_saved']:,.0f} days of total waiting time."
        })
    
    return recommendations


def export_fast_track_order(sorted_cases, filename='fast_track_order.csv'):
    """
    Export the fast-track order to CSV
    """
    # Add priority and order columns
    export_df = sorted_cases.copy()
    export_df['order'] = range(1, len(export_df) + 1)
    export_df['priority'] = export_df['duration_days'].apply(get_case_priority)
    
    # Select columns for export
    columns_to_export = ['order', 'priority', 'duration_days']
    
    # Add case identifier if available
    if 'cnr' in export_df.columns:
        columns_to_export.insert(1, 'cnr')
    
    if 'case_type' in export_df.columns:
        columns_to_export.append('case_type')
    
    if 'court' in export_df.columns:
        columns_to_export.append('court')
    
    export_df = export_df[columns_to_export]
    export_df.columns = ['Order', 'Priority', 'Duration (days)', 'Case Type', 'Court']
    
    export_df.to_csv(filename, index=False)
    return filename


def calculate_time_saved_visualization(metrics):
    """
    Calculate data for visualizing the race between FIFO and Fast-Track
    """
    return {
        'fifo_time': metrics['fifo_half_time'],
        'fast_time': metrics['fast_half_time'],
        'fifo_label': 'Normal Processing (FIFO)',
        'fast_label': '⚡ Fast-Track Processing',
        'time_saved': metrics['time_saved'],
        'pct_saved': metrics['pct_saved'],
        'fifo_color': '#ef5350',
        'fast_color': '#66bb6a'
    }


# ---------- EXAMPLE USAGE ----------
if __name__ == "__main__":
    
    print("="*60)
    print("⚡ FAST-TRACK ORDER - BACKEND")
    print("="*60)
    
    # Load data
    try:
        df = pd.read_csv('cleaned_cases_antarang.csv')
        print(f"✅ Loaded {len(df)} cases")
    except FileNotFoundError:
        try:
            df = pd.read_csv('data/cleaned_cases_antarang.csv')
            print(f"✅ Loaded {len(df)} cases from data/")
        except FileNotFoundError:
            print("❌ Cleaned data file not found")
            exit()
    
    # Check required columns
    if 'duration_days' not in df.columns:
        print("❌ 'duration_days' column not found")
        print(f"Available columns: {list(df.columns)}")
        exit()
    
    # Take a sample for testing (first 50 cases)
    sample_df = df.head(50).copy()
    
    # Calculate fast-track impact
    metrics = calculate_fast_track_impact(sample_df)
    
    # Print results
    print(f"\n📊 Fast-Track Impact Analysis")
    print(f"   ─────────────────────────────────────")
    print(f"   Total Cases: {metrics['total_cases']}")
    print(f"   FIFO Total: {metrics['fifo_total']:,.0f} days")
    print(f"   Fast-Track Total: {metrics['fast_total']:,.0f} days")
    print(f"   Time Saved: {metrics['time_saved']:,.0f} days ({metrics['pct_saved']:.1f}%)")
    
    print(f"\n   ⏱️ Time to Clear 50% of Cases:")
    print(f"   FIFO: {metrics['fifo_half_time']:,.0f} days")
    print(f"   Fast-Track: {metrics['fast_half_time']:,.0f} days")
    
    print(f"\n   📋 Cases Resolved in First 30 Days:")
    print(f"   FIFO: {metrics['fifo_cases_in_month']} cases")
    print(f"   Fast-Track: {metrics['fast_cases_in_month']} cases")
    
    print(f"\n   📋 Cases Resolved in First Year:")
    print(f"   FIFO: {metrics['fifo_cases_in_year']} cases")
    print(f"   Fast-Track: {metrics['fast_cases_in_year']} cases")
    
    # Get case summary
    summary = get_case_summary(sample_df)
    print(f"\n📋 Case Breakdown:")
    print(f"   Quick (<100 days): {summary['quick_count']} cases")
    print(f"   Medium (100-365 days): {summary['medium_count']} cases")
    print(f"   Long (>365 days): {summary['long_count']} cases")
    
    # Get sorted cases
    sorted_cases = metrics['sorted_cases']
    print(f"\n📋 Top 10 Cases (Shortest First):")
    print("   Order | Duration | Priority")
    print("   ──────┼──────────┼──────────────")
    for i, row in sorted_cases.head(10).iterrows():
        priority = get_case_priority(row['duration_days'])
        print(f"   {i+1:>5} | {row['duration_days']:>8} | {priority}")
    
    # Generate recommendations
    recommendations = generate_fast_track_recommendations(metrics)
    print(f"\n💡 Recommendations:")
    for rec in recommendations:
        print(f"   ✅ {rec['title']}")
        print(f"      {rec['message']}")
        print(f"      → {rec['action']}")
    
    # Export to CSV
    if len(sorted_cases) > 0:
        filename = export_fast_track_order(sorted_cases)
        print(f"\n📁 Exported to: {filename}")
    
    print("\n" + "="*60)
    print("✅ Fast-Track Order Backend Complete!")