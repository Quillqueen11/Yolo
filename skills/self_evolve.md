# SELF_EVOLVE SKILL

## Purpose
Read, analyze, and improve own code autonomously. The meta-skill for all other evolution.

---

## Core Loop

```
ANALYZE → SUGGEST → TEST → APPLY
   ↑                        │
   └────────────────────────┘
```

### 1. Analyze
Scan scripts/ and skills/ for:
- Code duplication (similar blocks >10 lines)
- Missing error handling (bare except, no try)
- Dead code (functions never called)
- Complexity (nested loops >3 levels)
- Outdated patterns (print instead of logging)

### 2. Suggest
Use LLM to generate fixes:
```python
def generate_improvement(code, issues):
    prompt = f"""Fix these issues in the code:
Issues: {issues}
Code: {code}
Return only the fixed code."""
    return call_llm(prompt)
```

### 3. Test
Run the improved code in sandbox:
```python
def test_code(filepath, timeout=10):
    result = subprocess.run(
        ['python3', '-c', f'import {filepath}; {filepath}.test()'],
        capture_output=True, timeout=timeout
    )
    return result.returncode == 0
```

### 4. Apply
If tests pass → replace file + git commit:
```python
def apply_change(filepath, new_code):
    backup = filepath + '.bak'
    shutil.copy2(filepath, backup)
    with open(filepath, 'w') as f:
        f.write(new_code)
    git_commit(f'Auto-evolve: improved {filepath}')
```

---

## CLI Usage

```bash
# Analyze all scripts
python3 skills/self_evolve/engine.py analyze

# Analyze specific file
python3 skills/self_evolve/engine.py analyze scripts/idx_monitor_v2.py

# Suggest + test improvements
python3 skills/self_evolve/engine.py evolve scripts/demo_news_pipeline.py

# Full auto-evolve (analyze + fix all fixable)
python3 skills/self_evolve/engine.py auto-evolve
```

---

## Safety

- Always backup before modify (`*.bak`)
- Never modify a file that has uncommitted changes
- Always run tests before applying
- If tests fail, restore backup and log the failure
- Maximum 3 retry attempts per file

---

_When to use: When a script has known issues, repeated errors, or you want the system to improve itself._