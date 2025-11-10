import streamlit as st
from datetime import datetime
from services.scheduler import Scheduler
from services.optimization import rank_slots

scheduler = Scheduler()


def render():
    st.title("🚗 Book a Service")

    center_id = st.number_input("Center ID", value=1, step=1)
    date = st.date_input("Choose Date")
    service_minutes = st.slider("Service Duration (mins)", 30, 180, 60, 15)

    if date:
        day = datetime.combine(date, datetime.min.time())
        available = scheduler.list_available(center_id, day)
        ranked = rank_slots(available, service_minutes)

        st.subheader("Recommended Slots")

        for s in ranked[:10]:
            cols = st.columns([4, 1, 1])
            with cols[0]:
                st.write(
                    f"{s['start']} → {s['end']} | remaining={s['remaining']} | score={s['score']}"
                )
            with cols[1]:
                if st.button("Hold", key=f"hold_{s['slot_id']}"):
                    booking_id = scheduler.hold_slot(
                        s['slot_id'], "Guest", "TS07AB1234", "General Service"
                    )
                    st.session_state["held_booking"] = booking_id
                    st.success("Slot held for 5 minutes.")

            with cols[2]:
                if st.button("Confirm", key=f"confirm_{s['slot_id']}"):
                    bid = st.session_state.get("held_booking")
                    if bid and scheduler.confirm_booking(bid):
                        st.success("✅ Booking Confirmed")
                    else:
                        st.error("Please hold a slot before confirming.")
