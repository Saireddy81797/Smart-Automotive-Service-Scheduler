import streamlit as st
from services.scheduler import Scheduler
from services.optimization import rank_slots
from datetime import datetime


scheduler = Scheduler()


def render():
st.header("Book a Service")
center_id = st.number_input("Center ID", value=1, step=1)
date = st.date_input("Choose a date")
service_minutes = st.slider("Service duration (mins)", 30, 180, 60, 15)


if date:
avail = scheduler.list_available(center_id, datetime.combine(date, datetime.min.time()))
ranked = rank_slots(avail, service_minutes)
for s in ranked[:10]:
cols = st.columns([4,1,1])
with cols[0]:
st.write(f"{s['start']} – {s['end']} | remaining={s['remaining']} | scor
