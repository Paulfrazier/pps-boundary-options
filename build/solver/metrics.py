"""Scorecard: the same metrics for any plan (baseline or solved option), at every level.

A plan is {level: np.array of school names per block (len 9295)} plus its config (programs,
K-8 list, floors).  Kids are neighborhood-program kids on the 2031-32 basis unless noted.

Usage:  python metrics.py            -> evaluates today / status_quo / scenario_A / scenario_B and
                                        writes out/baselines/<name>/...
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd

import common as C
import v2 as V2


def is_v2(cfg):
    return cfg.get('model_version') == 'v2'


def capacity(cfg, name):
    caps = cfg.get('capacity_overrides', {})
    return V2.capacity(name, caps) if is_v2(cfg) else C.capacity(name, caps)

WITHIN = {'K-5': [0.5, 1.0, 1.5], '6-8': [0.5, 1.0, 1.5], '9-12': [0.5, 1.0, 1.5, 2.0]}
BUS = {'K-5': 1.0, '6-8': 1.5, '9-12': 1.5}   # ORS 327.043 / PPS service guidelines


def plan_from_columns(cfg):
    b = C.blocks()
    plan = {lev: b[cfg['levels'][lev]['assign']].values.astype(object) for lev in C.LEVELS}
    return V2.reassign(cfg, plan) if is_v2(cfg) else plan


def level_kids(cfg, year='2031'):
    if is_v2(cfg):
        return dict(V2.kids(cfg, year))
    K = dict(C.kids(year, cfg.get('lr_nbhd_share', 0.02)))
    for prog in cfg.get('dissolve_programs', []):
        extra = C.dissolved_program_kids(prog, year)
        for lev in C.LEVELS:
            K[lev] = K[lev] + extra[lev]
    return K


def eligible_mask(lev, names, ref_plans=(), same_side=()):
    """(n_blocks, n_schools) bool: school reachable without a new I-84 / Willamette crossing.
    A school is eligible if its zone is one of the block's allowed zones (pps-model az), or the
    zone of the block's school in a reference plan (today / Status Quo), i.e. an existing crossing.
    same_side: schools that take no existing crossing either -- only blocks on their own side of I-84 / the river
    (Paul 2026-10-14: "keep sunnyside on one side of i84"); config levels.<lev>.same_side."""
    az, _ = C.block_zones()
    reg = C.school_region()
    allowed = [set(a) for a in az]
    for rp in ref_plans:
        for i, s in enumerate(rp):
            if s in reg:
                allowed[i].add(reg[s])
    M = np.zeros((len(az), len(names)), dtype=bool)
    for k, n in enumerate(names):
        r = reg[n]
        M[:, k] = [r in a for a in allowed]
    if same_side:
        _, z = C.block_zones()
        z = np.array(z)
        for k, n in enumerate(names):
            if n in same_side:
                M[:, k] &= (z == reg[n])
    return M


def program_totals(cfg, lev, year='2031'):
    if is_v2(cfg):
        return V2.fixed(cfg, lev, year)
    out = {}
    for host, keys in cfg['levels'][lev].get('programs', {}).items():
        out[host] = sum(C.program_size(k, year) for k in keys)
    return out


def building_table(cfg, plan, year='2031', scale=1.0):
    """One row per open building: neighborhood + program counts per level, building total, floor,
    ceiling, in-range flag."""
    K = level_kids(cfg, year)
    caps = cfg.get('capacity_overrides', {})
    floors = cfg['floors']
    exempt = set(cfg.get('exempt_floor', []))
    k8 = set(cfg['levels']['K-5'].get('k8', []))
    rows = {}
    for lev in C.LEVELS:
        asg = plan[lev]
        prog = program_totals(cfg, lev, year)
        names = set(cfg['levels'][lev]['zoned']) | set(prog)
        df = pd.DataFrame({'s': asg, 'k': K[lev]}).groupby('s')['k'].sum()
        for n in names:
            r = rows.setdefault(n, {'school': n})
            r[f'nbhd_{lev}'] = float(df.get(n, 0.0)) * scale
            r[f'prog_{lev}'] = prog.get(n, 0.0) * scale
            r[f'zoned_{lev}'] = n in cfg['levels'][lev]['zoned']
    out = []
    for n, r in rows.items():
        for lev in C.LEVELS:
            r.setdefault(f'nbhd_{lev}', 0.0)
            r.setdefault(f'prog_{lev}', 0.0)
            r.setdefault(f'zoned_{lev}', False)
        tot = sum(r[f'nbhd_{l}'] + r[f'prog_{l}'] for l in C.LEVELS)
        if n in k8:
            typ = 'K-8'
        elif r['nbhd_K-5'] + r['prog_K-5'] > 0 or r['zoned_K-5']:
            typ = 'K-5'
        elif r['nbhd_6-8'] + r['prog_6-8'] > 0 or r['zoned_6-8']:
            typ = '6-8'
        else:
            typ = '9-12'
        cap = capacity(cfg, n)
        ceil = cap
        if typ == 'K-5' and cfg.get('ceiling_k5_max'):
            ceil = min(cap, cfg['ceiling_k5_max']) if not np.isnan(cap) else cfg['ceiling_k5_max']
        floor = floors[typ]
        r.update({'type': typ, 'program_only': not any(r[f'zoned_{l}'] for l in C.LEVELS),
                  'total': tot, 'capacity': cap, 'floor': floor, 'ceiling': ceil,
                  'utilization': tot / cap if cap and not np.isnan(cap) else np.nan,
                  'floor_exempt': n in exempt})
        r['below_floor'] = (not r['floor_exempt']) and tot < floor - 1e-6
        r['above_ceiling'] = (not np.isnan(ceil)) and tot > ceil + 1e-6
        r['in_range'] = not r['below_floor'] and not r['above_ceiling']
        r['short_by'] = max(0.0, floor - tot) if not r['floor_exempt'] else 0.0
        r['over_by'] = max(0.0, tot - ceil) if not np.isnan(ceil) else 0.0
        out.append(r)
    df = pd.DataFrame(out).sort_values(['type', 'school']).reset_index(drop=True)
    return df


def durability(cfg, plan, bt=None, horizon=None):
    """Schools at target each year of the config's horizon (common.HORIZONS; default psu2041 = 2031-32 .. 2040-41)
    and the first year each school leaves its range.  Counted over zoned, non-exempt, non-focus schools of each level
    (K-8s at K-5, scaled band by band); program-only buildings are listed separately.
    horizon: override the config's horizon name (the solver scores its reference plan on the option's horizon)."""
    bt = building_table(cfg, plan) if bt is None else bt
    focus = set(cfg.get('focus', []))
    hname, H = C.horizon({'horizon': horizon} if horizon else cfg)
    YRS, REQ = H['years'], H['required']
    R = {lev: C.year_ratios(lev) for lev in C.LEVELS}
    out = {'years': YRS, 'basis': 'PSU medium Table 5.2 district ratio vs 2031-32, applied to every school at the level',
           'levels': {}}
    BTY = None
    if hname != 'psu2041' and not is_v2(cfg):
        raise ValueError(f'horizon {hname} needs model v2 (per-school sizes by year)')
    if is_v2(cfg):
        out['basis'] = ('model v2: every population scaled by its own PSU July 2026 Table 5.5 row by year (2031-32 to '
                        '2035-36); 2036-37 to 2040-41 extend each row with the PSU medium district trend (Table 5.2)')
        BTY = {y: building_table(cfg, plan, year=y[:4]).set_index('school') for y in YRS}
    if hname == 'pps2031':
        out['basis'] = ('model v2: every population scaled by its own PSU July 2026 Table 5.5 row by year. Required '
                        'window 2027-28 to 2031-32 = PPS Family Guide projection years (p. 1, "Estimates cover 2027-28 '
                        'through 2031-32"); 2032-33 to 2035-36 reported only (last year of PSU Table 5.5). No '
                        'extension past 2035-36.')
        out['horizon'] = hname
        out['required_years'] = REQ
        out['reported_years'] = [y for y in YRS if y not in REQ]
    for lev in C.LEVELS:
        typ = {'K-5': ('K-5', 'K-8'), '6-8': ('6-8',), '9-12': ('9-12',)}[lev]
        sel = bt[bt['type'].isin(typ) & ~bt['school'].isin(focus) & ~bt['floor_exempt']]
        counts = {y: 0 for y in YRS}
        counts_prog = {y: 0 for y in YRS}
        first = {}
        for _, r in sel.iterrows():
            fell = None
            inr = []
            for y in YRS:
                if BTY is not None:
                    size = float(BTY[y].loc[r['school'], 'total']) if r['school'] in BTY[y].index else 0.0
                else:
                    size = sum((r[f'nbhd_{l}'] + r[f'prog_{l}']) * R[l][y] for l in C.LEVELS)
                ok = size >= r['floor'] - 1e-6 and (np.isnan(r['ceiling']) or size <= r['ceiling'] + 1e-6)
                inr.append(bool(ok))
                if ok:
                    (counts_prog if r['program_only'] else counts)[y] += 1
                elif fell is None:
                    fell = (y, round(size - (r['floor'] if size < r['floor'] else r['ceiling']), 1))
            first[r['school']] = {'first_year_out': fell[0] if fell else None, 'by': fell[1] if fell else None,
                                  'sizes_by_year': ({y: round(float(BTY[y].loc[r['school'], 'total']), 1) for y in YRS}
                                                    if BTY is not None else None),
                                  'program_only': bool(r['program_only']), 'size_2031': round(r['total'], 1),
                                  # site request 2026-10-12: aligned with durability.years
                                  'in_range_by_year': inr}
            if hname == 'pps2031':
                first[r['school']]['in_range_all_required_years'] = all(
                    ok for y, ok in zip(YRS, inr) if y in REQ)
                first[r['school']]['in_range_all_years'] = all(inr)
        zon = sel[~sel['program_only']]
        L = {'n_zoned_non_exempt': int(len(zon)), 'at_target_zoned': counts,
             'n_program_only': int(sel['program_only'].sum()),
             'at_target_program_only': counts_prog, 'schools': first}
        n_all = int(sum(1 for s, v in first.items() if v['first_year_out'] is None and not v['program_only']))
        if hname == 'psu2041':
            L['durable_through_2040_41'] = n_all
        else:
            L['at_target_all_required_years'] = int(sum(1 for v in first.values()
                                                        if v['in_range_all_required_years'] and not v['program_only']))
            L['at_target_all_years_to_2035_36'] = n_all
        out['levels'][lev] = L
    return out


def durability_vs_reference(cfg, dur):
    """(pps2031) Scenario A's counts on the same horizon, and whether this plan meets or beats them in every
    required year at every level."""
    ref = (cfg.get('durability') or {}).get('reference', 'scenario_A')
    if cfg.get('name') == ref:
        return None
    p = os.path.join(C.SOLVER, 'configs', 'v2', f'{ref}.json')
    rc = C.load_config(p)
    rd = durability(rc, plan_from_columns(rc), horizon=C.horizon(cfg)[0])
    out = {'reference': ref, 'levels': {}}
    short = []
    for lev in C.LEVELS:
        a, b = dur['levels'][lev], rd['levels'][lev]
        out['levels'][lev] = {'at_target_zoned': b['at_target_zoned'],
                              'at_target_all_required_years': b['at_target_all_required_years']}
        for y in dur['required_years']:
            if a['at_target_zoned'][y] < b['at_target_zoned'][y]:
                short.append({'level': lev, 'year': y, 'plan': a['at_target_zoned'][y],
                              'reference': b['at_target_zoned'][y]})
    out['short_in_required_years'] = short
    out['meets_reference_every_required_year'] = not short
    return out


def _feeders(asg_from, asg_to, w, min_share=0.05, min_kids=5.0):
    df = pd.DataFrame({'a': asg_from, 'b': asg_to, 'w': w})
    g = df.groupby(['a', 'b'])['w'].sum().reset_index()
    out = {}
    for a, gg in g.groupby('a'):
        tot = gg['w'].sum()
        dest = {r.b: round(float(r.w), 1) for r in gg.itertuples() if r.w >= max(min_share * tot, min_kids)}
        if not dest and len(gg):
            dest = {gg.sort_values('w').iloc[-1]['b']: round(float(tot), 1)}
        out[a] = dest
    return out


def dissimilarity(asg, K, p):
    df = pd.DataFrame({'s': asg, 'poc': K * p, 'wh': K * (1 - p)}).groupby('s').sum()
    return float(0.5 * np.abs(df['poc'] / df['poc'].sum() - df['wh'] / df['wh'].sum()).sum())


def level_metrics(cfg, plan, lev, refs):
    K = level_kids(cfg, '2031')[lev]
    asg = plan[lev]
    names = sorted(set(cfg['levels'][lev]['zoned']))
    col = {n: k for k, n in enumerate(names)}
    W = C.dist('walk', names)
    rows = np.arange(len(asg))
    ai = np.array([col.get(s, -1) for s in asg])
    if (ai < 0).any():
        bad = sorted(set(asg[ai < 0]))
        raise ValueError(f'{lev}: blocks assigned to schools not in zoned list: {bad}')
    d = W[rows, ai].astype(float)
    tot = K.sum()
    m = {'kids': round(float(tot), 1), 'avg_walk_mi': round(float((K * d).sum() / tot), 3)}
    for t in WITHIN[lev]:
        m[f'pct_within_{t}mi'] = round(100 * float(K[d <= t].sum() / tot), 1)
    m['kids_over_bus_threshold'] = round(float(K[d > BUS[lev]].sum()), 0)
    m['bus_threshold_mi'] = BUS[lev]
    if lev != 'K-5':
        Bk = C.dist('bike', names)
        db = Bk[rows, ai].astype(float)
        m['avg_bike_mi'] = round(float((K * db).sum() / tot), 3)
    # kids past a closer open school (eligible = no new hard-edge crossing)
    ref_plans = [refs[r][lev] for r in ('today', 'status_quo') if r in refs]
    E = eligible_mask(lev, names, ref_plans)
    Wm = np.where(E, W, np.inf)
    dmin = Wm.min(axis=1)
    margin = cfg.get('past_margin_miles', 0.25)
    past = d - dmin >= margin
    m['kids_past_closer_school'] = round(float(K[past].sum()), 0)
    m['past_margin_mi'] = margin
    # moves
    p = C.poc_share()
    for rname in ('status_quo', 'today'):
        if rname in refs:
            mv = refs[rname][lev] != asg
            m[f'kids_reassigned_vs_{rname}'] = round(float(K[mv].sum()), 0)
            if rname == 'status_quo':
                m['poc_share_of_movers_vs_status_quo'] = round(float((K * p)[mv].sum() / max(K[mv].sum(), 1e-9)), 3)
    m['poc_share_district'] = round(float((K * p).sum() / tot), 3)
    m['dissimilarity_index'] = round(dissimilarity(asg, K, p), 3)
    return m


def scorecard(cfg, plan, refs):
    """refs: {'today': plan, 'status_quo': plan}"""
    bt = building_table(cfg, plan)
    bt25 = building_table(cfg, plan, year='2025')
    bt91 = building_table(cfg, plan, scale=0.91)
    focus = set(cfg.get('focus', []))
    sc = {'name': cfg['name'], 'label': cfg.get('label', ''), 'basis': cfg.get('basis'), 'levels': {}}
    K = level_kids(cfg, '2031')
    for lev in C.LEVELS:
        m = level_metrics(cfg, plan, lev, refs)
        typ = {'K-5': ('K-5', 'K-8'), '6-8': ('6-8', 'K-8'), '9-12': ('9-12',)}[lev]
        sel = bt[bt['type'].isin(typ) & ~bt['school'].isin(focus)]
        # K-8 buildings are judged on their K-8 total and appear in both the K-5 and 6-8 lists
        ev = sel[~sel['floor_exempt']]
        m['schools_open'] = int(len(sel))
        m['schools_in_range'] = int(sel['in_range'].sum())   # exempt schools: in range = under ceiling
        m['schools_evaluated_non_exempt'] = int(len(ev))
        m['schools_in_range_non_exempt'] = int(ev['in_range'].sum())
        m['below_floor'] = {r.school: round(r.total) for r in sel.itertuples() if r.below_floor}
        m['above_ceiling'] = {r.school: round(r.total) for r in sel.itertuples() if r.above_ceiling}
        m['avg_utilization'] = round(float(sel['utilization'].mean()), 3)
        m['min_size'] = round(float(sel['total'].min()))
        m['max_size'] = round(float(sel['total'].max()))
        sel25 = bt25[bt25['school'].isin(sel['school'])]
        m['schools_in_range_2025_26_basis'] = int(sel25['in_range'].sum())
        sel91 = bt91[bt91['school'].isin(sel['school'])]
        m['schools_in_range_at_minus9pct'] = int(sel91['in_range'].sum())
        sc['levels'][lev] = m
    # feeders
    f_es_ms = _feeders(plan['K-5'], plan['6-8'], K['6-8'])
    f_ms_hs = _feeders(plan['6-8'], plan['9-12'], K['9-12'])
    zoned_es = set(cfg['levels']['K-5']['zoned'])
    zoned_ms = set(cfg['levels']['6-8']['zoned'])
    split_es = {a: d for a, d in f_es_ms.items() if a in zoned_es and len(d) > 1}
    split_ms = {a: d for a, d in f_ms_hs.items() if a in zoned_ms and len(d) > 1}
    sc['levels']['6-8']['split_feeders_es_to_ms'] = split_es
    sc['levels']['6-8']['n_split_feeders_es_to_ms'] = len(split_es)
    sc['levels']['9-12']['split_feeders_ms_to_hs'] = split_ms
    sc['levels']['9-12']['n_split_feeders_ms_to_hs'] = len(split_ms)
    sc['levels']['9-12']['pct_ms_feeders_to_one_hs'] = round(100 * (1 - len(split_ms) / max(len(zoned_ms), 1)), 1)
    hs = bt[bt['type'] == '9-12']
    hs = hs[hs['zoned_9-12']]
    sc['levels']['9-12']['hs_range'] = round(float(hs['total'].max() - hs['total'].min()))
    # DLI / program moves vs today
    sc['programs'] = program_moves(cfg)
    if is_v2(cfg):
        pop = V2.population(cfg)
        sc['programs']['v2_follow'] = pop['program_moves']
        sc['programs']['dli_kids_arriving_2031'] = round(sum(m['arrive_2031'] for m in pop['program_moves']))
        sc['model_v2_notes'] = pop['notes']
        sc['model_version'] = 'v2'
    sc['durability'] = durability(cfg, plan, bt)
    if C.horizon(cfg)[0] == 'pps2031':
        vr = durability_vs_reference(cfg, sc['durability'])
        if vr:
            sc['durability']['reference'] = vr
    sc['split_feeder_rule'] = 'a destination counts if it gets >=5% of the feeder\'s kids and >=5 kids'
    return sc, bt, bt25


def program_moves(cfg):
    today = C.load_config(os.path.join(C.SOLVER, 'configs', 'today.json'))
    host_today = {}
    for lev in C.LEVELS:
        for h, keys in today['levels'][lev]['programs'].items():
            for k in keys:
                host_today[k] = h
    open_bldgs = set()
    for lev in C.LEVELS:
        open_bldgs |= set(cfg['levels'][lev]['zoned']) | set(cfg['levels'][lev].get('programs', {}))
    moved_close, moved_prog, rows = 0.0, 0.0, []
    for lev in C.LEVELS:
        for h, keys in cfg['levels'][lev].get('programs', {}).items():
            for k in keys:
                if host_today.get(k) != h:
                    n = C.program_size(k)
                    why = 'building closes' if host_today.get(k) not in open_bldgs else 'program moves'
                    if host_today.get(k) == 'Cesar Chavez' and k.endswith('6-8'):
                        why = 'grades 6-8 leave the K-8'
                    rows.append({'program': k, 'from': host_today.get(k), 'to': h, 'kids_2031': n, 'why': why})
                    if why == 'building closes':
                        moved_close += n
                    else:
                        moved_prog += n
    return {'dli_kids_moved_total': round(moved_close + moved_prog), 'because_building_closes': round(moved_close),
            'because_program_moves': round(moved_prog), 'moves': rows}


def per_school_csv(cfg, plan, bt, bt25, path):
    """Per-school stats incl. avg walk of its neighborhood kids at each level."""
    K = level_kids(cfg, '2031')
    out = bt.copy()
    out['total_2025_26_basis'] = out['school'].map(bt25.set_index('school')['total'])
    for lev in C.LEVELS:
        names = sorted(set(cfg['levels'][lev]['zoned']))
        W = C.dist('walk', names)
        col = {n: k for k, n in enumerate(names)}
        ai = np.array([col[s] for s in plan[lev]])
        d = W[np.arange(len(ai)), ai]
        df = pd.DataFrame({'s': plan[lev], 'k': K[lev], 'kd': K[lev] * d, 'far': K[lev] * (d > BUS[lev]),
                           'poc': K[lev] * C.poc_share()})
        g = df.groupby('s').sum()
        out[f'avg_walk_{lev}'] = out['school'].map((g['kd'] / g['k']).round(3))
        out[f'kids_over_bus_{lev}'] = out['school'].map(g['far'].round(1))
        out[f'poc_share_{lev}'] = out['school'].map((g['poc'] / g['k']).round(3))
    num = out.select_dtypes('number').columns
    out[num] = out[num].round(3)
    out.to_csv(path, index=False)
    return out


def write_plan(outdir, cfg, plan, refs, extra=None):
    os.makedirs(outdir, exist_ok=True)
    b = C.blocks()
    for lev in C.LEVELS:
        pd.DataFrame({'idx': np.arange(len(b)), 'GEOID': b['GEOID'].values, 'school': plan[lev]}).to_parquet(
            os.path.join(outdir, f'assign_{lev}.parquet'), index=False)
    sc, bt, bt25 = scorecard(cfg, plan, refs)
    if extra:
        sc.update(extra)
    per_school_csv(cfg, plan, bt, bt25, os.path.join(outdir, 'schools.csv'))
    with open(os.path.join(outdir, 'scorecard.json'), 'w') as f:
        json.dump(sc, f, indent=1, default=float)
    return sc


def load_refs(cfgdir=None):
    out = {}
    for n in ('today', 'status_quo'):
        cfg = C.load_config(os.path.join(cfgdir or os.path.join(C.SOLVER, 'configs'), f'{n}.json'))
        out[n] = plan_from_columns(cfg)
    return out


def outdir(cfg):
    return os.path.join(C.SOLVER, 'out_v2' if is_v2(cfg) else 'out')


def headline(sc):
    rows = []
    for lev in C.LEVELS:
        m = sc['levels'][lev]
        rows.append({k: v for k, v in m.items() if not isinstance(v, dict)})
    return pd.DataFrame(rows, index=C.LEVELS).T


if __name__ == '__main__':
    args = sys.argv[1:]
    v2run = '--v2' in args
    args = [a for a in args if a != '--v2']
    cfgdir = os.path.join(C.SOLVER, 'configs', 'v2') if v2run else os.path.join(C.SOLVER, 'configs')
    refs = load_refs(cfgdir)
    names = args or ['today', 'status_quo', 'scenario_A', 'scenario_B']
    for n in names:
        cfg = C.load_config(os.path.join(cfgdir, f'{n}.json'))
        plan = plan_from_columns(cfg)
        od = os.path.join(C.SOLVER, 'out_v2', n) if v2run else os.path.join(C.SOLVER, 'out', 'baselines', n)
        sc = write_plan(od, cfg, plan, refs)
        print('==', n)
        print(headline(sc).to_string())
        print(json.dumps({l: {'below': sc['levels'][l]['below_floor'], 'above': sc['levels'][l]['above_ceiling']}
                          for l in C.LEVELS}))
