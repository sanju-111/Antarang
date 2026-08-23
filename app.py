"""
ANTARANG — Justice Decoded
Master Landing Portal & Judicial Triage Command Center

Run:
    streamlit run app.py
"""

import base64
from pathlib import Path
import streamlit as st
import styles
st.markdown(styles.LUXURY_CSS, unsafe_allow_html=True)
# --------------------------------------------------------------------------------------
# CONFIG
# --------------------------------------------------------------------------------------
st.set_page_config(
    page_title="Antarang — Justice Decoded",
    page_icon="⚖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

GOLD = "#C9A227"
GOLD_BRIGHT = "#F0D67B"
BLACK = "#0B0B0B"
CARD = "#141414"
CARD_HOVER = "#1C1A14"
MARBLE = "#F3F0E7"

LOGO_PATH = Path(__file__).parent / "logo.png"


def logo_data_uri() -> str:
    if LOGO_PATH.exists():
        b64 = base64.b64encode(LOGO_PATH.read_bytes()).decode()
        return f"data:image/png;base64,{b64}"
    svg = f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'>
      <circle cx='100' cy='100' r='96' fill='{BLACK}' stroke='{GOLD}' stroke-width='4'/>
      <text x='100' y='118' font-size='72' text-anchor='middle'>⚖️</text></svg>"""
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


LOGO = logo_data_uri()

# --------------------------------------------------------------------------------------
# GLOBAL STYLE (Black + Gold + Marble Design System)
# --------------------------------------------------------------------------------------
st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Inter+Tight:wght@300;400;500;600;700&display=swap');

.stApp {{
    background:
        radial-gradient(circle at 50% -10%, rgba(201,162,39,.18), transparent 60%),
        {BLACK};
    color: {MARBLE};
    font-family: 'Inter Tight', system-ui, sans-serif;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 1.5rem; max-width: 1180px; }}

h1, h2, h3 {{ font-family: 'Cormorant Garamond', Georgia, serif !important; color: {MARBLE}; }}

.gold-text {{
    background: linear-gradient(115deg,#9A7B1E,{GOLD_BRIGHT} 45%,#B08A22);
    -webkit-background-clip: text; background-clip: text; color: transparent;
}}
.rule {{ height:1px; background:linear-gradient(90deg,transparent,{GOLD},transparent); margin:1.8rem 0; opacity:0.6; }}
.kicker {{ text-transform:uppercase; letter-spacing:.35em; font-size:.72rem; color:#A69C86; }}

/* ---------- Splash animation ---------- */
.splash-static {{
    display:flex; flex-direction:column; align-items:center; justify-content:center; gap:28px;
    height: 72vh;
    background: {BLACK};
}}
.seal {{ position:relative; width:220px; height:220px; animation: sealin 1.1s cubic-bezier(.2,.8,.2,1) both; }}
.seal img {{ width:100%; height:100%; border-radius:50%; object-fit:cover; }}
.seal .ring {{
    position:absolute; inset:-14px; border-radius:50%;
    border:2px solid transparent; border-top-color:{GOLD}; border-right-color:{GOLD};
    animation: spin 1.6s cubic-bezier(.4,0,.2,1) infinite;
}}
.seal .shine {{
    position:absolute; top:0; left:-40%; width:40%; height:100%;
    background:linear-gradient(90deg,transparent,rgba(240,214,123,.45),transparent);
    transform:skewX(-18deg); animation: sweep 1.8s ease-in-out .6s both; border-radius:50%;
}}
.splash-static h1 {{ font-size:2.4rem; letter-spacing:.42em; margin:0; animation: rise .8s ease .9s both; }}
.splash-static p  {{ animation: rise .8s ease 1.1s both; }}

@keyframes sealin  {{ 0%{{opacity:0;transform:scale(.7) rotate(-8deg);filter:blur(10px)}} 100%{{opacity:1;transform:none;filter:none}} }}
@keyframes spin    {{ to {{ transform: rotate(360deg); }} }}
@keyframes sweep   {{ 0%{{transform:translateX(-120%) skewX(-18deg)}} 100%{{transform:translateX(320%) skewX(-18deg)}} }}
@keyframes rise    {{ from{{opacity:0;transform:translateY(18px)}} to{{opacity:1;transform:none}} }}
@keyframes tilt    {{ 0%,100%{{transform:rotate(-3deg)}} 50%{{transform:rotate(3deg)}} }}

.hero-logo img {{ width:160px; height:160px; border-radius:50%; box-shadow:0 18px 60px -22px rgba(201,162,39,.8); }}
.hero-logo {{ text-align:center; animation: rise .8s ease both; }}

/* ---------- Uniform Clickable Card Grid ---------- */
div[data-testid="column"] {{
    display: flex;
    flex-direction: column;
}}

div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: {CARD};
    border: 1px solid rgba(201,162,39,.25);
    border-radius: 16px;
    position: relative;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
    min-height: 330px;
    padding: 1.4rem;
    box-sizing: border-box;
    transition: all .28s cubic-bezier(.2, .8, .2, 1);
}}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
    transform: translateY(-5px);
    background: {CARD_HOVER};
    border-color: {GOLD};
    box-shadow: 0 16px 40px -15px rgba(201,162,39,.75);
}}

/* Audience Selector Box Custom Min-Height */
.audience-box div[data-testid="stVerticalBlockBorderWrapper"] {{
    min-height: 210px !important;
    text-align: center;
    padding: 1.2rem;
}}

/* Stretches the link/button across the entire card container */
div[data-testid="stVerticalBlockBorderWrapper"] a[data-testid="stPageLink-NavLink"]::after,
div[data-testid="stVerticalBlockBorderWrapper"] .stButton > button::after {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 5;
    cursor: pointer;
}}

.stButton > button {{
    width: 100%;
    background: #181818;
    color: {MARBLE};
    border: 1px solid rgba(201,162,39,.35);
    border-radius: 10px;
    padding: .65rem 1rem;
    font-weight: 600;
    letter-spacing: .12em;
    text-transform: uppercase;
    font-size: .78rem;
    transition: all .25s ease;
}}
.stButton > button:hover {{
    border-color: {GOLD};
    color: {GOLD_BRIGHT};
    box-shadow: 0 10px 25px -10px rgba(201,162,39,.9);
}}

/* Page Link Styling */
div[data-testid="stPageLink-NavLink"] {{
    background: linear-gradient(115deg, #1C1C1C, #141414);
    border: 1px solid rgba(201,162,39,.35);
    border-radius: 10px;
    padding: 0.65rem 1rem;
    color: {GOLD_BRIGHT} !important;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-size: 0.78rem;
    transition: all 0.25s ease;
    margin-top: auto;
}}

div[data-testid="stPageLink-NavLink"]:hover {{
    border-color: {GOLD};
    background: linear-gradient(115deg, #262626, #1A1A1A);
    box-shadow: 0 8px 25px -10px rgba(201,162,39,.9);
}}

.glyph {{ font-size:2.2rem; display:inline-block; animation: tilt 4.5s ease-in-out infinite; color:{GOLD}; margin-bottom: 0.4rem; }}

/* Stat Banner */
.stat-strip {{
    background: linear-gradient(145deg, #121212, #0D0D0D);
    border: 1px solid rgba(201,162,39,0.22);
    border-radius: 16px;
    padding: 1.4rem;
    margin: 2.5rem 0 1rem 0;
    display: flex;
    justify-content: space-around;
    align-items: center;
    flex-wrap: wrap;
    gap: 1.5rem;
    text-align: center;
}}

.stat-item-num {{
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(115deg, #9A7B1E, #F0D67B 45%, #B08A22);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}}

.stat-item-label {{
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #A69C86;
    margin-top: 0.2rem;
}}

.badge-tag {{
    display: inline-block;
    font-size: 0.68rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.2rem 0.65rem;
    border-radius: 20px;
    background: rgba(201,162,39,0.12);
    border: 1px solid rgba(201,162,39,0.3);
    color: {GOLD_BRIGHT};
    margin-bottom: 0.6rem;
}}

.footer {{ margin-top:3rem; padding-top:1.2rem; border-top:1px solid rgba(201,162,39,.2);
    display:flex; justify-content:space-between; font-size:.72rem; letter-spacing:.28em;
    text-transform:uppercase; color:#8C8474; }}
</style>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------------------
# SPLASH SCREEN (Runs once per browser session)
# --------------------------------------------------------------------------------------
if "splash_done" not in st.session_state:
    st.markdown(
        f"""
        <style>
        /* Make the single Streamlit button invisible and cover the entire screen */
        .stButton > button {{
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            opacity: 0 !important;
            z-index: 99999 !important;
            cursor: pointer !important;
        }}
        .click-anywhere {{
            position: fixed;
            bottom: 8%;
            left: 0;
            width: 100%;
            text-align: center;
            color: #A69C86;
            letter-spacing: 0.2em;
            font-size: 0.85rem;
            text-transform: uppercase;
            animation: pulse-text 2.5s infinite;
            z-index: 99998;
        }}
        @keyframes pulse-text {{
            0%, 100% {{ opacity: 0.4; transform: translateY(0); }}
            50% {{ opacity: 1; transform: translateY(-3px); }}
        }}
        </style>
        <div class="splash-static">
          <div class="seal">
            <div class="ring"></div>
            <img src="{LOGO}" alt="Antarang"/>
            <div class="shine"></div>
          </div>
          <h1 class="gold-text">ANTARANG</h1>
          <p class="kicker">Justice Decoded</p>
        </div>
        <div class="click-anywhere">Click anywhere to enter portal</div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Enter Portal", use_container_width=True):
        st.session_state.splash_done = True
        st.rerun()
    st.stop()
# --------------------------------------------------------------------------------------
# STATE
# --------------------------------------------------------------------------------------
st.session_state.setdefault("audience", None)   # "public" | "admin"

# --------------------------------------------------------------------------------------
# HEADER & FOOTER
# --------------------------------------------------------------------------------------
def header():
    left, right = st.columns([3, 2])
    with left:
        st.markdown(
            f"""<div style="display:flex;align-items:center;gap:14px">
                <img src="{LOGO}" style="width:40px;height:40px;border-radius:50%"/>
                <span class="gold-text" style="font-family:'Cormorant Garamond',serif;
                      font-size:1.35rem;letter-spacing:.32em;font-weight:700">ANTARANG</span></div>""",
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            '<div class="kicker" style="text-align:right;padding-top:10px">'
            "Tech Fusion · Judicial AI Platform</div>",
            unsafe_allow_html=True,
        )
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)


def footer():
    st.markdown(
        '<div class="footer"><span>Team: Sanjana · Ujjwal · Geeta</span>'
        "<span>Antarang Judicial Triage System · 2026</span></div>",
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------------------
# HOME PORTAL HERO
# --------------------------------------------------------------------------------------
header()

st.markdown(
    f"""<div class="hero-logo"><img src="{LOGO}"/>
    <h1 class="gold-text" style="font-size:3.2rem;letter-spacing:.28em;margin:1.2rem 0 .3rem">ANTARANG</h1>
    <p class="kicker">Justice Decoded</p>
    <p style="max-width:680px;margin:1rem auto 0;color:#A69C86;font-size:.95rem;line-height:1.75">
    An end-to-end AI judicial intelligence system built to evaluate ADR mediation suitability, 
    forecast case lifecycles, audit statutory filings, balance court loads, and match litigants with specialist advocates.
    </p></div>""",
    unsafe_allow_html=True,
)

st.write("")

# --------------------------------------------------------------------------------------
# AUDIENCE SELECTOR (Symmetrical Equal-Size Boxes)
# --------------------------------------------------------------------------------------
pad1, c1, c2, pad2 = st.columns([1, 1.2, 1.2, 1])

# --- Public Card ---
with c1:
    st.markdown('<div class="audience-box">', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<div class="glyph">✦</div>', unsafe_allow_html=True)
        st.markdown("### Public")
        st.caption("Citizens & Litigants")
        st.write("")
        btn_label = "✓ Viewing Public" if st.session_state.audience == "public" else "Enter as Public"
        if st.button(btn_label, key="btn_public"):
            st.session_state.audience = "public"
    st.markdown('</div>', unsafe_allow_html=True)

# --- Admin Card ---
with c2:
    st.markdown('<div class="audience-box">', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<div class="glyph">✧</div>', unsafe_allow_html=True)
        st.markdown("### Admin")
        st.caption("Judicial Authorities & Registry")
        st.write("")
        btn_label = "✓ Viewing Admin" if st.session_state.audience == "admin" else "Enter as Admin"
        if st.button(btn_label, key="btn_admin"):
            st.session_state.audience = "admin"
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------------------------------------------
# FEATURE GRID (Symmetrical Uniform Cards)
# --------------------------------------------------------------------------------------
if st.session_state.audience:
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    
    if st.session_state.audience == "public":
        st.markdown('<h2 class="gold-text">🏛️ Citizen Legal Intelligence</h2>', unsafe_allow_html=True)
        st.caption("Click anywhere on any card box to launch the corresponding AI tool.")
        st.write("")
        
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown('<span class="badge-tag">ADR Assessment Engine</span>', unsafe_allow_html=True)
                st.markdown('<div class="glyph">⟡</div>', unsafe_allow_html=True)
                st.markdown("### Mediation Predictor")
                st.markdown(f'<p class="kicker" style="color:{GOLD}">Amicable Out-of-Court Settlement</p>', unsafe_allow_html=True)
                st.write("Evaluates dispute suitability for mediation across 26 distinct categories, predicting success probability and cost savings.")
                st.page_link("pages/1_⚖️_Mediation_Predictor.py", label="Launch Mediation Predictor →", icon="⚖️")
                
            st.write("")
            with st.container(border=True):
                st.markdown('<span class="badge-tag">Court Filing Compliance</span>', unsafe_allow_html=True)
                st.markdown('<div class="glyph">§</div>', unsafe_allow_html=True)
                st.markdown("### Document Checklist")
                st.markdown(f'<p class="kicker" style="color:{GOLD}">Mandatory Statutory Filings</p>', unsafe_allow_html=True)
                st.write("Interactive checklists of petitions, annexures, court fees, notarization requirements, and downloadable verification records.")
                st.page_link("pages/3_📋_Documents_Checklist.py", label="Launch Document Checklist →", icon="📋")

        with c2:
            with st.container(border=True):
                st.markdown('<span class="badge-tag">ML Timeline Forecaster</span>', unsafe_allow_html=True)
                st.markdown('<div class="glyph">⧗</div>', unsafe_allow_html=True)
                st.markdown("### Duration Predictor")
                st.markdown(f'<p class="kicker" style="color:{GOLD}">Judicial Lifecycle Estimation</p>', unsafe_allow_html=True)
                st.write("Random Forest regression modeling case lifecycle duration across court tiers, complexity factors, and historical disposal trends.")
                st.page_link("pages/2_⏱️_Duration_Predictor.py", label="Launch Duration Predictor →", icon="⏱️")
                
            st.write("")
            with st.container(border=True):
                st.markdown('<span class="badge-tag">Verified Representation</span>', unsafe_allow_html=True)
                st.markdown('<div class="glyph">⚖</div>', unsafe_allow_html=True)
                st.markdown("### Find My Advocate")
                st.markdown(f'<p class="kicker" style="color:{GOLD}">Specialist Recommendation Engine</p>', unsafe_allow_html=True)
                st.write("Matches litigants with top verified legal advocates filtered by practice domain, court tier, fee budget, and language.")
                st.page_link("pages/5_👨‍⚖️_Find_My_Advocate.py", label="Launch Advocate Finder →", icon="👨‍⚖️")

    elif st.session_state.audience == "admin":
        st.markdown('<h2 class="gold-text">⚖️ Court Registry & Executive Dashboard</h2>', unsafe_allow_html=True)
        st.caption("Click anywhere on any card box to launch the corresponding administrative tool.")
        st.write("")
        
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown('<span class="badge-tag">Pendency & Capacity Analytics</span>', unsafe_allow_html=True)
                st.markdown('<div class="glyph">🏛</div>', unsafe_allow_html=True)
                st.markdown("### Court Load Indicator")
                st.markdown(f'<p class="kicker" style="color:{GOLD}">Workload & Bottleneck Diagnostics</p>', unsafe_allow_html=True)
                st.write("Real-time monitoring of court pendency, disposal efficiency scores, state/tier comparisons, and CSV reporting.")
                st.page_link("pages/4_🏛️_Court_Load_Indicator.py", label="Launch Court Load Indicator →", icon="🏛️")

        with c2:
            with st.container(border=True):
                st.markdown('<span class="badge-tag">Docket Optimization</span>', unsafe_allow_html=True)
                st.markdown('<div class="glyph">🚀</div>', unsafe_allow_html=True)
                st.markdown("### Fast-Track Case Ordering")
                st.markdown(f'<p class="kicker" style="color:{GOLD}">Shortest-Job-First (SJF) Simulation</p>', unsafe_allow_html=True)
                st.write("Determine the optimal case sequencing queue based on expected disposal times to rapidly clear backlogs and decrease median wait times.")
                st.page_link("pages/6_🚀_Fast_Track_Case_Order.py", label="Run Order Optimization →", icon="🚀")

# --------------------------------------------------------------------------------------
# SYSTEM BENCHMARKS STRIP
# --------------------------------------------------------------------------------------
st.markdown(
    """
    <div class="stat-strip">
        <div>
            <div class="stat-item-num">5,000+</div>
            <div class="stat-item-label">Dispute Scenarios</div>
        </div>
        <div>
            <div class="stat-item-num">26</div>
            <div class="stat-item-label">Case Categories</div>
        </div>
        <div>
            <div class="stat-item-num">19</div>
            <div class="stat-item-label">State Jurisdictions</div>
        </div>
        <div>
            <div class="stat-item-num">94%</div>
            <div class="stat-item-label">Mediation Recall</div>
        </div>
        <div>
            <div class="stat-item-num">100+</div>
            <div class="stat-item-label">Statutory Checklists</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

footer()