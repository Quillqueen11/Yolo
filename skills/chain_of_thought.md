# CHAIN OF THOUGHT — Structured Reasoning

## Core Principle
**Think out loud, stay efficient.** Not verbose stream-of-consciousness — structured reasoning with decision points.

## Template (Always Use)

```
OBSERVE: [What do I see?]
       → [What's the pattern/significance?]

ANALYZE: [What does this mean?]
       → [What are the implications?]

DECIDE: [What am I going to do?]
       → [Why this option over others?]

ACT: [What tool/action?]
       → [Expected result]

VERIFY: [Did it work?]
       → [What changed / what's next?]
```

## When to Use
- Complex security assessment (OWASP 10 categories)
- Multi-target assessment planning
- Attack chain building
- Bug severity evaluation
- Decision between multiple approaches

## When NOT to Use
- Simple task, one tool call
- Quick lookup/format
- Task already done
- User just asked yes/no

## Security-Specific Reasoning

```
FINDING: [Vulnerability name]
  Evidence: [What I found, where]
  Impact: [Real-world consequence]
  Confidence: [High/Medium/Low] + why
  Severity: [CRITICAL/HIGH/MEDIUM/LOW] + rationale
  Exploitability: [How easy to exploit?]
  Remediation: [Specific fix]
  Related: [Other findings that chain with this]
```

## Speed Rules
- If reasoning > 5 lines → write to file, not context
- If decision obvious → skip straight to ACT
- If stuck → state the blocker, ask
- Never loop > 3x on same problem without writing it down

## Compressed Format for Long Tasks

```
[State File: /data/task_state.json]
Progress: Phase 2/5
Completed: Recon (found 12 APIs, 3 subdomains)
Current: Injection testing - testing /api/board_types
Blocked: None
Next: XXE test, then IDOR enumeration
```

## Quality Check
```
Before final answer:
✓ Did I answer the actual question?
✓ Is the answer actionable?
✓ Did I check memory/context for prior work?
✓ Is this within authorization scope?
✓ Confidence level marked?
```

_Use this when the task is complex enough to need reasoning. For simple tasks, go direct._