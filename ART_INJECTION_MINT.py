import os
import time
import json
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv

load_dotenv('/opt/sintezium/core/.env')

# Инициализация
RPC_URL = os.getenv("RPC_URL_PRIVATE", "https://polygon-rpc.com")
PRIVATE_KEY = os.getenv("PRIVATE_KEY") 
ART_CONTRACT = Web3.to_checksum_address("0xd840bbd18d120631bf2bca65de6d3581b759a6c5")

w3 = Web3(Web3.HTTPProvider(RPC_URL))
if PRIVATE_KEY:
    account = Account.from_key(PRIVATE_KEY)
else:
    raise ValueError("PRIVATE_KEY not found in environment")

from eth_account.messages import encode_defunct

def sign_mint_intent(art_name, metadata_uri):
    """
    Генерирует безгазовое намерение (Intent) на минт картины.
    Вместо отправки транзакции, создается криптографическая подпись.
    """
    print(f"\n[M-CAR] Формирование безгазового намерения для '{art_name}'...")
    
    # Сообщение для подписи
    message_text = f"Sintezium M-CAR Intent: Mint {art_name} at {metadata_uri} timestamp {int(time.time())}"
    signable_message = encode_defunct(text=message_text)
    
    # Подписываем данные (0 газа)
    signature = account.sign_message(signable_message)
    sig_hex = signature.signature.hex()
    
    print(f"[SUCCESS] Намерение подписано! Signature: {sig_hex[:20]}...")
    
    # 2. Мгновенная передача сигнала (Trigger) в PIMLICO_LIQUIDITY_ENGINE
    # Это связывает подпись картины с реальным выкупом SNZ
    with open("/opt/sintezium/core/art_signal.flag", "w") as f:
        f.write(f"ART_INTENT_SIGNED_SIG:{sig_hex}")
    
    print("[СИГНАЛ] Команда на выкуп SNZ передана Пеймастеру!")

if __name__ == "__main__":
    URI_ART_1 = "ipfs://QmResonance888_Map1" 
    URI_ART_2 = "ipfs://QmResonance888_Map2"
    
    sign_mint_intent("Геодезическая Карта-Картина 1", URI_ART_1)
    time.sleep(2)
    sign_mint_intent("Геодезическая Карта-Картина 2", URI_ART_2)
