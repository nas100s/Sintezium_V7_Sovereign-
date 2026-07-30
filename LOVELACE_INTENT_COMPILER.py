import os, json, datetime, time
from web3 import Web3
from eth_account.messages import encode_typed_data
from dotenv import load_dotenv

# Загрузка ключей из файла .env
load_dotenv('/opt/sintezium/core/.env')

print('\n[LOVELACE COMPILER] Инициализация алгоритмического ядра (Планкалкюль -> EVM)...')

# Ключи и адреса
# Пытаемся взять PAYMASTER_KEY, если нет - PRIVATE_KEY (как резерв)
PRIVATE_KEY = os.getenv('PAYMASTER_KEY') or os.getenv('PRIVATE_KEY')
OWNER_WALLET = '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC'
TARGET_LEGACY_SNZ = '0x2E32CCE1b65a4bd0f5375bEa97CAb87596e62e92'

w3 = Web3()

def compile_optimized_intents():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report_path = '/opt/sintezium/logs/FULL_MCAR_VALUATION_REPORT.json'
    
    if not os.path.exists(report_path):
        report_path = '/home/mllanastasiya88/FULL_MCAR_VALUATION_REPORT.json'
        if not os.path.exists(report_path):
            print('[ERROR] База данных ИИ пуста. Запустите MCAR_DISCOVERER_AGENT.')
            return

    with open(report_path, 'r') as f:
        rwa_data = json.load(f)

    optimized_data = sorted(rwa_data, key=lambda x: x.get('resonance_g', 0), reverse=True)
    print(f'[FORTRAN OPTIMIZE] Данные отсортированы. Лидер резонанса: {optimized_data[0]["file_name"]}')

    compiled_batch = []
    
    domain_data = {
        'name': 'Sintezium Analytical Engine',
        'version': '1.0',
        'chainId': 137, 
        'verifyingContract': Web3.to_checksum_address(TARGET_LEGACY_SNZ)
    }

    message_types = {
        'AnalyticalOrder': [
            {'name': 'author', 'type': 'address'},
            {'name': 'assetHash', 'type': 'string'},
            {'name': 'resonanceFactor', 'type': 'uint256'},
            {'name': 'requiredMATIC', 'type': 'uint256'}
        ]
    }

    print('[COMPILE] Генерация EIP-712 подписей для ТОП-3 активов...')
    for asset in optimized_data[:3]:
        matic_value = int(asset['valuation_matic'] * 10**18)
        res_factor = int(asset['resonance_g'] * 10**4)
        
        message_data = {
            'author': OWNER_WALLET,
            'assetHash': asset['file_name'],
            'resonanceFactor': res_factor,
            'requiredMATIC': matic_value
        }
        
        signable_bytes = encode_typed_data(domain_data, message_types, message_data)
        signed_message = w3.eth.account.sign_message(signable_bytes, private_key=PRIVATE_KEY)
        
        compiled_batch.append({
            'asset': asset['file_name'],
            'value_matic': asset['valuation_matic'],
            'resonance': asset['resonance_g'],
            'signature': signed_message.signature.hex()
        })
        print(f' -> Подписан: {asset["file_name"]} (Valuation: {asset["valuation_matic"]} MATIC)')

    batch_path = '/opt/sintezium/core/OPTIMIZED_INTENT_BATCH.json'
    with open(batch_path, 'w') as f:
        json.dump(compiled_batch, f, indent=2)
        
    print(f'\n[SUCCESS] Пакет ордеров записан в {batch_path}')
    
    with open('/opt/sintezium/logs/AUTONOMOUS_LOG.md', 'a') as f:
        f.write(f'[{now}] LOVELACE COMPILER: Optimized batch of 3 intents signed via EIP-712.\n')

if __name__ == '__main__':
    if PRIVATE_KEY:
        compile_optimized_intents()
    else:
        print('[FATAL ERROR] Ключ не найден в /opt/sintezium/core/.env')
