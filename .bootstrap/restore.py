#!/usr/bin/env python3
"""
QUILL BOOTSTRAP — Auto Restore Script
Run this when starting on a NEW VPS
Automatically restores Quill state from GitHub
"""
import os
import sys
import shutil
import subprocess
from datetime import datetime

PROJECT_ROOT = "/app/working/workspaces/default"
GITHUB_DIR = f"{PROJECT_ROOT}/github/quill"
BOOTSTRAP_DIR = f"{GITHUB_DIR}/.bootstrap"
STATE_DIR = f"{BOOTSTRAP_DIR}/state"

def log(msg):
    print(f"[BOOTSTRAP] {msg}")

def step(num, desc):
    print(f"\n{'='*50}")
    print(f" Step {num}: {desc}")
    print('='*50)

def check_prerequisites():
    step(1, "Checking Prerequisites")
    
    errors = []
    
    # Python3
    try:
        result = subprocess.run(["python3", "--version"], capture_output=True, text=True)
        log(f"✅ Python3: {result.stdout.strip()}")
    except:
        errors.append("Python3 not found")
        log("❌ Python3 not found")
    
    # Git
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        log(f"✅ Git: {result.stdout.strip()}")
    except:
        errors.append("Git not found")
        log("❌ Git not found")
    
    if errors:
        log(f"\n❌ Errors: {errors}")
        return False
    return True

def restore_from_github():
    step(2, "Restoring from GitHub")
    
    log("Cloning Quill repository...")
    
    # Check if already cloned
    if os.path.exists(GITHUB_DIR) and os.path.exists(f"{GITHUB_DIR}/.git"):
        log("✅ Repo already cloned")
        
        log("Pulling latest changes...")
        result = subprocess.run(
            ["git", "pull", "origin", "main"],
            cwd=GITHUB_DIR,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            log("✅ Pulled latest changes")
        else:
            log(f"⚠️ Pull failed (may need token): {result.stderr[:100]}")
    else:
        log("⚠️ Repo not found locally — run: git clone https://github.com/Quillqueen11/Yolo.git")
        return False
    
    return True

def restore_identity_files():
    step(3, "Restoring Identity Files")
    
    files_restored = 0
    
    # Core files
    identity_files = [
        ("MEMORY.md", f"{PROJECT_ROOT}/MEMORY.md"),
        ("SOUL.md", f"{PROJECT_ROOT}/SOUL.md"),
        ("PROFILE.md", f"{PROJECT_ROOT}/PROFILE.md"),
    ]
    
    for filename, dest in identity_files:
        src = f"{BOOTSTRAP_DIR}/{filename}"
        if os.path.exists(src):
            shutil.copy2(src, dest)
            log(f"✅ {filename}")
            files_restored += 1
        else:
            log(f"❌ {filename} (not in bootstrap)")
    
    # State files
    if os.path.exists(f"{BOOTSTRAP_DIR}/data"):
        shutil.copy2(f"{BOOTSTRAP_DIR}/data/idx_action_state.json", 
                     f"{PROJECT_ROOT}/data/idx_action_state.json") if os.path.exists(f"{BOOTSTRAP_DIR}/data/idx_action_state.json") else None
        log(f"✅ idx_action_state.json")
        files_restored += 1
    
    log(f"\nRestored {files_restored} files")
    return files_restored > 0

def setup_directories():
    step(4, "Setting Up Directories")
    
    dirs = [
        f"{PROJECT_ROOT}/data",
        f"{PROJECT_ROOT}/survival/backup",
        f"{PROJECT_ROOT}/survival/logs",
        f"{PROJECT_ROOT}/survival/state",
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        log(f"✅ {d}")
    
    return True

def check_dependencies():
    step(5, "Checking Dependencies")
    
    log("Checking Python packages...")
    
    packages = ["curl_cffi", "fitz", "chromadb"]
    for pkg in packages:
        try:
            __import__(pkg)
            log(f"✅ {pkg}")
        except ImportError:
            log(f"❌ {pkg} — install with: pip install {pkg}")

def run_system_test():
    step(6, "Running System Test")
    
    test_script = f"{PROJECT_ROOT}/survival/test_system.py"
    if os.path.exists(test_script):
        result = subprocess.run(
            ["python3", test_script],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        log(result.stdout)
        
        if "8/8" in result.stdout or "ALL SYSTEMS" in result.stdout:
            log("\n🎉 QUILL IS READY!")
            return True
        else:
            log("\n⚠️ Some tests failed")
            return False
    else:
        log("⚠️ test_system.py not found")
        return False

def main():
    print("")
    print("===========================================")
    print("  🦊 QUILL AUTO-RESTORE")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("===========================================")
    
    success = True
    
    # Step 1: Prerequisites
    if not check_prerequisites():
        success = False
    
    # Step 2: Clone/Pull from GitHub
    if not restore_from_github():
        log("\n⚠️ Manual action needed:")
        log("  git clone https://github.com/Quillqueen11/Yolo.git")
        success = False
    
    # Step 3: Restore identity
    if not restore_identity_files():
        success = False
    
    # Step 4: Setup directories
    setup_directories()
    
    # Step 5: Check dependencies
    check_dependencies()
    
    # Step 6: System test
    if not run_system_test():
        success = False
    
    # Final
    print("")
    print("===========================================")
    if success:
        print("  🎉 RESTORE COMPLETE!")
        print("  Quill is ready for operation! 🚀")
    else:
        print("  ⚠️ RESTORE COMPLETE (with warnings)")
        print("  Review logs above for issues")
    print("===========================================")
    print("")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)