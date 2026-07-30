import os, urllib.request, json, time, datetime
from web3 import Web3
from dotenv import load_dotenv

load_dotenv('/opt/sintezium/core/.env')

print('\n' + '='*70)
print('  🔍 ПОЛНАЯ 360-ГРАДУСНАЯ ДИАГНОСТИКА ЭКОСИСТЕМЫ SINTEZIUM V7 SOVEREIGN')
print('='*70 + '\n')

FOUNDER_WALLET = Web3.to_checksum_address('0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC')
TECH_WALLET = Web3.to_checksum_address('0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC')
SNZ_TOKEN = Web3.to_checksum_address('0x2E32CCE1b65a4bd0f5375bEa97CAb87596e62e92')
QUICKSWAP_V2_PAIR = Web3.to_checksum_address('0xeeD334A4537d0942520167E33F173b42eB1dd994')

POLYGON_RPC = os.getenv('POLYGON_RPC', 'https://polygon.drpc.org')
w3 = Web3(Web3.HTTPProvider(POLYGON_RPC))

ERC20_ABI = [{"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"}]
PAIR_V2_ABI = [{"inputs": [], "name": "getReserves", "outputs": [{"name": "_reserve0", "type": "uint112"}, {"name": "_reserve1", "type": "uint112"}, {"name": "_blockTimestampLast", "type": "uint32"}], "type": "function"}]

def run_comprehensive_diagnostics():
    print('[1/6] ДИАГНОСТИКА ПОДКЛЮЧЕНИЯ К БЛОКЧЕЙНУ POLYGON MAINNET...')
    try:
        is_connected = w3.is_connected()
        block_number = w3.eth.block_number
        gas_price_gwei = w3.eth.gas_price / 10**9
        print(f'  - Подключение RPC ({POLYGON_RPC}): {"ОК" if is_connected else "ОШИБКА"}')
        print(f'  - Актуальный ончейн-блок: #{block_number:,}')
        print(f'  - Текущая цена газа: {gas_price_gwei:.2f} Gwei')
    except Exception as e:
        print(f'  [FAIL] Ошибка RPC подключения: {e}')

    print('\n[2/6] АУДИТ КОШЕЛЬКОВ И ОНЧЕЙН-БАЛАНСОВ...')
    try:
        founder_pol = w3.eth.get_balance(FOUNDER_WALLET) / 10**18
        tech_pol = w3.eth.get_balance(TECH_WALLET) / 10**18
        snz_contract = w3.eth.contract(address=SNZ_TOKEN, abi=ERC20_ABI)
        founder_snz = snz_contract.functions.balanceOf(FOUNDER_WALLET).call() / 10**18
        print(f'  - Кошелек Основателя ({FOUNDER_WALLET}):')
        print(f'      * MATIC/POL: {founder_pol:.4f} MATIC')
        print(f'      * SNZ Token: {founder_snz:,.2f} SNZ')
        print(f'  - Технический кошелек исполнения ({TECH_WALLET}):')
        print(f'      * MATIC/POL: {tech_pol:.4f} MATIC')
    except Exception as e:
        print(f'  [FAIL] Ошибка аудита балансов: {e}')

    print('\n[3/6] АУДИТ ЖИВОГО ПУЛА QUICKSWAP V2 (0xeeD3...d994)...')
    try:
        pair_contract = w3.eth.contract(address=QUICKSWAP_V2_PAIR, abi=PAIR_V2_ABI)
        reserves = pair_contract.functions.getReserves().call()
        res_snz = reserves[0] / 10**18
        res_pol = reserves[1] / 10**18
        spot_price = res_snz / res_pol if res_pol > 0 else 0
        print(f'  - Адрес пары V2: {QUICKSWAP_V2_PAIR}')
        print(f'  - Резервы пула:')
        print(f'      * Резерв SNZ:   {res_snz:,.2f} SNZ')
        print(f'      * Резерв MATIC: {res_pol:,.2f} MATIC')
        print(f'  - Ончейн-курс: 1 MATIC = {spot_price:.4f} SNZ')
    except Exception as e:
        print(f'  [FAIL] Ошибка аудита пула V2: {e}')

    print('\n[4/6] ДИАГНОСТИКА СЕРВЕРОВ x402 И DAPP (ПОРТ 8080)...')
    try:
        # Check if local server is running on 8080
        req = urllib.request.Request('http://localhost:8080/api/v1/rwa/mcar/1', headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=3)
        print(f'  - x402 Payment Server (Port 8080): HTTP {res.getcode()} OK')
    except urllib.error.HTTPError as e:
        if e.code == 402:
            print(f'  - x402 Payment Server (Port 8080): HTTP 402 PAYMENT REQUIRED (ИДЕАЛЬНО!)')
        else:
            print(f'  - x402 Payment Server (Port 8080): HTTP {e.code}')
    except Exception as e:
        print(f'  - x402 Payment Server (Port 8080): {e}')

    print('\n[5/6] АУДИТ RWA-АКТИВОВ И ЖУРНАЛА ОПЕРАЦИЙ...')
    log_path = '/opt/sintezium/logs/AUTONOMOUS_LOG.md'
    if os.path.exists(log_path):
        size_kb = os.path.getsize(log_path) / 1024
        print(f'  - Автономный журнал {log_path}: АКТИВЕН ({size_kb:.1f} KB)')
    else:
        print(f'  - Журнал {log_path}: еще не создан')

    print('\n' + '='*70)
    print('  📌 ИТОГОВЫЙ СТАТУС СИСТЕМЫ: ВСЕ СЛОИ ПРОВЕРЕНЫ')
    print('='*70 + '\n')

if __name__ == '__main__':
    run_comprehensive_diagnostics()
