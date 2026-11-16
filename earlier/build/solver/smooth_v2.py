"""Line cleanup for a finished v2 run (Paul 2026-10-12 ~21:30: "less saw tooth, less long extensions ... we want
sensible lines").  Re-scores without re-solving; writes out_v2/<run>.staging/ (TRACKS.md write rule).

  python smooth_v2.py <run> [--config <cfg>] [--max-extra 0.15] [--src staging]

Greedy, rule-preserving: a K-5 "tooth" is a block whose shared boundary (Voronoi edge length, common.edges) is mostly
with ONE other school's area (same-school share <= 0.5).  It moves to that school when
  - the extra walk is at most --max-extra miles for that block's kids (and inside the level's max_walk_mi, if any);
  - the move needs no new I-84 / Willamette crossing (metrics.eligible_mask, as the solver);
  - no school, at any level, in any year of the horizon, gets further outside its range (a school in range stays in
    range; one already outside does not get worse), so the at-target counts and the PPS A comparison cannot drop;
  - the school losing the block stays connected (common.adjacency, as check_exclaves.py), and its building block never
    moves.
The block's 6-8 assignment follows its new K-5 school (the middle school that school's other blocks there feed), so
elementary zones stay nested in middle zones; the 6-8 move gets the same checks.  9-12 is not touched (PPS A lines).
Passes repeat until nothing moves, so a long finger erodes from its tip.  Moves are tried in order of extra walk."""
import argparse, json, os, shutil
from collections import defaultdict, deque
import numpy as np, pandas as pd
import common as C, metrics as MX

OUT = os.path.join(C.SOLVER, 'out_v2')


def run(name, cfgname=None, max_extra=0.15, src_staging=False, max_passes=25, toward=None):
    cfg = C.load_config(os.path.join(C.SOLVER, 'configs', 'v2', f'{cfgname or name}.json'))
    cfg['name'] = name
    src = os.path.join(OUT, name + ('.staging' if src_staging else ''))
    # (2026-10-13) runs with optional schools / movable programs: apply the run's own closures and program moves
    C.resolve_config(cfg, json.load(open(os.path.join(src, 'scorecard.json'))))
    st = os.path.join(OUT, name + '.staging')
    plan = {lev: pd.read_parquet(os.path.join(src, f'assign_{lev}.parquet'))['school'].values.astype(object)
            for lev in C.LEVELS}
    before = {lev: plan[lev].copy() for lev in C.LEVELS}
    NB = C.adjacency()[0]
    roots = C.school_block()
    EL = defaultdict(dict)
    for i, j, L in C.edges():
        if L > 0:
            EL[i][j] = L
            EL[j][i] = L
    _, H = C.horizon(cfg)
    YRS = H['years']
    KY = {y: MX.level_kids(cfg, y[:4]) for y in YRS}
    bt = MX.building_table(cfg, plan).set_index('school')
    tot = {y: MX.building_table(cfg, plan, year=y[:4]).set_index('school')['total'].to_dict() for y in YRS}
    lo = {s: (0.0 if bt.loc[s, 'floor_exempt'] else float(bt.loc[s, 'floor'])) for s in bt.index}
    hi = {s: (np.inf if np.isnan(bt.loc[s, 'ceiling']) else float(bt.loc[s, 'ceiling'])) for s in bt.index}

    def viol(s, v):
        return max(0.0, lo[s] - v) + max(0.0, v - hi[s])

    lv = {}
    for lev in ('K-5', '6-8'):
        names = sorted(cfg['levels'][lev]['zoned'])
        refs = MX.load_refs(os.path.join(C.SOLVER, 'configs', 'v2'))
        lv[lev] = {'names': names, 'idx': {n: k for k, n in enumerate(names)}, 'W': C.dist('walk', names),
                   'E': MX.apply_nest_hard(MX.eligible_mask(lev, names, [refs['today'][lev], refs['status_quo'][lev]],
                                                            cfg['levels'][lev].get('same_side', ())),
                                           names, cfg['levels'][lev].get('nest_hard')),
                   'cap': cfg['levels'][lev].get('max_walk_mi')}

    def walk_ok(lev, i, a, b):
        L = lv[lev]
        if b not in L['idx']:
            return False, 0.0
        ka, kb = L['idx'].get(a), L['idx'][b]
        if not L['E'][i, kb]:
            return False, 0.0
        db = float(L['W'][i, kb])
        da = float(L['W'][i, ka]) if ka is not None else db
        if np.isnan(db) or db - da > max_extra + 1e-9:
            return False, 0.0
        if L['cap'] and db > L['cap'] + 1e-9 and db > da:
            return False, 0.0
        return True, db - da

    def stays_connected(lev, i, s):
        asg = plan[lev]
        r = roots.get(s)
        if r is None or r == i:
            return r != i
        nbrs = [j for j in NB[i] if asg[j] == s]
        if not nbrs:
            return True

        def reach(skip):
            seen, q = {r}, deque([r])
            while q:
                k = q.popleft()
                for j in NB[k]:
                    if j not in seen and j != skip and asg[j] == s:
                        seen.add(j)
                        q.append(j)
            return seen
        if asg[r] != s:
            return True
        without = reach(i)
        if all(j in without for j in nbrs):
            return True
        with_i = reach(-1)
        return all(j in without for j in nbrs if j in with_i)

    def size_ok(moves):
        # moves: [(lev, i, a, b)]; no school in any year may get further outside its range
        for y in YRS:
            d = defaultdict(float)
            for lev, i, a, b in moves:
                k = float(KY[y][lev][i])
                d[a] -= k
                d[b] += k
            for s, dv in d.items():
                if abs(dv) < 1e-12 or s not in lo:
                    continue
                v0 = tot[y].get(s, 0.0)
                if viol(s, v0 + dv) > viol(s, v0) + 1e-6:
                    return False
        return True

    def apply(moves):
        for y in YRS:
            for lev, i, a, b in moves:
                k = float(KY[y][lev][i])
                tot[y][a] = tot[y].get(a, 0.0) - k
                tot[y][b] = tot[y].get(b, 0.0) + k
        for lev, i, a, b in moves:
            plan[lev][i] = b

    def undo(moves):
        apply([(lev, i, b, a) for lev, i, a, b in reversed(moves)])

    def ms_follow(i, b):
        # the 6-8 school the new K-5 school's neighbouring blocks feed
        fm = defaultdict(float)
        for j, L in EL[i].items():
            if plan['K-5'][j] == b:
                fm[plan['6-8'][j]] += L
        return max(fm, key=fm.get) if fm else plan['6-8'][i]

    geo = C.blocks()['GEOID'].astype(str).values

    def real_pockets(lev='K-5'):
        a = plan[lev]
        out = []
        for s in sorted(set(a)):
            mem = set(np.nonzero(a == s)[0])
            comps, seen = [], set()
            for i0 in mem:
                if i0 in seen:
                    continue
                comp, q = [], deque([i0])
                seen.add(i0)
                while q:
                    k = q.popleft()
                    comp.append(k)
                    for j in EL[k]:
                        if j in mem and j not in seen:
                            seen.add(j)
                            q.append(j)
                comps.append(comp)
            r = roots.get(s)
            main = next((c for c in comps if r in c), max(comps, key=len))
            for c in comps:
                if c is main or all(geo[i].startswith('41067') for i in c):
                    continue
                if any(a[j] != s for i in c for j in EL[i]):
                    out.append((s, c, main))
        return out

    def pocket_pass(max_comp=12, comp_extra=0.35):
        """(overnight 2026-10-12/13) move each real K-5 pocket to the school(s) around it; if that takes its school
        outside its range, pull blocks bordering the school's main area back in (smallest extra walk first, each
        <= comp_extra mi), all under the same size / connectivity / crossing rules."""
        done = []
        for s, comp, main in real_pockets():
            mv = []
            for i in comp:
                by = defaultdict(float)
                for j, L in EL[i].items():
                    if plan['K-5'][j] != s:
                        by[plan['K-5'][j]] += L
                if not by:          # interior block of the pocket: go with the pocket's dominant neighbour
                    continue
                b = max(by, key=by.get)
                if not walk_ok('K-5', i, s, b)[0]:
                    done.append({'school': s, 'blocks': len(comp), 'failed': f'walk/crossing to {b} for block {geo[i]}'})
                    mv = None
                    break
                mv.append(('K-5', i, s, b))
            if not mv:
                continue
            got = {i for _, i, _, _ in mv}
            tgt = defaultdict(int)
            for _, _, _, b in mv:
                tgt[b] += 1
            dom = max(tgt, key=tgt.get)
            for i in comp:
                if i not in got:
                    if not walk_ok('K-5', i, s, dom)[0]:
                        mv = None
                        break
                    mv.append(('K-5', i, s, dom))
            if not mv:
                continue
            full = []
            for _, i, a_, b in mv:
                full.append(('K-5', i, a_, b))
                m_new = ms_follow(i, b)
                if m_new != plan['6-8'][i] and walk_ok('6-8', i, plan['6-8'][i], m_new)[0]:
                    full.append(('6-8', i, plan['6-8'][i], m_new))
            if size_ok(full):
                apply(full)
                done.append({'school': s, 'blocks': len(comp), 'compensation_blocks': 0})
                continue
            # compensation: blocks of other schools touching s's main area
            mainset = set(main)
            cands = []
            for i in mainset:
                for j in EL[i]:
                    x_ = plan['K-5'][j]
                    if x_ == s or roots.get(x_) == j or j in comp:
                        continue
                    ok, dw = walk_ok('K-5', j, x_, s)
                    if ok or (s in lv['K-5']['idx'] and lv['K-5']['E'][j, lv['K-5']['idx'][s]]
                              and float(lv['K-5']['W'][j, lv['K-5']['idx'][s]]) -
                              float(lv['K-5']['W'][j, lv['K-5']['idx'][x_]]) <= comp_extra):
                        dw = float(lv['K-5']['W'][j, lv['K-5']['idx'][s]]) - float(lv['K-5']['W'][j, lv['K-5']['idx'][x_]])
                        cands.append((dw, j, x_))
            cands = sorted(set(cands))
            apply(full)
            pulled = []
            success = False
            for dw, j, x_ in cands:
                if len(pulled) >= max_comp:
                    break
                if plan['K-5'][j] != x_ or not stays_connected('K-5', j, x_):
                    continue
                step = [('K-5', j, x_, s)]
                m_new = ms_follow(j, s)
                if m_new != plan['6-8'][j]:
                    if not stays_connected('6-8', j, plan['6-8'][j]):
                        continue
                    step.append(('6-8', j, plan['6-8'][j], m_new))
                if not size_ok(step):      # the giving school must not get further outside its range
                    continue
                apply(step)
                pulled += step
                # sizes of everything touched, measured against the state before this pocket's moves
                undo(pulled)
                undo(full)
                ok_all = size_ok(full + pulled)
                apply(full)
                apply(pulled)
                if ok_all:
                    success = True
                    break
            if success:
                done.append({'school': s, 'blocks': len(comp),
                             'compensation_blocks': len([m for m in pulled if m[0] == 'K-5'])})
            else:
                done.append({'school': s, 'blocks': len(comp), 'failed': f'no size-preserving compensation within '
                             f'{max_comp} blocks / {comp_extra} mi ({len(cands)} candidates)'})
                undo(pulled)
                undo(full)
        return done

    # toward=<run>: only move a block back to the school it has in that run (e.g. status_quo for the fewest-moves plan,
    # so every cleanup move also undoes a reassignment); pocket swaps are skipped in this mode
    TW = (pd.read_parquet(os.path.join(OUT, toward, 'assign_K-5.parquet'))['school'].values if toward else None)
    log, moved = [], 0
    done_blocks = set()
    REJ = defaultdict(int)
    pockets_fixed = [] if toward else pocket_pass()
    for p in range(max_passes):
        a5 = plan['K-5']
        cands = []
        for i in range(len(a5)):
            nb = EL.get(i)
            if not nb:
                continue
            tl = sum(nb.values())
            same = sum(L for j, L in nb.items() if a5[j] == a5[i])
            if same / tl > 0.5 + 1e-9:
                continue
            by = defaultdict(float)
            for j, L in nb.items():
                if a5[j] != a5[i]:
                    by[a5[j]] += L
            b = max(by, key=by.get)
            if TW is not None and TW[i] != b:
                continue
            ok, dw = walk_ok('K-5', i, a5[i], b)
            if ok:
                cands.append((dw, i, b))
            elif p == 0:
                REJ['walk']+=1
        cands.sort()
        n_pass = 0
        for dw, i, b in cands:
            a = plan['K-5'][i]
            if a == b or roots.get(a) == i or i in done_blocks:
                continue
            same = sum(L for j, L in EL[i].items() if plan['K-5'][j] == a)
            if same / sum(EL[i].values()) > 0.5 + 1e-9:
                continue
            if not stays_connected('K-5', i, a):
                REJ['connect']+=1
                continue
            moves = [('K-5', i, a, b)]
            m_old = plan['6-8'][i]
            fm = defaultdict(float)
            for j, L in EL[i].items():
                if plan['K-5'][j] == b:
                    fm[plan['6-8'][j]] += L
            m_new = max(fm, key=fm.get) if fm else m_old
            if m_new != m_old:
                if roots.get(m_old) == i or not walk_ok('6-8', i, m_old, m_new)[0] or not stays_connected('6-8', i, m_old):
                    REJ['ms']+=1
                    continue
                moves.append(('6-8', i, m_old, m_new))
            if not size_ok(moves):
                REJ['size']+=1
                continue
            apply(moves)
            done_blocks.add(i)
            n_pass += 1
        log.append(n_pass)
        moved += n_pass
        if not n_pass:
            break

    K = MX.level_kids(cfg, '2031')
    chg = {lev: np.where(before[lev] != plan[lev])[0] for lev in ('K-5', '6-8')}
    info = {'when': '2026-10-12', 'rule': (f'tooth = same-school share of boundary <= 0.5; move to the dominant neighbour '
                                          f'school if extra walk <= {max_extra} mi, no new I-84/river crossing, no school '
                                          'further outside its range in any horizon year, losing school stays connected; '
                                          '6-8 follows the new K-5 school; 9-12 untouched'),
            'pockets_fixed': pockets_fixed, 'passes': log, 'rejected_first_try': dict(REJ), 'blocks_moved': {lev: int(len(v)) for lev, v in chg.items()},
            'kids_moved_2031': {lev: round(float(K[lev][v].sum()), 1) for lev, v in chg.items()}}

    os.makedirs(st, exist_ok=True)
    if os.path.abspath(src) != os.path.abspath(st):
        for f in os.listdir(src):
            if f not in ('scorecard.json', 'schools.csv') and not f.startswith('assign_') and \
                    os.path.isfile(os.path.join(src, f)):
                shutil.copy2(os.path.join(src, f), os.path.join(st, f))
    old = json.load(open(os.path.join(src, 'scorecard.json')))
    keep = {k: v for k, v in old.items() if k not in ('levels', 'durability', 'programs', 'name', 'label', 'basis')}
    keep['line_cleanup'] = info
    keep['line_cleanup_before'] = {lev: {k: old['levels'][lev].get(k) for k in
                                         ('avg_walk_mi', 'kids_past_closer_school', 'kids_over_bus_threshold',
                                          'kids_reassigned_vs_status_quo')} for lev in ('K-5', '6-8')}
    refs = MX.load_refs(os.path.join(C.SOLVER, 'configs', 'v2'))
    sc = MX.write_plan(st, cfg, plan, refs, extra=keep)
    return info, old, sc


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('runs', nargs='+')
    ap.add_argument('--config')
    ap.add_argument('--max-extra', type=float, default=0.15)
    ap.add_argument('--src', choices=['final', 'staging'], default='final')
    ap.add_argument('--toward', help='only move blocks back to their school in this run (e.g. status_quo)')
    a = ap.parse_args()
    for r in a.runs:
        info, old, sc = run(r, a.config, a.max_extra, a.src == 'staging', toward=a.toward)
        print(r, json.dumps(info))
        for lev in ('K-5', '6-8'):
            o, n = old['levels'][lev], sc['levels'][lev]
            print(f'  {lev}: walk {o.get("avg_walk_mi")} -> {n.get("avg_walk_mi")}; past closer '
                  f'{o.get("kids_past_closer_school")} -> {n.get("kids_past_closer_school")}; in range '
                  f'{o.get("schools_in_range_non_exempt")} -> {n.get("schools_in_range_non_exempt")}')
        d = sc['durability']
        print('  at target all required years:', {lev: d['levels'][lev]['at_target_all_required_years'] for lev in C.LEVELS},
              '| meets PPS A:', (sc.get('durability_reference') or d.get('reference') or {}).get(
                  'meets_reference_every_required_year'))
