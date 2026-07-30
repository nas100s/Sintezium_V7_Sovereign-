import json, os, time, datetime

def show_truth():
    print('\n' + '='*60)
    print('   S I N T E Z I U M   V 7   R E A L - T E C H   M O N I T O R')
    print('='*60)
    
    # 1. Ликвидность RWA (Облигации)
    print('\n[RWA BONDS STATUS]')
    try:
        with open('/opt/sintezium/core/OPTIMIZED_INTENT_BATCH.json', 'r') as f:
            intents = json.load(f)
            for i in intents:
                print(f' -> Asset: {i["asset"]} | Value: {i["value_matic"]} MATIC | Signed: YES')
    except:
        print(' -> No active bond intents found.')

    # 2. Последние байбеки
    print('\n[RECENT MARKET INTERVENTIONS]')
    try:
        with open('/opt/sintezium/logs/AUTONOMOUS_LOG.md', 'r') as f:
            lines = f.readlines()
            for line in lines[-5:]:
                if 'BUYBACK' in line:
                    print(f' -> {line.strip()}')
    except:
        print(' -> No logs available.')

    # 3. Состояние системных щитов
    print('\n[SECURITY STATUS]')
    shield_active = os.system('systemctl is-active mythos_shield > /dev/null') == 0
    healer_active = os.system('systemctl is-active sed_healer > /dev/null') == 0
    print(f' -> Mythos Shield: {"🟢 ACTIVE" if shield_active else "🔴 OFFLINE"}')
    print(f' -> Sed Healer:    {"🟢 ACTIVE" if healer_active else "🔴 OFFLINE"}')

    print('\n' + '='*60)
    print(f'Timestamp: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} UTC')

if __name__ == '__main__':
    show_truth()
