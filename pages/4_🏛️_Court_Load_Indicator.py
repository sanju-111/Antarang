# ============================================================
# ANTARANG - COURT LOAD INDICATOR PAGE
# Comprehensive Judiciary Workload, Pendency & Capacity Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Ensure utils can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import (
    load_cases_dataset,
    inject_custom_css
)

st.set_page_config(
    page_title="Court Load Indicator | Antarang",
    page_icon="🏛️",
    layout="wide"
)

inject_custom_css()

# Header Banner
st.markdown("""
<div class="main-header">
    <div class="hero-badge">Judicial Infrastructure Intelligence</div>
    <h1>🏛️ Court Load & Pendency Indicator</h1>
    <p>Real-time analytics on case processing velocities, bottleneck detection, and fast-track performance</p>
</div>
""", unsafe_allow_html=True)

# Load dataset
try:
    df = load_cases_dataset()
except Exception as e:
    st.error(f"❌ Error loading case data: {e}")
    st.stop()

# Validate required columns
required_cols = ['courtName', 'duration_days', 'stateName', 'tier']
missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    st.error(f"Missing required columns in dataset: {missing_cols}")
    st.stop()

# Computation
national_avg = df['duration_days'].mean()

court_stats = df.groupby('courtName').agg(
    avg_duration=('duration_days', 'mean'),
    case_count=('duration_days', 'count'),
    std_duration=('duration_days', 'std'),
    min_duration=('duration_days', 'min'),
    max_duration=('duration_days', 'max'),
    state=('stateName', 'first'),
    tier=('tier', 'first')
).round(1).reset_index()

court_stats = court_stats.rename(columns={'courtName': 'court'})

def get_load_status(avg):
    if avg > national_avg * 1.4:
        return "🔴 High Pendency"
    elif avg < national_avg * 0.75:
        return "🟢 Fast Track"
    else:
        return "🟡 Moderate"

court_stats['load_status'] = court_stats['avg_duration'].apply(get_load_status)
court_stats['pct_diff'] = ((court_stats['avg_duration'] - national_avg) / national_avg * 100).round(1)
court_stats = court_stats.sort_values('avg_duration', ascending=False)

# Top KPIs
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_courts = len(court_stats)
high_pendency_count = len(court_stats[court_stats['load_status'] == "🔴 High Pendency"])
fast_track_count = len(court_stats[court_stats['load_status'] == "🟢 Fast Track"])
moderate_count = len(court_stats[court_stats['load_status'] == "🟡 Moderate"])

with kpi1:
    st.markdown("""
    <div class="kpi-card">
        <div style="color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Monitored Courts</div>
        <div style="font-size: 2rem; font-weight: 700; color: #0f172a; margin-top: 4px;">{}</div>
        <div style="color: #10b981; font-size: 0.8rem; font-weight: 500;">Across {} States</div>
    </div>
    """.format(total_courts, df['stateName'].nunique()), unsafe_allow_html=True)

with kpi2:
    st.markdown("""
    <div class="kpi-card" style="border-left: 4px solid #ef4444;">
        <div style="color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">High Pendency (Critical)</div>
        <div style="font-size: 2rem; font-weight: 700; color: #dc2626; margin-top: 4px;">{}</div>
        <div style="color: #ef4444; font-size: 0.8rem; font-weight: 500;">Avg > 140% National Benchmark</div>
    </div>
    """.format(high_pendency_count), unsafe_allow_html=True)

with kpi3:
    st.markdown("""
    <div class="kpi-card" style="border-left: 4px solid #10b981;">
        <div style="color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Fast Track Benches</div>
        <div style="font-size: 2rem; font-weight: 700; color: #16a34a; margin-top: 4px;">{}</div>
        <div style="color: #16a34a; font-size: 0.8rem; font-weight: 500;">Avg < 75% National Benchmark</div>
    </div>
    """.format(fast_track_count), unsafe_allow_html=True)

with kpi4:
    st.markdown("""
    <div class="kpi-card" style="border-left: 4px solid #6366f1;">
        <div style="color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">National Benchmark</div>
        <div style="font-size: 2rem; font-weight: 700; color: #4338ca; margin-top: 4px;">{:.0f} Days</div>
        <div style="color: #6366f1; font-size: 0.8rem; font-weight: 500;">≈ {:.1f} Months Average</div>
    </div>
    """.format(national_avg, national_avg / 30.4), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Filters
st.markdown("### 🔍 Filter & Search Jurisdictions")
f_col1, f_col2, f_col3 = st.columns([1, 1, 1])

with f_col1:
    selected_status = st.selectbox(
        "Load Category",
        ["All Categories", "🔴 High Pendency", "🟡 Moderate", "🟢 Fast Track"]
    )

with f_col2:
    states_list = ["All States"] + sorted(court_stats['state'].dropna().unique().tolist())
    selected_state = st.selectbox("State Jurisdiction", states_list)

with f_col3:
    search_query = st.text_input("Search Court by Name", placeholder="e.g. Hyderabad, Tis Hazari, High Court...")

# Filter dataset
filtered_df = court_stats.copy()

if selected_status != "All Categories":
    filtered_df = filtered_df[filtered_df['load_status'] == selected_status]

if selected_state != "All States":
    filtered_df = filtered_df[filtered_df['state'] == selected_state]

if search_query:
    filtered_df = filtered_df[filtered_df['court'].str.contains(search_query, case=False, na=False)]

# Visual Analytics Tabs
st.markdown("---")
st.markdown("### 📊 Interactive Visual Analytics")

tab1, tab2, tab3 = st.tabs(["📊 Court Load Comparison", "🗺️ State Distribution", "📋 Detailed Data Table"])

with tab1:
    fig_bar = px.bar(
        filtered_df.head(25),
        x='court',
        y='avg_duration',
        color='load_status',
        color_discrete_map={
            "🔴 High Pendency": "#ef4444",
            "🟡 Moderate": "#f59e0b",
            "🟢 Fast Track": "#10b981"
        },
        title="Average Case Processing Duration per Court (Top 25 Filtered)",
        labels={'avg_duration': 'Average Lifecycle (Days)', 'court': 'Court Name'},
        hover_data=['case_count', 'state', 'tier', 'pct_diff']
    )
    fig_bar.add_hline(
        y=national_avg,
        line_dash="dot",
        line_color="#475569",
        annotation_text=f"National Average ({national_avg:.0f}d)",
        annotation_position="bottom right"
    )
    fig_bar.update_layout(xaxis_tickangle=-45, height=450, margin=dict(l=20, r=20, t=40, b=80))
    st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    col_pie1, col_pie2 = st.columns(2)
    with col_pie1:
        status_pie = court_stats['load_status'].value_counts().reset_index()
        status_pie.columns = ['Status', 'Count']
        fig_pie = px.pie(
            status_pie,
            values='Count',
            names='Status',
            color='Status',
            color_discrete_map={
                "🔴 High Pendency": "#ef4444",
                "🟡 Moderate": "#f59e0b",
                "🟢 Fast Track": "#10b981"
            },
            hole=0.45,
            title="Proportion of Courts by Pendency Status"
        )
        fig_pie.update_layout(height=350)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_pie2:
        state_agg = df.groupby('stateName')['duration_days'].mean().round(1).reset_index()
        fig_state = px.bar(
            state_agg.sort_values('duration_days', ascending=True),
            x='duration_days',
            y='stateName',
            orientation='h',
            title="State-wise Mean Duration (Days)",
            labels={'duration_days': 'Mean Duration (Days)', 'stateName': 'State'},
            color='duration_days',
            color_continuous_scale='Tealgrn'
        )
        fig_state.update_layout(height=350)
        st.plotly_chart(fig_state, use_container_width=True)

with tab3:
    st.markdown(f"**Showing {len(filtered_df)} courts matching criteria**")
    
    display_table = filtered_df[['court', 'load_status', 'avg_duration', 'case_count', 'pct_diff', 'state', 'tier']].copy()
    display_table.columns = ['Court Name', 'Load Status', 'Avg Days', 'Sample Cases', 'Variance vs Nat. (%)', 'State', 'Hierarchy']
    
    st.dataframe(
        display_table,
        use_container_width=True,
        height=380
    )

    # Download Button
    csv_bytes = display_table.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Court Analytics Report (CSV)",
        data=csv_bytes,
        file_name="antarang_court_load_report.csv",
        mime="text/csv",
        type="secondary"
    )

# Policy & Triage Recommendations
st.markdown("---")
st.markdown("### 💡 Strategic Triage Recommendations")

r_col1, r_col2 = st.columns(2)
with r_col1:
    st.error("""
    **🔴 Action Plan for High Pendency Courts:**
    - Deploy alternative dispute resolution (ADR) and Lok Adalat mechanisms for simple civil disputes.
    - Automate routine notice/summons tracking via digital case management.
    - Reallocate incoming cases or establish fast-track virtual benches.
    """)

with r_col2:
    st.success("""
    **🟢 Best Practices from Fast-Track Courts:**
    - Standardized pre-trial conferences and fixed timetable scheduling.
    - High adoption of electronic evidence and digital case files.
    - Replicate disposal workflows across peer courts in same state.
    """)

st.markdown("""
<div class="footer-note">
    🏛️ <b>Antarang Judicial Intelligence</b> • Designed for court administrators, registrars, and policy researchers.
</div>
""", unsafe_allow_html=True)
