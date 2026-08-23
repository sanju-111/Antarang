# styles.py
import streamlit as st

LUXURY_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Inter+Tight:wght@300;400;500;600;700&display=swap');

:root {
    --primary-color: #C9A227;
    --text-color: #F3F0E7;
    --background-color: #0B0B0B;
    --secondary-background-color: #141414;
}

.stApp { background-color: #0B0B0B; color: #F3F0E7; font-family: 'Inter Tight', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
h1, h2, h3 { font-family: 'Cormorant Garamond', serif !important; color: #F3F0E7 !important; }
.gold-text { background: linear-gradient(115deg,#9A7B1E,#F0D67B 45%,#B08A22); -webkit-background-clip: text; background-clip: text; color: transparent; }
.kicker { text-transform:uppercase; letter-spacing:.35em; font-size:.75rem; color:#A69C86; }
.rule { height:1px; background:linear-gradient(90deg,transparent,#C9A227,transparent); margin:1.6rem 0; }

/* Dropdowns */
div[data-baseweb="select"] > div {
    background-color: #141414 !important; border: 1px solid rgba(201, 162, 39, 0.35) !important;
    border-radius: 10px !important; color: #F3F0E7 !important; transition: all 0.3s ease;
}
div[data-baseweb="select"] > div:hover { border-color: #C9A227 !important; }
div[data-baseweb="select"] svg { fill: #C9A227 !important; stroke: #C9A227 !important; }
div[data-baseweb="popover"] ul { background-color: #141414 !important; border: 1px solid rgba(201, 162, 39, 0.3) !important; }
div[data-baseweb="popover"] li { color: #F3F0E7 !important; }
div[data-baseweb="popover"] li:hover { background-color: rgba(201, 162, 39, 0.15) !important; }

/* Sliders (Gold Track & Thumb) */
.stSlider [data-baseweb="slider"] div[data-testid="stSliderTrack"] { background-color: #333 !important; }
.stSlider [data-baseweb="slider"] div[data-testid="stSliderTrack"] > div { background-color: #C9A227 !important; box-shadow: 0 0 10px rgba(201, 162, 39, 0.4) !important; }
.stSlider [data-baseweb="slider"] div[role="slider"] { background: linear-gradient(145deg, #F0D67B, #C9A227) !important; border: 2px solid #0B0B0B !important; }
.stSlider [data-baseweb="slider"] div[role="slider"]:hover { box-shadow: 0 4px 14px rgba(240, 214, 123, 0.8) !important; }
.stSlider [data-testid="stSliderThumbValue"] { color: #F0D67B !important; font-weight: 700 !important; }

/* Number Inputs (+/- buttons) */
div[data-testid="stNumberInput"] button { background-color: #C9A227 !important; color: #0B0B0B !important; border: none !important; font-weight: 900 !important; }
div[data-testid="stNumberInput"] input { background-color: #141414 !important; border: 1px solid rgba(201, 162, 39, 0.35) !important; color: #F3F0E7 !important; }

/* Radio & Checkboxes */
div[role="radiogroup"] label { color: #F3F0E7 !important; }
div[role="radiogroup"] label[data-checked="true"] > div:first-child { background-color: #C9A227 !important; box-shadow: inset 0 0 0 4px #0B0B0B !important; }

/* Forms & Inputs */
div[data-testid="stForm"] { background: linear-gradient(145deg, #141414, #0D0D0D) !important; border: 1px solid rgba(201, 162, 39, 0.3) !important; border-radius: 16px !important; padding: 2.5rem !important; }
div[data-baseweb="input"] { background-color: #141414 !important; border: 1px solid rgba(201, 162, 39, 0.3) !important; color: #F3F0E7 !important; }

/* Buttons */
.stButton > button { background: #141414; color: #F3F0E7; border: 1px solid rgba(201, 162, 39, 0.35); border-radius: 12px; width: 100%; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; transition: all 0.3s ease; }
.stButton > button:hover { border-color: #C9A227; color: #F0D67B; transform: translateY(-2px); box-shadow: 0 8px 25px -10px rgba(201,162,39,.9); }

/* Submit buttons inside forms */
div[data-testid="stFormSubmitButton"] button { background: linear-gradient(115deg,#9A7B1E,#F0D67B) !important; color: #141005 !important; border: none !important; font-weight: 600; }
</style>
"""