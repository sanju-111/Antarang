# pages/6_🚀_Fast_Track_Case_Order.py - ANTARANG Fast-Track Case Processing Order
import os
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Ensure root and models are in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models')))

# Page Configuration
st.set_page_config(
    page_title="Fast-Track Case Ordering | Antarang",
    page_icon="🚀",
    layout="wide"
)

# Inject luxury styling from styles.py
from styles import inject_luxury_css
inject_luxury_css()

# Import backend logic
try:
    from models.Fast_Track_case_order import (
        calculate_fast_track_impact,
        get_case_priority,
        get_priority_color,
        get_case_type_name,
        get_case_summary,
        generate_fast_track_recommendations,
        export_fast_track_order,
        calculate_time_saved_visualization
    )
except ImportError:
    from Fast_Track_case_order import (
        calculate_fast_track_impact,
        get_case_priority,
        get_priority_color,
        get_case_type_name,
        get_case_summary,
        generate_fast_track_recommendations,
        export_fast_track_order,
        calculate_time_saved_visualization
    )

# Navigation back link
try:
    st.page_link("app.py", label="← Back to Portal", icon="🏛️")
except Exception:
    pass

# Header Banner
st.markdown("""
<div class="main-header">
    <div class="hero-badge">Docket Optimization Engine</div>
    <h1>🚀 Fast-Track Case Ordering & Queue Optimization</h1>
    <p>Shortest-Job-First (SJF) triage simulation to maximize case disposal throughput, reduce median citizen wait times & eliminate docket stagnation</p>
</div>
""", unsafe_allow_html=True)


# Load dataset
@st.cache_data
def load_data():
    paths = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'cleaned_cases_antarang.csv'),
        os.path.join('data', 'cleaned_cases_antarang.csv'),
        'cleaned_cases_antarang.csv'
    ]
    for p in paths:
        if os.path.exists(p):
            return pd.read_csv(p)
    return None

df = load_data()

if df is None:
    st.error("❌ Dataset (`cleaned_cases_antarang.csv`) not found in data/ folder!")
    st.stop()

# Ensure duration_days column exists
if 'duration_days' not in df.columns:
    st.error("❌ 'duration_days' column not found in dataset!")
    st.stop()

# Sidebar / Top Filter Controls
with st.container(border=True):
    st.markdown('<p class="section-title">⚜️ Simulation & Docket Scope Controls</p>', unsafe_allow_html=True)

    f_col1, f_col2, f_col3 = st.columns([1.5, 1.2, 1.2])

    with f_col1:
        sample_size = st.slider(
            "Docket Batch Size (Cases to Sequence)", 
            min_value=20, 
            max_value=min(1000, len(df)), 
            value=100, 
            step=20,
            help="Select the batch of pending cases to optimize in this triage session"
        )

    with f_col2:
        states_list = ["All States"] + sorted(df['stateName'].dropna().unique().tolist()) if 'stateName' in df.columns else ["All States"]
        selected_state = st.selectbox("Filter Jurisdiction", states_list)

    with f_col3:
        case_types_list = ["All Types"] + sorted(df['caseType'].dropna().unique().tolist()) if 'caseType' in df.columns else ["All Types"]
        selected_type = st.selectbox("Filter Case Category", case_types_list)

# Apply filters
filtered_df = df.copy()
if selected_state != "All States" and 'stateName' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['stateName'] == selected_state]
if selected_type != "All Types" and 'caseType' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['caseType'] == selected_type]

if len(filtered_df) == 0:
    st.warning("⚠️ No cases match the selected filters. Please broaden your selection.")
    st.stop()

# Take sample
sample_batch = filtered_df.head(sample_size).copy()

# Calculate Fast-Track Impact
metrics = calculate_fast_track_impact(sample_batch)
summary = get_case_summary(sample_batch)
recommendations = generate_fast_track_recommendations(metrics)

# ---------- Impact KPI Metrics Row ----------
st.markdown("### 📊 Triage Impact Overview")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        label="Total Waiting Time Saved",
        value=f"{metrics['time_saved']:,.0f} Days",
        delta=f"−{metrics['pct_saved']:.1f}% reduction",
        delta_color="normal"
    )

with kpi2:
    st.metric(
        label="50% Backlog Cleared In",
        value=f"{metrics['fast_half_time']:,.0f} Days",
        delta=f"vs {metrics['fifo_half_time']:,.0f}d standard",
        delta_color="inverse"
    )

with kpi3:
    st.metric(
        label="Disposed in First 30 Days",
        value=f"{metrics['fast_cases_in_month']} Cases",
        delta=f"+{metrics['fast_cases_in_month'] - metrics['fifo_cases_in_month']} vs FIFO",
        delta_color="normal"
    )

with kpi4:
    st.metric(
        label="Disposed in 1st Year",
        value=f"{metrics['fast_cases_in_year']} Cases",
        delta=f"of {metrics['total_cases']} total in batch"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ---------- Visual Race Comparison Tabs ----------
tab1, tab2, tab3 = st.tabs(["🏁 Cumulative Wait Time Race", "📈 Priority Breakdown", "💡 Strategic Recommendations"])

with tab1:
    col_race1, col_race2 = st.columns([1.8, 1.2])
    
    with col_race1:
        st.markdown("#### ⏳ Cumulative Citizen Wait Time: FIFO vs. Fast-Track")
        
        # Build cumulative timeline dataframe
        fifo_c = sample_batch.copy().reset_index(drop=True)
        fast_c = sample_batch.sort_values('duration_days').copy().reset_index(drop=True)
        
        fifo_cumsum = fifo_c['duration_days'].cumsum()
        fast_cumsum = fast_c['duration_days'].cumsum()
        
        chart_df = pd.DataFrame({
            'Case Index': list(range(1, len(sample_batch) + 1)),
            'Standard FIFO Queue (Days)': fifo_cumsum,
            'Fast-Track Optimized (Days)': fast_cumsum
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=chart_df['Case Index'], 
            y=chart_df['Standard FIFO Queue (Days)'],
            mode='lines',
            name='FIFO Standard Order',
            line=dict(color='#EF5350', width=3.5, dash='dash')
        ))
        fig.add_trace(go.Scatter(
            x=chart_df['Case Index'], 
            y=chart_df['Fast-Track Optimized (Days)'],
            mode='lines',
            name='Fast-Track (SJF)',
            line=dict(color='#F0D67B', width=4)
        ))
        
        fig.update_layout(
            paper_bgcolor='#141414',
            plot_bgcolor='#141414',
            font=dict(color='#F3F0E7', family='Inter Tight, sans-serif', size=14),
            height=380,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=13, color='#F3F0E7')
            ),
            xaxis=dict(
                title="Number of Cases Processed",
                gridcolor='rgba(201, 162, 39, 0.1)',
                title_font=dict(size=14, color='#A69C86')
            ),
            yaxis=dict(
                title="Cumulative Days Waited",
                gridcolor='rgba(201, 162, 39, 0.1)',
                title_font=dict(size=14, color='#A69C86')
            )
        )
        st.plotly_chart(fig, width='stretch')
    
    with col_race2:
        st.markdown("#### ⚡ Why Fast-Tracking Works")
        st.markdown(f"""
        <div style="background: #181818; border: 1px solid rgba(201,162,39,0.3); border-radius: 14px; padding: 1.4rem; font-size: 0.95rem; line-height: 1.7; color: #F3F0E7;">
            <p style="color: #F0D67B; font-weight: 700; margin-bottom: 0.6rem; font-size: 1.1rem; font-family: 'Cormorant Garamond', serif;">
                The Judicial Queue Paradox
            </p>
            When complex, multi-year trials occupy hearing slots first, dozens of quick-resolution matters (bails, consent petitions, motor claims) are blocked behind them.
            <br><br>
            By sequencing <b style="color: #F0D67B;">short-duration matters first</b>, the court disposes of <b>{metrics['fast_cases_in_month']} cases in 30 days</b> instead of just {metrics['fifo_cases_in_month']}, clearing citizen backlogs <b>{metrics['pct_saved']:.0f}% faster</b> without adding any extra judges.
        </div>
        """, unsafe_allow_html=True)

with tab2:
    p_col1, p_col2 = st.columns(2)
    
    with p_col1:
        st.markdown("#### 🎯 Case Distribution by Priority Tier")
        tier_data = pd.DataFrame({
            'Priority Tier': ['🚀 Immediate (<30d)', '🟢 Quick (30–100d)', '🟡 Medium (100–365d)', '🔴 Long (>365d)'],
            'Count': [
                len(sample_batch[sample_batch['duration_days'] < 30]),
                len(sample_batch[(sample_batch['duration_days'] >= 30) & (sample_batch['duration_days'] < 100)]),
                len(sample_batch[(sample_batch['duration_days'] >= 100) & (sample_batch['duration_days'] < 365)]),
                len(sample_batch[sample_batch['duration_days'] >= 365])
            ]
        })
        
        fig_pie = px.pie(
            tier_data,
            names='Priority Tier',
            values='Count',
            color='Priority Tier',
            color_discrete_map={
                '🚀 Immediate (<30d)': '#00E676',
                '🟢 Quick (30–100d)': '#66BB6A',
                '🟡 Medium (100–365d)': '#FFA726',
                '🔴 Long (>365d)': '#EF5350'
            },
            hole=0.45
        )
        fig_pie.update_layout(
            paper_bgcolor='#141414',
            plot_bgcolor='#141414',
            font=dict(color='#F3F0E7', family='Inter Tight, sans-serif', size=13),
            height=340,
            margin=dict(l=10, r=10, t=20, b=20),
            legend=dict(font=dict(size=13, color='#F3F0E7'))
        )
        st.plotly_chart(fig_pie, width='stretch')
        
    with p_col2:
        st.markdown("#### ⏱️ Duration Breakdown Summary")
        st.markdown(f"""
        <div style="background: #181818; border: 1px solid rgba(201,162,39,0.25); border-radius: 14px; padding: 1.4rem; color: #F3F0E7;">
            <table style="width: 100%; border-collapse: collapse; font-size: 0.95rem;">
                <tr style="border-bottom: 1px solid rgba(201,162,39,0.2); height: 38px;">
                    <td><b>Total Batch Cases:</b></td>
                    <td style="text-align: right; color: #F0D67B; font-weight: 700;">{summary.get('total_cases', 0):,}</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(201,162,39,0.15); height: 38px;">
                    <td>⚡ Quick Cases (&lt;100 days):</td>
                    <td style="text-align: right; color: #66BB6A; font-weight: 600;">{summary.get('quick_count', 0)} cases</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(201,162,39,0.15); height: 38px;">
                    <td>🟡 Medium Cases (100–365d):</td>
                    <td style="text-align: right; color: #FFA726; font-weight: 600;">{summary.get('medium_count', 0)} cases</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(201,162,39,0.15); height: 38px;">
                    <td>🔴 Long Trials (&gt;365 days):</td>
                    <td style="text-align: right; color: #EF5350; font-weight: 600;">{summary.get('long_count', 0)} cases</td>
                </tr>
                <tr style="height: 38px;">
                    <td><b>Median Lifecycle:</b></td>
                    <td style="text-align: right; color: #F0D67B; font-weight: 700;">{summary.get('median_duration', 0):.0f} days</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown("#### 💡 Algorithmic Triage Recommendations")
    for rec in recommendations:
        st.markdown(f"""
        <div style="background: #181818; border-left: 4px solid #C9A227; border: 1px solid rgba(201,162,39,0.25); border-radius: 10px; padding: 1.2rem; margin-bottom: 1rem;">
            <p style="color: #F0D67B; font-weight: 700; font-size: 1.1rem; margin: 0 0 0.4rem 0;">
                ✓ {rec['title']}
            </p>
            <p style="color: #F3F0E7; font-size: 0.95rem; margin: 0 0 0.4rem 0;">
                {rec['message']}
            </p>
            <p style="color: #A69C86; font-size: 0.88rem; margin: 0;">
                <b>Recommended Action:</b> {rec['action']}
            </p>
        </div>
        """, unsafe_allow_html=True)

# ---------- Ranked Fast-Track Docket Table ----------
st.markdown("---")
st.markdown("### 📋 Recommended Fast-Track Hearing Order")
st.caption("Cases arranged in optimal sequence (shortest expected disposal first) to maximize judicial clearance rate.")

sorted_df = metrics['sorted_cases'].copy()
sorted_df['Order'] = range(1, len(sorted_df) + 1)
sorted_df['Priority'] = sorted_df['duration_days'].apply(get_case_priority)

display_cols = ['Order', 'Priority', 'duration_days']
rename_map = {'duration_days': 'Expected Duration (Days)'}

if 'caseType' in sorted_df.columns:
    display_cols.append('caseType')
    rename_map['caseType'] = 'Case Type'
if 'courtName' in sorted_df.columns:
    display_cols.append('courtName')
    rename_map['courtName'] = 'Court Name'
if 'stateName' in sorted_df.columns:
    display_cols.append('stateName')
    rename_map['stateName'] = 'State'

table_df = sorted_df[display_cols].rename(columns=rename_map)

st.dataframe(
    table_df,
    hide_index=True,
    width='stretch',
    height=400
)

# Export CSV Button
csv_data = table_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Fast-Track Docket Order (CSV)",
    data=csv_data,
    file_name=f"fast_track_docket_{selected_state.replace(' ', '_')}.csv",
    mime="text/csv",
    width="stretch"
)

# Footer
st.markdown("""
<div class="footer">
    <span>⚜️</span> ANTARANG · Fast-Track Case Ordering Module <span>⚜️</span><br>
    Algorithmic Queue Optimization for Indian Judiciary
</div>
""", unsafe_allow_html=True)
