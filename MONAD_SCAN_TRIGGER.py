import os, time, requests, datetime
from dotenv import load_dotenv

load_dotenv('/opt/sintezium/core/.env')

print('\n[ETHERSCAN API STANDARD] Инициализация истинного MonadScan HFT Триггера...', flush=True)

MONADSCAN_API_KEY = os.getenv('MONADSCAN_API_KEY')
OWNER_WALLET = '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC'
API_URL = f'https://api-testnet.monadscan.com/api?module=account&action=txlist&address={OWNER_WALLET}&startblock=0&endblock=99999999&page=1&offset=1&sort=desc&apikey={MONADSCAN_API_KEY}'

last_tx_hash = None

def check_etherscan_api():
    global last_tx_hash
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        response = requests.get(API_URL, timeout=10)
        data = response.json()
        
        if data.get('status') == '1' and isinstance(data.get('result'), list) and len(data['result']) > 0:
            latest_tx = data['result'][0]['hash']
            
            if last_tx_hash is None:
                last_tx_hash = latest_tx
                print(f'[{now}] [OK] Etherscan API активен. Базовая TX: {latest_tx}', flush=True)
                return
            
            if latest_tx != last_tx_hash:
                print(f'\n[⚡ MONAD HFT SIGNAL] Новая ончейн-транзакция зафиксирована!', flush=True)
                last_tx_hash = latest_tx
                with open('/opt/sintezium/core/monad_signal.flag', 'w') as f:
                    f.write(f'TRIGGER_BY_ETHERSCAN_API_TX_{latest_tx}')
                print('[SIGNAL] Флаг передан в ядро на Polygon для выкупа SNZ!', flush=True)
        else:
            print(f'[{now}] [SCAN] Ожидание новых транзакций...', flush=True)
            
    except Exception as e:
        print(f'[{now}] [API HTTP ERROR]: {e}', flush=True)

if __name__ == '__main__':
    while True:
        check_etherscan_api()
        time.sleep(5) 
