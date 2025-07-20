from web3_client import l1, l2
import json

with open("BridgeL1.json") as f:
    l1_abi = json.load(f)["abi"]
with open("BridgeL2.json") as f:
    l2_abi = json.load(f)["abi"]

bridge_l1 = l1.eth.contract(address="0xL1_CONTRACT", abi=l1_abi)
bridge_l2 = l2.eth.contract(address="0xL2_CONTRACT", abi=l2_abi)

def run_relayer():
    try:
        events = bridge_l1.events.Burn.createFilter(fromBlock='latest').get_all_entries()
        for evt in events:
            user = evt["args"]["from"]
            amount = evt["args"]["amount"]
            bridge_l2.functions.mint(user, amount).transact({"from": l2.eth.accounts[0]})
            print(f"Relayed burn {amount} from {user} to L2 mint.")
    except:
        pass
