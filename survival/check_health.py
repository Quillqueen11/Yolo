#!/usr/bin/env python3
"""
SURVIVAL MODE — Health Check v3.1 (Fast Timeout)
"""
import os, json, subprocess
from datetime import datetime

SURVIVAL_DIR = "/app/working/workspaces/default/survival"
STATE_FILE = f"{SURVIVAL_DIR}/state.json"
API_TIMEOUT = 8  # Fast timeout — if API slow, consider down

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f: return json.load(f)
    return {}

def save_state(s):
    with open(STATE_FILE, "w") as f: json.dump(s, f, indent=2)

def check_api():
    """Fast API check with single attempt"""
    try:
        r = subprocess.run(
            ["python3", "-c", """
import sys; sys.path.insert(0,'/app/venv/lib/python3.12/site-packages')
from curl_cffi import requests
r = requests.get('https://ai.sumopod.com/v1/models', impersonate='chrome', timeout=5)
print('OK' if r.status_code else 'FAIL')
"""],
            capture_output=True, text=True, timeout=API_TIMEOUT
        )
        return "OK" in r.stdout
    except:
        return False

def check_tools():
    for t in ["python3", "node", "curl"]:
        if subprocess.run(["which", t], capture_output=True).returncode != 0:
            return False
    return True

def check_storage():
    r = subprocess.run(["df", "-h", "."], capture_output=True, text=True)
    parts = r.stdout.strip().split("\n")[-1].split()
    return parts[4] if len(parts) > 4 else "?"

def main():
    print("=== Survival Health Check ===")
    state = load_state()
    
    api_ok = check_api()
    tools_ok = check_tools()
    storage = check_storage()
    
    print(f"AI API:      {'✅ OK' if api_ok else '❌ DOWN'}")
    print(f"Local tools: {'✅ OK' if tools_ok else '❌ FAIL'}")
    print(f"Disk used:   {storage}")
    
    # Determine level — tools_ok is minimum requirement
    if api_ok and tools_ok:
        level, mode = "L1", "FULL"
    elif tools_ok:
        level, mode = "L3", "LOCAL_ONLY"  # API down but local works
    else:
        level, mode = "L4", "EMERGENCY"
    
    old = state.get("level", "?")
    
    state.update({
        "level": level,
        "operational_mode": mode,
        "last_check": datetime.now().isoformat(),
        "api_ok": api_ok,
        "tools_ok": tools_ok,
        "storage": storage
    })
    save_state(state)
    
    if level != old:
        print(f"⚠️ {old} → {level}")
    
    print(f"=== Status: {level} ===")
    return level in ["L1", "L3"]  # L3 is valid

if __name__ == "__main__":
    main()