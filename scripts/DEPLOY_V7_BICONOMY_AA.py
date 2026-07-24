import os
import json
import requests
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv

# Load environment
load_dotenv('!/Док/.env')

CHAIN_ID = 137
BICONOMY_API_KEY = "7312f3bd-4d2e-4002-96e9-095d459ba4e7" 

# RPC
RPC_URL = "https://polygon-mainnet.g.alchemy.com/v2/ne5Auv33XCB-WGQy_XWT1"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Admin Wallet
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
account = Account.from_key(PRIVATE_KEY)

def deploy_aa():
    print("=== [DEPLOY V7 BICONOMY SPONSORED] INITIALIZING ===")
    
    # 1. Load Bytecode
    bytecode_path = "SinteziumV7_Final.bin"
    with open(bytecode_path, "r") as f:
        bytecode = f.read().strip()
    if not bytecode.startswith("0x"): bytecode = "0x" + bytecode

    # 2. Build Deployment Data
    # Biconomy Forwarder (Checksum)
    FORWARDER = w3.to_checksum_address("0x84a0856b038eaad1cc7e2ae31a268a221f456073")
    abi = [{"inputs":[{"internalType":"address","name":"forwarder","type":"address"}],"stateMutability":"nonpayable","type":"constructor"}]
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    # Use standard build_transaction to get 'data' but don't send it yet
    deploy_data = contract.constructor(FORWARDER).data_in_transaction

    # 3. Sponsorship Request (Native Meta-TX approach via Factory)
    # Most reliable CLI method for sponsored deployment without full SDK
    native_url = "https://api.biconomy.io/api/v2/meta-tx/native"
    payload = {
        "from": account.address,
        "to": "0x4e59b44847b379578588920cA78FbF26c0B4956C", # Create2 Factory
        "api_key": BICONOMY_API_KEY,
        "params": [
            "888777", # Salt for V7 Awakening
            deploy_data
        ],
        "method": "deploy",
        "chainId": CHAIN_ID
    }
    
    headers = {
        "x-api-key": BICONOMY_API_KEY,
        "Content-Type": "application/json"
    }

    print(f"[*] Requesting sponsored deployment for V7 at Factory...")
    
    try:
        response = requests.post(native_url, json=payload, headers=headers, timeout=60)
        print(f"[RESULT] Status: {response.status_code}")
        
        data = response.json()
        if response.status_code in [200, 201]:
            print(f"✅ SUCCESS! Biconomy accepted the UserOp.")
            print(f"[TX] {data}")
        else:
            print(f"❌ REJECTED: {data}")
            print("[HINT] Ensure 0x4e59... is enabled in Biconomy Sponsorship policies.")

    except Exception as e:
        print(f"❌ Request Error: {e}")

if __name__ == "__main__":
    deploy_aa()
