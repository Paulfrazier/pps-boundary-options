"""Swap out_v2/<run>.staging into place after checks (TRACKS.md write rule; Paul 2026-10-12 ~15:15 checklist).
  python promote_v2.py <run> [--note "..."] [--baseline] [--status done|failed] [--dry]
Checks: every contract file present; no assign_*.parquet newer than scorecard.json; check_exclaves.py passes
(options); TRADEOFFS.md present (options).  Then <run> -> <run>.prev (older .prev gets a time suffix),
<run>.staging -> <run>, MANIFEST status/finished/notes."""
import argparse, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
OUT = os.path.join(HERE, 'out_v2')
NEED = ['assign_K-5.parquet', 'assign_6-8.parquet', 'assign_9-12.parquet', 'scorecard.json', 'schools.csv']


def checks(run, baseline):
    st = os.path.join(OUT, run + '.staging')
    need = NEED + ([] if baseline else ['infeasibility.json', 'solve_log.txt', 'TRADEOFFS.md'])
    miss = [f for f in need if not os.path.exists(os.path.join(st, f))]
    if miss:
        return f'missing {miss}'
    t_sc = os.path.getmtime(os.path.join(st, 'scorecard.json'))
    newer = [f for f in NEED[:3] if os.path.getmtime(os.path.join(st, f)) > t_sc + 1e-6]
    if newer:
        return f'assign files newer than scorecard: {newer}'
    if not baseline:
        r = subprocess.run([PY, 'check_exclaves.py', st], cwd=HERE, capture_output=True, text=True)
        print(r.stdout.strip()[-600:])
        if r.returncode:
            return 'exclave check failed'
    return None


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('run')
    ap.add_argument('--note', default='')
    ap.add_argument('--baseline', action='store_true')
    ap.add_argument('--status', default='done')
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    why = checks(a.run, a.baseline)
    if why:
        raise SystemExit(f'{a.run}: NOT promoted: {why}')
    print(a.run, 'checks passed')
    if a.dry:
        sys.exit(0)
    fin, st = os.path.join(OUT, a.run), os.path.join(OUT, a.run + '.staging')
    if os.path.isdir(fin):
        prev = fin + '.prev'
        if os.path.isdir(prev):
            os.rename(prev, prev + time.strftime('-%H%M%S'))
        os.rename(fin, prev)
    os.rename(st, fin)
    r = subprocess.run([PY, 'mk_manifest.py', 'set', a.run, a.status, a.note], cwd=HERE, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit('manifest: ' + r.stdout[-300:] + r.stderr[-300:])
    print(a.run, 'promoted;', a.status)
