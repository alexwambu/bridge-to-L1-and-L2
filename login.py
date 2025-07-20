import streamlit as st

def check_login():
    if "logged_in" not in st.session_state:
        username = st.text_input("Admin Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == "admin" and password == "admin":
                st.session_state.logged_in = True
            else:
                st.error("Invalid credentials")
        return False
    return True
