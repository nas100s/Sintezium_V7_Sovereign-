import os
import time
import json
from web3 import Web3
from dotenv import load_dotenv

# Загружаем окружение
load_dotenv('/opt/sintezium/core/.env')

# Конфигурация - переходим на HTTP для стабильности
RPC_URL = os.getenv("RPC_URL_PRIVATE", "https://polygon-rpc.com")
# Убеждаемся, что адрес в нижнем регистре с префиксом 0x для RPC
ART_CONTRACT_ADDRESS = "0xd840bbd18d120631bf2bca65de6d3581b759a6c5".lower()
if not ART_CONTRACT_ADDRESS.startswith("0x"):
    ART_CONTRACT_ADDRESS = "0x" + ART_CONTRACT_ADDRESS

# Сигнатура Transfer(address,address,uint256)
TRANSFER_EVENT_SIGNATURE = Web3.keccak(text="Transfer(address,address,uint256)").hex()
if not TRANSFER_EVENT_SIGNATURE.startswith("0x"):
    TRANSFER_EVENT_SIGNATURE = "0x" + TRANSFER_EVENT_SIGNATURE

print(f"[M-CAR] Инициализация Art-Liquidity Bridge (Polling Mode)...")
print(f"[*] Контракт: {ART_CONTRACT_ADDRESS}")
print(f"[*] Сигнатура: {TRANSFER_EVENT_SIGNATURE}")

w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    print("ОШИБКА: Не удалось подключиться к Polygon RPC.")
else:
    print(f"[SUCCESS] Подключено к Polygon. Текущий блок: {w3.eth.block_number}")

def handle_art_event(event):
    tx_hash = event['transactionHash'].hex()
    print(f"\n[💎 АРТ-РЕЗОНАНС] Обнаружено движение! TX: {tx_hash}")
    
    # Запись в лог
    log_path = "/opt/sintezium/logs/AUTONOMOUS_LOG.md"
    try:
        with open(log_path, "a") as log:
            log.write(f"### [{time.strftime('%X')}] M-CAR EVENT\n- Картина активирована. TX: {tx_hash}\n\n")
    except: pass
    
    # Сигнал для Pimlico
    with open("/opt/sintezium/core/art_signal.flag", "w") as flag:
        flag.write(f"BUYBACK_TRIGGERED_BY_ART:{tx_hash}")

def run_bridge():
    # Начинаем мониторинг с текущего блока
    last_checked_block = w3.eth.block_number
    print(f"[*] Мониторинг запущен с блока {last_checked_block}")

    while True:
        try:
            current_block = w3.eth.block_number
            if current_block > last_checked_block:
                # Получаем логи за новые блоки
                logs = w3.eth.get_logs({
                    "fromBlock": last_checked_block + 1,
                    "toBlock": current_block,
                    "address": Web3.to_checksum_address(ART_CONTRACT_ADDRESS),
                    "topics": [TRANSFER_EVENT_SIGNATURE]
                })
                
                for log_entry in logs:
                    handle_art_event(log_entry)
                
                last_checked_block = current_block
            
            time.sleep(10) # Интервал опроса 10 секунд
        except Exception as e:
            print(f"[!] Ошибка моста: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_bridge()
