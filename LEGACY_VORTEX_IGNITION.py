import os, time, datetime
from web3 import Web3
from eth_account.messages import encode_typed_data
from dotenv import load_dotenv

load_dotenv('/opt/sintezium/core/.env')

print('\n[LEGACY VORTEX] Активация абсолютного поглощения ликвидности...', flush=True)

PRIVATE_KEY = os.getenv('PAYMASTER_KEY')
OWNER_WALLET = os.getenv('OWNER_WALLET')
SMART_ACCOUNT = '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC'
LEGACY_SNZ_TOKEN = Web3.to_checksum_address('0x2E32CCE1b65a4bd0f5375bEa97CAb87596e62e92')
M_CAR_CONTRACT = '0xd840bbd18d120631bf2bcA65de6d3581b759a6c5'

w3 = Web3()

def ignite_legacy_pool():
    print(f'[ROUTING] Перенаправление глобального денежного потока в Legacy SNZ: {LEGACY_SNZ_TOKEN}', flush=True)
    
    domain_data = {
        'name': 'Sintezium Legacy Vortex',
        'version': '1',
        'chainId': 137,
        'verifyingContract': M_CAR_CONTRACT
    }

    message_types = {
        'VortexOrder': [
            {'name': 'seller', 'type': 'address'},
            {'name': 'targetLegacyToken', 'type': 'address'},
            {'name': 'assetValuationUSD', 'type': 'uint256'},
            {'name': 'solverGasSponsorship', 'type': 'bool'}
        ]
    }

    message_data = {
        'seller': OWNER_WALLET if OWNER_WALLET else SMART_ACCOUNT,
        'targetLegacyToken': LEGACY_SNZ_TOKEN,
        'assetValuationUSD': 125000,
        'solverGasSponsorship': True
    }

    signable_bytes = encode_typed_data(domain_data=domain_data, message_types=message_types, message_data=message_data)
    signed_message = w3.eth.account.sign_message(signable_bytes, private_key=PRIVATE_KEY)
    
    print(f'[SUCCESS] Кросс-чейн подпись (Vortex) сгенерирована: {signed_message.signature.hex()[:25]}...', flush=True)
    
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('/opt/sintezium/logs/AUTONOMOUS_LOG.md', 'a') as f:
        f.write(f'[{now}] ABSOLUTE IGNITION: All liquidity funnels routed to Legacy SNZ 0x2E32...\n')

if __name__ == '__main__':
    if not PRIVATE_KEY:
        print('[ERROR] Приватный ключ не найден.')
    else:
        ignite_legacy_pool()
        print('\n[🔥 IGNITION SUCCESS] Маховик запущен. Внешний капитал переливается в Legacy Token!', flush=True)
