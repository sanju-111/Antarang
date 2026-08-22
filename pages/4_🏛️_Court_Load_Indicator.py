# ============================================================
# ANTARANG - COURT LOAD INDICATOR FRONTEND
# Comprehensive Judiciary Workload, Pendency & Capacity Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import from backend logic module
try:
    from models.court_load_indicator_model import (
        calculate_court_load,
        get_court_load_summary,
        get_high_pendency_courts,
        get_fast_track_courts,
        generate_recommendations,
        export_court_load_csv,
        calculate_overall_efficiency_score
    )
except ImportError:
    from court_load_indicator_model import (
        calculate_court_load,
        get_court_load_summary,
        get_high_pendency_courts,
        get_fast_track_courts,
        generate_recommendations,
        export_court_load_csv,
        calculate_overall_efficiency_score
    )

# Page Configuration
st.set_page_config(
    page_title="Court Load Indicator | Antarang",
    page_icon="🏛️",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
    }
    
    .badge-red {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .badge-green {
        background-color: #dcfce7;
        color: #166534;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .badge-yellow {
        background-color: #fef3c7;
        color: #92400e;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load cleaned dataset from data/ folder or root"""
    data_paths = [
        os.path.join('data', 'cleaned_cases_antarang.csv'),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'cleaned_cases_antarang.csv'),
        'cleaned_cases_antarang.csv'
    ]
    for p in data_paths:
        if os.path.exists(p):
            return pd.read_csv(p)
    return None

def show_court_load_dashboard():
    """Display the court load dashboard"""
    
    st.title("🏛️ Court Load Indicator")
    st.markdown("*Real-time pendency monitoring, court throughput analysis & bottleneck identification*")
    
    # Load dataset
    df = load_data()
    if df is None:
        st.error("❌ Cleaned dataset (`cleaned_cases_antarang.csv`) not found!")
        st.info("Please ensure `cleaned_cases_antarang.csv` is located in the `data/` folder.")
        st.stop()
    
    # Calculate metrics via backend logic
    with st.spinner("📊 Analyzing court load data..."):
        court_stats, national_avg = calculate_court_load(df)
        summary = get_court_load_summary(court_stats, national_avg)
        efficiency_score = calculate_overall_efficiency_score(court_stats)
        recommendations = generate_recommendations(court_stats)
    
    # Summary Metrics Row
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("🏛️ Total Courts", summary['total_courts'])
    with col2:
        st.metric("🔴 High Pendency", summary['high_pendency'], delta=f"{summary['high_pendency_pct']}% of total", delta_color="inverse")
    with col3:
        st.metric("🟡 Moderate", summary['moderate'])
    with col4:
        st.metric("🟢 Fast Track", summary['fast_track'], delta=f"{summary['fast_track_pct']}% of total")
    with col5:
        st.metric("📊 National Avg", f"{summary['national_avg']:.0f} days")
    
    st.progress(efficiency_score / 100)
    st.caption(f"🏆 **National Judicial Efficiency Index:** **{efficiency_score}/100**")
    
    st.markdown("---")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "High Pendency", "Moderate", "Fast Track"]
        )
    with col2:
        if 'state' in court_stats.columns and court_stats['state'].dropna().any():
            states = ["All"] + sorted(court_stats['state'].dropna().unique().tolist())
            state_filter = st.selectbox("Filter by State", states)
        else:
            state_filter = "All"
    
    # Apply filters
    filtered = court_stats.copy()
    if status_filter != "All":
        filtered = filtered[filtered['load_status'] == status_filter]
    if state_filter != "All" and 'state' in filtered.columns:
        filtered = filtered[filtered['state'] == state_filter]
    
    # Display Table
    st.subheader("📋 Court Load Table")
    
    display_cols = ['court', 'load_status', 'avg_duration', 'case_count', 'pct_diff']
    if 'state' in filtered.columns:
        display_cols.append('state')
    if 'tier' in filtered.columns:
        display_cols.append('tier')
    
    display_df = filtered[display_cols].copy()
    display_df.columns = [col.replace('_', ' ').title() for col in display_df.columns]
    
    def color_status(val):
        if val == "High Pendency":
            return 'background-color: #ffebee; color: #c62828;'
        elif val == "Fast Track":
            return 'background-color: #e8f5e9; color: #2e7d32;'
        else:
            return 'background-color: #fff3e0; color: #e65100;'
    
    # Safe Styler mapping for all Pandas versions
    styler = display_df.style
    if hasattr(styler, 'map'):
        styler = styler.map(color_status, subset=['Load Status'])
    else:
        styler = styler.applymap(color_status, subset=['Load Status'])
    
    st.dataframe(
        styler,
        use_container_width=True,
        height=380
    )
    st.caption(f"Showing {len(filtered)} of {len(court_stats)} courts")
    
    st.markdown("---")
    
    # Visual Analytics Tabs
    st.subheader("📊 Visual Analytics")
    tab1, tab2, tab3 = st.tabs(["📊 Bar Chart", "🏛️ Court Details", "📈 Status Distribution"])
    
    with tab1:
        fig = px.bar(
            filtered.head(30),
            x='court',
            y='avg_duration',
            color='load_status',
            color_discrete_map={
                "High Pendency": "#ef5350",
                "Moderate": "#ffa726",
                "Fast Track": "#66bb6a"
            },
            title='Average Duration by Court (Days)',
            labels={'avg_duration': 'Average Days', 'court': 'Court'},
            hover_data=['case_count']
        )
        fig.add_hline(
            y=national_avg,
            line_dash="dot",
            line_color="#64748b",
            annotation_text=f"National Avg ({national_avg:.0f}d)",
            annotation_position="bottom right"
        )
        fig.update_layout(xaxis_tickangle=-45, height=420, margin=dict(l=10, r=10, t=40, b=80))
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("#### Court Performance Details")
        for _, row in filtered.head(10).iterrows():
            status = row['load_status']
            avg = row['avg_duration']
            max_val = max(1.0, court_stats['avg_duration'].max())
            bar_length = min(avg / max_val * 100, 100)
            
            if status == "High Pendency":
                color = "#ef5350"
                badge = "badge-red"
            elif status == "Fast Track":
                color = "#66bb6a"
                badge = "badge-green"
            else:
                color = "#ffa726"
                badge = "badge-yellow"
            
            st.markdown(f"""
            <div style="margin-bottom: 14px; background: #f8fafc; padding: 12px 16px; border-radius: 10px; border: 1px solid #e2e8f0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 15px;"><b>{row['court']}</b></span>
                    <span><span class="{badge}">{status}</span></span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 13px; color: #64748b; margin-top: 4px;">
                    <span>📋 {row['case_count']} cases</span>
                    <span>{row.get('state', '')}</span>
                    <span>{row.get('tier', '')}</span>
                </div>
                <div style="background: #e2e8f0; border-radius: 8px; height: 16px; margin-top: 6px; overflow: hidden;">
                    <div style="background: {color}; width: {bar_length}%; height: 100%; border-radius: 8px;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 12px; color: #94a3b8; margin-top: 4px;">
                    <span>Avg: {avg:.0f} days</span>
                    <span>{row['pct_diff']:+.1f}% vs national benchmark</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            status_counts = court_stats['load_status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            
            fig_pie = px.pie(
                status_counts,
                values='Count',
                names='Status',
                color='Status',
                color_discrete_map={
                    "High Pendency": "#ef5350",
                    "Moderate": "#ffa726",
                    "Fast Track": "#66bb6a"
                },
                hole=0.45,
                title='Court Distribution by Load Status'
            )
            fig_pie.update_layout(height=350)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("#### 🔴 Top High Pendency Courts")
            high_courts = get_high_pendency_courts(court_stats, top_n=5)
            if len(high_courts) > 0:
                for _, row in high_courts.iterrows():
                    st.markdown(f"""
                    <div style="background: #fee2e2; padding: 10px 14px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #ef4444; color: #1e293b;">
                        <b>{row['court']}</b> — <b>{row['avg_duration']:.0f} days</b>
                        <span style="float: right; font-size: 12px; color: #64748b;">{row['case_count']} cases</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No High Pendency courts found.")
    
    st.markdown("---")
    
    # Recommendations
    st.subheader("💡 Strategic Recommendations")
    if recommendations:
        for rec in recommendations:
            if rec['type'] == 'critical':
                st.error(f"🚨 **Critical Bottleneck:** {rec['message']}\n\nCourts: {', '.join(rec.get('details', []))}")
            elif rec['type'] == 'warning':
                st.warning(f"⚠️ **High Pendency Alert:** {rec['message']}\n\nCourts: {', '.join(rec.get('details', []))}")
            elif rec['type'] == 'success':
                st.success(f"✅ **Fast-Track Benchmark:** {rec['message']}\n\nCourts: {', '.join(rec.get('details', []))}")
    else:
        st.info("All monitored courts are currently performing within expected benchmarks!")
    
    # CSV Export
    st.markdown("---")
    st.subheader("📥 Export Data")
    csv = export_court_load_csv(filtered)
    st.download_button(
        label="📥 Download Court Load Report (CSV)",
        data=csv,
        file_name="court_load_data.csv",
        mime="text/csv",
        use_container_width=True
    )

if __name__ == "__main__":
    show_court_load_dashboard()
