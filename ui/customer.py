import streamlit as st
from datetime import datetime
from sqlalchemy import select
from core.db import SessionLocal
from core.models import ServiceCenter
from services.scheduler import Scheduler
from services.optimization import rank_slots
from ui.components import header, slot_card

scheduler = Scheduler()

def _centers():
    db = SessionLocal()
    rows = db.execute(select(ServiceCenter)).scalars().all()
    return [(c.id, c.name) for c in rows]

def render():
    header("🚗 Book a Service", "Pick a center and choose a convenient slot")

    centers = _centers()
    if not centers:
        st.warning("No service centers found. Click **Reseed Database** in the sidebar and refresh.")
        return

    center_names = {cid: name for cid, name in centers}
    colA, colB = st.columns([2,1], vertical_alignment="center")

    with colA:
        cid = st.selectbox(
            "Select Service Center",
            options=[c[0] for c in centers],
            format_func=lambda x: center_names[x],
            index=0
        )
    with colB:
        date = st.date_input("Choose Date", datetime.today())

    duration = st.slider("Service Duration (mins)", 30, 180, 60, 15)

    st.markdown("### 🎯 Recommended Slots")

    if date:
        day = datetime.combine(date, datetime.min.time())
        available = scheduler.list_available(cid, day)
        ranked = rank_slots(available, duration)

        if not ranked:
            st.info("No slots on this day. Try another date.")
            return

        for s in ranked[:10]:
            slot_card(s)
            c1, c2, _ = st.columns([1,1,8])
            with c1:
                if st.button("Hold", key=f"hold_{s['slot_id']}"):
                    booking_id = scheduler.hold_slot(
                        s["slot_id"], "Guest", "TS07AB1234", "General Service"
                    )
                    st.session_state["held_booking"] = booking_id
                    st.toast("Slot held for 5 minutes. Click Confirm to finalize.", icon="⏳")
            with c2:
                if st.button("Confirm", key=f"confirm_{s['slot_id']}"):
                    bid = st.session_state.get("held_booking")
                    if bid and scheduler.confirm_booking(bid):
                        st.toast("Booking Confirmed ✅", icon="✅")
                    else:
                        st.toast("Hold a slot before confirming.", icon="⚠️")
