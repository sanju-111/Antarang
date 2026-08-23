# styles.py - ANTARANG Luxury Design System
import streamlit as st

LUXURY_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Inter+Tight:wght@300;400;500;600;700&display=swap');

:root {
    --primary-gold: #C9A227;
    --bright-gold: #F0D67B;
    --dark-gold: #9A7B1E;
    --bg-black: #0B0B0B;
    --card-bg: #141414;
    --card-hover: #1C1A14;
    --text-marble: #F3F0E7;
    --text-muted: #A69C86;
}

/* Base App Canvas */
.stApp {
    background: radial-gradient(circle at 50% -10%, rgba(201,162,39,.18), transparent 60%), #0B0B0B;
    color: #F3F0E7;
    font-family: 'Inter Tight', system-ui, sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; max-width: 1180px; }

/* Typography */
h1, h2, h3 {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    color: #F3F0E7 !important;
    font-weight: 700;
}

h4, h5, h6 {
    font-family: 'Inter Tight', sans-serif !important;
    color: #C9A227 !important;
    font-weight: 600;
}

.gold-text {
    background: linear-gradient(115deg, #9A7B1E, #F0D67B 45%, #B08A22);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.kicker {
    text-transform: uppercase;
    letter-spacing: 0.35em;
    font-size: 0.75rem;
    color: #A69C86;
}

.rule {
    height: 1px;
    background: linear-gradient(90deg, transparent, #C9A227, transparent);
    margin: 1.6rem 0;
    opacity: 0.6;
}

/* Card & Containers */
.card-container {
    background: #141414;
    border: 1px solid rgba(201, 162, 39, 0.28);
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
    transition: border-color 0.25s ease, box-shadow 0.25s ease;
}

.card-container:hover {
    border-color: rgba(201, 162, 39, 0.45);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6);
}

.section-title {
    color: #F0D67B;
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 1.6rem;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 1.2rem;
    border-bottom: 1px solid rgba(201, 162, 39, 0.2);
    padding-bottom: 0.6rem;
}

.form-label {
    color: #F3F0E7;
    font-size: 0.95rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 6px;
}

.form-label .glyph-icon {
    color: #C9A227;
    font-size: 1.15rem;
}

/* ---------- 3. Select Boxes (Dropdowns) ---------- */
[data-testid="stSelectbox"] > div > div,
div[data-baseweb="select"] > div {
    background-color: #141414 !important;
    border: 1px solid rgba(201, 162, 39, 0.28) !important;
    border-radius: 8px !important;
    color: #F3F0E7 !important;
    min-height: 56px !important;
    font-size: 1.25rem !important;
    padding: 4px 8px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

[data-testid="stSelectbox"] > div > div:focus-within,
div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="select"] > div:hover {
    border-color: #C9A227 !important;
    box-shadow: 0 0 0 3px rgba(201, 162, 39, 0.15) !important;
}

div[data-baseweb="select"] svg {
    fill: #C9A227 !important;
    stroke: #C9A227 !important;
}

div[data-baseweb="popover"] ul {
    background-color: #141414 !important;
    border: 1px solid rgba(201, 162, 39, 0.35) !important;
    border-radius: 10px !important;
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.85) !important;
    padding: 6px !important;
}

div[data-baseweb="popover"] li {
    color: #F3F0E7 !important;
    font-size: 1.2rem !important;
    border-radius: 6px !important;
    padding: 12px 18px !important;
    transition: background 0.15s ease, color 0.15s ease;
}

div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] li[aria-selected="true"] {
    background: rgba(201, 162, 39, 0.15) !important;
    color: #F0D67B !important;
}

/* ---------- 4. Numeric Sliders (1–10) ---------- */
.stSlider [data-baseweb="slider"] div[data-testid="stSliderTrack"] {
    background-color: #222222 !important;
    height: 8px !important;
    border-radius: 4px !important;
}

.stSlider [data-baseweb="slider"] div[data-testid="stSliderTrack"] > div {
    background: linear-gradient(90deg, #9A7B1E, #F0D67B) !important;
    box-shadow: 0 0 8px rgba(201, 162, 39, 0.35) !important;
}

.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: linear-gradient(145deg, #F0D67B, #C9A227) !important;
    border: 2px solid #0B0B0B !important;
    width: 22px !important;
    height: 22px !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.6) !important;
    transition: transform 180ms ease, box-shadow 180ms ease;
}

.stSlider [data-baseweb="slider"] div[role="slider"]:hover,
.stSlider [data-baseweb="slider"] div[role="slider"]:active {
    transform: scale(1.22);
    box-shadow: 0 0 14px rgba(240, 214, 123, 0.85) !important;
}

/* Value Bubble as uppercase badge pill */
[data-testid="stSliderThumbValue"] {
    background: #1C1914 !important;
    border: 1px solid rgba(201, 162, 39, 0.45) !important;
    color: #F0D67B !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    padding: 3px 9px !important;
    border-radius: 12px !important;
    letter-spacing: 0.05em !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.5) !important;
}

/* Tick Mark scale endpoint cues */
.stSlider [data-baseweb="slider"] [data-testid="stSliderTickBar"] {
    color: #8C8474 !important;
    font-size: 0.85rem !important;
}

/* ---------- 5. Categorical Step Slider (Intensity) ---------- */
[data-testid="stSelectSlider"] [data-baseweb="slider"] div[data-testid="stSliderTrack"] {
    background-color: #1E1E1E !important;
    height: 8px !important;
}

[data-testid="stSelectSlider"] [data-baseweb="slider"] div[role="slider"] {
    background: linear-gradient(145deg, #F0D67B, #9A7B1E) !important;
    border-radius: 4px !important;
    width: 26px !important;
    height: 18px !important;
}

/* ---------- 6. Number Inputs ---------- */
div[data-testid="stNumberInput"] > div {
    background-color: #141414 !important;
    border: 1px solid rgba(201, 162, 39, 0.28) !important;
    border-radius: 8px !important;
    overflow: hidden;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

div[data-testid="stNumberInput"] > div:focus-within {
    border-color: #C9A227 !important;
    box-shadow: 0 0 0 3px rgba(201, 162, 39, 0.15) !important;
}

div[data-testid="stNumberInput"] input {
    background-color: #141414 !important;
    color: #F3F0E7 !important;
    border: none !important;
    font-weight: 500;
}

div[data-testid="stNumberInput"] button {
    background-color: #181818 !important;
    color: #C9A227 !important;
    border: none !important;
    border-left: 1px solid rgba(201, 162, 39, 0.2) !important;
    font-weight: 800 !important;
    transition: background-color 0.15s ease, color 0.15s ease;
}

div[data-testid="stNumberInput"] button:hover {
    background-color: #C9A227 !important;
    color: #0B0B0B !important;
}

div[data-testid="stNumberInput"] button:disabled {
    opacity: 0.3 !important;
    cursor: not-allowed !important;
}

/* ---------- 7. Advanced Details Accordion (st.expander) ---------- */
[data-testid="stExpander"] {
    background: #141414 !important;
    border: 1px solid rgba(201, 162, 39, 0.25) !important;
    border-radius: 12px !important;
    margin-bottom: 1.5rem !important;
    overflow: hidden;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

[data-testid="stExpander"]:hover {
    border-color: rgba(201, 162, 39, 0.45) !important;
}

[data-testid="stExpander"] summary {
    padding: 0.9rem 1.2rem !important;
    color: #F0D67B !important;
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    transition: background 200ms ease;
}

[data-testid="stExpander"] summary:hover {
    background: rgba(201, 162, 39, 0.08) !important;
}

[data-testid="stExpander"] summary svg {
    fill: #C9A227 !important;
    stroke: #C9A227 !important;
    transition: transform 200ms ease;
}

[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {
    padding: 1.2rem 1.4rem !important;
    border-top: 1px solid rgba(201, 162, 39, 0.15) !important;
    animation: fadeIn 200ms ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-4px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ---------- 8. Radio Buttons ---------- */
div[role="radiogroup"] label {
    color: #F3F0E7 !important;
    font-weight: 500;
}

div[role="radiogroup"] label[data-checked="true"] > div:first-child {
    background-color: #C9A227 !important;
    border-color: #F0D67B !important;
    box-shadow: inset 0 0 0 4px #0B0B0B !important;
}

/* ---------- 9. Hero Primary Action Button (Predict Eligibility) ---------- */
.stButton > button,
div[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(115deg, #9A7B1E, #F0D67B 45%, #B08A22) !important;
    color: #0B0B0B !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2rem !important;
    font-family: 'Inter Tight', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    font-size: 0.88rem !important;
    box-shadow: 0 4px 20px rgba(201, 162, 39, 0.4) !important;
    cursor: pointer !important;
    transition: transform 200ms ease, box-shadow 200ms ease, filter 200ms ease !important;
}

.stButton > button:hover,
div[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 30px rgba(201, 162, 39, 0.65) !important;
    filter: brightness(1.06) !important;
}

.stButton > button:active,
div[data-testid="stFormSubmitButton"] button:active {
    transform: translateY(-1px) !important;
    box-shadow: 0 3px 12px rgba(201, 162, 39, 0.4) !important;
}

.stButton > button:focus-visible,
div[data-testid="stFormSubmitButton"] button:focus-visible {
    outline: 2px solid #F0D67B !important;
    outline-offset: 2px !important;
}

/* Secondary Portal Back Link */
div[data-testid="stPageLink-NavLink"] {
    background: transparent !important;
    border: 1px solid rgba(201, 162, 39, 0.3) !important;
    border-radius: 8px !important;
    color: #F0D67B !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-size: 0.78rem !important;
    padding: 0.45rem 0.9rem !important;
    display: inline-flex !important;
    width: auto !important;
    margin-bottom: 1rem !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stPageLink-NavLink"]:hover {
    background: rgba(201, 162, 39, 0.12) !important;
    border-color: #C9A227 !important;
    box-shadow: 0 0 15px rgba(201, 162, 39, 0.3) !important;
    transform: translateY(-1px) !important;
}

/* Result Cards */
.result-card {
    border-radius: 14px;
    padding: 2.2rem;
    text-align: center;
    background: #141414;
    border: 1px solid rgba(201, 162, 39, 0.3);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
}

.result-eligible {
    border-color: #C9A227;
    background: linear-gradient(145deg, #18150D, #121008);
}

.result-conditional {
    border-color: #9A7B1E;
    background: linear-gradient(145deg, #16140D, #100E08);
}

.result-not-eligible {
    border-color: rgba(201, 162, 39, 0.2);
    background: #141414;
}

.confidence-bar {
    background: #222222;
    border-radius: 50px;
    height: 10px;
    overflow: hidden;
    margin-top: 0.5rem;
}

.confidence-fill {
    height: 100%;
    background: linear-gradient(90deg, #9A7B1E, #F0D67B);
    border-radius: 50px;
    transition: width 1s ease;
}

.footer {
    text-align: center;
    padding: 2rem 0;
    border-top: 1px solid rgba(201, 162, 39, 0.2);
    color: #8C8474;
    font-size: 0.72rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
}

/* Respect Reduced Motion */
@media (prefers-reduced-motion: reduce) {
    *, ::before, ::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
</style>
"""

def inject_luxury_css():
    """Inject luxury CSS globally"""
    st.markdown(LUXURY_CSS, unsafe_allow_html=True)
