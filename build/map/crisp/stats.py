"""Per-block helpers for the site map (read-only inputs, no solver imports so model-track edits can't break this):
walk miles block -> school (build/routing/walk_miles.parquet + school_points.csv, matched to build/data/schools.csv
the same way build/solver/common.py does), hard-edge zones (pps-model.json az / ZS), kids-of-color share per
block (pps-race.csv via model_port.py), school coordinates for every level."""
import os as _os  # _PPS_MAP_HDR (added by export: repo-relative paths)
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PPS_MAP = _os.environ.get('PPS_MAP_DIR') or _os.path.join(_HERE, '../../../data/pps-map')
import functools, json, os
import numpy as np
import pandas as pd

from geo import KIT

ROUTING = os.path.join(KIT, 'build', 'routing')
CSV2CANON = {'Lee (Sunrise)': 'Lee', 'Lane (Brentwood)': 'Lane'}   # as build/solver/common.py


@functools.lru_cache(None)
def schools_table():
    s = pd.read_csv(os.path.join(KIT, 'build', 'data', 'schools.csv'))
    s['name'] = s['name'].map(lambda n: CSV2CANON.get(n, n))
    return s.set_index('name')


@functools.lru_cache(None)
def model():
    return json.load(open(_os.path.join(_PPS_MAP, 'pps-model.json')))


@functools.lru_cache(None)
def blocks():
    return pd.read_parquet(os.path.join(KIT, 'build', 'data', 'blocks.parquet'))


@functools.lru_cache(None)
def _routing_index():
    sch = schools_table(); rp = pd.read_csv(os.path.join(ROUTING, 'school_points.csv'))
    out = {}
    for n, row in sch.iterrows():
        if pd.isna(row['lat']):
            continue
        d = np.hypot((rp['lat'] - row['lat']) * 69.0, (rp['lon'] - row['lon']) * 48.6)
        k = int(d.idxmin())
        if d[k] < 0.25:
            out[n] = k
    return out


@functools.lru_cache(None)
def _walk():
    df = pd.read_parquet(os.path.join(ROUTING, 'walk_miles.parquet'), columns=['block_idx', 'school_idx', 'walk_miles'])
    M = np.full((len(blocks()), 86), np.nan, dtype=np.float32)
    M[df['block_idx'].values, df['school_idx'].values] = df['walk_miles'].values
    return M


def walk(names):
    idx = _routing_index(); M = _walk()
    out = np.full((len(blocks()), len(names)), np.nan, dtype=np.float32)
    for k, n in enumerate(names):
        if n in idx:
            out[:, k] = M[:, idx[n]]
    return out


@functools.lru_cache(None)
def zones():
    m = model()
    return [set(b['az']) for b in m['BL']], [b['z'] for b in m['BL']]


@functools.lru_cache(None)
def school_region():
    m = model(); ZS = m['ZS']; sch = schools_table(); b = blocks(); _, z = zones()
    out = {}
    for n, row in sch.iterrows():
        if n in ZS:
            out[n] = ZS[n]
        elif not pd.isna(row['lat']):
            d = np.hypot((b['y'].values - row['lat']) * 69.0, (b['x'].values - row['lon']) * 48.6)
            out[n] = z[int(d.argmin())]
    return out


def eligible(names, ref_plans):
    """(n_blocks, len(names)) bool: no new I-84 / Willamette crossing (as build/solver/metrics.eligible_mask)."""
    az, _ = zones(); reg = school_region()
    allowed = [set(a) for a in az]
    for rp in ref_plans:
        for i, s in enumerate(rp):
            if s in reg:
                allowed[i].add(reg[s])
    M = np.zeros((len(az), len(names)), dtype=bool)
    for k, n in enumerate(names):
        r = reg.get(n)
        M[:, k] = [r in a for a in allowed]
    return M


@functools.lru_cache(None)
def poc():
    """kids-of-color share per block (Census 2020 under-18; same parse as model_port.py / cowork core.js)."""
    import sys
    sys.path.insert(0, os.path.join(KIT, 'build', 'map'))
    from model_port import BL
    return np.array([b['p'] for b in BL])


def coords(n):
    s = schools_table()
    if n in s.index and not pd.isna(s.loc[n, 'lat']):
        return [round(float(s.loc[n, 'lon']), 4), round(float(s.loc[n, 'lat']), 4)]
    return None
