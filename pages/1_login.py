import streamlit as st
from auth import login_user, register_user

st.title("Login / Register")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

col1, col2 = st.columns(2)

with col1:
    if st.button("Login"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.success("Login successful")
            st.switch_page("pages/2_Dashboard.py")
        else:
            st.error("Invalid username or password")

with col2:
    if st.button("Register"):
        if register_user(username, password):
            st.success("Registration successful")
        else:
            st.error("User already exists")
