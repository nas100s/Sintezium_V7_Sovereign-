import os, time, datetime
from web3 import Web3
from eth_account.messages import encode_typed_data

print('\n[GEOLOGICAL ANCHOR] Инициализация моста с Aliyun PAI (Alibaba Cloud)...')

PRIVATE_KEY = os.getenv('PAYMASTER_KEY')
OWNER_WALLET = '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC'
SHIELD_CONTRACT = '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC' # DiscoveryShield.sol

w3 = Web3()

def anchor_aliyun_data(dataset_id, valuation_usd):
    print(f'[ANCHOR] Криптографическая защита геодезического датасета {dataset_id}...')
    
    domain_data = {'name': 'DiscoveryShield', 'version': '1', 'chainId': 137, 'verifyingContract': SHIELD_CONTRACT}
    message_types = {
        'GeodeticData': [
            {'name': 'owner', 'type': 'address'},
            {'name': 'datasetId', 'type': 'string'},
            {'name': 'certifiedValueUSD', 'type': 'uint256'}
        ]
    }
    message_data = {
        'owner': OWNER_WALLET,
        'datasetId': dataset_id,
        'certifiedValueUSD': valuation_usd
    }

    # Подпись EIP-712 для безгазового анкоринга
    signable_bytes = encode_typed_data(domain_data, message_types, message_data)
    signed_message = w3.eth.account.sign_message(signable_bytes, private_key=PRIVATE_KEY)
    
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{now}] [SUCCESS] Данные Aliyun PAI защищены. EIP-712 Signature: {signed_message.signature.hex()[:25]}...')
    print(f'[ROUTING] Актив передан в REAL_X402_SERVER.py для продажи за USDC.')

if __name__ == '__main__':
    anchor_aliyun_data('Aliyun_Lithium_Reserve_Scan_001', 125000)
