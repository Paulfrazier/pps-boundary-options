"""Model v2 (2026-10-12, models track): fixes 1-6 of PLAN.md "Models track status".

A config opts in with  "model_version": "v2"  and a "v2" block (see gen_configs_v2.py).  v1 configs never touch
this module, so v1 results stay reproducible.

  fix 1  focus-lottery students at Sunnyside / Bridger / Buckman are a separate population: in-zone kids stay on
         the area's blocks; lottery kids sit at the host while its focus runs, and return to their own
         neighborhood blocks when it ends (PPS Family Guide p. 2 footnote)                 -> cfg v2.focus_lottery
  fix 2  ~117 Lent-area non-DLI kids (PPS capture report Oct 2025) live on Lent-area blocks; they are Marysville
         students today (taken out of Marysville's calibration) and follow the Lent area's line in a plan
                                                                                           -> cfg v2.lent_nondli
  fix 2b (2026-10-22, Paul: Rigler-area non-DLI kids) the Rigler analog: ~152 Rigler-area PPS students attend another
         neighborhood school (capture report Oct 2025, Rigler row); per destination school they are put on Rigler-area
         blocks and taken out of that school's own area (Scott 105 per PPS data; the rest a walk stand-in)
                                                                                           -> cfg v2.rigler_nondli
  fix 3  per-move, per-year DLI arrival shares implied by PPS projections (build/data/v2/dli_follow.json);
         non-arrivals stay at the sending building if it still serves those grades, else go home
  fix 4  capacities: PPS School Profiles 2025-26 functional capacity (build/data/v2/capacity_2025_26.csv)
  fix 6  every population is scaled by its own PSU Table 5.5 row, year by year (2027-28 .. 2035-36), and
         extended to 2040-41 with the PSU medium district trend by level (Table 5.2)
(fix 5 is a wording fix in build/research/targets.md.)
"""
from __future__ import annotations

import functools
import json
import os
import re

import numpy as np
import pandas as pd

import common as C

V2 = os.path.join(C.DATA, 'v2')
YEARS_ALL = [2025] + list(range(2027, 2041))      # 2025 = modeled 2025-26 basis (unscaled)
DLI_PREFIX = 'DLI '


def _norm(s):
    return re.sub(r'[^a-z]', '', str(s).lower().replace('é', 'e').replace('á', 'a'))


# ---------------------------------------------------------------------------------------------
# PSU Table 5.5 by year
# ---------------------------------------------------------------------------------------------
@functools.lru_cache(maxsize=None)
def psu_by_year():
    """canon name -> program -> {year: count}, 2023..2035 (fall year)."""
    t = pd.read_csv(os.path.join(V2, 'psu_table5_5_by_year.csv'))
    canon = {_norm(n): n for n in C.schools_table().index}
    canon.update({_norm(k): v for k, v in C.PSU2CANON.items()})
    canon.update({'cesarchavez': 'Cesar Chavez', 'idabwellsbarnett': 'Ida B. Wells', 'harriettubman': 'Tubman',
                  'mlkjr': 'MLK Jr', 'bensonpolytechnic': 'Benson', 'davinci': 'da Vinci'})
    out = {}
    for _, r in t.iterrows():
        n = canon.get(_norm(r['name_raw']), r['name_raw'])
        out.setdefault(n, {})[r['program']] = {y: float(r[f'y{y}']) for y in range(2023, 2036)}
    return out


def _district_ext(level, y, y0=2035):
    """PSU medium district trend multiplier from y0 to y (Table 5.2, common.PSU_MEDIUM)."""
    v = C.PSU_MEDIUM[level]
    i = lambda yy: yy - 2031
    return v[i(y)] / v[i(y0)]


def series_ratio(series: dict, level: str, y: int, base: int = 2025):
    """series(y)/series(base) with years after 2035 extended by the district medium trend for `level`."""
    if y == base:
        return 1.0
    if y <= 2035:
        return series[y] / series[base]
    return series[2035] / series[base] * _district_ext(level, y)


def area_row(level, area):
    """The PSU row v1 uses to scale an area (common.scale_factors logic)."""
    psu = psu_by_year()
    rows = psu[area]
    if level == 'K-5':
        if area in C.LR_AREAS:
            return rows['Spanish']
        if area == 'Cesar Chavez':
            return rows['Neighborhood']
        if C.schools_table().loc[area, 'level'] == 'K-8':
            return rows['Total']
    if area == 'Cesar Chavez':
        return rows['Neighborhood']
    return rows.get('Neighborhood', rows['Total'])


@functools.lru_cache(maxsize=None)
def area_year_factor(level):
    """{area: {year: factor}}: multiply 2025-26 modeled block kids by this to get year y.
    = v1 2031 scale factor x PSU_area(y)/PSU_area(2031) (2032-35 from Table 5.5, later years district trend)."""
    f31 = C.scale_factors()[level]
    out = {}
    for a, f in f31.items():
        s = area_row(level, a)
        out[a] = {2025: 1.0}
        for y in YEARS_ALL[1:]:
            out[a][y] = f * series_ratio(s, level, y, base=2031)
    return out


# ---------------------------------------------------------------------------------------------
# Programs by year
# ---------------------------------------------------------------------------------------------
def program_series(key):
    """{year: size} for a common.PROGRAMS key, 2025..2040 (Chavez K-5/6-8 split as v1)."""
    psu = psu_by_year()
    host, prog = key.split('|')
    lev = C.PROGRAMS[key][2]
    if host == 'Cesar Chavez':
        s = psu['Cesar Chavez']['Spanish']
        sh = C._CH_K5 if prog.endswith('K-5') else 1 - C._CH_K5
        base = {y: v * sh for y, v in s.items()}
    elif host == 'Richmond':
        base = psu['Richmond']['Total']
    else:
        base = psu[host][prog]
    out = {}
    for y in YEARS_ALL:
        out[y] = base[2025] * series_ratio(base, lev, y, base=2025)
    # consistency with v1 PROGRAMS (2025-26, 2031-32)
    n25, n31, _ = C.PROGRAMS[key]
    assert abs(out[2025] - n25) < 1 and abs(out[2031] - n31) < 1, (key, out[2025], n25, out[2031], n31)
    return out


def focus_series(name):
    psu = psu_by_year()
    base = psu[name]['Total']
    lev = '6-8' if name == 'da Vinci' else 'K-5'
    return {y: base[2025] * series_ratio(base, lev, y) for y in YEARS_ALL}


@functools.lru_cache(maxsize=None)
def follow_table():
    return json.load(open(os.path.join(V2, 'dli_follow.json')))


def follow_rate(key, y):
    ft = follow_table()
    m = ft['moves'].get(key)
    if m is None:
        return ft['_default']
    yy = str(min(max(y, 2027), 2031))
    return m['by_year'][yy]


@functools.lru_cache(maxsize=None)
def today_hosts():
    today = C.load_config(os.path.join(C.SOLVER, 'configs', 'today.json'))
    h = {}
    for lev in C.LEVELS:
        for host, keys in today['levels'][lev]['programs'].items():
            for k in keys:
                h[k] = host
    return h


def _serves(cfg, bldg, lev):
    L = cfg['levels'][lev]
    if bldg in ((cfg.get('optional_open') or {}).get(lev) or []) and bldg not in L.get('programs', {}):
        return False      # options 3b/5: an optional school may close, so nothing is pinned to it
    return bldg in L['zoned'] or bldg in L.get('programs', {})


@functools.lru_cache(maxsize=None)
def _homes(observed_lr=False):
    # (2026-10-22, Paul: fix Lent DLI overcount) cfg v2.lent_observed -> data/focus_dli_homes_lentobs.parquet, where the
    # Lent and Rigler columns use PPS's observed Oct 2025 home mix (Lent 80 of 256 own area, Rigler 215 of 289) instead
    # of 'own_area' (data/scripts/06c_lent_rigler_observed_homes.py); all other columns identical
    f = 'focus_dli_homes_lentobs.parquet' if observed_lr else 'focus_dli_homes.parquet'
    return pd.read_parquet(os.path.join(C.DATA, f))


def _home_col(key):
    host, prog = key.split('|')
    lang = prog.split()[0]
    for c in _homes().columns:
        if c.startswith(f'{DLI_PREFIX}{lang} @ {host}'):
            return c
    raise KeyError(key)


def _home_vec(key, observed_lr=False):
    v = _homes(bool(observed_lr))[_home_col(key)].values.astype(float)
    return v / max(v.sum(), 1e-9)


# ---------------------------------------------------------------------------------------------
# The v2 population: per level, per year, block kids + fixed populations by building
# ---------------------------------------------------------------------------------------------
def _cfg_key(cfg):
    keep = {k: cfg.get(k) for k in ('lr_nbhd_share', 'dissolve_programs', 'v2')}
    keep['programs'] = {lev: cfg['levels'][lev].get('programs', {}) for lev in C.LEVELS}
    keep['zoned'] = {lev: sorted(cfg['levels'][lev]['zoned']) for lev in C.LEVELS}
    return json.dumps(keep, sort_keys=True)


_CACHE = {}


def population(cfg):
    """Returns {'kids': {lev: {year: np.array}}, 'fixed': {lev: {year: {bldg: size}}}, 'notes': [...]}"""
    key = _cfg_key(cfg)
    if key in _CACHE:
        return _CACHE[key]
    b = C.blocks()
    n = len(b)
    sch = C.schools_table()
    v2 = cfg.get('v2', {})
    notes = []
    area_col = {'K-5': 'es_cur', '6-8': 'ms_cur', '9-12': 'sq_hs'}
    band = {'K-5': 'k5', '6-8': 'm68', '9-12': 'h912'}
    raw = {'K-5': 'raw_k5', '6-8': 'raw_m68', '9-12': 'raw_h912'}
    fac = {lev: area_year_factor(lev) for lev in C.LEVELS}
    # ---- base block vectors on the 2025-26 basis, with per-block area for the year factors
    base = {lev: b[band[lev]].values.astype(float).copy() for lev in C.LEVELS}
    lr_share = cfg.get('lr_nbhd_share', 0.02)
    lr = b['es_cur'].isin(C.LR_AREAS).values
    base['K-5'][lr] *= lr_share
    comps = []   # (lev, vec2025, series {y: mult vs 2025} or None for area factors, placement)
    # fix 2: Lent-area non-DLI kids
    ln = v2.get('lent_nondli')
    if ln:
        n_ln = float(ln['kids_2025_26'])
        lent = (b['es_cur'] == 'Lent').values
        mary = (b['es_cur'] == 'Marysville').values
        base['K-5'][lent] = 0.0          # the Lent DLI students are the 'Lent|Spanish' program
        mt = base['K-5'][mary].sum()
        base['K-5'][mary] *= (mt - n_ln) / mt
        w = b['raw_k5'].values * lent
        vec = w / w.sum() * n_ln
        ser = {y: fac['K-5']['Marysville'][y] for y in YEARS_ALL}   # they are Marysville students in PSU's base
        to = ln.get('baseline_to')
        if to:
            # PPS baselines only (Paul 2026-10-12, revised): PPS phases the Marysville change in ("Avoiding multiple
            # moves: Delaying full implementation ...", Marysville Family Guide p. 3), and its numbers keep these
            # students with Marysville's student body at Arleta.  Options assign by where kids live (blocks).
            fixed_ln = {y: n_ln * ser[y] for y in YEARS_ALL}
            notes.append(f'fix 2: {n_ln:.0f} Lent-area non-DLI kids (Marysville students today) held at {to} '
                         f'(PPS phase-in); Marysville area {mt:.0f} -> {mt - n_ln:.0f}')
        else:
            fixed_ln = None
            comps.append(('K-5', vec, ser, 'blocks'))
            notes.append(f'fix 2: {n_ln:.0f} Lent-area non-DLI kids on Lent-area blocks; Marysville area {mt:.0f} -> {mt - n_ln:.0f}')
    else:
        fixed_ln, to = None, None
    # fix 2b (2026-10-22, Paul: Rigler-area non-DLI kids): Rigler is whole-school Spanish DLI, so its area keeps only
    # lr_nbhd_share of its k5 as neighborhood kids; the Rigler-area residents who attend another neighborhood school
    # today were calibrated onto the blocks of the schools they attend.  Mirror fix 2: per destination d, take n_d out
    # of d's own (es_cur) area and put n_d on Rigler-area blocks (Census raw_k5 weighted), scaled by d's own area
    # factor (the population they are part of in PSU's base, so Status Quo stays = PSU).  With baseline_hold (Status
    # Quo / baselines, where Rigler stays whole-school DLI and these kids keep attending d) they are held at d as a
    # fixed population instead of going on Rigler blocks, which leaves every school total unchanged.
    rn = v2.get('rigler_nondli')
    fixed_rn = {}
    if rn:
        rig = (b['es_cur'] == 'Rigler').values
        wr = b['raw_k5'].values * rig
        wr = wr / wr.sum()
        moved = []
        for d, n_d in rn['to'].items():
            n_d = float(n_d)
            dm = (b['es_cur'] == d).values
            dt = base['K-5'][dm].sum()
            base['K-5'][dm] *= (dt - n_d) / dt
            ser_d = {y: fac['K-5'][d][y] for y in YEARS_ALL}
            if rn.get('baseline_hold'):
                fixed_rn[d] = {y: n_d * ser_d[y] for y in YEARS_ALL}
            else:
                comps.append(('K-5', wr * n_d, ser_d, 'blocks'))
            moved.append(f'{d} {n_d:.0f} (area {dt:.0f} -> {dt - n_d:.0f})')
        where = 'held at today\'s schools (baseline)' if rn.get('baseline_hold') else 'on Rigler-area blocks'
        notes.append(f'fix 2b: {sum(float(v) for v in rn["to"].values()):.0f} Rigler-area non-DLI kids {where}; '
                     + ', '.join(moved))
    # fix 1: focus-lottery split
    fixed = {lev: {y: {} for y in YEARS_ALL} for lev in C.LEVELS}
    if fixed_ln:
        for y in YEARS_ALL:
            fixed['K-5'][y][to] = fixed['K-5'][y].get(to, 0.0) + fixed_ln[y]
    for d, sd in fixed_rn.items():
        for y in YEARS_ALL:
            fixed['K-5'][y][d] = fixed['K-5'][y].get(d, 0.0) + sd[y]
    for host, spec in (v2.get('focus_lottery') or {}).items():
        share_in = spec['in_zone_2025_26'] / spec['enrollment_2025_26']
        for lev in ('K-5', '6-8'):
            m = (b[area_col[lev]] == host).values
            if not m.any():
                continue
            lot_vec = base[lev] * m * (1 - share_in)
            base[lev][m] *= share_in
            tot25 = lot_vec.sum()
            hrow = psu_by_year()[host]['Total']
            ser = {y: fac[lev][host][y] for y in YEARS_ALL}   # same factor as the area (keeps SQ = PSU)
            place = spec['placement'].get(lev, 'host')
            if isinstance(place, dict):
                # a named split of the host's enrolled lottery students (Buckman 50/50 Abernethy/Sunnyside, Oct 6
                # memo p. 2); a share whose target does not serve the band in this plan goes home instead
                home_share = 0.0
                for tgt, sh in place.items():
                    if _serves(cfg, tgt, lev):
                        for y in YEARS_ALL:
                            fixed[lev][y][tgt] = fixed[lev][y].get(tgt, 0.0) + sh * tot25 * ser[y]
                    else:
                        home_share += sh
                if home_share > 0:
                    w = _returner_weights(host, lev, m, v2.get('returner_weighting', 'other_nbhd'))
                    comps.append((lev, w / w.sum() * tot25 * home_share, ser, 'blocks'))
                place = ', '.join(f'{k} {v:.0%}' for k, v in place.items()) + (
                    f' ({home_share:.0%} home: target closed)' if home_share else '')
            elif place == 'phase_out':
                # lottery students already admitted stay through grade 5, no new lottery admits from 2027-28
                # (Sunnyside Family Guide p. 3, "Current lottery protection"): share at host = cohorts still
                # enrolled = (2032 - y) / 6 for 2027..2031, 0 from 2032-33; the rest return home
                w = _returner_weights(host, lev, m, v2.get('returner_weighting', 'other_nbhd'))
                stay = {y: (1.0 if y < 2027 else max(0.0, (2032 - y) / 6)) if _serves(cfg, host, lev) else 0.0
                        for y in YEARS_ALL}
                for y in YEARS_ALL:
                    fixed[lev][y][host] = fixed[lev][y].get(host, 0.0) + stay[y] * tot25 * ser[y]
                comps.append((lev, w / w.sum() * tot25, {y: (1 - stay[y]) * ser[y] for y in YEARS_ALL}, 'blocks'))
                place = 'phase-out at host through grade 5, then home'
            elif place == 'host':
                for y in YEARS_ALL:
                    fixed[lev][y][host] = fixed[lev][y].get(host, 0.0) + tot25 * ser[y]
            else:
                w = _returner_weights(host, lev, m, v2.get('returner_weighting', 'other_nbhd'))
                comps.append((lev, w / w.sum() * tot25, ser, 'blocks'))
            notes.append(f'fix 1: {host} {lev}: in-zone share {share_in:.3f}; {tot25:.0f} lottery kids (2025-26) -> {place}')
    # fix 3: programs with follow / stay
    th = today_hosts()
    prog_y = {lev: {y: {} for y in YEARS_ALL} for lev in C.LEVELS}
    moves = []
    for lev in C.LEVELS:
        for host, keys in cfg['levels'][lev].get('programs', {}).items():
            for k in keys:
                s = program_series(k)
                src = th.get(k)
                moved = src is not None and src != host
                for y in YEARS_ALL:
                    f = follow_rate(k, y) if moved else 1.0
                    prog_y[lev][y][host] = prog_y[lev][y].get(host, 0.0) + f * s[y]
                    if moved and f < 1.0:
                        stay = (1 - f) * s[y]
                        if _serves(cfg, src, lev):
                            fixed[lev][y][src] = fixed[lev][y].get(src, 0.0) + stay
                if moved:
                    f31 = follow_rate(k, 2031)
                    where = src if _serves(cfg, src, lev) else 'home blocks'
                    moves.append({'program': k, 'from': src, 'to': host, 'arrive_share_2031': f31,
                                  'arrive_2031': round(f31 * s[2031], 1), 'stay_2031': round((1 - f31) * s[2031], 1),
                                  'non_arrivals_go_to': where})
                    if f31 < 1.0 and not _serves(cfg, src, lev):
                        ser = {y: (1 - follow_rate(k, y)) * s[y] for y in YEARS_ALL}
                        comps.append((lev, _home_vec(k, v2.get('lent_observed')), ser, 'blocks_abs'))
    # dissolved focus programs (options 3a/3b): kids return to their home blocks
    for p in cfg.get('dissolve_programs', []):
        d25 = C.dissolved_program_kids(p, '2025', homes=v2.get('focus_homes', 'census'))
        fs = focus_series(p)
        for lev in C.LEVELS:
            if d25[lev].sum() > 0:
                comps.append((lev, d25[lev], {y: fs[y] / fs[2025] for y in YEARS_ALL}, 'blocks'))
        notes.append(f'dissolved {p}: {fs[2031]:.0f} kids (2031-32) to home blocks')
    # ---- assemble per year
    kids = {}
    for lev in C.LEVELS:
        areas = b[area_col[lev]].values
        kids[lev] = {}
        for y in YEARS_ALL:
            fy = pd.Series(areas).map({a: v[y] for a, v in fac[lev].items()}).values
            v = base[lev] * fy
            for (cl, vec, ser, kind) in comps:
                if cl != lev:
                    continue
                v = v + (vec * ser[y] if kind == 'blocks' else vec * ser[y])
            kids[lev][y] = v
    for lev in C.LEVELS:
        for y in YEARS_ALL:
            for h, v in fixed[lev][y].items():
                prog_y[lev][y][h] = prog_y[lev][y].get(h, 0.0) + v
    out = {'kids': kids, 'fixed': prog_y, 'notes': notes, 'program_moves': moves}
    _CACHE[key] = out
    return out


@functools.lru_cache(maxsize=None)
def _capture():
    c = pd.read_csv(os.path.join(V2, 'capture_2025_26.csv'))
    fix = {'Sunnyside Environmental': 'Sunnyside', 'Bridger Creative Science': 'Bridger', 'César Chávez': 'Cesar Chavez',
           'Harriet Tubman': 'Tubman'}
    c['area'] = c['area'].map(lambda x: fix.get(x, x))
    return c


def _returner_weights(host, lev, host_mask, how='other_nbhd'):
    """Where a focus-lottery school's out-of-zone students live (fix 1).
    how='residents': Census band residents (raw_*) in the host's 2025-26 HS cluster, host and Lent/Rigler areas
    excluded -- the same convention build/data uses for every other focus program's homes (data/README.md
    "focus_dli home locations").  how='other_nbhd' (first v2 pass): areas of the host's 2025-26 HS cluster,
    each weighted by PPS's count of its residents attending ANOTHER neighborhood school (capture report Oct 2025,
    'Other Neighborhood School'), spread within the area by Census band residents.  Lent and Rigler areas are left
    out (their 'other' counts are DLI-design flows, fix 2).  For 6-8, middle areas use the M rows and K-8 areas their
    E row x the area's 6-8 share of raw kids."""
    b = C.blocks()
    cap = _capture()
    E = cap[cap.level == 'E'].set_index('area')['other_nbhd_school']
    M = cap[cap.level == 'M'].set_index('area')['other_nbhd_school']
    col = 'es_cur' if lev == 'K-5' else 'ms_cur'
    rawc = 'raw_k5' if lev == 'K-5' else 'raw_m68'
    cl = b.loc[host_mask, 'hs_cluster_cur'].mode().iloc[0]
    inc = (b['hs_cluster_cur'] == cl).values & ~host_mask & ~b['es_cur'].isin(C.LR_AREAS).values
    if how == 'residents':
        return b[rawc].values.astype(float) * inc
    w = np.zeros(len(b))
    for a, g in b[inc].groupby(col):
        if lev == 'K-5':
            n = E.get(a, 0.0)
        elif a in M.index:
            n = M[a]
        else:
            ga = b[b[col] == a]
            n = E.get(a, 0.0) * ga['raw_m68'].sum() / max(ga['raw_k5'].sum() + ga['raw_m68'].sum(), 1e-9)
        r = g[rawc].values.astype(float)
        if r.sum() > 0:
            w[g.index.values] = r / r.sum() * n
    return w


def kids(cfg, year):
    y = int(year)
    return {lev: population(cfg)['kids'][lev][y] for lev in C.LEVELS}


def fixed(cfg, lev, year):
    return dict(population(cfg)['fixed'][lev][int(year)])


@functools.lru_cache(maxsize=None)
def _caps():
    c = pd.read_csv(os.path.join(V2, 'capacity_2025_26.csv'))
    return dict(zip(c['school'], c['capacity_2025_26']))


def capacity(name, overrides=None):
    if overrides and name in overrides:
        return float(overrides[name])
    c = _caps().get(name)
    if c is not None and c == c:
        return float(c)
    return C.capacity(name)


def reassign(cfg, plan):
    """fix 2 in today / Status Quo: Lent is whole-school DLI, so Lent-area non-DLI kids attend Marysville."""
    r = (cfg.get('v2') or {}).get('reassign_K5') or {}
    if not r:
        return plan
    p = dict(plan)
    p['K-5'] = np.array([r.get(s, s) for s in plan['K-5']], dtype=object)
    return p
