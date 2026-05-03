#!/usr/bin/env python3
"""
SURVIVAL MODE — Startup & Auto-Recovery
Run on boot or whenever we need to restore operations
"""
import os, json, subprocess
from datetime import datetime

SURVIVAL_DIR = "/app/working/workspaces/default/survival"

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] [SURVIVAL] {msg}")

def check_primary_api():
    try:
        r = subprocess.run(
            ["python3", "-c", """
import sys; sys.path.insert(0,'/app/venv/lib/python3.12/site-packages')
from curl_cffi import requests
r = requests.get('https://ai.sumopod.com/v1/models', impersonate='chrome', timeout=8)
print('OK' if r.status_code else 'FAIL')
"""],
            capture_output=True, text=True, timeout=12
        )
        return "OK" in r.stdout
    except: return False

def check_tools():
    for t in ["python3", "node", "curl"]:
        if subprocess.run(["which", t], capture_output=True).returncode != 0:
            return False
    return True

def ensure_dirs():
    os.makedirs(f"{SURVIVAL_DIR}/logs", exist_ok=True)
    os.makedirs(f"{SURVIVAL_DIR}/backup", exist_ok=True)
    os.makedirs(f"{SURVIVAL_DIR}/state", exist_ok=True)

def run_health_check():
    log("Running health check...")
    subprocess.run(["python3", f"{SURVIVAL_DIR}/check_health.py"])

def run_rule_engine():
    log("Running rule engine...")
    subprocess.run(["python3", f"{SURVIVAL_DIR}/rule_engine.py"])

def check_recovery_needed():
    state_file = f"{SURVIVAL_DIR}/state.json"
    if not os.path.exists(state_file):
        return True
    try:
        with open(state_file) as f:
            state = json.load(f)
        # If last check was > 1 hour ago, recovery needed
        last = state.get("last_check")
        if not last: return True
        from datetime import datetime
        last_time = datetime.fromisoformat(last)
        if (datetime.now() - last_time).seconds > 3600:
            return True
    except: return True
    return False

def main():
    log("=== SURVIVAL MODE STARTUP ===")
    log(f"Timestamp: {datetime.now().isoformat()}")
    
    ensure_dirs()
    
    # Check system status
    log("Checking system...")
    api_ok = check_primary_api()
    tools_ok = check_tools()
    
    log(f"  AI API: {'✅ OK' if api_ok else '❌ DOWN'}")
    log(f"  Tools:  {'✅ OK' if tools_ok else '❌ FAIL'}")
    
    if check_recovery_needed():
        log("⚠️ Recovery needed — running catch-up...")
        run_health_check()
        run_rule_engine()
    else:
        log("✅ System healthy — no recovery needed")
    
    log("=== STARTUP COMPLETE ===")
    
    # Final status
    status = {
        "timestamp": datetime.now().isoformat(),
        "api_status": api_ok,
        "tools_status": tools_ok,
        "survival_dir": SURVIVAL_DIR,
        "ready": tools_ok
    }
    print(json.dumps(status, indent=2))

if __name__ == "__main__":
    main()