# PERSISTENT MEMORY SKILL

## Purpose
Long-term memory that persists across sessions using vector DB + session linking.
Learns from mistakes and recognizes patterns automatically.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   MEMORY LAYERS                      │
├─────────────────────────────────────────────────────┤
│  L1: Working Memory    (current session context)     │
│  L2: Episodic Memory   (past conversations + events) │
│  L3: Semantic Memory   (learned patterns + facts)    │
│  L4: Procedural Memory (how to do things)           │
└─────────────────────────────────────────────────────┘
```

### L1 — Working Memory (Current Session)
Auto-tracked in session context. Resets each session.

### L2 — Episodic Memory (Chroma DB)
Past conversations, decisions, and events stored as vector embeddings.

### L3 — Semantic Memory (Chroma DB)
Learned patterns: "IDX API timeout at 05:00 = maintenance", "this approach failed before"

### L4 — Procedural Memory (Scripts + Skills)
"How to fetch IDX data", "How to bypass Cloudflare", etc.

---

## Core Functions

### Store a Memory
```python
memory.store(
    content="IDX API timeout at 05:00 WIB",
    tags=["idx", "api", "timeout", "pattern"],
    layer="episodic",
    importance=0.8  # 0.0-1.0
)
```

### Recall Related Memories
```python
results = memory.recall(
    query="IDX API error handling",
    n_results=5,
    min_score=0.3
)
```

### Learn a Pattern
```python
memory.learn(
    trigger="IDX timeout >2 retries",
    lesson="IDX API undergoes maintenance 05:00-05:30 WIB daily",
    action="Skip monitoring between 05:00-05:30"
)
```

### Forget (Prune)
```python
memory.forget(older_than="30d", importance_lt=0.3)
```

---

## CLI Usage

```bash
# Store a memory
python3 skills/persistent_memory/engine.py store "IDX API timeout at 05:00" --tags idx,api,pattern

# Recall memories
python3 skills/persistent_memory/engine.py recall "IDX error" --n 5

# Learn a pattern
python3 skills/persistent_memory/engine.py learn --trigger "IDX timeout" --lesson "Maintenance window"

# Summary
python3 skills/persistent_memory/engine.py summary

# Prune old/unimportant memories
python3 skills/persistent_memory/engine.py forget --older-than 30d --importance-below 0.3
```

---

## Storage

- Chroma DB: `/app/working/workspaces/default/data/persistent_memory/`
- Collection: `persistent_memory`
- Embeddings: `all-MiniLM-L6-v2` (384-dim)
- Metadata: timestamp, tags, importance, layer, source

---

_When to use: Before answering any question, always recall related memories first. After any significant event, store it._