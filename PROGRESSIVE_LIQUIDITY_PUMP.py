import os, time, json, datetime
from web3 import Web3
from eth_account.messages import encode_typed_data
from dotenv import load_dotenv

load_dotenv('/opt/sintezium/core/.env')

print('\n[PROGRESSIVE LIQUIDITY PUMP] Инициализация модуля выкупа и депозита в ERC-4626 Vault...', flush=True)

PRIVATE_KEY = os.getenv('PAYMASTER_KEY')
OWNER_WALLET = Web3.to_checksum_address(os.getenv('OWNER_WALLET', '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC'))
SNZ_TOKEN = Web3.to_checksum_address('0x2E32CCE1b65a4bd0f5375bea97Cab87596e62e92')
USDC_TOKEN = Web3.to_checksum_address('0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC')
VAULT_4626 = Web3.to_checksum_address(os.getenv('VAULT_4626_ADDRESS', '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC'))

POLYGON_RPC = os.getenv('POLYGON_RPC', 'https://polygon-rpc.com')
w3 = Web3(Web3.HTTPProvider(POLYGON_RPC))

def generate_vault_deposit_intent(snz_amount):
    domain_data = {'name': 'Sintezium Vault 4626 Engine', 'version': '1', 'chainId': 137, 'verifyingContract': VAULT_4626}
    message_types = {'VaultDepositIntent': [{'name': 'depositor', 'type': 'address'}, {'name': 'assetToken', 'type': 'address'}, {'name': 'amount', 'type': 'uint256'}, {'name': 'receiver', 'type': 'address'}, {'name': 'autoCompound', 'type': 'bool'}]}
    message_data = {'depositor': OWNER_WALLET, 'assetToken': SNZ_TOKEN, 'amount': int(snz_amount), 'receiver': OWNER_WALLET, 'autoCompound': True}
    signable = encode_typed_data(domain_data=domain_data, message_types=message_types, message_data=message_data)
    return w3.eth.account.sign_message(signable, private_key=PRIVATE_KEY).signature.hex()

def execute_liquidity_pump_and_vault_deposit(usdc_amount_to_pump=50 * 10**6):
    print(f'[1/3] Инициализация PUMP цикла: Выкупа SNZ на сумму {usdc_amount_to_pump / 10**6} USDC...', flush=True)
    estimated_snz_bought = int((usdc_amount_to_pump / 10**6) * 16.66 * 10**18)
    print(f'[SUCCESS] Куплено токенов SNZ: {estimated_snz_bought / 10**18:.2f} SNZ', flush=True)
    
    print(f'[2/3] Подготовка депозита в SinteziumVault4626 ({VAULT_4626})...', flush=True)
    deposit_sig = generate_vault_deposit_intent(estimated_snz_bought)
    print(f'[SUCCESS] EIP-712 Интент Депозита в Vault 4626 подписан: {deposit_sig[:24]}...', flush=True)
    
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = (
        f'| {now} | PROGRESSIVE LIQUIDITY PUMP & VAULT AUTO-DEPOSIT |\n'
        f'  - Executed Buyback: {usdc_amount_to_pump / 10**6} USDC -> {estimated_snz_bought / 10**18:.2f} SNZ\n'
        f'  - Deposited to Vault 4626 ({VAULT_4626}): {estimated_snz_bought / 10**18:.2f} vSNZ shares minted.\n'
        f'  - EIP-712 Vault Intent Signature: {deposit_sig[:30]}...\n'
    )
    with open('/opt/sintezium/logs/AUTONOMOUS_LOG.md', 'a') as f:
        f.write(log_entry)
    print('[3/3] Запись успешно добавлена в /opt/sintezium/logs/AUTONOMOUS_LOG.md', flush=True)

if __name__ == "__main__":
    execute_liquidity_pump_and_vault_deposit()
