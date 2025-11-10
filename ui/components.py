import streamlit as st
from datetime import datetime


def slot_badge(slot):
start = slot["start"].strftime('%d %b %Y, %I:%M %p')
rem = slot["remaining"]
st.markdown(f"**{start}** — Remaining: {rem}")
