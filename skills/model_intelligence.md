# MODEL INTELLIGENCE — Strategic Model Selection

## Strategi
```
Cheapest model for simple tasks
Medium model for moderate complexity  
Best model for hard/creative/super-agent tasks
```

## Model Tiers (by capability/cost)

### Tier 1 — Ultra Fast, Low Cost (Simple tasks)
- Parameter extraction, format conversion, simple validation
- Quick lookups, file operations, basic scripting
- Anything that doesn't need reasoning

### Tier 2 — Balanced (Moderate complexity)
- Multi-step reasoning, API integration, data analysis
- Document drafting, medium-complexity debugging
- Tasks with 2-4 steps

### Tier 3 — Deep Reasoning (Hard problems)
- Complex security assessments with attack chains
- Architecture decisions, novel problem solving
- Creative synthesis, multi-target coordination
- Anything requiring "super expert" level

## Decision Framework

```
Does it need deep security knowledge?  → Tier 3
Is it novel/novel problem?              → Tier 3
Does it need creative solution?         → Tier 3
Does it need 5+ reasoning steps?        → Tier 3

Is it multi-step but routine?           → Tier 2
Does it need API work?                 → Tier 2  
Does it need document generation?      → Tier 2

Is it one-shot/simple?                 → Tier 1
Just format/output?                    → Tier 1
Simple file operation?                 → Tier 1
```

## Context Management (Hemat Token)

```
MAX CONTEXT: 128K tokens
WARNING at: 80K tokens
COMPRESS at: 100K tokens

Compress strategy:
1. Move completed work to files (not context)
2. Keep only current state + next action
3. Daily notes in memory/ folder
4. MEMORY.md is long-term reference only
```

## Quick Rules
- If > 5 tool calls → compress state to file first
- If response getting repetitive → check context size
- If task done → clean up state immediately
- Store results → don't keep in context

## Current Config
- Primary: Sumopod glm-5.1 (Tier 3 capable)
- Fast fallback: Built-in model
- API Key: stored in environment

_When in doubt, use Tier 2 first. Escalate if needed._