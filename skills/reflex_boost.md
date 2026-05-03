# SKILL: reflex_boost

## Tujuan
Pre-response validation loop — bikin respons lebih smart, accurate, dan efficient tanpa tambahan token AI. Semua proses di layer ini cuma text processing + file reads, nggak pakai LLM call.

## Konsep dari OpenMythos

**Recursive refinement tanpa intermediate output.** 
OpenMythos loop di latent space; kita loop di "context space" — cek consistency, pull relevant memory, verify assumption, refine output — sebelum final.

## Workflow

```
Input: raw user message + our draft response
       ↓
┌─────────────────────────────────────────────┐
│  LAYER 1: CONTEXT GATHER                    │
│  • Search memory (kode, decisions, prefs)   │
│  • Check relevant skill docs               │
│  • Check today's memory notes              │
└────────────────────┬────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  LAYER 2: CONSISTENCY CHECK                 │
│  • Confidence level (absolute vs hedged)   │
│  • Flag: absolute statements needing verify│
│  • Check: memory vs draft contradictions   │
└────────────────────┬────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  LAYER 3: EFFICIENCY AUDIT                 │
│  • Count sentences — cap at 3 if simple    │
│  • Remove filler phrases                   │
│  • Ensure direct answer first              │
└────────────────────┬────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  LAYER 4: CONTEXT SIGNAL                   │
│  • [?uncertain] if confidence < 0.6       │
│  • [📁 file] if pulled from specific file  │
│  • [⚠️ contradiction] if found             │
└────────────────────┬────────────────────────┘
                    ↓
Output: enriched, validated response
```

## Usage

**From other Python scripts:**
```python
from skills.reflex_boost.reflex_boost import reflex_boost

raw_response = generate_response(user_message)
final_response = reflex_boost(user_message, raw_response)
send_to_user(final_response)
```

**Standalone test:**
```bash
cd /app/working/workspaces/default
python skills/reflex_boost/reflex_boost.py
```

## Effect

| Before | After |
|--------|-------|
| Verbose explanation | Direct answer, concise |
| Answer tanpa cek memory | Cross-reference memory dulu |
| Over-confident on uncertain topics | Signal [?uncertain] when needed |
| Filler phrases everywhere | Clean, natural speech |
| No self-correction | Flag contradictions sebelum kirim |

**Token cost:** ~0 (regex + file reads only)

## Files

- `reflex_boost.py` — Main implementation
- `__init__.py` — Module export