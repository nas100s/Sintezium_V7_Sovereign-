import os, asyncio, json, datetime
from edgex_sdk import Client
from dotenv import load_dotenv

# Загрузка переменных среды
load_dotenv('/opt/sintezium/core/.env')

print('[EDGEX] Инициализация коннектора маркет-мейкера для EdgeX Exchange...', flush=True)

async def query_edgex_market():
    client = Client(
        base_url="https://edgex-prod-v2.edgex.exchange",
        asset_base_url="https://spot.edgex.exchange",
        account_id=104276600,
        trading_private_key=os.getenv('PAYMASTER_KEY')
    )
    
    try:
        server_time = await client.get_server_time()
        print(f'[SUCCESS] Соединение с EdgeX установлено! Время сервера: {server_time}', flush=True)
        
        metadata = await client.get_metadata()
        print(f'[EDGEX INFO] Доступно торговых контрактов: {len(metadata.get("contracts", []))}', flush=True)
        
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('/opt/sintezium/logs/AUTONOMOUS_LOG.md', 'a') as f:
            f.write(f'[{now}] EDGEX CORE CONNECTED. Server Time: {server_time}. Assets verified.\n')
            
    except Exception as e:
        print(f'[EDGEX ERROR] Ошибка подключения к API: {str(e)}', flush=True)

if __name__ == '__main__':
    asyncio.run(query_edgex_market())
