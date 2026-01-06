import streamlit as st

def load_css():
    st.markdown("""
    <style>
    body { background-color:#0f172a; color:#e5e7eb; }
    .stButton button {
        background-color:#2563eb;
        color:white;
        border-radius:8px;
    }
    </style>
    """, unsafe_allow_html=True)
