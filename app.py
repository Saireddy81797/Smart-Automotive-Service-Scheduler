# ------------ IMPORTS (must come first) ------------
import os
import streamlit as st

from core.db import init_db
from ui import customer, admin


# ------------ PAGE CONFIG ------------
st.set_page_config(
    page_title="Smart Automotive Scheduler",
    page_icon="🚗",
    layout="wide"
)


# ------------ ONE-TIME BOOTSTRAP (create tables + seed) ------------
@st.cache_resource
def bootstrap():
    init_db()
    from core.seed import main as seed_main
    seed_main()
    return True

bootstrap()


# ------------ THEME TOGGLE (Light / Dark) ------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True  # default

st.sidebar.write("")  # spacing
st.session_state.dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)

# CSS design tokens for both themes
THEME = {
    "dark": {
        "bg":        "#0B1220",
        "bg2":       "#0F1629",
        "panel":     "rgba(17, 24, 39, 0.55)",
        "border":    "rgba(124, 58, 237, 0.35)",
        "text":      "#E6EAF2",
        "muted":     "#AAB1C5",
        "primary":   "#7C3AED",
        "shadow":    "0 10px 30px rgba(0,0,0,.35)"
    },
    "light": {
        "bg":        "#F5F7FB",
        "bg2":       "#FFFFFF",
        "panel":     "rgba(255,255,255,0.65)",
        "border":    "rgba(124, 58, 237, 0.25)",
        "text":      "#0B1220",
        "muted":     "#4A5568",
        "primary":   "#7C3AED",
        "shadow":    "0 10px 30px rgba(16,24,40,.10)"
    }
}

tokens = THEME["dark" if st.session_state.dark_mode else "light"]


# ------------ GLOBAL STYLES ------------
st.markdown(f"""
<style>
:root {{
  --bg: {tokens['bg']};
  --bg2: {tokens['bg2']};
  --panel: {tokens['panel']};
  --border: {tokens['border']};
  --text: {tokens['text']};
  --muted: {tokens['muted']};
  --primary: {tokens['primary']};
  --shadow: {tokens['shadow']};
}}

html, body, [data-testid="stAppViewContainer"] {{
  background: var(--bg);
  color: var(--text);
}}

.block-container {{ max-width: 1100px; }}
h1, h2, h3 {{ letter-spacing: .3px; }}

.gradient-header {{
  margin: 6px 0 18px 0;
  padding: 14px 18px;
  border-radius: 16px;
  background: linear-gradient(135deg, #2B1C55 0%, #7C3AED 55%, #2B1C55 100%);
  color: #fff;
  box-shadow: var(--shadow);
  border: 1px solid {tokens['border']};
}}

.card {{
  padding: 14px 16px;
  border-radius: 16px;
  background: var(--bg2);
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  margin-bottom: 12px;
}}

.badge {{
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
}}

.badge.green {{ background: #DCFCE7; color: #065F46; border: 1px solid #10B98166; }}
.badge.yellow{{ background: #FEF9C3; color: #854D0E; border: 1px solid #F59E0B66; }}
.badge.red    {{ background: #FEE2E2; color: #7F1D1D; border: 1px solid #EF444466; }}

.stButton>button {{
  border-radius: 12px; padding: 8px 14px; font-weight: 600;
  border: 1px solid var(--border);
  background: var(--bg2); color: var(--text);
}}
.stButton>button:hover {{ transform: translateY(-1px); transition: .15s }}

[data-testid="stSidebar"] {{
  background: transparent;
}}
.sidebar-glass {{
  margin: 6px 8px 18px 8px;
  padding: 14px 14px;
  border-radius: 18px;
  background: var(--panel);
  border: 1px solid var(--border);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: var(--shadow);
}}

.sidebar-title {{
  display:flex; align-items:center; gap:10px; font-weight:800; font-size:20px;
}}
.sidebar-title img {{ width:26px; height:26px; border-radius:6px; }}

@media (max-width: 640px) {{
  .block-container {{ padding: 0 14px; }}
  .gradient-header {{ border-radius: 12px; padding: 12px 14px; }}
  .card {{ border-radius: 12px; }}
}}
</style>
""", unsafe_allow_html=True)


# ------------ SIDEBAR (logo + nav with icons) ------------
def sidebar_logo_html():
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        return f'<img src="app://{logo_path}" alt="logo" />'
    # fallback emoji
    return "🚗"

st.sidebar.markdown('<div class="sidebar-glass">', unsafe_allow_html=True)
st.sidebar.markdown(
    f'<div class="sidebar-title">{sidebar_logo_html()} <span>Smart Scheduler</span></div>',
    unsafe_allow_html=True
)

nav = st.sidebar.radio(
    "Navigation",
    options=["👤 Customer", "🛠️ Admin"],
    label_visibility="collapsed",
)

st.sidebar.markdown('</div>', unsafe_allow_html=True)  # close glass panel


# ------------ TOP GRADIENT HEADER ------------
st.markdown("""
<div class="gradient-header">
  <div style="display:flex;justify-content:space-between;align-items:center;">
    <div style="font-weight:800;font-size:20px;letter-spacing:.3px;">Smart Automotive Scheduler</div>
    <div style="opacity:.9;">Seamless booking • Real-time slots • ML ranking</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ------------ ROUTING ------------
if nav.startswith("👤"):
    customer.render()
else:
    st.sidebar.subheader("Admin Login")
    pwd = st.sidebar.text_input("Enter Password", type="password")
    ADMIN_PASS = os.getenv("ADMIN_PASS", "admin123")
    if pwd == ADMIN_PASS:
        admin.render()
    else:
        st.warning("Invalid admin password.")
