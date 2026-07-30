import os, datetime
from google.cloud import kms
from web3 import Web3

print('\n[KMS HSM SIGNER] Инициализация аппаратного подписанта Google Cloud...', flush=True)

# Инициализируем клиент KMS
client = kms.KeyManagementServiceClient()

# Полный путь к вашему аппаратному ключу в Google Cloud
KEY_NAME = client.crypto_key_path('snz119', 'europe-west3', 'sintezium-hsm-ring', 'paymaster-hsm-key')

def sign_hash_with_hsm(digest_hash_bytes):
    print(f'[KMS API] Отправка хэша транзакции внутрь чипа HSM во Франкфурте...', flush=True)
    
    # Формируем структуру запроса к HSM
    digest = kms.Digest(sha256=digest_hash_bytes)
    
    # Запрос на асимметричную подпись
    response = client.asymmetric_sign(
        name=KEY_NAME,
        digest=digest
    )
    
    print('[SUCCESS] Подпись успешно сгенерирована аппаратным чипом Google!', flush=True)
    # Возвращаем готовую сигнатуру подписи
    return response.signature

if __name__ == '__main__':
    # Пример: Тестовый хэш транзакции выкупа (32 байта)
    test_hash = Web3.keccak(text='Sintezium_V7_HSM_Test_2026')
    
    try:
        signature = sign_hash_with_hsm(test_hash)
        print(f' -> Аппаратная подпись (Hex): {signature.hex()[:40]}...', flush=True)
        
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('/opt/sintezium/logs/AUTONOMOUS_LOG.md', 'a') as f:
            f.write(f'[{now}] KMS HSM SIGNATURE GENERATED. Key: paymaster-hsm-key\n')
            
    except Exception as e:
        print(f'[KMS ERROR] Сбой аппаратной подписи: {e}', flush=True)
