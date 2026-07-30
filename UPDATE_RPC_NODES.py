import os, urllib.request, json
from dotenv import load_dotenv

load_dotenv("/opt/sintezium/core/.env")

print("\n[RPC GATEWAY AUTO-REPAIR] Сканирование и восстановление подключения к Polygon RPC...", flush=True)

TEST_RPC_LIST = [
    "https://polygon.drpc.org",
    "https://1rpc.io/matic",
    "https://polygon-bor-rpc.publicnode.com",
    "https://rpc.ankr.com/polygon"
]

def test_rpc_node(url):
    data = json.dumps({"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
    try:
        res = urllib.request.urlopen(req, timeout=5)
        body = json.loads(res.read())
        if "result" in body:
            return True, int(body["result"], 16)
    except Exception as e:
        return False, str(e)
    return False, "Invalid response"

def find_and_save_working_rpc():
    working_rpc = None
    for rpc in TEST_RPC_LIST:
        success, info = test_rpc_node(rpc)
        if success:
            print(f"  [OK] {rpc} -> Блок #{info:,}", flush=True)
            if working_rpc is None:
                working_rpc = rpc
        else:
            print(f"  [FAIL] {rpc} -> {info}", flush=True)
            
    if not working_rpc:
        working_rpc = "https://polygon.drpc.org"

    print(f"\n[SUCCESS] Выбран наилучший рабочий RPC шлюз: {working_rpc}", flush=True)

    env_path = "/opt/sintezium/core/.env"
    lines = []
    found = False
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if line.startswith("POLYGON_RPC="):
            new_lines.append(f"POLYGON_RPC={working_rpc}\n")
            found = True
        else:
            new_lines.append(line)
    
    if not found:
        new_lines.append(f"POLYGON_RPC={working_rpc}\n")
    
    with open(env_path, "w") as f:
        f.writelines(new_lines)
    print(f"[CONFIG UPDATED] Записано: POLYGON_RPC={working_rpc}", flush=True)

if __name__ == "__main__":
    find_and_save_working_rpc()
