import streamlit as st
from core.seed import main

if st.button("Run Seed"):
    main()
    st.success("✅ Database seeded!")
