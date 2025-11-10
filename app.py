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
