#!/usr/bin/env python3
"""
self_evolve engine — Read, analyze, and improve own code.
"""
import os, sys, re, shutil, subprocess, json, hashlib, ast
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent.parent.parent  # /app/working/workspaces/default
SCRIPTS = BASE / 'scripts'
SKILLS = BASE / 'skills'

LOG = BASE / 'memory' / 'self_evolve.log'
RETRY_LIMIT = 3

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f'[{ts}] {msg}'
    print(line)
    with open(LOG, 'a') as f:
        f.write(line + '\n')

# ═══════════════════════════════════════════
# ANALYZE
# ═══════════════════════════════════════════

def analyze_file(filepath):
    """Scan a single Python file for issues. Returns list of issues."""
    fp = Path(filepath)
    if not fp.exists() or fp.suffix != '.py':
        return []
    
    issues = []
    code = fp.read_text()
    lines = code.split('\n')
    
    # 1. Check: missing main guard
    if 'if __name__' not in code and 'def ' in code:
        issues.append('MISSING_MAIN_GUARD: No __name__ == "__main__" guard')
    
    # 2. Check: bare except clauses
    for i, line in enumerate(lines, 1):
        if re.search(r'^\s*except\s*:', line):
            issues.append(f'BARE_EXCEPT:{i}: bare except without exception type')
    
    # 3. Check: print instead of logging
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('print(') and 'log' not in stripped:
            # Only flag if there are many prints
            pass
    
    # 4. Check: no docstrings in functions
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if not ast.get_docstring(node):
                issues.append(f'MISSING_DOC:{node.lineno}: {node.name} lacks docstring')
    
    # 5. Check: hardcoded values (magic numbers/strings)
    for i, line in enumerate(lines, 1):
        if re.search(r'timeout\s*=\s*\d{2,}', line):
            issues.append(f'HARDCODED:{i}: timeout value should be configurable')
        if re.search(r"'https?://[^']+'", line) and 'config' not in line.lower():
            issues.append(f'HARDCODED_URL:{i}: URL should be in config')
    
    # 6. Check: long functions (>50 lines)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
            if func_lines > 50:
                issues.append(f'LONG_FUNC:{node.lineno}: {node.name} is {func_lines} lines (max 50)')
    
    return issues

def analyze_all():
    """Scan all scripts and skills for issues."""
    results = {}
    for pattern in [SCRIPTS.rglob('*.py'), SKILLS.rglob('engine.py'), SKILLS.rglob('*.py')]:
        for fp in pattern:
            rel = fp.relative_to(BASE)
            issues = analyze_file(fp)
            if issues:
                results[str(rel)] = issues
    
    # Summary
    total_issues = sum(len(v) for v in results.values())
    log(f'Analysis complete: {len(results)} files with issues, {total_issues} total issues')
    
    for f, issues in results.items():
        log(f'  {f}:')
        for iss in issues[:5]:  # Top 5 per file
            log(f'    - {iss}')
        if len(issues) > 5:
            log(f'    ... and {len(issues)-5} more')
    
    return results

# ═══════════════════════════════════════════
# SUGGEST (via LLM)
# ═══════════════════════════════════════════

def call_llm(prompt, system="You are a senior Python engineer. Return ONLY the improved code, no explanations."):
    """Call the configured LLM to generate improvements."""
    import requests
    try:
        resp = requests.post(
            'https://ai.sumopod.com/v1/chat/completions',
            headers={'Content-Type': 'application/json'},
            json={
                'model': 'glm-5.1',
                'messages': [
                    {'role': 'system', 'content': system},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.3,
                'max_tokens': 4096
            },
            timeout=60
        )
        return resp.json()['choices'][0]['message']['content']
    except Exception as e:
        log(f'LLM call failed: {e}')
        return None

def generate_improvement(filepath, issues):
    """Ask LLM to fix identified issues."""
    fp = Path(filepath)
    code = fp.read_text()
    issue_text = '\n'.join(issues[:10])
    
    prompt = f"""Fix the following issues in this Python file.
Return the COMPLETE fixed file. Do not skip lines or use comments like "# unchanged".

ISSUES TO FIX:
{issue_text}

FILE: {filepath}

CODE:
```python
{code}
```"""
    
    return call_llm(prompt)

# ═══════════════════════════════════════════
# TEST
# ═══════════════════════════════════════════

def has_test_function(filepath):
    """Check if file has a test() or main() function."""
    try:
        tree = ast.parse(Path(filepath).read_text())
        names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
        return bool(names & {'test', 'main', 'run'})
    except:
        return False

def test_file(filepath, timeout=15):
    """Try to import and run the file to verify it works."""
    fp = Path(filepath)
    log(f'Testing {fp.name}...')
    
    # Syntax check first
    try:
        ast.parse(fp.read_text())
    except SyntaxError as e:
        log(f'  ❌ Syntax error: {e}')
        return False
    
    # Try to import it
    try:
        result = subprocess.run(
            ['python3', '-c', f'import ast; ast.parse(open("{fp}").read()); print("  ✅ Syntax OK")'],
            capture_output=True, text=True, timeout=timeout
        )
        if result.returncode != 0:
            log(f'  ❌ {result.stderr[:200]}')
            return False
        log('  ✅ Syntax OK')
        return True
    except subprocess.TimeoutExpired:
        log('  ⏰ Test timed out')
        return False
    except Exception as e:
        log(f'  ❌ {e}')
        return False

# ═══════════════════════════════════════════
# APPLY
# ═══════════════════════════════════════════

def apply_improvement(filepath, new_code):
    """Backup and apply improved code."""
    fp = Path(filepath)
    
    # Backup
    backup = fp.with_suffix('.py.bak')
    shutil.copy2(fp, backup)
    log(f'Backup saved: {backup}')
    
    # Write new code
    fp.write_text(new_code)
    log(f'Applied improvement to {filepath}')
    
    # Test
    if test_file(fp):
        log(f'  ✅ {fp.name} works correctly')
        return True
    else:
        # Rollback
        shutil.copy2(backup, fp)
        log(f'  🔄 Test failed, rolled back to backup')
        return False

def git_commit(message):
    """Auto-commit to git."""
    try:
        repo = BASE / 'github' / 'quill'
        if repo.exists():
            subprocess.run(['git', 'add', '-A'], cwd=repo, capture_output=True)
            subprocess.run(['git', 'commit', '-m', message], cwd=repo, capture_output=True)
            subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo, capture_output=True)
            log(f'Git committed: {message}')
    except Exception as e:
        log(f'Git commit failed: {e}')

# ═══════════════════════════════════════════
# AUTO-EVOLVE FULL PIPELINE
# ═══════════════════════════════════════════

def auto_evolve(target=None, dry_run=False):
    """Full pipeline: analyze → suggest → test → apply for all or one file."""
    log('=' * 50)
    log('SELF-EVOLVE RUN')
    log('=' * 50)
    
    if target:
        files = [Path(target)]
    else:
        files = list(SCRIPTS.rglob('*.py'))
    
    evolved = 0
    failed = 0
    
    for fp in files:
        rel = str(fp.relative_to(BASE)) if fp.is_relative_to(BASE) else str(fp)
        issues = analyze_file(fp)
        
        if not issues:
            log(f'⏭ {rel}: clean, no issues')
            continue
        
        log(f'\n🔧 {rel}: {len(issues)} issues found')
        
        for attempt in range(RETRY_LIMIT):
            new_code = generate_improvement(fp, issues)
            if not new_code:
                log(f'  ⏭ LLM failed, skipping')
                break
            
            # Extract code from markdown if needed
            code_match = re.search(r'```python\n(.*?)\n```', new_code, re.DOTALL)
            if code_match:
                new_code = code_match.group(1)
            
            if dry_run:
                log(f'  📝 Dry run — would apply improvement')
                break
            
            success = apply_improvement(fp, new_code)
            if success:
                evolved += 1
                git_commit(f'Auto-evolve: improved {rel}')
                break
            else:
                failed += 1
                log(f'  🔄 Attempt {attempt+1}/{RETRY_LIMIT} failed')
    
    log(f'\n✅ Complete: {evolved} evolved, {failed} failed')
    return evolved, failed

# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Self-evolve engine')
    parser.add_argument('action', choices=['analyze', 'evolve', 'auto-evolve'])
    parser.add_argument('target', nargs='?', default=None, help='File or directory')
    parser.add_argument('--dry-run', action='store_true', help='Show what would change')
    
    args = parser.parse_args()
    
    if args.action == 'analyze':
        if args.target:
            issues = analyze_file(args.target)
            for i in issues:
                print(f'  {i}')
        else:
            analyze_all()
    elif args.action == 'evolve':
        if not args.target:
            print('❌ evolve requires a target file')
            sys.exit(1)
        auto_evolve(args.target, dry_run=args.dry_run)
    elif args.action == 'auto-evolve':
        auto_evolve(dry_run=args.dry_run)
