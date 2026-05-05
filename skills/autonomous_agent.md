# AUTONOMOUS AGENT SKILL

## Purpose  
Self-scheduling tasks, anomaly detection, and proactive reporting.  
The skill that lets Quill act without waiting for commands.

---

## Architecture

```
┌──────────────────────────────────────────────┐
│               AUTONOMOUS AGENT                 │
├──────────────────────────────────────────────┤
│  1. Scheduler    — Self-manage cron tasks     │
│  2. Anomaly      — Detect unusual patterns    │
│  3. Proactive    — Generate reports on own    │
│  4. Guardian     — Safety limits & breaks     │
└──────────────────────────────────────────────┘
```

## Safety Rules

1. **Never** modify or delete files without backup
2. **Never** execute financial transactions or trades
3. **Never** send messages to users without `--allow-send` flag
4. **Auto-stop** after 5 consecutive failures
5. **Rate limit**: max 1 external API call per 10 seconds
6. **Always log** every autonomous action

## CLI Usage

```bash
# Check system health (like a heartbeat)
python3 skills/autonomous_agent/engine.py health

# Detect anomalies in logs/system
python3 skills/autonomous_agent/engine.py detect

# List scheduled self-tasks
python3 skills/autonomous_agent/engine.py tasks

# Add a self-task (autonomous)
python3 skills/autonomous_agent/engine.py add-task --name "disk cleanup" --cmd "scripts/cleanup.py" --schedule "0 3 * * *"

# Generate proactive report
python3 skills/autonomous_agent/engine.py report

# Full autonomous cycle (scheduler + detect + report)
python3 skills/autonomous_agent/engine.py cycle
```

## Integration

```
autonomous_agent
├── cron skill (scheduling)
├── persistent_memory (learn from anomalies)
├── self_evolve (fix issues found)
├── resilience_core (failover when critical)
└── HEARTBEAT.md (registered tasks)
```

---

_When to use: For routine checks, anomaly detection, and proactive maintenance._