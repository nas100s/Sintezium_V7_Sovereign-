import os, time, json, datetime
from web3 import Web3
from dotenv import load_dotenv

load_dotenv('/opt/sintezium/core/.env')

print('\n' + '='*80)
print('  🔄 SINTEZIUM V7: LEGACY -> PREMIUM SNZ TOKEN UNIFICATION & MIGRATOR')
print('='*80 + '\n')

FOUNDER_WALLET = Web3.to_checksum_address('0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC')
PRIVATE_KEY = os.getenv('OWNER_PRIVATE_KEY') or os.getenv('PAYMASTER_KEY') or os.getenv('PRIVATE_KEY')

LEGACY_SNZ_TOKEN = Web3.to_checksum_address('0x2E32CCE1b65a4bd0f5375bEa97CAb87596e62e92')
PREMIUM_SNZ_TOKEN = Web3.to_checksum_address('0xAfF9205ebD024ADc92fDe128ba29080266057A0A')
ETHEREUM_VAULT_ADDR = Web3.to_checksum_address('0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC')

POLYGON_RPC = os.getenv('POLYGON_RPC', 'https://polygon.drpc.org')
w3 = Web3(Web3.HTTPProvider(POLYGON_RPC))

ERC20_ABI = [{"inputs": [{"name": "account", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}]

def run_legacy_to_premium_unification():
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f'[{now_str}] === СТАРТ АЛГОРИТМА ОБЪЕДИНЕНИЯ LEGACY И PREMIUM SNZ ===\n')

    print('[1/4] 🔍 АНАЛИЗ И ВАЛИДАЦИЯ БАЛАНСОВ ОБОИХ ТОКЕНОВ:')
    try:
        legacy_contract = w3.eth.contract(address=LEGACY_SNZ_TOKEN, abi=ERC20_ABI)
        premium_contract = w3.eth.contract(address=PREMIUM_SNZ_TOKEN, abi=ERC20_ABI)
        legacy_bal = legacy_contract.functions.balanceOf(FOUNDER_WALLET).call() / 10**18
        premium_bal = premium_contract.functions.balanceOf(FOUNDER_WALLET).call() / 10**18
        
        print(f'      - Legacy SNZ  ({LEGACY_SNZ_TOKEN}): {legacy_bal:,.2f} SNZ')
        print(f'      - Premium SNZ ({PREMIUM_SNZ_TOKEN}): {premium_bal:,.2f} SNZ\n')
    except Exception as e: print(f'      [NOTICE] RPC Анализ: {e}\n')

    print('[2/4] 📜 РАЗРАБОТКА СМАРТ-КОНТРАКТА 1:1 МИГРАЦИИ (Sintezium_Token_Migrator.sol):')
    migrator_file = '/opt/sintezium/defi_core/Sintezium_Token_Migrator.sol'
    os.makedirs('/opt/sintezium/defi_core', exist_ok=True)
    migrator_code = """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20 {
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    function transfer(address recipient, uint256 amount) external returns (bool);
}

contract Sintezium_Token_Migrator {
    address public legacySNZ = 0x2E32CCE1b65a4bd0f5375bEa97CAb87596e62e92;
    address public premiumSNZ = 0xAfF9205ebD024ADc92fDe128ba29080266057A0A;
    address public owner = 0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC;

    function migrate(uint256 amount) external {
        require(IERC20(legacySNZ).transferFrom(msg.sender, address(this), amount), "Transfer failed");
        require(IERC20(premiumSNZ).transfer(msg.sender, amount), "Premium failed");
    }
}
"""
    with open(migrator_file, 'w', encoding='utf-8') as f: f.write(migrator_code)
    print(f'      - Контракт миграции готов: {migrator_file}\n')

    print('[3/4] ⚙️ ОБНОВЛЕНИЕ CORE CONFIG С УЧЕТОМ PREMIUM SNZ (0xAfF9...7A0A):')
    config_path = '/opt/sintezium/configs/settings.json'
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f: cfg = json.load(f)
    else: cfg = {}
        
    cfg['legacy_snz_token'] = LEGACY_SNZ_TOKEN
    cfg['premium_snz_token'] = PREMIUM_SNZ_TOKEN
    cfg['primary_omnichain_token'] = PREMIUM_SNZ_TOKEN
    cfg['migrator_contract_status'] = 'READY_1_TO_1'
    
    with open(config_path, 'w', encoding='utf-8') as f: json.dump(cfg, f, indent=2)
    print(f'      - Первичным Omnichain-токеном назначен: {cfg["primary_omnichain_token"]}\n')

    log_entry = f'[{now_str}] UNIFICATION ALGORITHM EXECUTED: Legacy -> Premium ({PREMIUM_SNZ_TOKEN})\n'
    os.makedirs('/opt/sintezium/logs', exist_ok=True)
    with open('/opt/sintezium/logs/AUTONOMOUS_LOG.md', 'a', encoding='utf-8') as f: f.write(log_entry)

    print('='*80)
    print('  📌 АЛГОРИТМ ОБЪЕДИНЕНИЯ LEGACY -> PREMIUM SNZ УСПЕШНО СФОРМИРОВАН!')
    print('='*80 + '\n')

if __name__ == "__main__":
    run_legacy_to_premium_unification()
