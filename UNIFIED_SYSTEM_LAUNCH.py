import subprocess
import time
import os
import json

def launch_subsystem(name, command):
    print(f"[SYSTEM] Launching Subsystem: {name}...")
    # Using nohup to keep processes running in background
    return subprocess.Popen(f"nohup python3 {command} > {name}.log 2>&1 &", shell=True)

def main():
    print("=== [UNIFIED SINTEZIUM V7 ORCHESTRATOR] ===")
    print("[MANDATE] Real-Tech / Anti-Theatre / Sovereign")
    
    # 1. Start Liquidity Monitoring & Intervention
    launch_subsystem("Liquidity_Pump", "PROGRESSIVE_LIQUIDITY_PUMP.py")
    
    # 2. Start AntChain Synchronization (Periodic)
    launch_subsystem("AntChain_Sync", "alibaba_antchain_sync_real.py")
    
    # 3. Start Chislobog Time Cycles (Legacy Orchestrator)
    launch_subsystem("Chislobog", "chislobog_orchestrator.py")

    print("[SUCCESS] All systems ignited. Monitoring logs...")
    
    # Initial state snapshot
    state = {
        "timestamp": time.time(),
        "status": "SOVEREIGN_IGNITION",
        "active_subsystems": ["Liquidity_Pump", "AntChain_Sync", "Chislobog"],
        "resonance_target": 1.19
    }
    
    with open("FINAL_SOVEREIGN_STATE.json", "w") as f:
        json.dump(state, f, indent=2)

    # Keep the main process alive for systemd monitoring
    print("[*] Orchestrator is now in persistent monitoring mode.")
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
