import streamlit as st

st.set_page_config(
    page_title="Week 9 Cyber Security App",
    layout="centered"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("Week 9 Cyber Security Application")
st.write("Use sidebar to navigate ")
