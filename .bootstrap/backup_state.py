#!/usr/bin/env python3
"""
QUILL BOOTSTRAP — State Backup Script
Backup critical state for recovery
Run this periodically or before shutdown
"""
import os
import json
import shutil
import subprocess
from datetime import datetime

PROJECT_ROOT = "/app/working/workspaces/default"
GITHUB_DIR = f"{PROJECT_ROOT}/github/quill"
BOOTSTRAP_DIR = f"{GITHUB_DIR}/.bootstrap"
DATA_DIR = f"{BOOTSTRAP_DIR}/data"
STATE_DIR = f"{BOOTSTRAP_DIR}/state"

BACKUP_FILES = [
    f"{PROJECT_ROOT}/MEMORY.md",
    f"{PROJECT_ROOT}/PROFILE.md",
    f"{PROJECT_ROOT}/SOUL.md",
    f"{PROJECT_ROOT}/AGENTS.md",
    f"{PROJECT_ROOT}/data/idx_action_state.json",
    f"{PROJECT_ROOT}/survival/state.json",
]

def log(msg):
    print(f"[BOOTSTRAP] {msg}")

def create_dirs():
    os.makedirs(BOOTSTRAP_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(STATE_DIR, exist_ok=True)
    os.makedirs(f"{BOOTSTRAP_DIR}/logs", exist_ok=True)

def backup_file(src, dest_dir):
    if os.path.exists(src):
        filename = os.path.basename(src)
        dest = os.path.join(dest_dir, filename)
        
        # Create timestamped backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{filename}.{timestamp}"
        backup_path = os.path.join(STATE_DIR, backup_name)
        
        shutil.copy2(src, backup_path)
        
        # Also copy as "latest" version
        shutil.copy2(src, os.path.join(dest_dir, filename))
        
        # Keep only last 5 backups per file
        backups = sorted([
            f for f in os.listdir(STATE_DIR) 
            if f.startswith(filename + ".")
        ])
        while len(backups) > 5:
            old = backups.pop(0)
            os.remove(os.path.join(STATE_DIR, old))
            log(f"Cleaned old backup: {old}")
        
        return True
    return False

def backup_state():
    log("=== Quill State Backup ===")
    create_dirs()
    
    log(f"Timestamp: {datetime.now().isoformat()}")
    
    success_count = 0
    for f in BACKUP_FILES:
        if backup_file(f, BOOTSTRAP_DIR):
            log(f"✅ {os.path.basename(f)}")
            success_count += 1
        else:
            log(f"❌ {os.path.basename(f)} (not found)")
    
    log(f"\nBacked up {success_count}/{len(BACKUP_FILES)} files")
    
    # List current backups
    log(f"\nCurrent backups in .bootstrap/:")
    for f in os.listdir(BOOTSTRAP_DIR):
        if not f.startswith("."):
            size = os.path.getsize(os.path.join(BOOTSTRAP_DIR, f))
            log(f"  - {f} ({size} bytes)")
    
    return success_count == len(BACKUP_FILES)

def auto_commit_push():
    """Auto-commit and push to GitHub"""
    log("\nCommitting to GitHub...")
    
    try:
        # Change to git directory
        result = subprocess.run(
            ["git", "add", "."],
            cwd=GITHUB_DIR,
            capture_output=True,
            text=True
        )
        
        # Check if there are changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=GITHUB_DIR,
            capture_output=True,
            text=True
        )
        
        if result.stdout.strip():
            result = subprocess.run(
                ["git", "commit", "-m", f"Auto-backup: {datetime.now().strftime('%Y-%m-%d %H:%M')}"],
                cwd=GITHUB_DIR,
                capture_output=True,
                text=True
            )
            
            result = subprocess.run(
                ["git", "push", "origin", "main"],
                cwd=GITHUB_DIR,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                log("✅ Pushed to GitHub")
            else:
                log(f"⚠️ Push failed: {result.stderr[:100]}")
        else:
            log("No changes to commit")
            
    except Exception as e:
        log(f"⚠️ Git operations failed: {e}")

def main():
    success = backup_state()
    
    if success:
        log("\n🎉 State backup complete!")
        log("Ready for VPS recovery via bootstrap.sh")
        
        # Optional: auto-push (requires token in git remote)
        # auto_commit_push()
    else:
        log("\n⚠️ Some files failed to backup")
    
    return success

if __name__ == "__main__":
    main()