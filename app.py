import streamlit as st
import os

from core.db import init_db
from ui import customer, admin

# -------------------------------------------------
# ✅ Streamlit Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Smart Automotive Scheduler",
    page_icon="🚗",
    layout="wide"
)


# -------------------------------------------------
# ✅ Initialize Database (cached once)
# -------------------------------------------------
@st.cache_resource
def bootstrap():
    init_db()
    return True


bootstrap()

st.sidebar.info(f"DB Exists: {os.path.exists('smart_scheduler.db')}")


# -------------------------------------------------
# ✅ Sidebar Navigation
# -------------------------------------------------
st.sidebar.title("🚗 Smart Scheduler")

# ✅ Add RESYNC/SEED button for fixing OperationalError
if st.sidebar.button("🔄 Reseed Database"):
    from core.seed import main as seed_main
    seed_main()
    st.success("✅ Database reseeded successfully!")


page = st.sidebar.radio(
    "Select Role",
    ["Customer", "Admin"]
)


# -------------------------------------------------
# ✅ Page Rendering Logic
# -------------------------------------------------
if page == "Customer":
    customer.render()

elif page == "Admin":
    st.sidebar.subheader("Admin Login")

    password = st.sidebar.text_input(
        "Enter Password",
        type="password"
    )

    admin_pass = os.getenv("ADMIN_PASS", "admin123")

    if password == admin_pass:
        admin.render()
    else:
        st.warning("Invalid admin password.")

