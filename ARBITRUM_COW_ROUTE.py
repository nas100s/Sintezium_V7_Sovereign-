import os, time, requests, datetime
from web3 import Web3
from eth_account.messages import encode_typed_data
from dotenv import load_dotenv

# Load environment
load_dotenv('/opt/sintezium/core/.env')

# Arbitrum CoW Swap Production API Endpoint
COW_SWAP_API_URL = "https://api.cow.fi/api/v1/orders"

OWNER_WALLET = '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC'
PRIVATE_KEY = os.getenv('PAYMASTER_KEY')

# Токен SNZ на Polygon и WETH на Arbitrum
SNZ_POLYGON = '0xd840bbd18d120631bf2bcA65de6d3581b759a6c5'
WETH_ARBITRUM = '0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC'

w3 = Web3()

def deploy_real_arbitrum_intent():
    print('[ARBITRUM] Формирование реального ордера EIP-712 для CoW Swap...', flush=True)
    
    domain_data = {
        "name": "Gnosis Protocol",
        "version": "v2",
        "chainId": 42161, # Arbitrum One
        "verifyingContract": Web3.to_checksum_address("0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC")
    }

    message_types = {
        "Order": [
            {"name": "sellToken", "type": "address"},
            {"name": "buyToken", "type": "address"},
            {"name": "receiver", "type": "address"},
            {"name": "sellAmount", "type": "uint256"},
            {"name": "buyAmount", "type": "uint256"},
            {"name": "validTo", "type": "uint32"},
            {"name": "appData", "type": "bytes32"},
            {"name": "feeAmount", "type": "uint256"},
            {"name": "kind", "type": "string"},
            {"name": "partiallyFillable", "type": "bool"},
            {"name": "sellTokenBalance", "type": "string"},
            {"name": "buyTokenBalance", "type": "string"}
        ]
    }

    valid_to = int(time.time()) + 86400

    message_data = {
        "sellToken": WETH_ARBITRUM, 
        "buyToken": WETH_ARBITRUM,
        "receiver": OWNER_WALLET,
        "sellAmount": 1000000000000000000,
        "buyAmount": 950000000000000000,
        "validTo": valid_to,
        "appData": w3.solidity_keccak(['string'], ['Sintezium_Element_119_RWA']),
        "feeAmount": 0,
        "kind": "sell",
        "partiallyFillable": False,
        "sellTokenBalance": "erc20",
        "buyTokenBalance": "erc20"
    }

    signable_bytes = encode_typed_data(domain_data=domain_data, message_types=message_types, message_data=message_data)
    signed_message = w3.eth.account.sign_message(signable_bytes, private_key=PRIVATE_KEY)

    order_payload = {
        "sellToken": message_data["sellToken"],
        "buyToken": message_data["buyToken"],
        "receiver": message_data["receiver"],
        "sellAmount": str(message_data["sellAmount"]),
        "buyAmount": str(message_data["buyAmount"]),
        "validTo": message_data["validTo"],
        "appData": message_data["appData"].hex(),
        "feeAmount": str(message_data["feeAmount"]),
        "kind": message_data["kind"],
        "partiallyFillable": message_data["partiallyFillable"],
        "sellTokenBalance": message_data["sellTokenBalance"],
        "buyTokenBalance": message_data["buyTokenBalance"],
        "signingScheme": "eip712",
        "signature": signed_message.signature.hex(),
        "from": OWNER_WALLET
    }

    print(f'[HTTP] Отправка запроса на {COW_SWAP_API_URL}...', flush=True)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(COW_SWAP_API_URL, json=order_payload, headers=headers)
    
    if response.status_code == 201:
        order_uid = response.json()
        print(f'\n[SUCCESS] Ордер на Arbitrum успешно создан!', flush=True)
        with open('/opt/sintezium/logs/AUTONOMOUS_LOG.md', 'a') as f:
            f.write(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] REAL ARBITRUM INTENT DEPLOYED. UID: {order_uid}\n')
    else:
        print(f'\n[ERROR] Arbitrum API отклонил запрос. Код: {response.status_code}', flush=True)

if __name__ == "__main__":
    if not PRIVATE_KEY:
        print("[ERROR] Приватный ключ отсутствует!")
    else:
        deploy_real_arbitrum_intent()
