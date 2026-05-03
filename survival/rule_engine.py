#!/usr/bin/env python3
"""
SURVIVAL MODE — Rule Engine v3.1 (Fast)
"""
import json, os, subprocess
from datetime import datetime

SURVIVAL_DIR = "/app/working/workspaces/default/survival"
STATE_FILE = f"{SURVIVAL_DIR}/state.json"

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f: return json.load(f)
    return {}

def save_state(s):
    with open(STATE_FILE, "w") as f: json.dump(s, f, indent=2)

def check_api():
    try:
        r = subprocess.run(
            ["python3", "-c", """
import sys; sys.path.insert(0,'/app/venv/lib/python3.12/site-packages')
from curl_cffi import requests
r = requests.get('https://ai.sumopod.com/v1/models', impersonate='chrome', timeout=5)
print('OK' if r.status_code else 'FAIL')
"""],
            capture_output=True, text=True, timeout=8
        )
        return "OK" in r.stdout
    except:
        return False

def main():
    print("=== Rule Engine ===")
    state = load_state()
    
    api_ok = check_api()
    tools_ok = all(subprocess.run(["which", t], capture_output=True).returncode == 0 
                   for t in ["python3", "node", "curl"])
    
    print(f"API:   {'✅ OK' if api_ok else '❌ DOWN'}")
    print(f"Tools: {'✅ OK' if tools_ok else '❌ FAIL'}")
    
    if api_ok and tools_ok:
        state["level"] = "L1"
        state["operational_mode"] = "FULL"
        state["api_ok"] = True
        print("✅ FULL operation")
    elif tools_ok:
        state["level"] = "L3"
        state["operational_mode"] = "LOCAL_ONLY"
        state["api_ok"] = False
        print("⚠️ L3 LOCAL_ONLY")
    else:
        state["level"] = "L4"
        state["operational_mode"] = "EMERGENCY"
        state["api_ok"] = False
        print("🚨 L4 EMERGENCY")
    
    save_state(state)
    print(f"=== Done: {state['level']} ===")

if __name__ == "__main__":
    main()