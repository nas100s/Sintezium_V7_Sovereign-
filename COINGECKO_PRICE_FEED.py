import requests, os
print('[COINGECKO] Получение цен на золото и активы...')
try:
    api_key = os.getenv('COINGECKO_DEMO_API_KEY', '')
    url = f'https://api.coingecko.com/api/v3/simple/price?ids=gold,ethereum,matic-network&vs_currencies=usd&x_cg_demo_api_key={api_key}'
    res = requests.get(url).json()
    print(f'[DATA] Текущие котировки: {res}')
except Exception as e:
    print(f'[ERROR] Оракул CoinGecko недоступен: {e}')
