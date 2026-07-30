import os
import time
from web3 import Web3
from dotenv import load_dotenv

load_dotenv('blockchain_gateway/.env')

NINA_TOKEN = '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC'
WALLET = os.getenv('WALLET_ADDRESS')
RPC = 'https://polygon-bor-rpc.publicnode.com'

def monitor_and_guard():
    w3 = Web3(Web3.HTTPProvider(RPC))
    print(f"[!] AUTONOMOUS GUARDIAN STARTED FOR NINA.")
    
    while True:
        try:
            # Проверка баланса MATIC (как топлива для моста)
            balance = w3.eth.get_balance(WALLET)
            eth_val = w3.from_wei(balance, 'ether')
            
            with open('AUTONOMOUS_GUARDIAN.log', 'a') as f:
                f.write(f"{time.ctime()}: Balance {eth_val} MATIC. Health: OK\n")
            
            # Логика: если баланс растет (от торговли на бирже), мы готовимся к прыжку на ETH
            if balance > w3.to_wei(50, 'ether'): # Порог для переезда на Mainnet
                print("[🚀] ПОРУЧЕНИЕ: ЛИКВИДНОСТЬ ДОСТАТОЧНА ДЛЯ ПРИВЯЗКИ К ETHEREUM.")
                # Здесь будет вызов скрипта DEPLOY_NINA_ETHEREUM_FINAL.py
            
            time.sleep(3600) # Проверка раз в час
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    monitor_and_guard()
