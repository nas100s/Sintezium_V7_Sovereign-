
import os
import requests
import json
from web3 import Web3
from dotenv import load_dotenv

# LOAD CONFIG
load_dotenv('!/Док/.env')

# BLOCKCHAIN CONFIG
RPC_URL = os.getenv("RPC_URL", "https://polygon-mainnet.g.alchemy.com/v2/ne5Auv33XCB-WGQy_XWT1")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# BICONOMY / THIRDWEB GASLESS CONFIG
ENGINE_URL = os.getenv("ENGINE_URL", "https://engine.thirdweb.com")
SECRET_KEY = os.getenv("THIRDWEB_SECRET")
BICONOMY_API_KEY = "mee_PjAQAfgT3C2rFy4QZg3NRD"
DAPP_KEY = "7312f3bd-4d2e-4002-96e9-095d459ba4e7"

# CONTRACTS
TOKEN_SNZ = "0x2E32CCE1b65a4bd0f5375bEa97CAb87596e62e92"
ROUTER_QUICKSWAP = "0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff"
TREASURY_WALLET = "0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC"

class GaslessLiquidityEngine:
    """
    Real-Tech Gasless Liquidity Engine.
    Uses Thirdweb Engine to execute transactions sponsored by the Treasury/Paymaster.
    """
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "x-secret-key": SECRET_KEY
        }

    def get_token_balance(self, token, account):
        url = f"{ENGINE_URL}/v1/read/contract"
        payload = {
            "chainId": 137,
            "contractAddress": token,
            "function": "balanceOf(address)",
            "params": [account]
        }
        res = requests.post(url, headers=self.headers, json=payload)
        return int(res.json().get("result", 0))

    def inject_liquidity_gasless(self, amount_snz, amount_matic):
        """
        Executes a gasless liquidity injection.
        In a Real-Tech setup, this calls the Thirdweb Engine backend to sign and relay.
        """
        print(f"[*] Initiating Gasless Injection: {amount_snz} SNZ / {amount_matic} MATIC")
        
        # 1. Approve Router (Gasless via Engine)
        approve_url = f"{ENGINE_URL}/v1/write/contract"
        approve_payload = {
            "chainId": 137,
            "contractAddress": TOKEN_SNZ,
            "function": "approve(address,uint256)",
            "params": [ROUTER_QUICKSWAP, str(amount_snz * 10**18)]
        }
        
        # This will be queued and signed by the Thirdweb Backend (0x6Fc3... or similar)
        # using the backend's gas/paymaster.
        resp = requests.post(approve_url, headers=self.headers, json=approve_payload)
        print(f"[✅] Approval Transaction Queued: {resp.json().get('queueId')}")

        return resp.json()

if __name__ == "__main__":
    engine = GaslessLiquidityEngine()
    # Diagnostic check before real run
    bal = engine.get_token_balance(TOKEN_SNZ, TREASURY_WALLET)
    print(f"[*] Treasury SNZ Balance: {bal / 10**18:.2f}")
    
    # engine.inject_liquidity_gasless(100, 0) # UNCOMMENT FOR REAL EXECUTION
