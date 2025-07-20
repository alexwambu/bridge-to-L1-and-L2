import streamlit as st
import streamlit.components.v1 as components
from web3 import Web3
import json
import os

# --- Admin credentials ---
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"

# --- Bridge contract config ---
with open("BridgeL1_ABI.json") as f:
    BRIDGE_L1_ABI = json.load(f)

with open("BridgeL2_ABI.json") as f:
    BRIDGE_L2_ABI = json.load(f)

BRIDGE_L1_ADDRESS = "0xYourL1BridgeContractAddress"
BRIDGE_L2_ADDRESS = "0xYourL2BridgeContractAddress"

# --- Session state for login ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔐 GBT Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.success("✅ Logged in")
            st.session_state.logged_in = True
        else:
            st.error("❌ Invalid credentials")

def main_app():
    st.title("🌉 GBT Bridge Dashboard")

    # --- Web3 connections ---
    rpc_l1 = "http://localhost:8545"
    rpc_l2 = "http://GBTNetwork:8545"
    w3_l1 = Web3(Web3.HTTPProvider(rpc_l1))
    w3_l2 = Web3(Web3.HTTPProvider(rpc_l2))

    bridge_l1 = w3_l1.eth.contract(address=BRIDGE_L1_ADDRESS, abi=BRIDGE_L1_ABI)
    bridge_l2 = w3_l2.eth.contract(address=BRIDGE_L2_ADDRESS, abi=BRIDGE_L2_ABI)

    # MetaMask UI
    if os.path.exists("wallet_connect.html"):
        st.subheader("🦊 Connect Wallet")
        components.html(open("wallet_connect.html").read(), height=350)
    else:
        st.warning("wallet_connect.html not found")

    st.subheader("🔁 Bridge Operations")
    user_address = st.text_input("Your Wallet Address")
    action = st.selectbox("Select Action", ["Deposit to L2", "Withdraw to L1", "Check Balances"])

    if user_address:
        if action == "Deposit to L2":
            amount = st.number_input("Amount (GBT)", min_value=0.0)
            if st.button("Deposit"):
                try:
                    tx = bridge_l1.functions.depositToL2(Web3.to_checksum_address(user_address)).transact({
                        'from': user_address,
                        'value': w3_l1.to_wei(amount, 'ether')
                    })
                    st.success(f"Deposit TX sent: {tx.hex()}")
                except Exception as e:
                    st.error(f"Error: {e}")

        elif action == "Withdraw to L1":
            amount = st.number_input("Amount (GBT)", min_value=0.0)
            if st.button("Withdraw"):
                try:
                    tx = bridge_l2.functions.withdrawToL1(Web3.to_checksum_address(user_address)).transact({
                        'from': user_address,
                        'value': w3_l2.to_wei(amount, 'ether')
                    })
                    st.success(f"Withdraw TX sent: {tx.hex()}")
                except Exception as e:
                    st.error(f"Error: {e}")

        elif action == "Check Balances":
            try:
                bal1 = w3_l1.eth.get_balance(user_address)
                bal2 = w3_l2.eth.get_balance(user_address)
                st.info(f"Layer 1: {w3_l1.from_wei(bal1, 'ether')} ETH")
                st.info(f"Layer 2: {w3_l2.from_wei(bal2, 'ether')} GBT")
            except Exception as e:
                st.error(f"Failed to fetch balances: {e}")


// 1. BridgeL1_ABI.json
[
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "user",
        "type": "address"
      }
    ],
    "name": "depositToL2",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  }
]

// 2. BridgeL2_ABI.json
[
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "user",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "mintFromL1",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]

// 3. wallet_connect.html
<!DOCTYPE html>
<html>
<head>
  <title>Connect Wallet</title>
  <script src="https://cdn.jsdelivr.net/npm/web3@1.10.0/dist/web3.min.js"></script>
</head>
<body>
  <button onclick="connectWallet()">Connect MetaMask</button>
  <p id="wallet-address"></p>

  <script>
    async function connectWallet() {
      if (window.ethereum) {
        try {
          const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
          document.getElementById('wallet-address').innerText = 'Connected: ' + accounts[0];
        } catch (err) {
          console.error('User rejected connection:', err);
        }
      } else {
        alert('MetaMask not found!');
      }
    }
  </script>
</body>
</html>

# Entrypoint
if __name__ == "__main__":
    if not st.session_state.logged_in:
        login()
    else:
        main_app()
