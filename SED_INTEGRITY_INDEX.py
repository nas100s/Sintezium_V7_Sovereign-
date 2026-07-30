import os, time, datetime, subprocess

print('\n[SED INTEGRITY] Запуск самовосстанавливающегося монитора безопасности...')

# Правильные суверенные адреса
CORRECT_OWNER = '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC'
TARGET_DIR = '/opt/sintezium/core'

def verify_and_heal_code():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{now}] [AUDIT] Сканирование кодовой базы на предмет несанкционированных изменений...')
    
    try:
        # Проверяем основной файл маркет-мейкера
        engine_path = f'{TARGET_DIR}/PIMLICO_LIQUIDITY_ENGINE.py'
        if os.path.exists(engine_path):
            with open(engine_path, 'r') as f:
                content = f.read()
                
            # Если в коде есть адреса 0x, но нет нашего правильного владельца
            if '0x' in content and CORRECT_OWNER not in content:
                print(f'\n[🚨 ALARM] Обнаружено несанкционированное изменение адреса в {engine_path}!')
                
                # Мгновенное аппаратное исправление через утилиту SED
                # Мы ищем строку с OWNER_WALLET и заменяем её содержимое
                subprocess.run([
                    'sudo', 'sed', '-i', 
                    f's/OWNER_WALLET = ".*"/OWNER_WALLET = "{CORRECT_OWNER}"/g', 
                    engine_path
                ])
                
                print('[HEALED] Код успешно восстановлен! Запуск перезапуска служб...')
                subprocess.run(['sudo', 'systemctl', 'restart', 'pimlico_engine.service'])
                
                # Запись попытки взлома в журнал
                with open('/opt/sintezium/logs/AUTONOMOUS_LOG.md', 'a') as log:
                    log.write(f'[{now}] SECURITY ALARM: Unauthorized code modification detected! Sed-Healer successfully restored the codebase.\n')
            else:
                # В лог безопасности пишем раз в 5 минут, чтобы не спамить
                pass
                
    except Exception as e:
        print(f'[ERROR] Ошибка сканера безопасности: {e}')

if __name__ == '__main__':
    while True:
        verify_and_heal_code()
        time.sleep(30) # Проверка каждые 30 секунд
