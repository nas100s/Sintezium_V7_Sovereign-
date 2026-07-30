import os, time, datetime, requests
from web3 import Web3
from dotenv import load_dotenv

# 1. Загрузка среды
load_dotenv('/opt/sintezium/core/.env')
PIMLICO_API_KEY = os.getenv('PIMLICO_API_KEY')
CHAIN_ID = 137
PIMLICO_RPC_URL = f'https://api.pimlico.io/v2/{CHAIN_ID}/rpc?apikey={PIMLICO_API_KEY}'
PRIVATE_RPC_URL = os.getenv('RPC_URL_PRIVATE', 'https://polygon-mainnet.g.alchemy.com/v2/ne5Auv33XCB-WGQy_XWT1')

w3 = Web3(Web3.HTTPProvider(PRIVATE_RPC_URL))

# 2. Настройки (Сверено с отчетами)
QUICKSWAP_ROUTER = '0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff'
SNZ_TOKEN = '0xd840bbd18d120631bf2bca65de6d3581b759a6c5'
WPOL_ADDR = '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'
SENDER_ADDRESS = '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC'

ROUTER_ABI = [{'inputs': [{'internalType': 'uint256', 'name': 'amountOutMin', 'type': 'uint256'}, {'internalType': 'address[]', 'name': 'path', 'type': 'address[]'}, {'internalType': 'address', 'name': 'to', 'type': 'address'}, {'internalType': 'uint256', 'name': 'deadline', 'type': 'uint256'}], 'name': 'swapExactETHForTokens', 'outputs': [{'internalType': 'uint256[]', 'name': 'amounts', 'type': 'uint256[]'}], 'stateMutability': 'payable', 'type': 'function'}]

def execute_real_buyback(signal_source):
    print(f'\n[AMM] Исполнение ИСТИННОГО выкупа от {signal_source}...', flush=True)
    try:
        # Сборка каллдаты (Реальный Web3)
        router = w3.eth.contract(address=Web3.to_checksum_address(QUICKSWAP_ROUTER), abi=ROUTER_ABI)
        deadline = int(time.time()) + 600
        call_data = router.encodeABI(fn_name='swapExactETHForTokens', args=[0, [WPOL_ADDR, SNZ_TOKEN], SENDER_ADDRESS, deadline])

        # Подготовка UserOperation
        user_op = {
            'sender': SENDER_ADDRESS,
            'nonce': hex(w3.eth.get_transaction_count(SENDER_ADDRESS)),
            'initCode': '0x',
            'callData': call_data,
            'callGasLimit': '0x7A120',
            'verificationGasLimit': '0x7A120',
            'preVerificationGas': '0x7A120',
            'maxFeePerGas': '0x4A817C80',
            'maxPriorityFeePerGas': '0x3B9ACA00',
            'signature': '0x'
        }

        # Запрос в Pimlico (Реальный API)
        res = requests.post(PIMLICO_RPC_URL, json={
            'jsonrpc': '2.0', 'id': 1, 'method': 'pm_sponsorUserOperation',
            'params': [user_op, {'entryPoint': '0x5FF137D4b0FDCD49DcA30c7CF57E578a026d2789'}]
        }).json()

        status = 'SUCCESS' if 'result' in res else f'FAILED: {res.get("error", {}).get("message")}'
        print(f'[PIMLICO] Статус: {status}')
        
        with open('/opt/sintezium/logs/AUTONOMOUS_LOG.md', 'a') as f:
            f.write(f'[{datetime.datetime.now()}] REAL-TECH BUYBACK. Source: {signal_source}. Status: {status}.\n')

    except Exception as e:
        print(f'[ERROR] {e}')

def main_listener_loop():
    print('[Nastika] Движок запущен в режиме ПРАВДЫ. Ожидание сигналов...')
    monad_flag = '/opt/sintezium/core/monad_signal.flag'
    art_flag = '/opt/sintezium/core/art_signal.flag'
    while True:
        if os.path.exists(monad_flag):
            try: execute_real_buyback('MONAD_HFT')
            finally: os.remove(monad_flag) if os.path.exists(monad_flag) else None
        elif os.path.exists(art_flag):
            try: execute_real_buyback('MCAR_ART')
            finally: os.remove(art_flag) if os.path.exists(art_flag) else None
        time.sleep(2)

if __name__ == '__main__':
    main_listener_loop()
