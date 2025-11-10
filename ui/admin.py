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

    st.header(f"📅 Dashboard – {date.strftime('%d %b %Y')}")

    # ----------------------------------------
    # ✅ Live Slot Availability
    # ----------------------------------------
    st.subheader("📢 Live Slot Availability")

    dt = datetime.combine(date, datetime.min.time())
    available = scheduler.list_available(center_id, dt)

    if not available:
        st.info("No slots available for this date.")
    else:
        for s in available:
            st.write(
                f"**{s['start']} → {s['end']}** | "
                f"Remaining: **{s['remaining']}**"
            )

    st.markdown("---")

    # ----------------------------------------
    # ✅ Daily KPI Analytics
    # ----------------------------------------
    st.subheader("📊 Daily Analytics")

    report = analytics.daily_report(center_id, dt)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Fill Rate (%)", report["fill_rate"])

    with col2:
        st.metric("No-Show Rate (%)", report["no_show_rate"])

    with col3:
        st.metric("Avg Lead Time (hrs)", report["avg_lead_time_hours"])

    # ----------------------------------------
    # ✅ Peak Hours
    # ----------------------------------------
    st.subheader("🔥 Peak Hours (Top 3)")
    if report["peak_hours"]:
        for ph in report["peak_hours"]:
            st.write(f"**{ph['start']}** — {ph['bookings']} bookings")
    else:
        st.info("No bookings yet.")

    # ----------------------------------------
    # ✅ Service Type Distribution
    # ----------------------------------------
    st.subheader("🧾 Service Type Distribution")

    if report["service_type_distribution"]:
        for item in report["service_type_distribution"]:
            st.write(f"**{item['service_type']}** → {item['count']}")
    else:
        st.info("No service types recorded for this date.")

    st.markdown("---")
    st.success("✅ Admin dashboard loaded successfully.")
