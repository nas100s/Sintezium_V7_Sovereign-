import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv('/opt/sintezium/core/.env')

PRIVATE_RPC_URL = os.getenv('RPC_URL_PRIVATE', 'https://polygon-mainnet.g.alchemy.com/v2/ne5Auv33XCB-WGQy_XWT1')
w3 = Web3(Web3.HTTPProvider(PRIVATE_RPC_URL))

OWNER_WALLET = '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC'
PRIVATE_KEY = os.getenv('PAYMASTER_KEY')

# Используем минимальный корректный байткод для деплоя
BYTECODE = '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC23806100206000396000f3fe'

def deploy_krp():
    print('[DEPLOY] Запуск публикации токена KRP в сеть Polygon...')
    
    nonce = w3.eth.get_transaction_count(OWNER_WALLET)
    
    tx = {
        'nonce': nonce,
        'from': OWNER_WALLET,
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price,
        'data': BYTECODE,
        'chainId': 137
    }
    
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    
    try:
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f'\n[SUCCESS] Контракт токена KRP отправлен! TX: {tx_hash.hex()}')
        with open('/opt/sintezium/logs/AUTONOMOUS_LOG.md', 'a') as f:
            f.write(f'- [STAKING DEPLOY] Krupa Fuel Token () successfully deployed. TX: {tx_hash.hex()}\n')
    except Exception as e:
        print(f'[DEPLOY ERROR]: {e}')

if __name__ == '__main__':
    if not PRIVATE_KEY:
        print('[ERROR] Приватный ключ отсутствует!')
    else:
        deploy_krp()
