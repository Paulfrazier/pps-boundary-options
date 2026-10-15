"""Shared data loading for the PPS boundary solver and scorecard.

Everything is indexed by block idx (0..9294, same order as pps-model.json BL / NB and
build/data/blocks.parquet).  School names are the canonical names used in blocks.parquet
(K-5: pps-model names, e.g. 'Lee', 'MLK Jr'; middle: 'Lane', 'Tubman', 'Gray'; high: 'Ida B. Wells').

Kids are NEIGHBORHOOD-PROGRAM kids (DLI strands and focus programs are separate fixed
populations, see PROGRAMS below), scaled to the PSU 2031-32 forecast (see scale_2031()).
"""
from __future__ import annotations

import os as _os  # _PPS_MAP_HDR (added by export: repo-relative paths)
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PPS_MAP = _os.environ.get('PPS_MAP_DIR') or _os.path.join(_HERE, '../../data/pps-map')
import functools
import json
import math
import os
from collections import defaultdict

import numpy as np
import pandas as pd

KIT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA = os.path.join(KIT, 'build', 'data')
ROUTING = os.path.join(KIT, 'build', 'routing')
RESEARCH = os.path.join(KIT, 'build', 'research')
COWORK = os.path.join(KIT, 'cowork', 'model')
PPS_MODEL = _os.path.join(_PPS_MAP, 'pps-model.json')
PPS_RACE = _os.path.join(_PPS_MAP, 'pps-race.csv')
SOLVER = os.path.dirname(os.path.abspath(__file__))

LEVELS = ['K-5', '6-8', '9-12']
BAND = {'K-5': 'k5', '6-8': 'm68', '9-12': 'h912'}

# schools.csv name -> canonical (blocks.parquet) name
CSV2CANON = {'Lee (Sunrise)': 'Lee', 'Lane (Brentwood)': 'Lane'}
# PSU Table 5.5 name -> canonical
PSU2CANON = {'Bridger Creative Science': 'Bridger', 'Sunnyside Environmental': 'Sunnyside',
             'César Chávez': 'Cesar Chavez', 'Harriet Tubman': 'Tubman',
             'Ida B Wells-Barnett': 'Ida B. Wells', 'Benson Polytechnic': 'Benson'}

# ---------------------------------------------------------------------------------------
# Fixed programs: (2025-26 count, 2031-32 count, level).  PSU/PRC Table 5.5 program rows
# (targets.json dli.strands_psu + PSU json); focus programs from PSU totals.
# Cesar Chavez K-8 Spanish (300 / 295) is split K-5 vs 6-8 by its ODE grade mix (273/443 K-5).
# ---------------------------------------------------------------------------------------
_CH_K5 = 273 / 443
PROGRAMS = {
    # K-5 DLI strands (key = 'original host|language')
    'Ainsworth|Spanish': (287, 291, 'K-5'),
    'Rigler|Spanish': (289, 321, 'K-5'),          # whole school; its kids are the Rigler-area block k5
    'Lent|Spanish': (256, 274, 'K-5'),            # whole school; its kids are the Lent-area block k5
    'Scott|Spanish': (222, 223, 'K-5'),
    'Atkinson|Spanish': (178, 183, 'K-5'),
    'Beach|Spanish': (155, 127, 'K-5'),
    'Sitton|Spanish': (138, 113, 'K-5'),
    'James John|Spanish': (133, 136, 'K-5'),
    'Cesar Chavez|Spanish K-5': (round(300 * _CH_K5, 1), round(295 * _CH_K5, 1), 'K-5'),
    'MLK Jr|Mandarin': (193, 196, 'K-5'),
    'Woodstock|Mandarin': (190, 194, 'K-5'),
    'Clark|Mandarin': (91, 87, 'K-5'),
    'Richmond|Japanese': (512, 497, 'K-5'),       # whole school, no attendance area
    'Kelly|Russian': (143, 145, 'K-5'),
    'Rose City Park|Vietnamese': (207, 210, 'K-5'),
    # 6-8 DLI strands
    'Cesar Chavez|Spanish 6-8': (round(300 * (1 - _CH_K5), 1), round(295 * (1 - _CH_K5), 1), '6-8'),
    'West Sylvan|Spanish': (116, 133, '6-8'),
    'Kellogg|Spanish': (201, 257, '6-8'),
    'George|Spanish': (109, 123, '6-8'),
    'Beaumont|Spanish': (101, 145, '6-8'),
    'Roseway Heights|Spanish': (93, 78, '6-8'),
    'Ockley Green|Spanish': (63, 34, '6-8'),
    'Roseway Heights|Vietnamese': (64, 72, '6-8'),
    'Harrison Park|Mandarin': (111, 98, '6-8'),
    'Tubman|Mandarin': (48, 52, '6-8'),
    'Mt Tabor|Japanese': (222, 210, '6-8'),
    'Lane|Russian': (36, 30, '6-8'),
    # 9-12 programs (DLI + PISA)
    'Lincoln|Spanish': (178, 180, '9-12'),
    'Roosevelt|Spanish': (299, 282, '9-12'),
    'Roosevelt|PISA': (38, 53, '9-12'),
    'McDaniel|Spanish': (205, 174, '9-12'),
    'McDaniel|Vietnamese': (34, 110, '9-12'),
    'McDaniel|PISA': (65, 72, '9-12'),
    'Franklin|Spanish': (173, 225, '9-12'),
    'Franklin|Russian': (29, 25, '9-12'),
    'Cleveland|Mandarin': (115, 112, '9-12'),
    'Jefferson|Mandarin': (14, 11, '9-12'),
    'Grant|Japanese': (265, 221, '9-12'),
}
# Focus / alternative schools: fixed enrollment, no attendance area. (2025-26, 2031-32, grades)
FOCUS = {
    'Winterhaven': (316, 310, 'K-8'),
    'da Vinci': (429, 419, '6-8'),
    'Odyssey': (217, 224, 'K-8'),
    'ACCESS': (324, 275, '1-8'),
    'MLC': (275, 199, 'K-12'),
    'Benson': (1025, 1213, '9-12'),
}
# focus_dli_homes.parquet column for programs that an option may dissolve into the blocks
FOCUS_HOME_COL = {'Winterhaven': 'Focus: Winterhaven K-8 (STEM)', 'da Vinci': 'Focus: da Vinci 6-8 (arts)',
                  # added 2026-10-12 for v2 options 3c/3d (v1 configs never dissolve these two)
                  'Odyssey': 'Focus: Odyssey K-8', 'ACCESS': 'Focus: ACCESS 1-8 (TAG)'}

LR_AREAS = ('Lent', 'Rigler')  # whole-school DLI areas: block k5 = DLI kids that follow the program


def _psu_rows():
    rows = json.load(open(os.path.join(RESEARCH, 'sources', 'psu_forecast_table5_5_by_school_program.json')))
    out = defaultdict(dict)
    for r in rows:
        n = PSU2CANON.get(r['name'], r['name'])
        out[n][r['program']] = (r['y2526'], r['y3132'])
    return out


@functools.lru_cache(maxsize=None)
def schools_table() -> pd.DataFrame:
    s = pd.read_csv(os.path.join(DATA, 'schools.csv'))
    s['canon'] = s['name'].map(lambda n: CSV2CANON.get(n, n))
    return s.set_index('canon')


@functools.lru_cache(maxsize=None)
def blocks() -> pd.DataFrame:
    b = pd.read_parquet(os.path.join(DATA, 'blocks.parquet'))
    assert (b['idx'].values == np.arange(len(b))).all()
    return b


@functools.lru_cache(maxsize=None)
def model():
    return json.load(open(PPS_MODEL))


@functools.lru_cache(maxsize=None)
def neighbors():
    return [list(x) for x in model()['NB']]


@functools.lru_cache(maxsize=None)
def adjacency():
    """NB adjacency made connected within each hard-edge zone.

    pps-model NB comes from block Voronoi cells clipped to the district, which leaves the rural
    Skyline / Sauvie / Bybee Lake area as ~35 fragments with no NB neighbours (and the W side as
    a separate graph from the east side, as it should be).  Contiguity is impossible across
    such gaps, so each fragment is bridged to the nearest block (centroid distance) of a
    different fragment in the same zone (W, or N/S which are already one graph), repeatedly,
    until every zone is one connected graph.  Bridges have boundary length 0.
    Returns (adjacency lists, list of added bridge pairs)."""
    NB = [set(x) for x in neighbors()]
    b = blocks()
    _, z = block_zones()
    zz = np.array(['E' if v in ('N', 'S') else 'W' for v in z])
    X = b['x'].values * 48.6
    Y = b['y'].values * 69.0
    bridges = []
    while True:
        n = len(NB)
        comp = -np.ones(n, dtype=int)
        c = 0
        for i in range(n):
            if comp[i] >= 0:
                continue
            stack = [i]
            comp[i] = c
            while stack:
                k = stack.pop()
                for j in NB[k]:
                    if comp[j] < 0:
                        comp[j] = c
                        stack.append(j)
            c += 1
        added = False
        for zone in ('W', 'E'):
            zc = np.unique(comp[zz == zone])
            if len(zc) <= 1:
                continue
            sizes = {cc: int((comp == cc).sum()) for cc in zc}
            main = max(sizes, key=sizes.get)
            for cc in zc:
                if cc == main:
                    continue
                mem = np.where(comp == cc)[0]
                other = np.where((zz == zone) & (comp != cc))[0]
                d = (X[mem, None] - X[None, other]) ** 2 + (Y[mem, None] - Y[None, other]) ** 2
                a, bb = np.unravel_index(d.argmin(), d.shape)
                i, j = int(mem[a]), int(other[bb])
                NB[i].add(j)
                NB[j].add(i)
                bridges.append((i, j))
                added = True
        if not added:
            break
    return [sorted(s) for s in NB], bridges


@functools.lru_cache(maxsize=None)
def edges():
    """Undirected NB edges (i<j) and shared Voronoi edge length in km (cowork edges.json;
    0 across hard-edge zone lines; 0.03 km if missing)."""
    el = json.load(open(os.path.join(COWORK, 'edges.json')))
    NB = neighbors()
    E = []
    for i, nb in enumerate(NB):
        for j in nb:
            if j > i:
                E.append((i, j, float(el.get(f'{i},{j}', 0.03))))
    return E


# ---------------------------------------------------------------------------------------
# 2031-32 scaling
# ---------------------------------------------------------------------------------------
def _nbhd31(psu, name, kind):
    """PSU 2031-32 neighborhood-program count for a school (Neighborhood row, else Total)."""
    rows = psu[name]
    if 'Neighborhood' in rows:
        return rows['Neighborhood']
    return rows['Total']


@functools.lru_cache(maxsize=None)
def scale_factors():
    """Per-area ratios r = PSU 2031-32 neighborhood forecast / modeled 2025-26 neighborhood kids.

    K-5 by current K-5 area (es_cur), 6-8 by current 6-8 area (ms_cur): the PSU forecast is
    school-by-school on today's lines, so the ratio applies to the area that school serves.
    K-8 schools: PSU gives K-8 totals only, so both bands get the same ratio (total 31 / total 25).
    9-12 by Status-Quo 2027-28 area (sq_hs): PSU's 2031-32 HS numbers already reflect the end of
    Jefferson dual assignment (Jefferson 377 -> 1,172 neighborhood), so the SQ map is the right unit.
    Lent/Rigler K-5: ratio of their whole-school Spanish program.
    """
    psu = _psu_rows()
    b = blocks()
    sch = schools_table()
    r = {'K-5': {}, '6-8': {}, '9-12': {}}
    # K-5
    for a, g in b.groupby('es_cur'):
        tot25 = g['k5'].sum()
        rows = psu[a]
        if a in LR_AREAS:
            t25, t31 = rows['Spanish']
            ratio = t31 / t25
        elif a == 'Cesar Chavez':
            t25, t31 = rows['Neighborhood']
            ratio = t31 / t25
        elif sch.loc[a, 'level'] == 'K-8':
            t25, t31 = rows['Total']
            ratio = t31 / t25
        else:
            t25, t31 = _nbhd31(psu, a, 'K-5')
            ratio = t31 / t25
        r['K-5'][a] = ratio
    # 6-8
    for a, g in b.groupby('ms_cur'):
        rows = psu[a]
        if a == 'Cesar Chavez':
            t25, t31 = rows['Neighborhood']
        elif 'Neighborhood' in rows:
            t25, t31 = rows['Neighborhood']
        else:
            t25, t31 = rows['Total']
        r['6-8'][a] = t31 / t25
    # 9-12 (Status-Quo areas; target = PSU 2031-32 neighborhood count, ratio vs block sum)
    for a, g in b.groupby('sq_hs'):
        t25, t31 = _nbhd31(psu, a, '9-12')
        r['9-12'][a] = t31 / g['h912'].sum()
    return r


@functools.lru_cache(maxsize=None)
def kids(year: str = '2031', lr_share: float = 0.02):
    """Neighborhood-program kids per block per level -> dict level -> np.array.

    lr_share: fraction of Lent/Rigler-area K-5 kids treated as neighborhood-program kids (the
    rest are the whole-school Spanish DLI students and follow the program).  PPS's own A
    projections imply ~2% (Kelly gains about 5 from Lent's area; Scott A = 470, unchanged).
    """
    b = blocks()
    out = {}
    f = scale_factors()
    lr = b['es_cur'].isin(LR_AREAS).values
    for lev, col, area in (('K-5', 'k5', 'es_cur'), ('6-8', 'm68', 'ms_cur'), ('9-12', 'h912', 'sq_hs')):
        v = b[col].values.astype(float).copy()
        if year == '2031':
            v = v * b[area].map(f[lev]).values
        if lev == 'K-5':
            v[lr] *= lr_share
        out[lev] = v
    return out


FOCUS_SHEET_COL = {'Winterhaven': 'Winterhaven', 'da Vinci': 'da Vinci', 'Odyssey': 'Odyssey', 'ACCESS': 'ACCESS'}
SHEET_NAME = {'Harriet Tubman': 'Tubman', 'Bridger Creative Science': 'Bridger', 'César Chávez': 'Cesar Chavez',
              'Sunnyside Environmental': 'Sunnyside'}


def catchment_program_kids(program: str):
    """(Paul 2026-10-12 ~22:30) 2025-26 home catchments of a focus program's students, from the community
    spreadsheet build/data/v2/focus_by_catchment_2025_26.csv (archived: build/pps-texts/
    focus-students-by-catchment-sheet-2025-26.md; second-hand, original source not stated).  Rows are 2025-26
    catchments: elementary rows = K-5 residents, middle rows = 6-8, K-8 rows = both.  Within a catchment, students
    are spread by Census band residents (raw_k5 / raw_m68).  K-8 rows split K-5 vs 6-8 by the program's grade mix
    (6-8-only programs: all 6-8).  Returns {level: 2025-26 block vector}, summing to the sheet's row total."""
    fc = pd.read_csv(os.path.join(DATA, 'v2', 'focus_by_catchment_2025_26.csv'))
    b = blocks()
    es, ms = b['es_cur'].values, b['ms_cur'].values
    k8 = {n for n in set(es) if n and (ms[es == n] == n).all()}
    mids = set(ms) - set(es)
    fd = pd.read_csv(os.path.join(DATA, 'focus_dli.csv')).set_index('program')
    row = fd.loc[FOCUS_HOME_COL[program]]
    gk5 = sum(row[f'est_g_{k}'] for k in ['K', 1, 2, 3, 4, 5])
    g68 = sum(row[f'est_g_{k}'] for k in [6, 7, 8])
    if program == 'ACCESS':
        gk5 -= row['est_g_K']
    share68 = g68 / (gk5 + g68)
    out = {'K-5': np.zeros(len(b)), '6-8': np.zeros(len(b)), '9-12': np.zeros(len(b))}
    for _, r in fc.iterrows():
        n = SHEET_NAME.get(r['catchment'], r['catchment'])
        c = r[FOCUS_SHEET_COL[program]]
        c = 0.0 if pd.isna(c) else float(c)
        if not c:
            continue
        if n in mids:
            parts = [('6-8', ms == n, 'raw_m68', 1.0)]
        elif n in k8:
            parts = [('K-5', es == n, 'raw_k5', 1 - share68), ('6-8', es == n, 'raw_m68', share68)]
        elif n in set(es):
            parts = [('K-5', es == n, 'raw_k5', 1.0)] if share68 < 1 else [('6-8', es == n, 'raw_m68', 1.0)]
        elif r['catchment'].startswith('Out of District'):
            continue      # live outside PPS: no neighborhood school to return to (left out; the total is rescaled)
        else:
            raise ValueError(f'sheet catchment {r["catchment"]!r} not found in es_cur/ms_cur')
        for lev, m, col, f in parts:
            w = b[col].values * m
            if w.sum() <= 0:
                w = m.astype(float)
            out[lev] += c * f * w / w.sum()
    return out


def dissolved_program_kids(program: str, year: str = '2031', homes: str = 'census'):
    """Block-level home locations of a focus program's students, split by level and scaled to
    the program's 2031-32 total (focus_dli_homes.parquet; estimated, district-wide).
    homes='catchment': use the per-catchment spreadsheet instead (catchment_program_kids)."""
    if homes == 'catchment':
        n25, n31, _ = FOCUS[program]
        v = catchment_program_kids(program)      # in-district students only (out-of-district row left out)
        scale = (n31 / n25) if year == '2031' else 1.0
        return {lev: x * scale for lev, x in v.items()}
    homes = pd.read_parquet(os.path.join(DATA, 'focus_dli_homes.parquet'))
    col = FOCUS_HOME_COL[program]
    fd = pd.read_csv(os.path.join(DATA, 'focus_dli.csv')).set_index('program')
    row = fd.loc[col]
    g = {f'g{k}': row[f'est_g_{k}'] for k in ['K', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}
    if program == 'ACCESS':
        g['gK'] = 0.0     # ACCESS serves grades 1-8 (focus_dli.csv's even split includes K): returners 5/8 K-5, 3/8 6-8
    k5 = sum(g[x] for x in ['gK', 'g1', 'g2', 'g3', 'g4', 'g5'])
    m68 = sum(g[x] for x in ['g6', 'g7', 'g8'])
    tot = k5 + m68
    n25, n31, _ = FOCUS[program]
    scale = (n31 / n25) if year == '2031' else 1.0
    base = homes[col].values.astype(float) / max(homes[col].sum(), 1e-9) * n25 * scale
    return {'K-5': base * k5 / tot, '6-8': base * m68 / tot, '9-12': np.zeros_like(base)}


# ---------------------------------------------------------------------------------------
# Distances
# ---------------------------------------------------------------------------------------
@functools.lru_cache(maxsize=None)
def routing_points():
    return pd.read_csv(os.path.join(ROUTING, 'school_points.csv'))


@functools.lru_cache(maxsize=None)
def school_routing_index():
    """canonical school name -> column (school_idx) in the routing matrices, matched by
    nearest coordinates (all within ~60 m)."""
    sch = schools_table()
    rp = routing_points()
    out = {}
    for n, row in sch.iterrows():
        if pd.isna(row['lat']):
            continue
        d = np.hypot((rp['lat'] - row['lat']) * 69.0, (rp['lon'] - row['lon']) * 48.6)
        k = int(d.idxmin())
        if d[k] < 0.25:
            out[n] = k
    return out


@functools.lru_cache(maxsize=None)
def dist_matrix(mode: str = 'walk'):
    """(n_blocks, 86) float32 miles."""
    df = pd.read_parquet(os.path.join(ROUTING, f'{mode}_miles.parquet'),
                         columns=['block_idx', 'school_idx', f'{mode}_miles'])
    M = np.full((len(blocks()), 86), np.nan, dtype=np.float32)
    M[df['block_idx'].values, df['school_idx'].values] = df[f'{mode}_miles'].values
    return M


def dist(mode: str, names):
    """(n_blocks, len(names)) miles to the named schools."""
    idx = school_routing_index()
    M = dist_matrix(mode)
    return np.stack([M[:, idx[n]] for n in names], axis=1)


# ---------------------------------------------------------------------------------------
# Hard edges (W = west of the Willamette, N = east side north of I-84, S = east side south)
# ---------------------------------------------------------------------------------------
@functools.lru_cache(maxsize=None)
def block_zones():
    m = model()
    return [set(bl['az']) for bl in m['BL']], [bl['z'] for bl in m['BL']]


@functools.lru_cache(maxsize=None)
def school_region():
    """Hard-edge zone of every school building: pps-model ZS for K-5 names; otherwise the zone
    of the nearest block centroid."""
    m = model()
    ZS = m['ZS']
    sch = schools_table()
    b = blocks()
    _, z = block_zones()
    out = {}
    for n, row in sch.iterrows():
        if n in ZS:
            out[n] = ZS[n]
        elif not pd.isna(row['lat']):
            d = np.hypot((b['y'].values - row['lat']) * 69.0, (b['x'].values - row['lon']) * 48.6)
            out[n] = z[int(d.argmin())]
    return out


@functools.lru_cache(maxsize=None)
def school_block():
    """Block whose centroid is nearest each school building (the root of its zone)."""
    sch = schools_table()
    b = blocks()
    out = {}
    for n, row in sch.iterrows():
        if pd.isna(row['lat']):
            continue
        d = np.hypot((b['y'].values - row['lat']) * 69.0, (b['x'].values - row['lon']) * 48.6)
        out[n] = int(d.argmin())
    return out


# ---------------------------------------------------------------------------------------
# Race: kids-of-color share per block (Census 2020 under-18, pps-race.csv; same parse as
# cowork core.js: cols GEOID, tot, hisp, white, black, asian, then the 18+ versions).
# ---------------------------------------------------------------------------------------
@functools.lru_cache(maxsize=None)
def poc_share():
    R = {}
    with open(PPS_RACE) as f:
        for line in f:
            c = line.strip().split(',')
            if len(c) < 11:
                continue
            v = [float(x) for x in c[1:]]
            R[c[0]] = v
    b = blocks()
    NB = neighbors()
    p = np.full(len(b), np.nan)
    for i, g in enumerate(b['GEOID'].values):
        v = R.get(str(g))
        if v is None:
            continue
        kids_ = v[0] - v[5]
        kw = v[2] - v[7]
        if kids_ > 0:
            p[i] = min(1.0, max(0.0, 1 - kw / kids_))
    for _ in range(3):
        for i in range(len(p)):
            if np.isnan(p[i]):
                vals = [p[j] for j in NB[i] if not np.isnan(p[j])]
                if vals:
                    p[i] = float(np.mean(vals))
    p[np.isnan(p)] = 0.35
    return p


def capacity(name: str, overrides: dict | None = None):
    if overrides and name in overrides:
        return float(overrides[name])
    sch = schools_table()
    if name not in sch.index:
        return float('nan')
    c = sch.loc[name, 'capacity_functional_2021']
    if pd.isna(c):
        c = sch.loc[name, 'capacity_functional_model']
    return float(c)


def program_size(key: str, year: str = '2031', share: float = 1.0):
    n25, n31, _ = PROGRAMS[key]
    return (n31 if year == '2031' else n25) * share


def load_config(path):
    with open(path) as f:
        return json.load(f)


def resolve_config(cfg, scorecard):
    """(2026-10-13) Apply a finished run's own choices (optional schools closed, program units moved; scorecard keys
    optional_schools / program_moves) to its config, as solve.py does after each level, so tools that re-score a run
    (smooth_v2, lines_qa) see the same open schools and program hosts."""
    for lev, r in (scorecard.get('optional_schools') or {}).items():
        cl = set(r.get('closed', []))
        lc = cfg['levels'][lev]
        lc['zoned'] = [n for n in list(lc['zoned']) + [n for n in r.get('kept_open', []) if n not in lc['zoned']]
                       if n not in cl]
    for lev, mv in (scorecard.get('program_moves') or {}).items():
        progs = cfg['levels'][lev].setdefault('programs', {})
        fl_ = (cfg.get('v2') or {}).get('focus_lottery') or {}
        popped = {u: progs.pop(u) for u in mv if u in progs}
        for u, d in mv.items():
            if u in popped:
                progs[d] = progs.get(d, []) + popped[u]
            if u in fl_:
                fl_[u].setdefault('placement', {})[lev] = {d: 1.0}
    cfg.pop('optional_open', None)
    cfg.pop('program_choice', None)
    return cfg


if __name__ == '__main__':
    f = scale_factors()
    for lev in LEVELS:
        print(lev, {k: round(v, 3) for k, v in f[lev].items()})
    K25 = kids('2025')
    K31 = kids('2031')
    for lev in LEVELS:
        print(lev, 'kids 2025-26', round(K25[lev].sum()), '2031-32', round(K31[lev].sum()))
    idx = school_routing_index()
    rp = routing_points()
    for n, k in idx.items():
        print(f'{n:22s} -> {rp.loc[k, "name"]}')
    print('unmatched', [n for n in schools_table().index if n not in idx])
    print(school_region())
    p = poc_share()
    print('poc share mean', p.mean(), 'kid-weighted', (p * K31['K-5']).sum() / K31['K-5'].sum())
    print('edges', len(edges()))


# ---------------------------------------------------------------------------------------
# Durability: PSU MEDIUM district forecast 2031-32 .. 2040-41 (PPS_Forecast_2026_27.pdf,
# Table 5.2, district totals; K-5 = K-2 + 3-5).  Every school at a level is scaled by the same
# district ratio vs 2031-32 (Table 5.5 per-school rows stop at 2031-32 in our extract, and PSU's
# per-school table only runs to 2035-36, so a per-area version is not available here).
# ---------------------------------------------------------------------------------------
YEARS = [f'{y}-{(y + 1) % 100:02d}' for y in range(2031, 2041)]
PSU_MEDIUM = {
    'K-5': [17948, 17673, 17303, 16830, 16566, 16492, 16435, 16483, 16571, 16687],
    '6-8': [8315, 8288, 8456, 8670, 8650, 8391, 8043, 7805, 7719, 7624],
    '9-12': [12986, 12491, 12097, 11681, 11547, 11588, 11868, 11890, 11705, 11462],
}


def year_ratios(level):
    v = PSU_MEDIUM[level]
    return {y: v[k] / v[0] for k, y in enumerate(YEARS)}


# ---------------------------------------------------------------------------------------
# Durability horizons (config key "horizon"; Paul 2026-10-12 ~15:15).
#   psu2041 (default, every result before 2026-10-12 15:15): years 2031-32 .. 2040-41, all required; 2036-41 extend
#           PSU's per-school rows with the district medium trend.
#   pps2031: PPS's own window.  REQUIRED 2027-28 .. 2031-32 (PPS Family Guide p. 1: "Estimates cover 2027-28
#           through 2031-32"); REPORTED (not required) through 2035-36, the last year of PSU's per-school Table 5.5.
#           No extension past 2035-36.  Model v2 only (per-school sizes by year).
# ---------------------------------------------------------------------------------------
def _yr(y):
    return f'{y}-{(y + 1) % 100:02d}'


HORIZONS = {
    'psu2041': {'years': YEARS, 'required': YEARS, 'label': '2031-32 to 2040-41 (all required)'},
    'pps2031': {'years': [_yr(y) for y in range(2027, 2036)], 'required': [_yr(y) for y in range(2027, 2032)],
                'label': 'required 2027-28 to 2031-32 (PPS Family Guide window); reported to 2035-36 (PSU Table 5.5)'},
}


def horizon(cfg):
    h = (cfg or {}).get('horizon', 'psu2041')
    if h not in HORIZONS:
        raise ValueError(f'unknown horizon {h!r}')
    return h, HORIZONS[h]
