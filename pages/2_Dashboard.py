import streamlit as st
import pandas as pd

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first")
    st.stop()

st.title("Cyber Incidents Dashboard")

df = pd.read_csv("data/cyber_incidents_sample.csv")

st.subheader("Dataset Preview")
st.dataframe(df)

st.subheader("Incident Count")

if "Incident_Type" in df.columns:
    st.bar_chart(df["Incident_Type"].value_counts())

if st.button("Logout"):
    st.session_state.logged_in = False
    st.switch_page("pages/1_login.py")

