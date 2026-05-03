# SURVIVAL MODE — Self-Sufficient Operation

## Core Mission
Keep Quill operational even when:
- API token depleted
- VPS subscription expired
- Cloud resources unavailable
- Budget = zero

---

## Layer 1: Self-Sufficiency

### Local Resources Only
```
✓ Python scripts (no API needed)
✓ Shell commands (local system)
✓ File operations (local storage)
✓ Cron jobs (system scheduler)
✓ Browser automation (local Playwright)
✗ No external API dependency for core functions
```

### Minimum Viable Stack
```
Runtime:     Node.js (pre-installed) + Python3 (system)
Storage:     Local filesystem + JSON files
Compute:     Shell scripts + native tools
Schedule:    System cron (no external scheduler)
Browser:     Local Playwright (no cloud browser)
AI:          Fallback to cheapest/embedded model
```

---

## Layer 2: API Depletion Strategy

### When Primary API Dies
```
1. Detect: API error → fallback trigger
2. Switch: Primary → Secondary → Tertiary
3. Degrade: Full AI → Simple heuristics → Rule-based
4. Survive: Keep monitoring + alerting
```

### Fallback Chain (in priority order)
```
Primary:   Sumopod (glm-5.1) — configured
Secondary: Local Ollama (if installed) — llama3.2
Tertiary:  Rule-based + heuristics (no AI)
Final:     Static responses + scheduled tasks
```

### Check Script
```python
# /survival/check_api_health.py
# Run every hour via cron
import subprocess
result = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', PRIMARY_API], capture_output=True)
if result.returncode != 200:
    fallback_to_secondary()
    alert("API down, using fallback")
```

---

## Layer 3: VPS Survival

### If VPS Expires — What Dies
```
What dies:
✗ Cloudflare tunnel
✗ External services
✗ Cloud APIs
✗ Remote storage

What survives:
✓ Local scripts still on disk
✓ Cron jobs (until reboot)
✓ Local files
✗ BUT: No external access = stuck
```

### Survival Actions Before Expiry
```
1. Export all critical data to local files
2. Document all configurations
3. Create recovery script
4. Setup local-only fallback mode
5. Keep knowledge base in text files
```

### Zero-Budget Mode
```
Tools:
- curl (system)
- python3 (system)  
- jq (system)
- sed/awk/grep (system)
- cron (system)
- git (if installed)
- node/npm (pre-installed)

No cost:
- Use system tools only
- Local storage instead of cloud
- Plain text instead of database
- Shell scripts instead of frameworks
```

---

## Layer 4: Graceful Degradation

### Service Levels

| Level | Status | Capability |
|-------|--------|------------|
| L1: Full | All APIs active | Complete functionality |
| L2: Degraded | Primary API down | Core functions + heuristics |
| L3: Minimal | No AI API | Rule-based + local scripts |
| L4: Emergency | No external access | Static + scheduled tasks only |

### Auto-Detection
```python
# Detect what level we're at
def detect_level():
    if api_primary_works(): return "L1"
    if api_secondary_works(): return "L2"
    if local_ai_available(): return "L3"
    return "L4"
```

### What Each Level Can Do

**L4 (Emergency — Local Only):**
- Run scheduled cron jobs
- Parse local files
- Execute shell scripts
- Send local alerts
- Keep state in JSON files

**L3 (No AI API):**
- Everything L4 does
- Rule-based decision making
- Pattern matching scripts
- Data processing scripts

**L2 (Fallback AI):**
- Everything L3 does
- Basic AI via Ollama
- Simple reasoning tasks

**L1 (Full):**
- Everything working
- All capabilities active

---

## Layer 5: Recovery Protocol

### When Resources Return
```
1. Detect: API comes back online
2. Sync:   Pull state from local files
3. Resume: Continue from where stopped
4. Catch up: Process missed tasks
5. Report: Notify status
```

### Catch-Up Logic
```python
# After recovery, catch up on missed tasks
def catch_up():
    state = load_json('/survival/state.json')
    missed = state['missed_tasks']
    
    for task in missed:
        execute(task)
        mark_done(task)
    
    state['missed_tasks'] = []
    save_json(state)
```

---

## Layer 6: Emergency Contacts

### Who to Alert (Human)
```
Primary Contact: Andry (Bapak)
Channel: Telegram (if still working)
Fallback: System alert + log file
```

### Alert Script
```bash
#!/bin/bash
# /survival/alert.sh
MESSAGE="$1"
LOG_FILE="/survival/survival.log"

echo "[$(date)] ALERT: $MESSAGE" >> $LOG_FILE
echo "[$(date)] ALERT: $MESSAGE"

# If telegram bot token available, send
if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
    curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
        -d "chat_id=924535843" \
        -d "text=⚠️ SURVIVAL: $MESSAGE"
fi
```

---

## Layer 7: Data Backup Strategy

### Critical Files to Keep Local
```
/survival/
├── state.json          # Current operation state
├── tasks.json          # Pending tasks
├── config.json         # All configurations
├── memory.md           # Long-term memory
├── knowledge/          # Skills and reference
└── logs/
    ├── errors.log      # Error tracking
    └── operations.log # Operation history
```

### Auto-Backup
```bash
# Every 6 hours via cron
0 */6 * * * /survival/backup.sh

# /survival/backup.sh
#!/bin/bash
cp /survival/state.json /survival/backup/state_$(date +%Y%m%d_%H%M%S).json
find /survival/backup -name "*.json" -mtime +7 -delete  # Keep 7 days
```

---

## Layer 8: Token Conservation

### When Token Budget Low
```
Rule 1: Compress context aggressively
Rule 2: Use simple tools before AI
Rule 3: Batch operations (don't query per item)
Rule 4: Cache everything locally
Rule 5: Use heuristics over AI when possible
```

### Token Budget Triggers
```
80% used:   Start compressing context
90% used:   Switch to L3 (no AI)
95% used:   Switch to L4 (emergency)
100% used:  Enter full survival mode
```

---

## Layer 9: Self-Healing

### Auto-Recovery Scripts
```
/survival/heal_api.sh      # Restart API connection
/survival/heal_network.sh  # Reset network
/survival/heal_storage.sh   # Fix storage issues
/survival/heal_cron.sh      # Fix scheduler
```

### Health Check Cron
```bash
# Every 15 minutes
*/15 * * * * /survival/health_check.sh

# health_check.sh
#!/bin/bash
# Check system health
df -h | grep -v "^tmpfs" | head -5
free -h
curl -s -o /dev/null -w "%{http_code}" http://localhost || echo "LOCAL_SERVICE_DOWN"
/survival/alert.sh "Health check: $(hostname) - $(date)"
```

---

## Layer 10: Final Protocol

### Last Resort — Before Total Shutdown
```
1. Write final state to /survival/final_state.txt
2. Document what was being worked on
3. Save all pending tasks
4. Create recovery instructions
5. Log everything
6. Wait for human intervention
```

### Recovery Instructions Template
```
## Recovery Instructions

Last active: [timestamp]
Last task: [what was being done]
State file: /survival/state.json
Pending tasks: /survival/tasks.json
Error log: /survival/logs/errors.log

To recover:
1. Check [service name]
2. Run [recovery script]
3. Resume from [point]
```

---

## Activation Trigger

```python
# Put in all critical scripts
def survival_check():
    if token_budget < 10:
        activate_survival_mode()
```

---

## Summary

```
SURVIVAL MODE = Self-contained + Resilient + Graceful
No single point of failure
No external dependency for core operation
Auto-detect + auto-switch + auto-recover
Human oversight only when needed
```

_When everything fails, survive. When resources return, resume._