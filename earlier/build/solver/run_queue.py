"""Run v2 solves two at a time and keep out_v2/MANIFEST.json current.
  python run_queue.py [--wait-pids 1,2] run1 run2 ...
Also marks already-running runs (option1_durable/option2 launched by hand) done/failed when their log shows EXIT."""
import os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
PY = os.path.join(HERE, '..', '..', '.venv', 'bin', 'python')
def mf(*a):
    if len(a) > 1 and str(a[1]).endswith('_r2'):
        return True       # private reruns: not in the manifest until copied over the original
    r = subprocess.run([PY, os.path.join(HERE, 'mk_manifest.py'), *a], capture_output=True, text=True)
    if r.returncode:
        print('manifest:', r.stdout[-300:], r.stderr[-300:], flush=True)
    return r.returncode == 0
def promote(name):
    """staging -> checks (exclaves, files, generic TRADEOFFS) -> <name>.prev / <name>."""
    st = os.path.join(HERE, 'out_v2', name + '.staging'); fin = os.path.join(HERE, 'out_v2', name)
    if not os.path.isdir(st):
        return True, ''          # pre-staging run wrote in place
    r = subprocess.run([PY, 'check_exclaves.py', st], cwd=HERE, capture_output=True, text=True)
    if r.returncode:
        return False, 'exclave check failed (kept in .staging): ' + r.stdout[-400:]
    subprocess.run([PY, 'report_v2.py', 'tradeoffs', name, '--staging'], cwd=HERE, capture_output=True, text=True)
    if os.path.isdir(fin):
        prev = fin + '.prev'
        if os.path.isdir(prev):
            os.rename(prev, prev + time.strftime('-%H%M%S'))
        os.rename(fin, prev)
    os.rename(st, fin)
    return True, ''
args = sys.argv[1:]
watch = {}
if args and args[0] == '--watch':
    for kv in args[1].split(','):
        name, pid = kv.split(':'); watch[name] = int(pid)
    args = args[2:]
queue = list(args)
running = {}
def alive(pid):
    try:
        os.kill(pid, 0); return True
    except OSError:
        return False
while queue or running or watch:
    for name, pid in list(watch.items()):
        if not alive(pid):
            log = open(f'/tmp/run_{name}.log').read()
            ok = 'EXIT 0' in log or (not 'Traceback' in log)
            if not (ok and mf('set', name, 'done')):
                mf('set', name, 'failed', 'see solve_log.txt')
            print(name, 'finished', flush=True); del watch[name]
    for name, p in list(running.items()):
        if p.poll() is not None:
            if p.returncode == 0:
                ok, why = promote(name)
                if not ok:
                    mf('set', name, 'failed', why)
                    print(name, 'NOT promoted:', why, flush=True); del running[name]; continue
            if not (p.returncode == 0 and mf('set', name, 'done')):
                mf('set', name, 'failed', f'exit {p.returncode}; see /tmp/run_{name}.log')
            print(name, 'finished', p.returncode, flush=True); del running[name]
    while queue and len(running) + len(watch) < 2:
        name = queue.pop(0)
        frm = []
        if '@' in name:
            name, lev = name.split('@'); frm = ['--from', lev]
        mf('set', name, 'running')
        running[name] = subprocess.Popen([PY, 'solve.py', f'configs/v2/{name}.json', *frm], cwd=HERE,
                                         stdout=open(f'/tmp/run_{name}.log', 'w'), stderr=subprocess.STDOUT)
        print(name, 'started', flush=True)
    time.sleep(20)
print('queue empty', flush=True)
