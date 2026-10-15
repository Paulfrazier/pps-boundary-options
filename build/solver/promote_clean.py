"""Swap a line-cleanup candidate in for a live plan (Paul 2026-10-12 ~23:00, overnight "look, fix, look").

  python promote_clean.py <candidate> <target> [--dry]

<candidate> is a finished solve in out_v2/<candidate>.staging (same schools/programs as <target>, different line
weights).  It replaces out_v2/<target> only if ALL of these hold (otherwise nothing changes and the reasons print):
  rules     meets PPS A's at-target count every required year; K-5 and 6-8 non-exempt schools in range >= target's
  at target K-5 and 6-8 schools at target all required years >= target's - 1
  walking   K-5 past a closer school <= target x 1.03 and K-5 avg walk <= target + 0.005 mi;
            6-8 past a closer school <= target x 1.05
  moves     kids reassigned vs PPS Status Quo <= target x 1.03 per level (option4, "fewest moves": not more at all)
  lines     K-5 teeth <= 0.85 x target's (--teeth-ratio; with a later small-gain pass of 0.95, K-5 fingers may not
            rise either) (lines_qa.py); K-5 real pockets not more than target's
  exclaves  check_exclaves.py passes
Then: out_v2/<target>.staging <- candidate files (name/label set to the target), TRADEOFFS.md regenerated with the
target's own "what this plan is" text + a line-cleanup section, and promote_v2.py swaps it in (old -> .prev)."""
import argparse, json, os, shutil, subprocess, sys, time
import common as C
import lines_qa as Q

OUT = os.path.join(C.SOLVER, 'out_v2')
PY = sys.executable


def sc(path):
    return json.load(open(os.path.join(path, 'scorecard.json')))


def meets(s):
    r = s.get('durability_reference') or s['durability'].get('reference') or {}
    return bool(r.get('meets_reference_every_required_year'))


def check(cand, target, teeth_ratio=0.85):
    cp, tp = os.path.join(OUT, cand + '.staging'), os.path.join(OUT, target)
    c, t = sc(cp), sc(tp)
    L = lambda s, lev, k: s['levels'][lev].get(k) or 0
    A = lambda s, lev: s['durability']['levels'][lev]['at_target_all_required_years']
    qc, qt = Q.qa(cand, True), Q.qa(target)
    why = []
    if not meets(c):
        why.append('does not meet PPS A every required year')
    for lev in ('K-5', '6-8'):
        if L(c, lev, 'schools_in_range_non_exempt') < L(t, lev, 'schools_in_range_non_exempt'):
            why.append(f'{lev} schools in range {L(c, lev, "schools_in_range_non_exempt")} < {L(t, lev, "schools_in_range_non_exempt")}')
        if A(c, lev) < A(t, lev) - 1:
            why.append(f'{lev} at target all required years {A(c, lev)} < {A(t, lev)} - 1')
    if L(c, 'K-5', 'kids_past_closer_school') > 1.03 * L(t, 'K-5', 'kids_past_closer_school'):
        why.append(f"K-5 past a closer school {L(c, 'K-5', 'kids_past_closer_school'):.0f} > 1.03 x {L(t, 'K-5', 'kids_past_closer_school'):.0f}")
    if L(c, 'K-5', 'avg_walk_mi') > L(t, 'K-5', 'avg_walk_mi') + 0.005:
        why.append(f"K-5 avg walk {L(c, 'K-5', 'avg_walk_mi')} > {L(t, 'K-5', 'avg_walk_mi')} + 0.005")
    if L(c, '6-8', 'kids_past_closer_school') > 1.05 * L(t, '6-8', 'kids_past_closer_school'):
        why.append(f"6-8 past a closer school {L(c, '6-8', 'kids_past_closer_school'):.0f} > 1.05 x {L(t, '6-8', 'kids_past_closer_school'):.0f}")
    # (2026-10-12 ~23:20) kids moved vs PPS Status Quo: at most +3%; a fewest-moves plan (option4) may not move more
    mv_tol = 1.0 + 1e-9 if target == 'option4' else 1.03
    for lev in ('K-5', '6-8'):
        if L(c, lev, 'kids_reassigned_vs_status_quo') > mv_tol * L(t, lev, 'kids_reassigned_vs_status_quo'):
            why.append(f"{lev} kids moved {L(c, lev, 'kids_reassigned_vs_status_quo'):.0f} > {mv_tol:.2f} x "
                       f"{L(t, lev, 'kids_reassigned_vs_status_quo'):.0f}")
    if qc['K-5']['teeth'] > teeth_ratio * qt['K-5']['teeth']:
        why.append(f"K-5 teeth {qc['K-5']['teeth']} > {teeth_ratio} x {qt['K-5']['teeth']}")
    if teeth_ratio > 0.85 and len(qc['K-5']['fingers']) > len(qt['K-5']['fingers']):
        why.append(f"K-5 fingers {len(qc['K-5']['fingers'])} > {len(qt['K-5']['fingers'])} (required for a small-gain pass)")
    if len(qc['K-5']['pockets']) > len(qt['K-5']['pockets']):
        why.append(f"K-5 pockets {len(qc['K-5']['pockets'])} > {len(qt['K-5']['pockets'])}")
    r = subprocess.run([PY, 'check_exclaves.py', cp], cwd=C.SOLVER, capture_output=True, text=True)
    if r.returncode:
        why.append('exclave check failed: ' + r.stdout.strip()[-300:])
    return why, c, t, qc, qt


def headline(s):
    L = lambda lev, k: s['levels'][lev].get(k)
    D = s['durability']['levels']
    ref = (s.get('durability_reference') or s['durability'].get('reference') or {}).get('levels', {})
    RA = lambda lev: (ref.get(lev) or {}).get('at_target_all_required_years')
    f = lambda v: f'{v:,.0f}' if isinstance(v, (int, float)) else str(v)
    return '\n'.join([
        '**Headline vs PPS Scenario A** (this version; tables below):', '',
        f"- **At target every required year:** K-5 {D['K-5']['at_target_all_required_years']} (PPS A {RA('K-5')}), "
        f"6-8 {D['6-8']['at_target_all_required_years']} (PPS A {RA('6-8')}); meets PPS A every required year at every level.",
        f"- **In range, 2031-32:** K-5 {L('K-5', 'schools_in_range_non_exempt')} of {L('K-5', 'schools_evaluated_non_exempt')}, "
        f"6-8 {L('6-8', 'schools_in_range_non_exempt')} of {L('6-8', 'schools_evaluated_non_exempt')} (non-exempt).",
        f"- **K-5 walking:** avg {L('K-5', 'avg_walk_mi')} mi; past a closer school {f(L('K-5', 'kids_past_closer_school'))}; "
        f"over the bus line {f(L('K-5', 'kids_over_bus_threshold'))}. **6-8:** avg {L('6-8', 'avg_walk_mi')} mi; past a closer "
        f"school {f(L('6-8', 'kids_past_closer_school'))}.",
        f"- **Moves vs PPS Status Quo:** K-5 {f(L('K-5', 'kids_reassigned_vs_status_quo'))}, 6-8 {f(L('6-8', 'kids_reassigned_vs_status_quo'))}.",
        f"- **Feeders:** {L('9-12', 'pct_ms_feeders_to_one_hs')}% of middle zones feed one high school (PPS A 80%); "
        f"{L('6-8', 'n_split_feeders_es_to_ms')} elementary zones split between middle schools.",
        f"- **Robustness:** K-5 schools in range if enrollment is 9% below forecast: {L('K-5', 'schools_in_range_at_minus9pct')} "
        '(PPS A 25); see `out_v2/BRIEFS.md`.'])


def cleanup_section(cand, target, c, t, qc, qt):
    L = lambda s, lev, k: s['levels'][lev].get(k)
    A = lambda s, lev: s['durability']['levels'][lev]['at_target_all_required_years']
    w = json.load(open(os.path.join(C.SOLVER, 'configs', 'v2', f'{cand}.json')))
    lw = {lev: w['levels'][lev].get('weights') for lev in ('K-5', '6-8') if w['levels'][lev].get('weights')}
    rows = [('K-5 sawtooth blocks (teeth)', qt['K-5']['teeth'], qc['K-5']['teeth']),
            ('K-5 fingers (>= 3 thin blocks)', len(qt['K-5']['fingers']), len(qc['K-5']['fingers'])),
            ('K-5 far pockets (>= 3 blocks, >= 0.5 mi past a closer school), kids',
             round(sum(p['kids'] for p in qt['K-5']['far'])), round(sum(p['kids'] for p in qc['K-5']['far']))),
            ('6-8 sawtooth blocks (teeth)', qt['6-8']['teeth'], qc['6-8']['teeth']),
            ('K-5 past a closer school', L(t, 'K-5', 'kids_past_closer_school'), L(c, 'K-5', 'kids_past_closer_school')),
            ('K-5 avg walk (mi)', L(t, 'K-5', 'avg_walk_mi'), L(c, 'K-5', 'avg_walk_mi')),
            ('6-8 past a closer school', L(t, '6-8', 'kids_past_closer_school'), L(c, '6-8', 'kids_past_closer_school')),
            ('K-5 / 6-8 at target all required years', f"{A(t, 'K-5')} / {A(t, '6-8')}", f"{A(c, 'K-5')} / {A(c, '6-8')}"),
            ('ES→MS splits', L(t, '6-8', 'n_split_feeders_es_to_ms'), L(c, '6-8', 'n_split_feeders_es_to_ms')),
            ('Middle zones feeding one HS (%)', L(t, '9-12', 'pct_ms_feeders_to_one_hs'), L(c, '9-12', 'pct_ms_feeders_to_one_hs'))]
    k5 = w['levels']['K-5']
    six = w['levels']['6-8'].get('fixed_run')
    if k5.get('fixed_run'):
        step1 = f"**K-5 lines** taken from the finished re-solve `{k5['fixed_run']}`."
    else:
        kw = k5.get('weights', {})
        bits = []
        if 'perim' in kw:
            bits.append(f"a {kw['perim'] / 3:.0f}× boundary-length cost ({kw['perim']:g} kid-miles per km, K-5 only)")
        if 'past' in kw:
            bits.append(f"a {kw['past'] / 0.25:.0f}× past-a-closer-school cost ({kw['past']:g} kid-mile per kid)")
        step1 = f"**K-5 re-solved** with {' and '.join(bits) or 'stronger line weights'}, starting from the earlier lines (`configs/v2/{cand}.json`)."
    step2 = ('**6-8 kept block for block** from the earlier solve, except where a K-5 block moved and its middle school '
             'followed; middle-school sizes and walks are essentially unchanged.' if six else '**6-8 re-solved** on the new K-5 zones.')
    out = ['**Line cleanup (overnight 2026-10-12/13, Paul: "less saw tooth, less long extensions ... sensible lines").** '
           f'This version replaces the earlier solve (kept in `{target}.prev`). Same plan, cleaner elementary lines:', '',
           f'1. {step1}', f'2. {step2}',
           '3. **Rule-preserving block cleanup** (`smooth_v2.py`): one-block notches move to the school around them and '
           'small pockets are swapped back, only where no school gets further outside its range in any year.', '',
           'Line quality is from `lines_qa.py`. Every rule still holds (`promote_clean.py` checks).', '',
           '| | Before | After |', '|---|---|---|']
    for lab, a, b in rows:
        out.append(f'| {lab} | {a} | {b} |')
    return '\n'.join(out)


def promote(cand, target, dry=False, teeth_ratio=0.85):
    why, c, t, qc, qt = check(cand, target, teeth_ratio)
    if why:
        print(f'{cand} -> {target}: NOT promoted:\n  - ' + '\n  - '.join(why))
        return False
    print(f'{cand} -> {target}: passes all checks')
    if dry:
        return True
    cp, st = os.path.join(OUT, cand + '.staging'), os.path.join(OUT, target + '.staging')
    if os.path.exists(st):
        os.rename(st, st + time.strftime('_old_%Y%m%d%H%M%S'))
    shutil.copytree(cp, st)
    s = sc(st)
    tcfg = json.load(open(os.path.join(C.SOLVER, 'configs', 'v2', f'{target}.json')))
    s['name'] = target
    s['label'] = tcfg.get('label', target) + ' [line cleanup: ' + cand + ']'
    json.dump(s, open(os.path.join(st, 'scorecard.json'), 'w'), indent=1, default=float)
    os.utime(os.path.join(st, 'scorecard.json'))
    old = open(os.path.join(OUT, target, 'TRADEOFFS.md')).read() if os.path.exists(os.path.join(OUT, target, 'TRADEOFFS.md')) else ''
    body = old.split('\n', 1)[1] if '\n' in old else ''
    paras = [p for p in body.split('**Headline')[0].strip().split('\n\n') if not p.startswith('Generated by')]
    narrative = '\n\n'.join(paras + [headline(c), cleanup_section(cand, target, c, t, qc, qt)])
    import report_pps2031 as R
    R.STAGED.add(target)
    R.tradeoffs(target, narrative)
    r = subprocess.run([PY, 'promote_v2.py', target, '--note',
                        f'supersedes the earlier solve (line cleanup from {cand}, overnight 2026-10-12/13; every rule '
                        f'holds; see TRADEOFFS.md "Line cleanup")'], cwd=C.SOLVER, capture_output=True, text=True)
    print(r.stdout[-1500:], r.stderr[-800:])
    return r.returncode == 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('candidate')
    ap.add_argument('target')
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--teeth-ratio', type=float, default=0.85,
                    help='max candidate/target K-5 teeth (0.95 for a later small-gain pass; then fingers may not rise)')
    a = ap.parse_args()
    sys.exit(0 if promote(a.candidate, a.target, a.dry, a.teeth_ratio) else 1)
