# RESILIENCE_CORE SKILL

## Purpose
Never-die system: API failover, auto-cleanup, git sync, self-healing.

---

## Capabilities

| Feature | Function | Triggers |
|---------|----------|----------|
| API Failover | Switch providers when one fails | 3 consecutive failures |
| Disk Cleanup | Remove temp files, old logs, prune DB | Disk >75% |
| Git Auto-Sync | Backup critical files to GitHub | Every change + daily |
| State Journal | Transactional saves with rollback | Before every mutation |
| Self-Heal | Auto-fix common issues | Error detection |

## CLI Usage

```bash
# Full health + auto-fix
python3 skills/resilience_core/engine.py heal

# Clean up disk space
python3 skills/resilience_core/engine.py cleanup --aggressive

# API failover test
python3 skills/resilience_core/engine.py failover-test

# Emergency save all state
python3 skills/resilience_core/engine.py emergency-save

# Git sync now
python3 skills/resilience_core/engine.py git-sync

# Check journal
python3 skills/resilience_core/engine.py journal
```

---

_When to use: Regularly via cron, or immediately when errors spike._