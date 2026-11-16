"""Scorecard basis for the site map: the exact kids-per-block, walk distances and "past a closer school" rule
that build/solver/metrics.py uses for each plan's scorecard, so every count on the map matches the scorecards.

build/solver/ is read only here. Its modules import cleanly (constants + functions, no side effects), but the
solver's `common` module shares a name with build/map/common.py, so they are loaded under private names and
sys.modules is restored afterwards. Functions used (unchanged): metrics.level_kids (2031-32 neighborhood-program
kids per block), metrics.eligible_mask (no new I-84 / Willamette crossing), metrics.load_refs (today / Status
Quo plans the scorecard used), common.dist('walk', ...), common.load_config.

past rule (metrics.level_metrics): names = the config's zoned schools at the level; d = walk to the assigned
school; dmin = min walk over eligible zoned schools (NaN-propagating, as numpy min there); past = d - dmin >=
cfg past_margin_miles (0.25); kids = sum of 2031-32 kids over past blocks.
"""
import functools, os, sys
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, '..', '..'))
SOLVER = os.path.join(KIT, 'build', 'solver')
_MODS = ('common', 'v2', 'metrics')


@functools.lru_cache(None)
def solver():
    saved = {k: sys.modules.pop(k) for k in _MODS if k in sys.modules}
    sys.path.insert(0, SOLVER)
    try:
        import metrics as M          # noqa: E402  (pulls in the solver's common + v2)
        C = sys.modules['common']; V2 = sys.modules['v2']
    finally:
        sys.path.remove(SOLVER)
        for k in _MODS:
            sys.modules.pop(k, None)
        sys.modules.update(saved)
    return M, C, V2


def cfg_path(o):
    v2 = o.get('model_version') == 'v2'
    return os.path.join(SOLVER, 'configs', *(['v2'] if v2 else []), '%s.json' % o['name'])


@functools.lru_cache(None)
def config(name, version):
    M, C, _ = solver()
    return C.load_config(cfg_path({'name': name, 'model_version': version}))


@functools.lru_cache(None)
def refs(version):
    M, C, _ = solver()
    return M.load_refs(os.path.join(SOLVER, 'configs', *(['v2'] if version == 'v2' else [])))


def kids(o, lv):
    """2031-32 neighborhood-program kids per block at this level for plan o (scorecard 'kids')."""
    M, _, _ = solver()
    return np.asarray(M.level_kids(config(o['name'], o.get('model_version', 'v1')), '2031')[lv], dtype=float)


def past(o, lv, lab):
    """dict: names, d (walk to assigned), dmin, amin (index of nearest eligible school), past mask, margin, K."""
    M, C, _ = solver()
    ver = o.get('model_version', 'v1')
    cfg = config(o['name'], ver)
    K = kids(o, lv)
    names = sorted(set(cfg['levels'][lv]['zoned']))
    col = {n: k for k, n in enumerate(names)}
    W = C.dist('walk', names)
    ai = np.array([col.get(s, -1) for s in lab])
    if (ai < 0).any():
        raise ValueError('%s %s: blocks assigned to schools not zoned: %s' % (o['name'], lv, sorted(set(lab[ai < 0]))))
    d = W[np.arange(len(lab)), ai].astype(float)
    R = refs(ver)
    E = M.eligible_mask(lv, names, [R[r][lv] for r in ('today', 'status_quo') if r in R])
    Wm = np.where(E, W, np.inf)
    dmin = Wm.min(axis=1)
    with np.errstate(invalid='ignore'):
        amin = np.where(np.isnan(Wm), np.inf, Wm).argmin(axis=1)
        margin = cfg.get('past_margin_miles', 0.25)
        p = d - dmin >= margin
    return {'names': names, 'd': d, 'dmin': dmin, 'amin': amin, 'past': p, 'margin': margin, 'K': K,
            'n': float(K[p].sum())}
