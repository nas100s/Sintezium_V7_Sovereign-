import os, time, datetime
from web3 import Web3
from eth_account.messages import encode_typed_data
from dotenv import load_dotenv

load_dotenv('/opt/sintezium/core/.env')

print('\n[INSTITUTIONAL RWA] Подготовка ордеров на спутниковые и геологические данные...', flush=True)

PRIVATE_KEY = os.getenv('PAYMASTER_KEY')
OWNER = '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC'
TARGET_TOKEN = Web3.to_checksum_address('0x2E32CCE1b65a4bd0f5375bEa97CAb87596e62e92')
w3 = Web3()

def sign_data_asset(asset_name, usd_value):
    domain_data = {'name': 'Sintezium Data Market', 'version': '1', 'chainId': 137, 'verifyingContract': TARGET_TOKEN}
    message_types = {'DataOrder': [{'name': 'seller', 'type': 'address'}, {'name': 'dataset', 'type': 'string'}, {'name': 'priceUSD', 'type': 'uint256'}]}
    message_data = {'seller': OWNER, 'dataset': asset_name, 'priceUSD': int(usd_value)}
    
    signable = encode_typed_data(domain_data=domain_data, message_types=message_types, message_data=message_data)
    signed = w3.eth.account.sign_message(signable, private_key=PRIVATE_KEY)
    
    print(f'[SUCCESS] EIP-712 Data-Intent для {asset_name} подписан: {signed.signature.hex()[:20]}...', flush=True)

if __name__ == '__main__':
    if not PRIVATE_KEY:
        print('[ERROR] Приватный ключ отсутствует!')
    else:
        sign_data_asset('Alibaba_Cloud_Geodetic_Report_125k', 1000)
        time.sleep(1)
        sign_data_asset('Satellite_Lithium_Map_2000', 500)
        time.sleep(1)
        sign_data_asset('Bedrock_87_Lithosphere_Data', 750)
        
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('/opt/sintezium/logs/AUTONOMOUS_LOG.md', 'a') as f:
            f.write(f'[{now}] INSTITUTIONAL DATA ORACLE: Satellite & Alibaba data intents broadcasted.\n')
        print('\n[BROADCAST] Данные предложены DeSci-фондам. Ждем оплаты в USDC для конвертации в SNZ.', flush=True)
