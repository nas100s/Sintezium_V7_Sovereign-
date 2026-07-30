import os, json, datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from web3 import Web3
from eth_account.messages import encode_typed_data

# Настройка
w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))
SNZ_CONTRACT = '0x2E32CCE1b65a4bd0f5375bEa97CAb87596e62e92'
FRONTEND_DIR = '/opt/sintezium/frontend'

class UnifiedHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def do_POST(self):
        if self.path == '/api/v1/stake':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                message = data.get('message')
                signature = data.get('signature')
                user_address = Web3.to_checksum_address(message['user'])
                amount = message['amount']

                domain_data = {'name': 'Sintezium Vault', 'version': '1', 'chainId': 137, 'verifyingContract': SNZ_CONTRACT}
                message_types = {'Stake': [{'name': 'user', 'type': 'address'}, {'name': 'amount', 'type': 'uint256'}, {'name': 'nonce', 'type': 'uint256'}]}
                signable_bytes = encode_typed_data(domain_data=domain_data, message_types=message_types, message_data=message)
                recovered_address = w3.eth.account.recover_message(signable_bytes, signature=signature)

                if recovered_address == user_address:
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    with open('/opt/sintezium/logs/AUTONOMOUS_LOG.md', 'a') as f:
                        f.write(f'[{now}] VAULT LOCK: {user_address} locked {amount} SNZ via SafePal (Unified).\n')
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'Success', 'user': user_address}).encode('utf-8'))
                else:
                    self.send_error(401, 'Invalid signature')
            except Exception as e:
                self.send_error(400, str(e))
        else:
            self.send_error(404)

if __name__ == '__main__':
    os.chdir(FRONTEND_DIR)
    server = HTTPServer(('0.0.0.0', 80), UnifiedHandler)
    print('[SERVER] Единый SafePal-совместимый веб-сервер запущен на порту 80')
    server.serve_forever()
