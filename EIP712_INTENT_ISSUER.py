import os, time, datetime
from web3 import Web3
from eth_account.messages import encode_typed_data
from dotenv import load_dotenv

load_dotenv('/opt/sintezium/core/.env')

print('[M-CAR EIP-712] Инициализация...')

OWNER_WALLET = '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC'
ART_CONTRACT = '0xd840bbd18d120631bf2bca65de6d3581b759a6c5'
PRIVATE_KEY = os.getenv('PAYMASTER_KEY')

w3 = Web3()

def sign_art_sale_intent(art_id, price_in_usd):
    domain_data = {
        'name': 'M-CAR Art Liquidity Protocol',
        'version': '1',
        'chainId': 137,
        'verifyingContract': ART_CONTRACT
    }
    message_types = {
        'Order': [
            {'name': 'owner', 'type': 'address'},
            {'name': 'artId', 'type': 'uint256'},
            {'name': 'priceUSD', 'type': 'uint256'},
            {'name': 'nonce', 'type': 'uint256'}
        ]
    }
    message_data = {
        'owner': OWNER_WALLET,
        'artId': int(art_id),
        'priceUSD': int(price_in_usd),
        'nonce': int(time.time())
    }
    signable_bytes = encode_typed_data(domain_data=domain_data, message_types=message_types, message_data=message_data)
    signed_message = w3.eth.account.sign_message(signable_bytes, private_key=PRIVATE_KEY)
    
    print(f'\n[SUCCESS] Ордер для Картины {art_id}!')
    print(f' -> SIG: {signed_message.signature.hex()}')
    
    with open('/opt/sintezium/logs/AUTONOMOUS_LOG.md', 'a') as f:
        f.write('[EIP-712 INTENT SIGNED]\n')

if __name__ == '__main__':
    sign_art_sale_intent(1, 62500)
    sign_art_sale_intent(2, 62500)
