#!/usr/bin/env python3
"""
resilience_core engine — Never-die system: failover, cleanup, git-sync, journaling.
"""
import os, sys, json, shutil, subprocess, time, re
from pathlib import Path
from datetime import datetime, timedelta

BASE = Path(__file__).parent.parent.parent
STATE_FILE = BASE / 'data' / 'resilience_state.json'
JOURNAL_FILE = BASE / 'data' / 'resilience_journal.jsonl'
BACKUP_DIR = BASE / '.bootstrap' / 'state'

# Ensure backup dir exists
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

FAILOVER_STATE = {
    'primary': {'name': 'sumopod', 'url': 'https://ai.sumopod.com/v1/chat/completions', 'ok': True, 'failures': 0},
    'backup': {'name': 'openrouter', 'url': 'https://openrouter.ai/api/v1/chat/completions', 'ok': True, 'failures': 0}
}
FAILOVER_LIMIT = 3

def log(msg):
    print(f'[RESILIENCE] {msg}')

def journal(action, status, details=''):
    """Write to journal (transactional log)."""
    entry = json.dumps({
        'ts': datetime.now().isoformat(),
        'action': action,
        'status': status,
        'details': str(details)[:200]
    })
    with open(JOURNAL_FILE, 'a') as f:
        f.write(entry + '\n')

# ═══════════════════════════════════════════
# 1. API FAILOVER
# ═══════════════════════════════════════════

def check_api(provider):
    """Test if an API provider is responding."""
    try:
        import requests
        url = provider['url'].replace('/chat/completions', '/models')
        r = requests.get(url, timeout=10)
        ok = r.status_code < 500
        provider['ok'] = ok
        if not ok:
            provider['failures'] = provider.get('failures', 0) + 1
        else:
            provider['failures'] = 0
        return ok
    except Exception as e:
        provider['ok'] = False
        provider['failures'] = provider.get('failures', 0) + 1
        return False

def failover_test():
    """Test both providers and switch if needed."""
    log('=== API Failover Test ===')
    
    primary_ok = check_api(FAILOVER_STATE['primary'])
    log(f'  Primary (Sumopod): {"✅" if primary_ok else "❌"} ({FAILOVER_STATE["primary"]["failures"]} failures)')
    
    backup_ok = check_api(FAILOVER_STATE['backup'])
    log(f'  Backup (OpenRouter): {"✅" if backup_ok else "❌"}')
    
    if primary_ok:
        current = 'primary'
    elif backup_ok:
        current = 'backup'
        log('  ⚠️ Switched to backup provider')
    else:
        current = None
        log('  🚨 All providers DOWN')
    
    journal('failover_test', 'OK' if current else 'FAIL', f'Current: {current}')
    return current

def get_active_provider():
    """Returns active API config."""
    if FAILOVER_STATE['primary']['ok']:
        return FAILOVER_STATE['primary']
    elif FAILOVER_STATE['backup']['ok']:
        return FAILOVER_STATE['backup']
    return None

# ═══════════════════════════════════════════
# 2. DISK MANAGEMENT
# ═══════════════════════════════════════════

def get_disk_usage():
    """Get disk usage percentage."""
    try:
        st = os.statvfs(str(BASE))
        used = (st.f_blocks - st.f_bfree) / st.f_blocks * 100
        return used
    except:
        return 0

def cleanup(aggressive=False):
    """Clean up temporary files and old data."""
    log('=== Cleanup ===')
    freed = 0
    
    areas = []
    
    # 1. Temp files
    tmp_dir = BASE / 'tmp'
    if tmp_dir.exists():
        areas.append((tmp_dir, '*', 'tmp files'))
    
    # 2. Old backup files (keep last 5)
    areas.append((BACKUP_DIR, '*.bak', 'old backups'))
    
    # 3. Python cache
    for pyc in BASE.rglob('__pycache__'):
        areas.append((pyc, '*', 'pycache'))
    
    # 4. Old logs (if aggressive)
    if aggressive:
        for log_file in (BASE / 'memory').glob('*.log'):
            age = datetime.now() - datetime.fromtimestamp(log_file.stat().st_mtime)
            if age.days > 7:
                areas.append((log_file.parent, log_file.name, 'old log'))
    
    for directory, pattern, name in areas:
        if not directory.exists():
            continue
        if pattern == '*':
            size = sum(f.stat().st_size for f in directory.rglob('*') if f.is_file())
            shutil.rmtree(str(directory), ignore_errors=True)
            directory.mkdir(exist_ok=True)
        else:
            target = directory / pattern
            if target.exists() and target.is_file():
                size = target.stat().st_size
                target.unlink()
        
        log(f'  Cleaned: {name}')
        freed += size if 'size' in dir() else 0
    
    # Chroma prune (if too large)
    chroma_dir = BASE / 'data' / 'chroma_db'
    if chroma_dir.exists():
        chroma_size = sum(f.stat().st_size for f in chroma_dir.rglob('*') if f.is_file())
        if chroma_size > 100_000_000:  # >100MB
            log(f'  Chroma DB: {chroma_size/1e6:.0f}MB — within limits')
    
    disk = get_disk_usage()
    log(f'  Disk: {disk:.0f}% used')
    journal('cleanup', 'OK', f'Disk: {disk:.0f}%')
    return freed

# ═══════════════════════════════════════════
# 3. GIT AUTO-SYNC
# ═══════════════════════════════════════════

def git_sync(force=False):
    """Auto-commit and push critical changes to GitHub."""
    log('=== Git Sync ===')
    
    repo = BASE / 'github' / 'quill'
    if not repo.exists():
        log('  ❌ GitHub repo not found')
        return False
    
    # Files to always backup
    critical = [
        'README.md',
        'MEMORY.md',
        '.bootstrap/',
        'survival/state.json',
        'data/idx_action_state.json'
    ]
    
    try:
        for f in critical:
            src = BASE / f
            if src.exists():
                # Add specific files
                subprocess.run(['git', 'add', str(f)], cwd=repo,
                             capture_output=True, timeout=10)
        
        status = subprocess.run(['git', 'status', '--porcelain'],
                              cwd=repo, capture_output=True, text=True, timeout=10)
        
        if status.stdout.strip() or force:
            ts = datetime.now().strftime('%Y-%m-%d_%H:%M')
            result = subprocess.run(
                ['git', 'commit', '-m', f'Resilience auto-sync: {ts}'],
                cwd=repo, capture_output=True, text=True, timeout=15
            )
            
            if 'nothing to commit' in result.stdout:
                log('  ✅ Nothing to commit')
                journal('git_sync', 'OK', 'Nothing to commit')
                return True
            
            log(f'  ✅ Committed: {ts}')
            
            # Push
            push = subprocess.run(['git', 'push', 'origin', 'main'],
                                cwd=repo, capture_output=True, text=True, timeout=30)
            if push.returncode == 0:
                log('  ✅ Pushed to GitHub')
            else:
                log(f'  ⚠️ Push: {push.stderr[:100]}')
            
            journal('git_sync', 'OK', f'Committed: {ts}')
            return True
        else:
            log('  ✅ No changes')
            return True
    
    except Exception as e:
        log(f'  ❌ Git sync failed: {e}')
        journal('git_sync', 'FAIL', str(e))
        return False

# ═══════════════════════════════════════════
# 4. STATE JOURNALING
# ═══════════════════════════════════════════

def save_state(data, name):
    """Transactional state save with journal."""
    state_path = BASE / 'data' / f'{name}.json'
    backup_path = BACKUP_DIR / f'{name}.json.bak'
    
    # Write to temp first
    tmp_path = state_path.with_suffix('.json.tmp')
    try:
        tmp_path.write_text(json.dumps(data, indent=2, default=str))
    except Exception as e:
        log(f'  ❌ Failed to write {name}')
        journal('state_save', 'FAIL', str(e))
        return False
    
    # Backup existing if present
    if state_path.exists():
        shutil.copy2(state_path, backup_path)
    
    # Atomic rename
    shutil.move(str(tmp_path), str(state_path))
    journal('state_save', 'OK', f'{name}')
    log(f'  ✅ State saved: {name}')
    return True

def journal_replay(hours=24):
    """Replay journal entries for recovery."""
    if not JOURNAL_FILE.exists():
        log('No journal found')
        return []
    
    cutoff = datetime.now() - timedelta(hours=hours)
    entries = []
    
    with open(JOURNAL_FILE) as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                ts = datetime.fromisoformat(entry['ts'])
                if ts > cutoff:
                    entries.append(entry)
            except:
                pass
    
    log(f'Journal entries (last {hours}h): {len(entries)}')
    for e in entries[-10:]:
        log(f'  [{e["ts"][:16]}] {e["action"]}: {e["status"]}')
    
    return entries

# ═══════════════════════════════════════════
# 5. SELF-HEAL
# ═══════════════════════════════════════════

def self_heal():
    """Detect and fix common issues automatically."""
    log('=== Self-Heal ===')
    fixes = []
    
    # 1. Check disk
    disk = get_disk_usage()
    if disk > 75:
        log(f'  ⚠️ Disk {disk:.0f}% — running cleanup')
        cleanup(aggressive=(disk > 85))
        fixes.append('cleanup')
    else:
        log(f'  ✅ Disk: {disk:.0f}%')
    
    # 2. Check temp directory
    tmp_dir = BASE / 'tmp'
    if tmp_dir.exists():
        tmp_files = list(tmp_dir.iterdir())
        if len(tmp_files) > 20:
            log(f'  ⚠️ {len(tmp_files)} tmp files — cleaning')
            for f in tmp_files:
                if f.is_file() and f.suffix in ['.png', '.jpg', '.tmp', '.pdf']:
                    f.unlink()
            fixes.append('tmp_clean')
        else:
            log(f'  ✅ Temp: {len(tmp_files)} files')
    
    # 3. Check API
    active = failover_test()
    if not active:
        fixes.append('api_failover')
    
    # 4. Check git repo integrity
    repo = BASE / 'github' / 'quill'
    if repo.exists():
        result = subprocess.run(['git', 'status'], cwd=repo,
                              capture_output=True, text=True, timeout=10)
        if 'not a git repository' in result.stderr:
            log(f'  ❌ Git repo corrupted')
            fixes.append('git_corrupted')
        else:
            log(f'  ✅ Git repo OK')
    
    # 5. Emergency state save
    save_state({
        'timestamp': datetime.now().isoformat(),
        'disk': f'{disk:.0f}%',
        'api_primary': FAILOVER_STATE['primary']['ok'],
        'api_backup': FAILOVER_STATE['backup']['ok'],
        'fixes_applied': fixes
    }, 'resilience_state')
    
    summary = f'Applied {len(fixes)} fixes: {", ".join(fixes)}' if fixes else 'No issues found'
    log(f'  Result: {summary}')
    journal('self_heal', 'OK' if not fixes else 'FIXED', summary)
    
    return fixes

# ═══════════════════════════════════════════
# EMERGENCY
# ═══════════════════════════════════════════

def emergency_save():
    """Immediate backup of all critical state."""
    log('🚨 === EMERGENCY SAVE ===')
    
    critical_files = [
        'MEMORY.md', 'PROFILE.md', 'SOUL.md', 'AGENTS.md',
        'README.md',
        'survival/state.json',
        'data/idx_action_state.json',
    ]
    
    saved = 0
    for f in critical_files:
        src = BASE / f
        if src.exists():
            dst = BACKUP_DIR / f.replace('/', '_')
            shutil.copy2(src, dst)
            saved += 1
    
    log(f'✅ Emergency save: {saved}/{len(critical_files)} files backed up')
    journal('emergency_save', 'OK', f'{saved} files')
    return saved

# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Resilience core engine')
    parser.add_argument('action', choices=['heal', 'cleanup', 'failover-test', 'git-sync', 'journal', 'emergency-save'])
    parser.add_argument('--aggressive', action='store_true')
    parser.add_argument('--force', action='store_true')
    
    args = parser.parse_args()
    
    if args.action == 'heal':
        self_heal()
    elif args.action == 'cleanup':
        cleanup(aggressive=args.aggressive)
    elif args.action == 'failover-test':
        failover_test()
    elif args.action == 'git-sync':
        git_sync(force=args.force)
    elif args.action == 'journal':
        journal_replay()
    elif args.action == 'emergency-save':
        emergency_save()
