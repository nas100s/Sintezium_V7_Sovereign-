import os, json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv('/opt/sintezium/core/.env')
RPC_URL = os.getenv('RPC_URL_PRIVATE', 'https://polygon-rpc.com')
w3 = Web3(Web3.HTTPProvider(RPC_URL))

PAIR_ADDR = '0xeeD334A4537d0942520167E33F173b42eB1dd994'
SNZ_TOKEN = '0xd840bbd18d120631bf2bca65de6d3581b759a6c5'

PAIR_ABI = [
    {'constant': True, 'inputs': [], 'name': 'getReserves', 'outputs': [{'name': '_reserve0', 'type': 'uint112'}, {'name': '_reserve1', 'type': 'uint112'}, {'name': '_blockTimestampLast', 'type': 'uint32'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'},
    {'constant': True, 'inputs': [], 'name': 'token0', 'outputs': [{'name': '', 'type': 'address'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}
]

def get_market_truth():
    pair_contract = w3.eth.contract(address=Web3.to_checksum_address(PAIR_ADDR), abi=PAIR_ABI)
    token0 = pair_contract.functions.token0().call()
    reserves = pair_contract.functions.getReserves().call()
    
    res_pol, res_snz = (reserves[0], reserves[1]) if token0.lower() != SNZ_TOKEN.lower() else (reserves[1], reserves[0])
    
    price = (res_pol / 10**18) / (res_snz / 10**18)
    print(f'\n[MARKET TRUTH] Цена: {price:.8f} POL/SNZ | Ликвидность: {res_pol/10**18:.2f} POL')

if __name__ == '__main__':
    get_market_truth()
