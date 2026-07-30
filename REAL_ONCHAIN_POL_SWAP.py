import os, time, datetime
from web3 import Web3
from dotenv import load_dotenv

load_dotenv('/opt/sintezium/core/.env')

print('\n[FOUNDER WALLET PUMP ENGINE] Повторная попытка транзакции с расширенными параметрами...', flush=True)

FOUNDER_WALLET = Web3.to_checksum_address('0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC')
PRIVATE_KEY = os.getenv('PAYMASTER_KEY')

SNZ_TOKEN = Web3.to_checksum_address('0x2E32CCE1b65a4bd0f5375bEa97CAb87596e62e92')
WMATIC_POL = Web3.to_checksum_address('0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270')
QUICKSWAP_V2_ROUTER = Web3.to_checksum_address('0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff')

POLYGON_RPC = os.getenv('POLYGON_RPC', 'https://polygon.drpc.org')
w3 = Web3(Web3.HTTPProvider(POLYGON_RPC))

# ABI with swapExactETHForTokensSupportingFeeOnTransferTokens
ROUTER_V2_ABI = [
    {
        "inputs": [
            {"name": "amountOutMin", "type": "uint256"},
            {"name": "path", "type": "address[]"},
            {"name": "to", "type": "address"},
            {"name": "deadline", "type": "uint256"}
        ],
        "name": "swapExactETHForTokensSupportingFeeOnTransferTokens",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    }
]

def execute_founder_onchain_pump(amount_pol_to_swap=0.5):
    try:
        account = w3.eth.account.from_key(PRIVATE_KEY)
        derived_address = account.address
        
        print(f'[1/4] Кошелек-отправитель: {derived_address}')
        pol_balance_wei = w3.eth.get_balance(derived_address)
        print(f'      Баланс: {pol_balance_wei / 1e18:.4f} MATIC')
        
        swap_value_wei = int(amount_pol_to_swap * 10**18)
        router = w3.eth.contract(address=QUICKSWAP_V2_ROUTER, abi=ROUTER_V2_ABI)
        
        path = [WMATIC_POL, SNZ_TOKEN]
        deadline = int(time.time()) + 600
        
        print(f'\n[2/4] Формирование транзакции (Supporting Fee On Transfer)...')
        
        nonce = w3.eth.get_transaction_count(derived_address)
        gas_price = w3.eth.gas_price
        
        tx = router.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
            0, path, FOUNDER_WALLET, deadline
        ).build_transaction({
            'from': derived_address,
            'value': swap_value_wei,
            'gas': 500000,
            'gasPrice': int(gas_price * 1.5),
            'nonce': nonce,
            'chainId': 137
        })
        
        print(f'[3/4] Подписание и отправка...')
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_hash_hex = tx_hash.hex()
        
        print(f'[SUCCESS] Отправлено: https://polygonscan.com/tx/{tx_hash_hex}')
        print('[4/4] Ожидание подтверждения...')
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        
        if receipt.status == 1:
            print(f'\n[🚀 PUMP SUCCESS!] ПОДТВЕРЖДЕНО В БЛОКЕ #{receipt.blockNumber}!')
        else:
            print(f'[FAIL] Транзакция отклонена: https://polygonscan.com/tx/{tx_hash_hex}')

    except Exception as e:
        print(f'[ERROR] Ошибка: {e}')

if __name__ == '__main__':
    execute_founder_onchain_pump()
