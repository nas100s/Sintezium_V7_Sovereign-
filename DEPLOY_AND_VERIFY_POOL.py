import os, json, datetime
from web3 import Web3
from dotenv import load_dotenv

load_dotenv('/opt/sintezium/core/.env')

print('\n[POOL RECOVERY ENGINE] Полная ончейн-диагностика пулов ликвидности SNZ...', flush=True)

SNZ_TOKEN = Web3.to_checksum_address('0x2E32CCE1b65a4bd0f5375bEa97CAb87596e62e92')
WMATIC_POL = Web3.to_checksum_address('0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270')
USDC_TOKEN = Web3.to_checksum_address('0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC')

QUICKSWAP_V3_FACTORY = Web3.to_checksum_address('0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC')
UNISWAP_V3_FACTORY = Web3.to_checksum_address('0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC')

POLYGON_RPC = os.getenv('POLYGON_RPC', 'https://polygon.drpc.org')
w3 = Web3(Web3.HTTPProvider(POLYGON_RPC))

FACTORY_ABI = [{"inputs": [{"name": "tokenA", "type": "address"}, {"name": "tokenB", "type": "address"}, {"name": "fee", "type": "uint24"}], "name": "getPool", "outputs": [{"name": "pool", "type": "address"}], "type": "function"}]

def scan_all_pools():
    fee_tiers = [500, 3000, 10000]
    paired_tokens = [('POL', WMATIC_POL), ('USDC', USDC_TOKEN)]
    pools_found = []
    
    for token_name, token_addr in paired_tokens:
        for fee in fee_tiers:
            for factory_name, factory_addr in [('QuickSwap v3', QUICKSWAP_V3_FACTORY), ('Uniswap v3', UNISWAP_V3_FACTORY)]:
                try:
                    factory = w3.eth.contract(address=factory_addr, abi=FACTORY_ABI)
                    pool_addr = factory.functions.getPool(SNZ_TOKEN, token_addr, fee).call()
                    if pool_addr and pool_addr != "0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC":
                        pools_found.append((factory_name, token_name, fee / 10000, pool_addr))
                except Exception:
                    pass

    if pools_found:
        print('[SUCCESS] Найдены активные пулы:')
        for f, t, fee, addr in pools_found:
            print(f'  - {f} | SNZ/{t} ({fee}%) -> {addr}')
    else:
        print('[⚠️ ПОДТВЕРЖДЕНО] Пул еще не развернут в сети Polygon!')

if __name__ == '__main__':
    scan_all_pools()
