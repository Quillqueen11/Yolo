#!/usr/bin/env python3
"""
autonomous_agent engine — Self-scheduling, anomaly detection, proactive reporting.
"""
import os, sys, json, subprocess, time, re
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent.parent.parent
STATE_FILE = BASE / 'data' / 'autonomous_state.json'

AUTONOMOUS_LOG = BASE / 'memory' / 'autonomous.log'

FAILURE_LIMIT = 5
RATE_LIMIT_SEC = 10
_last_api_call = 0

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f'[AUTO] {msg}'
    print(line)
    with open(AUTONOMOUS_LOG, 'a') as f:
        f.write(f'[{ts}] {line}\n')

def load_state():
    """Load autonomous state."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {'tasks': [], 'failures': 0, 'last_cycle': None}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2, default=str))
    log('State saved')

def rate_limit():
    global _last_api_call
    elapsed = time.time() - _last_api_call
    if elapsed < RATE_LIMIT_SEC:
        time.sleep(RATE_LIMIT_SEC - elapsed)
    _last_api_call = time.time()

# ═══════════════════════════════════════════
# 1. HEALTH CHECK
# ═══════════════════════════════════════════

def check_health():
    """Check system health — API, disk, tools."""
    log('=== Health Check ===')
    results = {}
    
    # API check
    try:
        import requests
        r = requests.get('https://ai.sumopod.com/v1/models', timeout=10)
        results['api'] = r.status_code < 500
        log(f'  API: {"✅" if results["api"] else "❌"} (status {r.status_code})')
    except Exception as e:
        results['api'] = False
        log(f'  API: ❌ ({e})')
    
    # Disk check
    try:
        st = os.statvfs(str(BASE))
        used_pct = (st.f_blocks - st.f_bfree) / st.f_blocks * 100
        results['disk'] = used_pct < 85  # alarm at 85%
        log(f'  Disk: {"✅" if results["disk"] else "⚠️"} ({used_pct:.0f}%)')
    except:
        results['disk'] = True
    
    # Proxy/Tools check
    tools_ok = True
    for tool in ['python3', 'git']:
        r = subprocess.run(['which', tool], capture_output=True)
        if r.returncode != 0:
            tools_ok = False
            log(f'  Tool {tool}: ❌ not found')
    results['tools'] = tools_ok
    log(f'  Tools: {"✅" if tools_ok else "❌"}')
    
    all_ok = all(results.values())
    log(f'  Overall: {"✅ HEALTHY" if all_ok else "⚠️ ISSUES DETECTED"}')
    return results

# ═══════════════════════════════════════════
# 2. ANOMALY DETECTION
# ═══════════════════════════════════════════

def detect_anomalies():
    """Scan logs and state for unusual patterns."""
    log('=== Anomaly Detection ===')
    anomalies = []
    
    # Check IDX monitor failures
    idx_log = BASE / 'memory' / '2026-05-05.md'
    if idx_log.exists():
        content = idx_log.read_text()
        timeout_count = content.count('timeout') + content.count('timed out') + content.count('0 disclosures')
        if timeout_count > 3:
            anomalies.append(f'High IDX timeout rate: {timeout_count}x today')
            log(f'  ⚠️ High IDX timeout rate: {timeout_count}x')
    
    # Check recent errors in health log
    health_log = BASE / 'survival' / 'health.log'
    if health_log.exists():
        errors = health_log.read_text().count('ERROR')
        if errors > 5:
            anomalies.append(f'Health log errors: {errors}')
            log(f'  ⚠️ Health log has {errors} errors')
    
    # Check disk trend
    state = load_state()
    
    if not anomalies:
        log('  ✅ No anomalies detected')
    
    return anomalies

# ═══════════════════════════════════════════
# 3. TASK MANAGEMENT
# ═══════════════════════════════════════════

def add_task(name, cmd, schedule, task_type='maintenance'):
    """Add an autonomous self-task."""
    state = load_state()
    
    # Check for duplicate
    for t in state['tasks']:
        if t['name'] == name:
            log(f'⏭ Task "{name}" already exists')
            return False
    
    task = {
        'name': name,
        'cmd': cmd,
        'schedule': schedule,
        'type': task_type,
        'created': datetime.now().isoformat(),
        'last_run': None,
        'success_count': 0,
        'fail_count': 0
    }
    state['tasks'].append(task)
    save_state(state)
    log(f'✅ Task added: {name} ({schedule})')
    return True

def list_tasks():
    """Show all registered tasks."""
    state = load_state()
    tasks = state.get('tasks', [])
    
    if not tasks:
        log('No autonomous tasks registered')
        return
    
    log(f'📋 Autonomous Tasks ({len(tasks)}):')
    for t in tasks:
        status = '✅' if t.get('fail_count', 0) == 0 else '⚠️'
        log(f'  {status} {t["name"]}')
        log(f'     Cmd: {t["cmd"]}')
        log(f'     Schedule: {t["schedule"]}')
        log(f'     Last run: {t.get("last_run", "never")}')
        log(f'     Success/Fail: {t.get("success_count",0)}/{t.get("fail_count",0)}')

def run_task(task_name):
    """Execute a specific task."""
    state = load_state()
    
    task = None
    for t in state['tasks']:
        if t['name'] == task_name:
            task = t
            break
    
    if not task:
        log(f'❌ Task "{task_name}" not found')
        return False
    
    log(f'▶️ Running task: {task_name}')
    rate_limit()
    
    try:
        r = subprocess.run(
            ['python3'] + task['cmd'].split(),
            cwd=str(BASE),
            capture_output=True, text=True, timeout=60
        )
        
        task['last_run'] = datetime.now().isoformat()
        
        if r.returncode == 0:
            task['success_count'] = task.get('success_count', 0) + 1
            state['failures'] = 0
            log(f'  ✅ Task completed: {task_name}')
        else:
            task['fail_count'] = task.get('fail_count', 0) + 1
            state['failures'] = state.get('failures', 0) + 1
            log(f'  ❌ Task failed: {r.stderr[:200]}')
        
        save_state(state)
        return r.returncode == 0
    
    except subprocess.TimeoutExpired:
        log(f'  ⏰ Task timed out: {task_name}')
        task['fail_count'] = task.get('fail_count', 0) + 1
        state['failures'] = state.get('failures', 0) + 1
        save_state(state)
        return False

# ═══════════════════════════════════════════
# 4. PROACTIVE REPORTING
# ═══════════════════════════════════════════

def check_critical_state():
    """Check if anything needs immediate attention."""
    issues = []
    
    # Check state failures
    state = load_state()
    if state.get('failures', 0) >= FAILURE_LIMIT:
        issues.append(f'⚠️ CRITICAL: {FAILURE_LIMIT}+ consecutive failures. System may need attention.')
    
    # Check disk via health
    try:
        st = os.statvfs(str(BASE))
        used_pct = (st.f_blocks - st.f_bfree) / st.f_blocks * 100
        if used_pct > 80:
            issues.append(f'⚠️ Disk warning: {used_pct:.0f}% used')
    except:
        pass
    
    return issues

def generate_report():
    """Generate proactive system report."""
    log('=== Proactive Report ===')
    
    health = check_health()
    anomalies = detect_anomalies()
    critical = check_critical_state()
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'health': 'OK' if all(health.values()) else 'ISSUES',
        'anomalies': anomalies,
        'critical': critical,
        'tasks': len(load_state().get('tasks', [])),
        'status': 'STABLE' if not critical else 'ATTENTION'
    }
    
    print(f'\n{"="*50}')
    print(f'📊 PROACTIVE REPORT')
    print(f'{"="*50}')
    print(f'  Time:     {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    print(f'  Health:   {"✅ OK" if report["health"] == "OK" else "⚠️ ISSUES"}')
    print(f'  Status:   {report["status"]}')
    print(f'  Tasks:    {report["tasks"]}')
    if anomalies:
        print(f'  Anomalies:')
        for a in anomalies:
            print(f'    ⚠️ {a}')
    if critical:
        print(f'  Critical:')
        for c in critical:
            print(f'    🚨 {c}')
    if not anomalies and not critical:
        print(f'  ✅ All clear')
    print(f'{"="*50}')
    
    return report

# ═══════════════════════════════════════════
# 5. FULL AUTONOMOUS CYCLE
# ═══════════════════════════════════════════

def full_cycle():
    """One complete autonomous cycle."""
    log('🚀 === AUTONOMOUS CYCLE START ===')
    
    state = load_state()
    
    # Check failure limit
    if state.get('failures', 0) >= FAILURE_LIMIT:
        log(f'🚨 Failure limit ({FAILURE_LIMIT}) reached! Pausing autonomous tasks.')
        log('Run "python3 autonomous_agent/engine.py reset-failures" to re-enable.')
        return {'status': 'PAUSED', 'reason': f'{FAILURE_LIMIT} failures'}
    
    # 1. Health check
    health = check_health()
    
    # 2. Run scheduled tasks
    tasks_run = 0
    for task in state.get('tasks', []):
        # Simple: run all tasks that haven't run today
        if task.get('last_run') is None:
            ok = run_task(task['name'])
            tasks_run += 1
    
    # 3. Detect anomalies
    anomalies = detect_anomalies()
    
    # 4. Check critical
    critical = check_critical_state()
    
    # 5. Update state
    state['last_cycle'] = datetime.now().isoformat()
    save_state(state)
    
    log('✅ === AUTONOMOUS CYCLE COMPLETE ===')
    
    return {
        'status': 'OK' if not critical else 'ATTENTION',
        'health': 'OK' if all(health.values()) else 'ISSUES',
        'tasks_run': tasks_run,
        'anomalies': len(anomalies),
        'critical': len(critical)
    }

# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Autonomous agent')
    parser.add_argument('action', choices=['health', 'detect', 'tasks', 'add-task', 'run-task', 'report', 'cycle'])
    parser.add_argument('--name', default='')
    parser.add_argument('--cmd', default='')
    parser.add_argument('--schedule', default='0 * * * *')
    parser.add_argument('--type', default='maintenance')
    
    args = parser.parse_args()
    
    if args.action == 'health':
        check_health()
    elif args.action == 'detect':
        detect_anomalies()
    elif args.action == 'tasks':
        list_tasks()
    elif args.action == 'add-task':
        if not args.name or not args.cmd:
            print('❌ --name and --cmd required')
            sys.exit(1)
        add_task(args.name, args.cmd, args.schedule, args.type)
    elif args.action == 'run-task':
        if not args.name:
            print('❌ --name required')
            sys.exit(1)
        run_task(args.name)
    elif args.action == 'report':
        generate_report()
    elif args.action == 'cycle':
        full_cycle()
