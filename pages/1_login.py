import streamlit as st
from auth import verify_user, register_user

def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if verify_user(username, password):
            st.session_state["logged_in"] = True
            st.session_state["user"] = username
            st.success(f"Logged in as {username}")
        else:
            st.error("Invalid credentials")

    if st.button("Register"):
        if not username or not password:
            st.error("Enter username and password")
        else:
            success = register_user(username, password)
            if success:
                st.success("User registered. Login now.")
            else:
                st.error("Username already exists")

if __name__ == "__main__":
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    login_page()
