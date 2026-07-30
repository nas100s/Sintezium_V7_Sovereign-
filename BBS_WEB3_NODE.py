import socket, threading, time, datetime
from web3 import Web3

print('\n[BBS NODE] Обновление: Внедрение Real-Tech верификации Web3...')

# Конфигурация Arbitrum
ARBITRUM_RPC = 'https://arb1.arbitrum.io/rpc'
USDC_CONTRACT = '0xaf88d065e77c8cC2239327C5EDb3A432268e5831' # Native USDC on Arbitrum
MASTER_WALLET = '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC'

w3 = Web3(Web3.HTTPProvider(ARBITRUM_RPC))

ASCII_ART = '''
===================================================
  ____  _____ _   _ _____ _____ _________  _   _ 
 / ___||_   _| \ | |_   _| ____|__  / _ _| | | |
 \___ \  | | |  \| | | | |  _|   / / | | | | | |
  ___) | | | | |\  | | | | |___ / /| | | |_| | |
 |____/  |_| |_| \_| |_| |_____/____|___|\___/  
       E L E M E N T   1 1 9   N O D E
===================================================
Welcome to Sovereign RWA BBS. Real-Tech Active.
'''

def verify_arbitrum_usdc_payment(tx_hash):
    try:
        # Проверка статуса транзакции
        tx = w3.eth.get_transaction_receipt(tx_hash)
        if tx is None:
            return False, 'Transaction not found.'
        if tx['status'] != 1:
            return False, 'Transaction failed in blockchain.'

        # Анализ логов (Transfer event)
        # Topic 0: keccak('Transfer(address,address,uint256)')
        # Topic 1: from (indexed)
        # Topic 2: to (indexed)
        transfer_topic = '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC63c4a11628f55a4df523b3ef'
        
        for log in tx['logs']:
            if log['address'].lower() == USDC_CONTRACT.lower():
                if log['topics'][0].hex() == transfer_topic:
                    # Проверяем получателя (Master Wallet)
                    to_address = '0x' + log['topics'][2].hex()[-40:]
                    if to_address.lower() == MASTER_WALLET.lower():
                        # Проверяем сумму (6 знаков после запятой для USDC)
                        amount = int(log['data'].hex(), 16) / 10**6
                        if amount >= 50.0:
                            return True, f'Confirmed {amount} USDC'
        
        return False, 'Payment to target wallet not found or amount insufficient.'
    except Exception as e:
        return False, f'Error: {str(e)}'

def handle_client(client_socket, address):
    try:
        client_socket.sendall(ASCII_ART.encode('utf-8'))
        client_socket.sendall(b'\nSYSTEM: Alibaba 25k Geodetic Report Vault.\n')
        client_socket.sendall(b'1. Read Manifesto\n2. Purchase RWA Access (50 USDC via Arbitrum)\n')
        client_socket.sendall(b'Select option (1/2): ')

        data = client_socket.recv(1024).decode('utf-8').strip()
        
        if data == '1':
            client_socket.sendall(b'\n[MANDATE] Real-Tech Sovereign Liquidity. Zero-Gas driven.\nDisconnected.\n')
        elif data == '2':
            client_socket.sendall(b'\n[REAL-TECH PAYMENT] Send 50 USDC on Arbitrum to:\n')
            client_socket.sendall(f'ADDR: {MASTER_WALLET}\n'.encode('utf-8'))
            client_socket.sendall(b'Paste your Arbitrum TX Hash (0x...) to unlock: ')
            
            tx_hash = client_socket.recv(1024).decode('utf-8').strip()
            
            if len(tx_hash) == 66 and tx_hash.startswith('0x'):
                client_socket.sendall(b'\n[VERIFYING ON-CHAIN...] Connecting to Arbitrum node...\n')
                
                success, message = verify_arbitrum_usdc_payment(tx_hash)
                
                if success:
                    client_socket.sendall(f'[SUCCESS] {message}. RWA Access Granted!\n'.encode('utf-8'))
                    client_socket.sendall(b'RWA Data Link: https://storage.googleapis.com/sreda/MCAR/secure_asset.zip\n')
                    
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    with open('/opt/sintezium/logs/AUTONOMOUS_LOG.md', 'a') as f:
                        f.write(f'[{now}] REAL BBS PAYMENT: TX {tx_hash} verified. {message}. Access granted to {address[0]}.\n')
                else:
                    client_socket.sendall(f'\n[VERIFICATION FAILED] {message}\n'.encode('utf-8'))
            else:
                client_socket.sendall(b'\n[ERROR] Invalid TX Hash format. Connection terminated.\n')
        else:
            client_socket.sendall(b'\n[ERROR] Unknown command.\n')
            
    except Exception as e:
        pass
    finally:
        client_socket.close()

def start_bbs_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 1995))
    server.listen(5)
    print('[BBS NODE] Терминал слушает входящие подключения...')
    
    while True:
        client_sock, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_sock, addr))
        client_handler.start()

if __name__ == '__main__':
    start_bbs_server()
