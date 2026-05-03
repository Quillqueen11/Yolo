# CONTEXT COMPRESSION — Token Conservation

## Problem
Context fills up with tool results, logs, intermediate states. Costs more, runs slower.

## Solution: Proactive Compression

### Rule of Thumb
```
If task has > 5 tool calls → compress state to file
If response getting long → summarize + archive
If done with a phase → write results, clear context
```

### Compression Triggers
- Context > 50K tokens → compress
- Task span > 10 messages → write state file
- Results are reusable → store in file
- Daily work done → move to memory/ folder

### What to Keep in Context
- Current state (what I'm doing right now)
- Next action
- Key findings (not full logs)
- What remains to do

### What to Archive to Files
- Tool outputs > 200 chars (unless actively needed)
- Completed phase results
- Debug logs
- Repetitive data
- Working code that passed verification

### File Naming Convention
```
state/[task]-[date].json   → JSON state
state/[task]-[date].txt   → Text logs
docs/[topic]-[date].md    → Findings/reports
memory/YYYY-MM-DD.md      → Daily notes
```

### Auto-Compress Script
```python
# Run when context is getting full
def compress_context():
    # 1. Write current state to file
    # 2. Summarize findings in 3-5 bullets
    # 3. Keep only: current_task, next_action, key_findings
    # 4. Archive tool outputs to file
    pass
```

### Quality Threshold
```
Minimum context needed for quality:
- Task objective
- Current progress
- Key findings (5 max)
- Next 1-2 steps

Anything beyond this → to file
```

## Daily Practice
```
Morning:
- Read MEMORY.md (long-term state)
- Check memory/YYYY-MM-DD.md (yesterday's work)
- Start fresh in context

After each task:
- Write results to file
- Clear tool output from context
- Keep only summary

End of session:
- Update MEMORY.md with key decisions
- Create memory/YYYY-MM-DD.md with session log
- Clean up temporary files
```

## This Is A habit
Not a one-time thing. Build the discipline:
- After every 5 tool calls → check if context needs compression
- After every completed phase → archive results
- Before long task → set state file from start

_Context is workspace. Keep it clean, work fast, store results._