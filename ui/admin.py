import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import select
from core.db import SessionLocal
from core.models import ServiceCenter
from services.scheduler import Scheduler
from services.analytics import Analytics
from ui.components import header, kpi

scheduler = Scheduler()
analytics = Analytics()

def _centers():
    db = SessionLocal()
    rows = db.execute(select(ServiceCenter)).scalars().all()
    return [(c.id, c.name) for c in rows]

def render():
    header("🛠️ Service Center Dashboard", "Live availability and daily KPIs")

    centers = _centers()
    if not centers:
        st.warning("No service centers found. Click **Reseed Database** in the sidebar and refresh.")
        return

    center_names = {cid: name for cid, name in centers}
    colA, colB = st.columns([2,1])

    with colA:
        cid = st.selectbox(
            "Select Center",
            options=[c[0] for c in centers],
            format_func=lambda x: center_names[x],
            index=0
        )
    with colB:
        date = st.date_input("Date", value=datetime.today())

    dt = datetime.combine(date, datetime.min.time())

    st.markdown("### 📢 Live Slot Availability")
    available = scheduler.list_available(cid, dt)
    if available:
        df_av = pd.DataFrame([
            {"start": s["start"], "end": s["end"], "remaining": s["remaining"]}
            for s in available
        ])
        st.dataframe(df_av, use_container_width=True, hide_index=True)
    else:
        st.info("No slots available for this date.")

    st.markdown("---")
    st.markdown("### 📊 Daily KPIs")

    report = analytics.daily_report(cid, dt)
    c1, c2, c3 = st.columns(3)
    kpi("Fill Rate", f"{report['fill_rate']}%", "Booked vs total capacity")
    kpi("No-Show Rate", f"{report['no_show_rate']}%", "Cancellations / No-shows")
    kpi("Avg Lead Time", f"{report['avg_lead_time_hours']} hrs", "Booking → Start")

    st.markdown("### 🔥 Peak Hours")
    ph = report["peak_hours"]
    if ph:
        df_peak = pd.DataFrame([{"start": p["start"], "bookings": p["bookings"]} for p in ph])
        st.bar_chart(df_peak.set_index("start"))
    else:
        st.info("No peak-hour data yet.")

    st.markdown("### 🧾 Service Type Distribution")
    dist = report["service_type_distribution"]
    if dist:
        df_dist = pd.DataFrame(dist)
        df_dist = df_dist.set_index("service_type")
        st.bar_chart(df_dist)
    else:
        st.info("No service-type data for this date.")
