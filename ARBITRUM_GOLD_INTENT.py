import os, time, datetime
from web3 import Web3
from eth_account.messages import encode_typed_data
from dotenv import load_dotenv

load_dotenv('/opt/sintezium/core/.env')

print('\n[GOLD-RESONANCE] Инициализация золотого моста с Pleasing Market...', flush=True)

OWNER_WALLET = '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC'
PRIVATE_KEY = os.getenv('PAYMASTER_KEY')

PGOLD_TOKEN = os.getenv('PGOLD_ARBITRUM', '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC7')
USDPM_STABLE = os.getenv('USDPM_ARBITRUM', '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC')

w3 = Web3()

def generate_gold_backed_intent(art_id, value_usdpm):
    print(f'\n[RWA GOLD] Формирование ордера для Картины M-CAR ID {art_id}...', flush=True)
    
    domain_data = {
        'name': 'Pleasing Market RWA Bridge',
        'version': '1',
        'chainId': 42161,
        'verifyingContract': Web3.to_checksum_address('0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC')
    }

    message_types = {
        'GoldIntent': [
            {'name': 'seller', 'type': 'address'},
            {'name': 'assetId', 'type': 'uint256'},
            {'name': 'paymentToken', 'type': 'address'},
            {'name': 'priceUSDpm', 'type': 'uint256'},
            {'name': 'targetPoolPolygon', 'type': 'address'}
        ]
    }

    message_data = {
        'seller': OWNER_WALLET,
        'assetId': int(art_id),
        'paymentToken': USDPM_STABLE,
        'priceUSDpm': int(value_usdpm * 10**6),
        'targetPoolPolygon': '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC'
    }

    signable_bytes = encode_typed_data(domain_data=domain_data, message_types=message_types, message_data=message_data)
    signed_message = w3.eth.account.sign_message(signable_bytes, private_key=PRIVATE_KEY)
    
    print(f'[SUCCESS] Золотой интент успешно подписан: {signed_message.signature.hex()[:25]}...', flush=True)
    
    with open('/opt/sintezium/logs/AUTONOMOUS_LOG.md', 'a') as f:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f'[{now}] GOLD-BACKED INTENT GENERATED FOR ART {art_id} via USDpm.\n')

if __name__ == '__main__':
    if not PRIVATE_KEY:
        print('[ERROR] Приватный ключ отсутствует!')
    else:
        generate_gold_backed_intent(1, 50)
