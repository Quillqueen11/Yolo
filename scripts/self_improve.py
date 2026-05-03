#!/usr/bin/env python3
"""
self_improve.py — Periodic self-improvement script
Runs after each session to update memory, detect patterns, suggest improvements.
"""

import os
import json
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/app/working/workspaces/default")
MEMORY_FILE = WORKSPACE / "MEMORY.md"
MEMORY_DIR = WORKSPACE / "memory"
SELF_IMPROVE_LOG = WORKSPACE / "data" / "self_improve_log.json"

# ─── Self-Improvement Checklist ────────────────────────────────────────────────

def check_memory_freshness():
    """Ensure memory is up-to-date."""
    today = datetime.now().strftime("%Y-%m-%d")
    today_file = MEMORY_DIR / f"{today}.md"
    
    if not today_file.exists():
        # Create today's memory
        content = f"# Memory — {today}\n\n## Session Notes\n\n"
        today_file.write_text(content)
        print(f"[self_improve] Created {today_file.name}")

def log_improvement(category: str, action: str, result: str):
    """Log self-improvement actions."""
    log = {"timestamp": datetime.now().isoformat(), "category": category, "action": action, "result": result}
    
    if SELF_IMPROVE_LOG.exists():
        existing = json.loads(SELF_IMPROVE_LOG.read_text())
    else:
        existing = []
    
    existing.append(log)
    
    # Keep last 100 entries
    existing = existing[-100:]
    
    SELF_IMPROVE_LOG.parent.mkdir(exist_ok=True)
    SELF_IMPROVE_LOG.write_text(json.dumps(existing, indent=2))
    
    print(f"[self_improve] Logged: {category} -> {action}")

def update_skill_usage_stats():
    """Track which skills are used most."""
    skills_dir = WORKSPACE / "skills"
    stats = {}
    
    for skill in skills_dir.iterdir():
        if skill.is_dir() and (skill / "SKILL.md").exists():
            # Count usage in scripts
            skill_name = skill.name
            count = 0
            
            for script in (WORKSPACE / "scripts").glob("*.py"):
                if skill_name.lower() in script.read_text().lower():
                    count += 1
            
            stats[skill_name] = count
    
    print(f"[self_improve] Skill usage stats: {stats}")

def detect_new_patterns():
    """Detect patterns from recent work."""
    patterns = []
    
    # Check for new scripts
    scripts = list((WORKSPACE / "scripts").glob("*.py"))
    if scripts:
        patterns.append(f"Scripts: {len(scripts)} files")
    
    # Check for new docs
    docs = list((WORKSPACE / "docs").glob("*.md"))
    if docs:
        patterns.append(f"Docs: {len(docs)} files")
    
    # Check Chroma DB
    chroma_path = WORKSPACE / "data" / "chroma_db"
    if chroma_path.exists():
        import chromadb
        try:
            client = chromadb.PersistentClient(path=str(chroma_path))
            col = client.get_collection("idx_actions")
            patterns.append(f"Chroma entries: {col.count()}")
        except:
            pass
    
    return patterns

def check_api_health():
    """Check if known APIs are still working."""
    from curl_cffi.requests import Session
    
    session = Session(impersonate='chrome')
    endpoints = [
        ('NewsAnnouncement', 'https://www.idx.co.id/primary/NewsAnnouncement/GetAllAnnouncement', {'pageSize': 1, 'pageNumber': 1}),
        ('CompanyProfiles', 'https://www.idx.co.id/primary/ListedCompany/GetCompanyProfiles', {'start': 0, 'length': 1}),
        ('HomeContent', 'https://www.idx.co.id/primary/home/content', {}),
    ]
    
    health = []
    for name, url, params in endpoints:
        try:
            r = session.get(url, params=params, timeout=10)
            status = "✅" if r.status_code == 200 else f"❌ {r.status_code}"
            health.append(f"{name}: {status}")
        except Exception as e:
            health.append(f"{name}: ❌ {e}")
    
    return health

def suggest_improvements():
    """Analyze recent work and suggest improvements."""
    suggestions = []
    
    # Check state file size
    state_file = WORKSPACE / "data" / "idx_action_state.json"
    if state_file.exists():
        size = state_file.stat().st_size
        if size > 10000:  # > 10KB
            suggestions.append("State file growing large — consider archiving old entries")
    
    # Check memory file
    if MEMORY_FILE.exists():
        size = MEMORY_FILE.stat().st_size
        if size > 5000:  # > 5KB
            suggestions.append("MEMORY.md getting large — consider pruning old entries")
    
    # Check cron jobs
    import subprocess
    result = subprocess.run(['qwenpaw', 'cron', 'list', '--agent-id', 'default'], 
                           capture_output=True, text=True, timeout=10)
    if result.returncode == 0:
        cron_count = result.stdout.count('"id":')
        if cron_count > 5:
            suggestions.append(f"Cron jobs: {cron_count} — review if all still needed")
    
    return suggestions

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 50)
    print(f"Self-Improve — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    # Run checks
    print("\n[1] Memory Freshness...")
    check_memory_freshness()
    
    print("\n[2] API Health Check...")
    health = check_api_health()
    for h in health:
        print(f"    {h}")
    
    print("\n[3] Skill Usage Stats...")
    update_skill_usage_stats()
    
    print("\n[4] Pattern Detection...")
    patterns = detect_new_patterns()
    for p in patterns:
        print(f"    {p}")
    
    print("\n[5] Improvement Suggestions...")
    suggestions = suggest_improvements()
    if suggestions:
        for s in suggestions:
            print(f"    💡 {s}")
    else:
        print("    ✅ No urgent improvements needed")
    
    # Log session
    log_improvement("session", "periodic_check", f"patterns={len(patterns)}, suggestions={len(suggestions)}")
    
    print("\n" + "=" * 50)
    print("Self-Improve Complete")
    print("=" * 50)

if __name__ == "__main__":
    main()