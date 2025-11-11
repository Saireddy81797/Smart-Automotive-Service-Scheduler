st.markdown("""
<style>
/* page width */
.block-container {max-width: 1100px;}

/* headers */
h1, h2, h3 {letter-spacing: .3px}

/* cards */
.card {
  padding: 14px 16px;
  border-radius: 16px;
  background: #111827;
  border: 1px solid rgba(124,58,237,.25);
  box-shadow: 0 6px 24px rgba(0,0,0,.25);
  margin-bottom: 12px;
}

/* pill badges */
.badge {
  display:inline-block; padding:4px 10px; border-radius:999px;
  font-size: 12px; font-weight: 600;
}
.badge.green { background:#064e3b; color:#a7f3d0; border:1px solid #10b98133;}
.badge.yellow{ background:#4d3a10; color:#fde68a; border:1px solid #f59e0b33;}
.badge.red   { background:#4c1d1d; color:#fecaca; border:1px solid #ef444433;}

/* nicer buttons */
.stButton>button {
  border-radius: 12px; padding: 8px 14px; font-weight: 600;
  border: 1px solid rgba(124,58,237,.35);
}
.stButton>button:hover {transform: translateY(-1px); transition: .15s}
</style>
""", unsafe_allow_html=True)

import streamlit as st
import os
import sqlite3

from core.db import init_db
from ui import customer, admin


# -------------------------------------------------
# ✅ Streamlit Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Smart Automotive Scheduler",
    page_icon="🚗",
    layout="wide"
)


# -------------------------------------------------
# ✅ Initialize DB + Seed ONCE (cached)
# -------------------------------------------------
@st.cache_resource
def bootstrap():
    # create tables
    init_db()

    # seed database (important)
    from core.seed import main as seed_main
    seed_main()

    return True


bootstrap()  # run initialization


# -------------------------------------------------
# ✅ SIDEBAR DEBUG INFORMATION (VERY IMPORTANT)
# -------------------------------------------------

# ✅ 1. Does DB file exist?
db_exists = os.path.exists("smart_scheduler.db")
st.sidebar.info(f"DB Exists: {db_exists}")

# ✅ 2. List DB tables (see if tables were created)
if db_exists:
    conn = sqlite3.connect("smart_scheduler.db")
    tables = conn.execute("SELECT name FROM sqlite_master").fetchall()
    st.sidebar.write("Tables:", tables)
    conn.close()
else:
    st.sidebar.error("❌ smart_scheduler.db NOT FOUND")


# ✅ Buttons to manage DB
if st.sidebar.button("🗑️ DELETE DATABASE FILE"):
    try:
        os.remove("smart_scheduler.db")
        st.sidebar.success("✅ Deleted DB. Reload app to recreate.")
    except Exception as e:
        st.sidebar.error(f"Error deleting DB: {e}")

if st.sidebar.button("🔄 Reseed Database"):
    from core.seed import main as seed_main
    seed_main()
    st.sidebar.success("✅ Database reseeded.")


# -------------------------------------------------
# ✅ Sidebar Navigation
# -------------------------------------------------
st.sidebar.title("🚗 Smart Scheduler")

page = st.sidebar.radio("Select Role", ["Customer", "Admin"])


# -------------------------------------------------
# ✅ Render Pages
# -------------------------------------------------
if page == "Customer":
    customer.render()

elif page == "Admin":
    st.sidebar.subheader("Admin Login")

    pwd = st.sidebar.text_input("Enter Password", type="password")
    ADMIN_PASS = os.getenv("ADMIN_PASS", "admin123")

    if pwd == ADMIN_PASS:
        admin.render()
    else:
        st.warning("Invalid Admin Password")
