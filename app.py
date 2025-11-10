import streamlit as st
import os

from core.db import init_db
from ui import customer, admin


# -------------------------------------------------
# ✅ Streamlit App Config
# -------------------------------------------------
st.set_page_config(
    page_title="Smart Automotive Scheduler",
    layout="wide",
    page_icon="🚗"
)


# -------------------------------------------------
# ✅ Initialize DB only once (Streamlit cache)
# -------------------------------------------------
@st.cache_resource
def bootstrap():
    init_db()
    return True


bootstrap()


# -------------------------------------------------
# ✅ Sidebar Navigation
# -------------------------------------------------
st.sidebar.title("🚗 Smart Scheduler")

page = st.sidebar.radio(
    "Select Role",
    ["Customer", "Admin"]
)


# -------------------------------------------------
# ✅ Render Pages
# -------------------------------------------------
if page == "Customer":
    customer.render()

else:
    st.sidebar.subheader("Admin Login")
    password = st.sidebar.text_input(
        "Enter Password",
        type="password"
    )

    admin_pass = os.getenv("ADMIN_PASS", "admin123")

    if password == admin_pass:
        admin.render()
    else:
        st.warning("Please enter a valid admin password to continue.")
