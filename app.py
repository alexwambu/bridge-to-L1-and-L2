import streamlit as st
import streamlit.components.v1 as components
import json
import os

try:
    from web3 import Web3
except ImportError:
    st.error("⚠️ Web3.py not installed. Run `pip install web3` in your terminal.")

# Safe fallback for pkg_resources shim
try:
    import pkg_resources
    _ = pkg_resources.get_distribution("streamlit")
except (ImportError, AttributeError):
    try:
        import pkg_resources as local_pkg
        _ = local_pkg.get_distribution("streamlit")
    except Exception:
        st.warning("🟡 Warning: pkg_resources shim in use. Some dependencies may behave unexpectedly.")

# --- Admin login credentials ---
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Admin login form ---
def login():
    st.title("🔐 GBT Network Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.success("✅ Logged in successfully")
            st.session_state.logged_in = True
        else:
            st.error("❌ Invalid login")

# --- Main app after login ---
def main_app():
    st.title("🌉 GBT Network Bridge Interface")

    # --- Web3 connection to local & GBT RPC ---
    local_rpc = "http://localhost:8545"
    gbt_rpc = "http://GBTNetwork:8545"

    try:
        w3_local = Web3(Web3.HTTPProvider(local_rpc))
        w3_gbt = Web3(Web3.HTTPProvider(gbt_rpc))

        if w3_local.is_connected() and w3_gbt.is_connected():
            st.success("✅ Connected to both Layer 1 and Layer 2 nodes")
        else:
            st.warning("⚠️ Could not connect to one or both nodes")

    except Exception as e:
        st.error(f"❌ Web3 connection error: {str(e)}")

    # --- Load MetaMask Connect UI ---
    if os.path.exists("wallet_connect.html"):
        st.subheader("🦊 Connect Wallet (MetaMask)")
        components.html(open("wallet_connect.html").read(), height=350)
    else:
        st.warning("⚠️ MetaMask UI file 'wallet_connect.html' not found.")

    # --- Bridge Actions ---
    st.subheader("🚀 Bridge Actions")
    action = st.selectbox("Choose action", ["Deposit to Layer 2", "Withdraw to Layer 1", "View Balance"])
    user_address = st.text_input("Your Wallet Address")

    if user_address:
        if action == "Deposit to Layer 2":
            amount = st.number_input("Amount to deposit", min_value=0.0)
            if st.button("Send Deposit"):
                st.info(f"Simulating deposit of {amount} GBT from L1 → L2 (Address: {user_address})")
                # TODO: Add BridgeL1.sol integration here

        elif action == "Withdraw to Layer 1":
            amount = st.number_input("Amount to withdraw", min_value=0.0)
            if st.button("Withdraw"):
                st.info(f"Simulating withdrawal of {amount} GBT from L2 → L1 (Address: {user_address})")
                # TODO: Add BridgeL2.sol integration here

        elif action == "View Balance":
            if st.button("Check Balances"):
                try:
                    balance1 = w3_local.eth.get_balance(user_address)
                    st.success(f"Layer 1 Balance: {w3_local.from_wei(balance1, 'ether')} ETH")

                    balance2 = w3_gbt.eth.get_balance(user_address)
                    st.success(f"Layer 2 Balance: {w3_gbt.from_wei(balance2, 'ether')} GBT")
                except Exception as e:
                    st.error(f"Error fetching balances: {str(e)}")

# --- Entrypoint ---
if __name__ == "__main__":
    if not st.session_state.logged_in:
        login()
    else:
        main_app()
