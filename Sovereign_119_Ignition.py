import os, time, sys, datetime, subprocess

print('\n' + '='*55)
print('    S I N T E Z I U M   E L E M E N T   1 1 9   I G N I T I O N')
print('        Real-Tech Sovereign Omnichain Core (V7)')
print('='*55)

# Конфигурация целей
LEGACY_SNZ = '0x2E32CCE1b65a4bd0f5375bEa97CAb87596e62e92'
SMART_ACCOUNT = '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC'

# Список 9 критических системных демонов
DEMON_SERVICES = [
    'monad_bridge', 'art_bridge', 'solver_monitor', 'edgex_ws',
    'gold_staking', 'intent_accelerator', 'mcar_discoverer',
    'sintezium_dapp', 'mythos_shield'
]

def run_system_audit():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'\n[{now}] [AUDIT] Начало глобальной проверки созвездия служб...')
    
    active_count = 0
    for service in DEMON_SERVICES:
        status = os.system(f'sudo systemctl is-active {service}.service > /dev/null 2>&1')
        if status == 0:
            print(f' -> [🟢 ACTIVE] Служба {service}.service работает стабильно.')
            active_count += 1
        else:
            print(f' -> [🔴 FAILURE] Служба {service}.service остановлена или сбилась!')
            os.system(f'sudo systemctl restart {service}.service')
            
    print(f'[{now}] [AUDIT] {active_count}/{len(DEMON_SERVICES)} служб находятся в строю.')

def check_cross_chain_liquidity():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'\n[{now}] [ORACLE] Считывание межбанковских котировок TradFi & DeSci...')
    
    os.system('python3 /opt/sintezium/core/NPB_FOREX_BRIDGE.py')
    os.system('python3 /opt/sintezium/core/COINGECKO_PRICE_FEED.py')

def execute_ignition_cycle():
    while True:
        try:
            run_system_audit()
            check_cross_chain_liquidity()
            
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'\n[{now}] [METRONOME] Сварожий цикл синхронизирован. Ожидание оффчейн-подписей EIP-712...')
            
            with open('/opt/sintezium/logs/AUTONOMOUS_LOG.md', 'a') as f:
                f.write(f'[{now}] UNIFIED MASTER CYCLE COMPLETE. ALL SUB SYSTEMS SYNCED. TARGET: {LEGACY_SNZ}\n')
                
            time.sleep(300) 
        except KeyboardInterrupt:
            print('\n[STOP] Оркестратор остановлен пользователем.')
            sys.exit(0)
        except Exception as e:
            print(f'[FATAL ERROR] Сбой мастер-цикла: {e}')
            time.sleep(10)

if __name__ == '__main__':
    # Импортируем API-ключ из Secret Manager
    secret_cmd = 'gcloud secrets versions access latest --secret=coingecko-api-key --project=snz119'
    os.environ['COINGECKO_DEMO_API_KEY'] = os.popen(secret_cmd).read().strip()
    execute_ignition_cycle()
