import streamlit as st
from datetime import datetime
from services.scheduler import Scheduler
from services.analytics import Analytics

scheduler = Scheduler()
analytics = Analytics()


def render():
    st.title("🛠️ Service Center Dashboard")

    st.sidebar.subheader("Admin Controls")
    center_id = st.sidebar.number_input("Center ID", value=1, step=1)
    date = st.sidebar.date_input("Select a Date", datetime.today())

    dt = datetime.combine(date, datetime.min.time())

    st.subheader("📢 Live Slot Availability")
    available = scheduler.list_available(center_id, dt)

    if available:
        for s in available:
            st.write(f"{s['start']} → {s['end']} | Remaining: {s['remaining']}")
    else:
        st.info("No slots available.")

    st.markdown("---")

    st.subheader("📊 Analytics")
    report = analytics.daily_report(center_id, dt)

    c1, c2, c3 = st.columns(3)
    c1.metric("Fill Rate (%)", report["fill_rate"])
    c2.metric("No-Show Rate (%)", report["no_show_rate"])
    c3.metric("Avg Lead Time (hrs)", report["avg_lead_time_hours"])

    st.subheader("🔥 Peak Hours")
    if report["peak_hours"]:
        for ph in report["peak_hours"]:
            st.write(f"{ph['start']} — {ph['bookings']} bookings")
    else:
        st.info("No peak-hour data.")

    st.subheader("🧾 Service Distribution")
    if report["service_type_distribution"]:
        for item in report["service_type_distribution"]:
            st.write(f"{item['service_type']} → {item['count']}")
    else:
        st.info("No service data.")
