import streamlit as st
import streamlit.components.v1 as components
import json
from web3 import Web3
import os

# --- Admin login credentials ---
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"

# --- Session state for login ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Admin login form ---
def login():
    st.title("🔐 GBT Network Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.success("Logged in as admin ✅")
            st.session_state.logged_in = True
        else:
            st.error("Invalid credentials")

# --- Main App after login ---
def main_app():
    st.title("🚀 GBT Network Bridge DApp")

    # Web3 connection
    local_provider = "http://localhost:8545"
    gbt_provider = "http://GBTNetwork:8545"

    try:
        w3_local = Web3(Web3.HTTPProvider(local_provider))
        w3_gbt = Web3(Web3.HTTPProvider(gbt_provider))
        st.success("✅ Connected to both Layer 1 and Layer 2 nodes")
    except Exception as e:
        st.error(f"Web3 connection error: {str(e)}")

    # Load Wallet UI
    if os.path.exists("wallet_connect.html"):
        components.html(open("wallet_connect.html").read(), height=300)
    else:
        st.warning("MetaMask connect UI not found (wallet_connect.html)")

    st.subheader("Bridge Actions")
    action = st.selectbox("Select action", ["Deposit to Layer 2", "Withdraw to Layer 1", "View Balance"])
    user_address = st.text_input("Your Wallet Address")

    if action == "Deposit to Layer 2":
        amount = st.number_input("Amount to deposit", min_value=0.0)
        if st.button("Send Deposit"):
            st.info(f"🔄 Simulating deposit of {amount} GBT from L1 to L2 (Address: {user_address})")
            # Integrate bridgeL1.sol contract logic here

    elif action == "Withdraw to Layer 1":
        amount = st.number_input("Amount to withdraw", min_value=0.0)
        if st.button("Withdraw"):
            st.info(f"🔄 Simulating withdraw of {amount} GBT from L2 to L1 (Address: {user_address})")
            # Integrate bridgeL2.sol contract logic here

    elif action == "View Balance":
        if st.button("Check Balance"):
            try:
                balance = w3_local.eth.get_balance(user_address)
                st.success(f"Balance on Layer 1: {w3_local.from_wei(balance, 'ether')} ETH")
                balance2 = w3_gbt.eth.get_balance(user_address)
                st.success(f"Balance on Layer 2: {w3_gbt.from_wei(balance2, 'ether')} GBT")
            except Exception as e:
                st.error(f"Error fetching balance: {str(e)}")

# --- App Entrypoint ---
if __name__ == "__main__":
    if not st.session_state.logged_in:
        login()
    else:
        main_app()

