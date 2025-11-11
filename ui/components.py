import streamlit as st
from datetime import datetime

def header(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div class="card" style="background: linear-gradient(135deg,#1F1635 0%, #0B1220 100%);">
      <h1 style="margin:0;">{title}</h1>
      <p style="margin:.25rem 0 0; opacity:.85;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def kpi(label: str, value, help_text: str = ""):
    with st.container():
        st.markdown(f"""
        <div class="card">
          <div style="font-size:13px;opacity:.8;margin-bottom:4px;">{label}</div>
          <div style="font-size:28px;font-weight:700;line-height:1">{value}</div>
          <div style="font-size:12px;opacity:.7;margin-top:2px;">{help_text}</div>
        </div>
        """, unsafe_allow_html=True)

def slot_card(slot: dict):
    start = slot["start"].strftime("%d %b %Y, %I:%M %p")
    end   = slot["end"].strftime("%I:%M %p")
    rem = slot["remaining"]
    cls = "green" if rem >= 3 else "yellow" if rem == 2 else "red" if rem == 1 else "red"

    st.markdown(f"""
    <div class="card">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <div>
          <div style="font-size:16px;font-weight:700">🕒 {start} → {end}</div>
          <div style="margin-top:4px;font-size:13px;opacity:.85">Service bay slot</div>
        </div>
        <span class="badge {cls}">Remaining: {rem}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
