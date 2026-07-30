import os, time, datetime
from web3 import Web3
from dotenv import load_dotenv

load_dotenv('/opt/sintezium/core/.env')

# Извлекаем приватный RPC из окружения
PRIVATE_RPC_URL = os.getenv('RPC_URL_PRIVATE', 'https://polygon-mainnet.g.alchemy.com/v2/ne5Auv33XCB-WGQy_XWT1')
w3 = Web3(Web3.HTTPProvider(PRIVATE_RPC_URL))

# Адреса
SENDER_ADDRESS = '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC'
POOL_ADDRESS = '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC'

print('[MONITOR] Запуск автономного ловца транзакций от Сольверов на Polygon...')

def check_for_buyback():
    try:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        balance_wei = w3.eth.get_balance(SENDER_ADDRESS)
        balance_matic = w3.from_wei(balance_wei, 'ether')
        
        # Запись в лог монитора
        print(f'[{now}] [OK] Баланс маркет-мейкера: {balance_matic} POL. Слушаем пул {POOL_ADDRESS}...')
    except Exception as e:
        print(f'[MONITOR ERROR]: {e}')

if __name__ == '__main__':
    while True:
        check_for_buyback()
        time.sleep(15)
