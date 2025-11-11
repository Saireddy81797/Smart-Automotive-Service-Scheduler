# ---- IMPORTS FIRST (so st exists before we use it) ----
import os
import sqlite3
import streamlit as st

from core.db import init_db
from ui import customer, admin

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Smart Automotive Scheduler", page_icon="🚗", layout="wide")

# ---- GLOBAL CSS (after imports) ----
st.markdown("""
<style>
.block-container {max-width: 1100px;}
h1, h2, h3 {letter-spacing: .3px}
.card { padding: 14px 16px; border-radius: 16px; background: #111827;
        border: 1px solid rgba(124,58,237,.25); box-shadow: 0 6px 24px rgba(0,0,0,.25);
        margin-bottom: 12px; }
.badge { display:inline-block; padding:4px 10px; border-radius:999px; font-size:12px; font-weight:600; }
.badge.green { background:#064e3b; color:#a7f3d0; border:1px solid #10b98133;}
.badge.yellow{ background:#4d3a10; color:#fde68a; border:1px solid #f59e0b33;}
.badge.red   { background:#4c1d1d; color:#fecaca; border:1px solid #ef444433;}
.stButton>button { border-radius: 12px; padding: 8px 14px; font-weight: 600; border: 1px solid rgba(124,58,237,.35); }
.stButton>button:hover { transform: translateY(-1px); transition: .15s }
</style>
""", unsafe_allow_html=True)

# ---- BOOTSTRAP: create tables + seed (cached) ----
@st.cache_resource
def bootstrap():
    init_db()
    from core.seed import main as seed_main
    seed_main()
    return True

bootstrap()

# ---- SIDEBAR: DB debug + controls ----
st.sidebar.title("🚗 Smart Scheduler")

db_exists = os.path.exists("smart_scheduler.db")
st.sidebar.info(f"DB Exists: {db_exists}")

if db_exists:
    try:
        conn = sqlite3.connect("smart_scheduler.db")
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        st.sidebar.write("Tables:", tables)
    finally:
        conn.close()
else:
    st.sidebar.error("❌ smart_scheduler.db NOT FOUND")

if st.sidebar.button("🗑️ DELETE DATABASE FILE"):
    try:
        if os.path.exists("smart_scheduler.db"):
            os.remove("smart_scheduler.db")
            st.sidebar.success("✅ Deleted DB. Reload app to recreate.")
        else:
            st.sidebar.info("DB file did not exist.")
    except Exception as e:
        st.sidebar.error(f"Error deleting DB: {e}")

if st.sidebar.button("🔄 Reseed Database"):
    from core.seed import main as seed_main
    seed_main()
    st.sidebar.success("✅ Database reseeded.")

# ---- NAV ----
page = st.sidebar.radio("Select Role", ["Customer", "Admin"])

# ---- ROUTES ----
if page == "Customer":
    customer.render()
else:
    st.sidebar.subheader("Admin Login")
    pwd = st.sidebar.text_input("Enter Password", type="password")
    ADMIN_PASS = os.getenv("ADMIN_PASS", "admin123")
    if pwd == ADMIN_PASS:
        admin.render()
    else:
        st.warning("Invalid admin password.")
