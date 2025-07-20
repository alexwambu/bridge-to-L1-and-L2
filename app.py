import streamlit as st
import streamlit.components.v1 as components
from login import check_login
from web3_client import get_balance
from relayer import run_relayer

st.set_page_config(page_title="GBT Bridge", layout="wide")

if check_login():
    st.title("🔁 GBT Layer1 ↔ Layer2 Bridge")

    st.subheader("Wallet Connect")
    with open("wallet_connect.html") as f:
        components.html(f.read(), height=300)

    st.subheader("Balance Checker")
    wallet = st.text_input("Wallet Address")
    if st.button("Check"):
        l1, l2 = get_balance(wallet)
        st.success(f"L1: {l1} GBT — L2: {l2} GBT")

    st.subheader("Bridge Actions")
    st.button("Deposit to Layer 2")
    st.button("Withdraw to Layer 1")

    run_relayer()
