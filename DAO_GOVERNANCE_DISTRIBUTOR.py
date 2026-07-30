import os, time, json, datetime
from web3 import Web3
from eth_account.messages import encode_typed_data
from dotenv import load_dotenv
load_dotenv("/opt/sintezium/core/.env")
PRIVATE_KEY = os.getenv("PAYMASTER_KEY")
