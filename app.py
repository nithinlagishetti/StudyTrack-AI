import streamlit as st
import pandas as pd
import plotly.express as px

from database import create_tables
from auth import login_user, register_user
from ml_model import clean_data, train_model
from recommender import recommend
from styles import load_css

create_tables()
load_css()
st.set_page_config("StudyTrack AI", layout="wide")

# ---------------- SESSION INIT ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN PAGE ----------------
if not st.session_state.logged_in:
    st.title("🔐 StudyTrack AI Login")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_user(u, p):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        ru = st.text_input("New Username")
        rp = st.text_input("New Password", type="password")
        if st.button("Register"):
            if register_user(ru, rp):
                st.success("Registered successfully")
            else:
                st.error("User already exists")

    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.title("📌 Modules")
module = st.sidebar.radio("Navigate", [
    "About Project",
    "Upload Dataset",
    "Clean Dataset",
    "Model Training",
    "Recommendations (Cleaned Data Only)",
    "Single Student Recommendation"
])

# ---------------- MODULE 1 ----------------
if module == "About Project":
    st.title("📘 StudyTrack AI")
    st.write("""
    AI-based **Student Study Habit Recommendation System**.
    
    Focuses on:
    - Sleep
    - Study hours
    - Attendance
    - Study timing
    
    Provides **actionable habit improvement suggestions**.
    """)

# ---------------- MODULE 2 ----------------
elif module == "Upload Dataset":
    st.title("📤 Upload Dataset")
    file = st.file_uploader("Upload CSV / Excel", type=["csv", "xlsx"])

    if file:
        st.session_state.raw = (
            pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
        )
        st.success("Dataset uploaded successfully")
        st.dataframe(st.session_state.raw)

# ---------------- MODULE 3 ----------------
elif module == "Clean Dataset":
    st.title("🧹 Data Cleaning")

    if "raw" not in st.session_state:
        st.warning("Upload dataset first")
    else:
        if st.button("Clean Data"):
            st.session_state.cleaned = clean_data(st.session_state.raw)

        if "cleaned" in st.session_state:
            col1, col2 = st.columns(2)
            col1.subheader("Original Data")
            col1.dataframe(st.session_state.raw)
            col2.subheader("Cleaned Data")
            col2.dataframe(st.session_state.cleaned)

# ---------------- MODULE 4 ----------------
elif module == "Model Training":
    st.title("🤖 Model Training")

    if "cleaned" not in st.session_state:
        st.warning("Clean data first")
    elif "model" in st.session_state:
        st.success("Model already trained")
        st.metric("Accuracy", f"{st.session_state.accuracy*100:.2f}%")
    else:
        if st.button("Train Model"):
            model, scaler, accuracy, features = train_model(st.session_state.cleaned)
            st.session_state.model = model
            st.session_state.scaler = scaler
            st.session_state.accuracy = accuracy
            st.session_state.features = features
            st.success("Model trained successfully")

# ---------------- MODULE 5 ----------------
elif module == "Recommendations (Cleaned Data Only)":
    st.title("✅ Recommendations (Cleaned Dataset)")

    if "cleaned" not in st.session_state:
        st.warning("Clean dataset first")
    else:
        df = st.session_state.cleaned.copy()
        df["Recommendation"] = df.apply(recommend, axis=1)
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download Recommendations", csv, "StudyTrack_Report.csv")

# ---------------- MODULE 6 ----------------
elif module == "Single Student Recommendation":
    st.title("🎯 Single Student Recommendation")

    if "model" not in st.session_state:
        st.warning("Train model first")
    else:
        age = st.number_input("Age", 10, 30)
        study = st.number_input("Study Hours / Day", 0.0, 10.0)
        pref = st.selectbox("Preferred Study Time", ["Morning", "Evening", "Night"])
        attend = st.number_input("Attendance %", 0.0, 100.0)
        sleep = st.number_input("Sleep Hours", 0.0, 12.0)

        if st.button("Recommend"):
            pref_map = {"Morning": 0, "Evening": 1, "Night": 2}
            rec = recommend({
                "Study_Hours_Per_Day": study,
                "Sleep_Hours": sleep,
                "Attendance_Percentage": attend
            })
            st.success("Recommendation")
            st.write(rec)
