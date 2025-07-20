from web3 import Web3

l1 = Web3(Web3.HTTPProvider("http://localhost:8545"))
l2 = Web3(Web3.HTTPProvider("http://GBTNetwork:8545"))

def get_balance(address):
    # Replace with real on-chain balance calls
    return 1000, 2000
