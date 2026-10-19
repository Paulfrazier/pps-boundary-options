"""CP-SAT boundary optimizer: one generic block-assignment engine, run per level.

  python solve.py configs/option1.json            -> out/option1/

Levels run in order K-5 -> 6-8 -> 9-12.  At 6-8 the blocks are grouped by their K-5 school and
at 9-12 by their 6-8 school; a group must go whole to one school (clean feeders) unless that is
infeasible, in which case a second phase allows penalized splits.  See METHOD.md.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from collections import defaultdict, deque

import numpy as np
from ortools.sat.python import cp_model

import common as C
import metrics as MX

KID = 100     # size units: 0.01 kid
MARGIN = 50   # bounds are tightened by 0.5 kid so rounding never lands a school a hair outside
COST = 100    # cost units: 0.01 kid-mile


# =========================================================================================
# Generic engine
# =========================================================================================
class Problem:
    """Assign every block to one of its candidate schools.

    cand[i]      list of school indices (into names) allowed for block i
    cost[i][k]   integer cost of block i -> cand[i][k]
    sz[i][k]     integer size contribution (units of 0.1 kid)
    fixed[s]     fixed size of school s (programs, 0.1 kid units)
    lo[s], hi[s] size bounds (0.1 kid units; None = unbounded)
    group[i]     group id (or -1): a group goes whole to one school unless split is allowed
    root[s]      block that must belong to s (rooted contiguity) or None (unrooted)
    """

    def __init__(self, level, names):
        self.level = level
        self.names = names
        self.S = len(names)
        self.n = len(C.blocks())
        self.cand = None
        self.cost = None
        self.sz = None
        self.fixed = [0] * self.S
        self.lo = [None] * self.S
        self.lo_raw = [None] * self.S   # unmargined floor of non-exempt schools (durability thresholds)
        self.hi = [None] * self.S
        self.group = None
        self.root = [None] * self.S
        self.hint = None
        self.range_schools = None
        self.range_max = None
        self.w = {}
        self.order = None  # per block: eligible schools by walk (fallback for pruning)
        self.div = None   # (coef_plus[i], coef_minus[i]) per block, unit 0.1 kid


def components_by_school(P):
    """Independent subproblems: schools linked when some block can go to both."""
    par = list(range(P.S))

    def f(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for c in P.cand:
        for k in c[1:]:
            ra, rb = f(c[0]), f(k)
            if ra != rb:
                par[ra] = rb
    if getattr(P, 'dur', None):
        for s in range(1, P.S):
            ra, rb = f(0), f(s)
            if ra != rb:
                par[ra] = rb
    if P.range_schools:
        rs = P.range_schools
        for s in rs[1:]:
            ra, rb = f(rs[0]), f(s)
            if ra != rb:
                par[ra] = rb
    comp = defaultdict(list)
    for s in range(P.S):
        comp[f(s)].append(s)
    blocks_of = defaultdict(list)
    for i, c in enumerate(P.cand):
        blocks_of[f(c[0])].append(i)
    return [(sorted(v), blocks_of[r]) for r, v in comp.items() if blocks_of[r]]


def find_islands(P, asg, blocks_sub, rooted):
    """Return [(s, island_blocks, anchor_block_or_None)] for every non-main piece of a zone."""
    NB = C.adjacency()[0]
    sub = set(blocks_sub)
    by_s = defaultdict(list)
    for i in blocks_sub:
        by_s[asg[i]].append(i)
    out = []
    seen = {}
    for s, mem in by_s.items():
        comps = []
        for i in mem:
            if i in seen:
                continue
            q = deque([i])
            seen[i] = len(comps)
            cm = []
            while q:
                k = q.popleft()
                cm.append(k)
                for j in NB[k]:
                    if j in sub and j not in seen and asg[j] == s:
                        seen[j] = len(comps)
                        q.append(j)
            comps.append(cm)
        if len(comps) <= 1:
            if rooted and P.root[s] is not None and comps and P.root[s] not in comps[0]:
                pass  # cannot happen: root is fixed to s
            continue
        if rooted and P.root[s] is not None:
            main = next(ci for ci, cm in enumerate(comps) if P.root[s] in cm)
            anchor = None
        else:
            K = P.kids
            main = max(range(len(comps)), key=lambda ci: (sum(K[k] for k in comps[ci]), len(comps[ci])))
            anchor = comps[main][0]
        for ci, cm in enumerate(comps):
            if ci != main:
                out.append((s, cm, anchor))
    return out


def repair_islands(P, asg, blocks_sub, rooted, max_iter=20):
    """Greedy hint repair: move each island to the neighbouring school it touches most
    (among its blocks' candidates).  Used only to build warm-start hints and as a last resort."""
    NB = C.adjacency()[0]
    for _ in range(max_iter):
        isl = find_islands(P, asg, blocks_sub, rooted)
        if not isl:
            return asg, 0
        for s, cm, _a in isl:
            cms = set(cm)
            cnt = defaultdict(int)
            for k in cm:
                for j in NB[k]:
                    if j not in cms and asg[j] != s:
                        cnt[asg[j]] += 1
            opts = [t for t in sorted(cnt, key=lambda t: -cnt[t]) if all(t in P.cand_set[k] for k in cm)]
            if opts:
                for k in cm:
                    asg[k] = opts[0]
    return asg, len(find_islands(P, asg, blocks_sub, rooted))


def solve_component(P, schools, blks, rooted, allow_split, cfg_solver, log, cuts=None):
    """Solve one independent component with lazy contiguity cuts.  Returns (asg dict, info)."""
    E = C.edges()
    bset = set(blks)
    sset = set(schools)
    cuts = cuts if cuts is not None else []
    hint = {i: P.hint[i] for i in blks}
    info = {'rounds': [], 'schools': [P.names[s] for s in schools], 'n_blocks': len(blks)}
    t_first, t_round, max_rounds = cfg_solver['time_first'], cfg_solver['time_round'], cfg_solver['max_rounds']
    best = None
    relax = None
    t_star = cfg_solver.get('time_star', 300)
    first_rnd = -1 if (rooted and not getattr(P, 'skip_relax', False)) else 0
    for rnd in range(first_rnd, max_rounds + 1):
        star = rooted and rnd >= 0
        m = cp_model.CpModel()
        x = {}
        for i in blks:
            vs = []
            for k, s in enumerate(P.cand[i]):
                v = m.NewBoolVar('')
                x[i, s] = v
                vs.append(v)
            m.AddExactlyOne(vs)
        # (2026-10-13, capstone stage 1) coarse ties: blocks of one piece (status-quo zone x block group x HS area)
        # move together, so choosing which schools stay open is a search over ~700 pieces, not 9,000 blocks
        for grp_ in (getattr(P, 'ties', None) or []):
            mem_ = [i for i in grp_ if i in bset]
            if len(mem_) < 2:
                continue
            common_ = set.intersection(*(set(P.cand[i]) for i in mem_))
            if not common_:
                continue        # no school every block of the piece can take: leave its blocks free
            r_ = mem_[0]
            for i in mem_:
                for s in P.cand[i]:
                    if s not in common_:
                        m.Add(x[i, s] == 0)
                    elif i != r_:
                        m.Add(x[i, s] == x[r_, s])
        # optional schools (options 3b, 5): y[s] = school kept open; a closed school takes no blocks
        yopen = {s: m.NewBoolVar('') for s in (getattr(P, 'optional', None) or set()) if s in sset}
        for (i, s), v in x.items():
            if s in yopen:
                m.AddImplication(v, yopen[s])
        # (Paul 2026-10-13, capstone) program units: a host's whole fixed population (immersion strands, focus
        # lottery group) stays or moves as one unit to one of a few nearby schools; the receiving school must be open
        pmv = {}
        for u, U in (getattr(P, 'punits', None) or {}).items():
            if u not in sset:
                continue
            opts = [u] + [d for d in U['alts'] if d in sset]
            vs_ = []
            for d in opts:
                v = m.NewBoolVar('')
                pmv[u, d] = v
                vs_.append(v)
                if d in yopen:
                    m.AddImplication(v, yopen[d])
            m.AddExactlyOne(vs_)
        obj = []
        soft = []   # everything except size slack, durability-count slack and splits
        if yopen and getattr(P, 'w_open', 0):
            soft.extend(P.w_open * v for v in yopen.values())
        # (2026-10-18, Paul: no big gaps when a school closes) spacing: a cost per kid on a block left with no open
        # school within levels.<lev>.coverage.miles; blocks with no school that close even today are exempt
        # (2026-10-18, hard version) every block keeps an open school within max(min_mi, its distance under the reference
        # run + slack_mi): no kid ends up much farther from a school than under PPS A, and the gaps PPS A leaves can close
        for i, nr0 in (getattr(P, 'cov_hard', None) or {}).items() if yopen else []:
            if i not in bset:
                continue
            nr_ = [s for s in nr0 if s in sset]
            if not nr_ or any(s not in yopen for s in nr_):
                continue
            m.AddBoolOr([yopen[s] for s in nr_])
        # (tiers, 2026-10-18: a flat cost at one distance let the solver leave Forest Park kids 4.5 mi away) each tier
        # (miles, cost) is charged separately, so a kid with nothing within 3 mi pays all three
        for cov, w_cov in (getattr(P, 'cov_tiers', None) or []) if yopen else []:
            for i in blks:
                nr_ = [s for s in cov[i] if s in sset]
                if not nr_ or any(s not in yopen for s in nr_) or not P.kids[i]:
                    continue
                z_ = m.NewBoolVar('')
                m.AddBoolOr([yopen[s] for s in nr_] + [z_])
                soft.append(int(round(w_cov * P.kids[i])) * z_)
        for (u, d), v in pmv.items():
            if d != u and P.punits[u]['size']:
                # (2026-10-13) cost grows with the distance moved: program_move kid-miles per student per mile (min 1 mi)
                dm_ = max(1.0, (getattr(P, 'unit_dist', {}).get(u) or {}).get(d, 1.0))
                soft.append(int(round(P.w_pm * P.punits[u]['size'] * dm_)) * v)
        for i in blks:
            for k, s in enumerate(P.cand[i]):
                if P.cost[i][k]:
                    soft.append(P.cost[i][k] * x[i, s])
        # roots
        if rooted:
            for s in schools:
                r = P.root[s]
                if r is not None and r in bset:
                    if s in yopen:
                        m.Add(x[r, s] == yopen[s])
                    else:
                        m.Add(x[r, s] == 1)
        # distance-ordered ("star") contiguity: a non-root block may join s only if a neighbour
        # strictly closer to s's building (geodesic potential) also joins s.  Every chain of
        # strictly decreasing potential ends at the root, so each zone is connected.
        if star and P.group is not None and not allow_split:
            # zone-level rule: units are connected pieces of whole feeder zones
            for s in schools:
                up = P.uphi.get(s)
                if up is None:
                    continue
                for u, pu in up.items():
                    rep = P.units[u][0]
                    if rep not in bset or (rep, s) not in x or u == P.uroot.get(s):
                        continue
                    lower = [x[P.units[w][0], s] for w in P.uadj[u]
                             if w in up and up[w] < pu and (P.units[w][0], s) in x]
                    if lower:
                        m.AddBoolOr(lower).OnlyEnforceIf(x[rep, s])
                    else:
                        m.Add(x[rep, s] == 0)
                # units unreachable for s on the unit graph cannot take s
                for u in P.units_of_school.get(s, []):
                    if u not in up:
                        m.Add(x[P.units[u][0], s] == 0)
        elif star:
            NBa = C.adjacency()[0]
            for (i, s), v in x.items():
                ph = P.phi.get(s)
                if ph is None or P.root[s] == i:
                    continue
                pi = ph.get(i)
                lower = [x[j, s] for j in NBa[i] if (j, s) in x and ph.get(j, float('inf')) < (pi if pi is not None else -1)]
                if lower:
                    m.AddBoolOr(lower).OnlyEnforceIf(v)
                else:
                    m.Add(v == 0)
        # sizes
        size_expr = {}
        slack = {}
        for s in schools:
            terms = []
            for i in P.blocks_of[s]:
                if i in bset:
                    k = P.cand_idx[i][s]
                    if P.sz[i][k]:
                        terms.append(P.sz[i][k] * x[i, s])
            terms += [P.punits[u]['size'] * v for (u, d), v in pmv.items() if d == s and P.punits[u]['size']]
            e = sum(terms) + P.fixed[s] if terms else cp_model.LinearExpr.Constant(P.fixed[s])
            size_expr[s] = e
            if P.lo[s] is not None:
                sl = m.NewIntVar(0, max(P.lo[s], 1), '')
                if s in yopen:
                    m.Add(e + sl >= P.lo[s]).OnlyEnforceIf(yopen[s])
                else:
                    m.Add(e + sl >= P.lo[s])
                slack[s, 'lo'] = sl
                obj.append(P.w_slack * sl)
            if P.hi[s] is not None:
                sh = m.NewIntVar(0, 10 ** 6, '')
                m.Add(e - sh <= P.hi[s])
                slack[s, 'hi'] = sh
                obj.append(P.w_slack * sh)
        # (option1_full, Paul 2026-10-12 ~18:00) 6-8 size need fed back into 9-12: each high-school area must hold enough
        # middle schoolers for the middle-school buildings inside it (floor) and no more than they fit (capacity).
        # A building's area = the high school its building block takes, so the bound is linear in x.
        MN = getattr(P, 'ms_need', None)
        if MN:
            for h in schools:
                terms = [MN['k68'][i] * x[i, h] for i in P.blocks_of[h] if i in bset and MN['k68'][i]]
                need = [MN['net_floor'][q] * x[r, h] for q, r in MN['root'].items() if (r, h) in x and MN['net_floor'][q]]
                room = [MN['net_cap'][q] * x[r, h] for q, r in MN['root'].items() if (r, h) in x]
                if not terms:
                    continue
                sn = m.NewIntVar(0, 10 ** 7, '')
                m.Add(sum(terms) + sn >= sum(need)) if need else m.Add(sn == 0)
                so = m.NewIntVar(0, 10 ** 7, '')
                m.Add(sum(terms) - so <= sum(room)) if room else m.Add(so == 0)
                slack[h, 'ms_need'] = sn
                slack[h, 'ms_room'] = so
                obj.append(MN['w'] * sn)
                obj.append(MN['w'] * so)
        # receiving-school cap (option 5; PPS deck 2026-10-06 p. 11, "Capped receiving schools at no more than two
        # per closure"): blocks of a closed school's current area go to at most `cap` schools
        if yopen and getattr(P, 'cap_receivers', None):
            for c, area in P.closure_area.items():
                if c not in yopen:
                    continue
                ab = [i for i in area if i in bset]
                zs = {}
                for i in ab:
                    for t in P.cand[i]:
                        if t == c:
                            continue
                        if t not in zs:
                            zs[t] = m.NewBoolVar('')
                        m.AddImplication(x[i, t], zs[t])
                if len(zs) > P.cap_receivers:
                    m.Add(sum(zs.values()) <= P.cap_receivers).OnlyEnforceIf(yopen[c].Not())
        # HS range (soft)
        rng = None
        if P.range_schools and set(P.range_schools) <= sset:
            ub = 10 ** 6
            sv = {}
            for s in P.range_schools:
                v = m.NewIntVar(0, ub, '')
                m.Add(v == size_expr[s])
                sv[s] = v
            mx, mn = m.NewIntVar(0, ub, ''), m.NewIntVar(0, ub, '')
            m.AddMaxEquality(mx, list(sv.values()))
            m.AddMinEquality(mn, list(sv.values()))
            rng = m.NewIntVar(0, ub, '')
            m.Add(rng >= mx - mn - P.range_max)
            soft.append(P.w_range * rng)
        # durability: school s 'at target' in year y  <=>  size * r_y within [floor, ceiling]
        dur_b, dur_d, dur_slack = {}, {}, {}
        D = getattr(P, 'dur', None)
        if D:
            cnt = [s for s in schools if s in D['countable']]
            for s in cnt:
                ds = m.NewBoolVar('')
                dur_d[s] = ds
                soft.append(-D['w_durable'] * ds)
                for y, ry in D['ratios'].items():
                    b = m.NewBoolVar('')
                    dur_b[s, y] = b
                    m.AddImplication(ds, b)
                    if D.get('sz_y') is not None:
                        # model v2: each block/population has its own year factor -> a size expression per year
                        szy = D['sz_y'][y]
                        terms = [szy[i][P.cand_idx[i][s]] * x[i, s] for i in P.blocks_of[s]
                                 if i in bset and szy[i][P.cand_idx[i][s]]]
                        terms += [P.punits[u]['size_y'][y] * v for (u, d), v in pmv.items()
                                  if d == s and P.punits[u]['size_y'][y]]
                        ey = sum(terms) + D['fixed_y'][y][s] if terms else cp_model.LinearExpr.Constant(D['fixed_y'][y][s])
                        if P.lo_raw[s] is not None:
                            m.Add(ey >= P.lo_raw[s] + MARGIN).OnlyEnforceIf(b)
                        if P.hi[s] is not None:
                            m.Add(ey <= P.hi[s]).OnlyEnforceIf(b)
                    else:
                        if P.lo_raw[s] is not None:
                            m.Add(size_expr[s] * 1 >= math.ceil((P.lo_raw[s] + MARGIN) / ry)).OnlyEnforceIf(b)
                        if P.hi[s] is not None:
                            m.Add(size_expr[s] * 1 <= math.floor((P.hi[s]) / ry)).OnlyEnforceIf(b)
                    soft.append(-D['w_year'] * b)
            # frontier runs: at least N schools at target in EVERY year (hard via big slack penalty); only
            # meaningful when this component holds every countable school of the level
            nmin = D.get('min_durable')
            if nmin and len(cnt) == len(D['countable']):
                sl = m.NewIntVar(0, len(cnt) + 1, '')
                m.Add(sum(dur_d.values()) + sl >= int(nmin))
                dur_slack['min_durable'] = sl
                obj.append(D['w_count_slack'] * sl)
            if D.get('all_open'):
                for s in cnt:
                    nd = m.NewBoolVar('')
                    if s in yopen:
                        m.Add(dur_d[s] + nd >= 1).OnlyEnforceIf(yopen[s])
                    else:
                        m.Add(dur_d[s] + nd >= 1)
                    dur_slack[f'not_durable:{P.names[s]}'] = nd
                    obj.append(D['w_count_slack'] * nd)
            for y in D['ratios']:
                req = D['required'].get(y, 0)
                if req > 0:
                    sl = m.NewIntVar(0, len(cnt) + 1, '')
                    m.Add(sum(dur_b[s, y] for s in cnt) + sl >= req)
                    dur_slack[y] = sl
                    obj.append(D['w_count_slack'] * sl)
        # diversity (optional)
        if P.div is not None and P.w_div:
            cp_, cm_ = P.div
            for s in schools:
                tp = [cp_[i] * x[i, s] for i in P.blocks_of[s] if i in bset and cp_[i]]
                tm = [cm_[i] * x[i, s] for i in P.blocks_of[s] if i in bset and cm_[i]]
                d = m.NewIntVar(0, 10 ** 6, '')
                if tp:
                    m.Add(d >= sum(tp))
                if tm:
                    m.Add(d >= sum(tm))
                soft.append(P.w_div * d)
        # boundary length
        if P.w_perim:
            for (i, j, L) in E:
                if L <= 0 or i not in bset or j not in bset:
                    continue
                ci, cj = P.cand_set[i], P.cand_set[j]
                if len(ci) == 1 and ci == cj:
                    continue
                coef = int(round(P.w_perim * L))
                if coef <= 0:
                    continue
                d = m.NewBoolVar('')
                for s in ci | cj:
                    a = x.get((i, s))
                    b = x.get((j, s))
                    if a is not None and b is not None:
                        m.Add(d >= a - b)
                    elif a is not None:
                        m.AddImplication(a, d)
                soft.append(coef * d)
        # groups (clean feeders)
        split_vars = {}
        if P.group is not None:
            members = defaultdict(list)
            for i in blks:
                if P.group[i] >= 0:
                    members[P.group[i]].append(i)
            for g, mem in members.items():
                r = mem[0]
                if allow_split:
                    z = m.NewBoolVar('')
                    split_vars[g] = z
                    obj.append(P.w_split * z)
                for i in mem[1:]:
                    for s in P.cand[i]:
                        if allow_split:
                            m.Add(x[i, s] - x[r, s] <= z)
                            m.Add(x[r, s] - x[i, s] <= z)
                        else:
                            m.Add(x[i, s] == x[r, s])
        # parent (e.g. middle-school) split penalty: u[p,h] = 1 if any child zone of p goes to h
        parent_u = {}
        if getattr(P, 'parent', None) is not None and P.group is not None:
            reps = {}
            for i in blks:
                reps.setdefault(P.group[i], i)
            pkids = defaultdict(set)
            for g, r in reps.items():
                for i in P.group_members_all[g]:
                    pkids[P.parent[i]].add(g)
            for p, gs in pkids.items():
                hs = set()
                for g in gs:
                    hs |= set(P.cand[reps[g]])
                if len(hs) <= 1:
                    continue
                for h in hs:
                    u = m.NewBoolVar('')
                    parent_u[p, h] = u
                    for g in gs:
                        if (reps[g], h) in x:
                            m.AddImplication(x[reps[g], h], u)
                    if not getattr(P, 'parent_target', None):
                        obj.append(P.w_parent_split * u)
            if getattr(P, 'parent_floor', None):
                # (v2 tactical HS) share of middle zones feeding one high school >= floor (penalized slack)
                ones = []
                for p in pkids:
                    us = [u for (pp, h), u in parent_u.items() if pp == p]
                    o = m.NewBoolVar('')
                    if us:
                        m.Add(sum(us) <= 1).OnlyEnforceIf(o)
                    ones.append(o)
                pf = P.parent_floor
                need = int(math.ceil(pf['min_share'] * pf['n_zoned'] - 1e-9)) - pf.get('n_outside', 0)
                psl = m.NewIntVar(0, len(ones) + 1, '')
                m.Add(sum(ones) + psl >= need)
                obj.append(pf['w_floor'] * psl)
                dur_slack['parent_one_hs_short'] = psl
                PT = getattr(P, 'parent_target', None)
                if PT:
                    # (option1_full, Paul 2026-10-12) soft push only up to soft_to (85%): w_soft per middle zone short of
                    # that line, nothing beyond it; the per-(zone, HS) penalty is off
                    need2 = int(math.ceil(PT['soft_to'] * pf['n_zoned'] - 1e-9))
                    psl2 = m.NewIntVar(0, len(ones) + 1, '')
                    m.Add(sum(ones) + psl2 >= need2)
                    obj.append(PT['w_soft'] * psl2)
        # tactical budget: kids moved off the start assignment (hard)
        if getattr(P, 'start', None) is not None:
            mv = [int(round(KID * P.kids[i])) * x[i, s] for (i, s) in x if P.names[s] != P.start[i] and P.kids[i] > 0]
            if mv:
                m.Add(sum(mv) <= P.budget_max)
        # middle -> high feeders (v2, Paul 2026-10-12): with fixed 9-12 lines (A_hs), count the high schools each
        # middle zone feeds (a destination counts at >= min_kids 9-12-band kids, as metrics._feeders), penalize every
        # high school fed, and require share of middle zones feeding ONE high school >= min_share (penalized slack)
        msf_z, msf_one, msf_sl = {}, {}, None
        MF = getattr(P, 'msfeed', None)
        if MF and len(schools) == P.S:
            tot = max(1, int(sum(MF['w'][i] for i in blks)))
            for s in schools:
                byh = defaultdict(list)
                allow = (MF.get('allow') or {}).get(P.names[s], ())
                for i in P.blocks_of[s]:
                    if i in bset and MF['w'][i]:
                        h_ = MF['hs'][i]
                        # (Paul 2026-10-12 ~22:15) an allowed split feeder (e.g. Tubman -> Grant + Jefferson, as in
                        # PPS Status Quo) counts its allowed high schools as one destination
                        byh[allow[0] if h_ in allow else h_].append(MF['w'][i] * x[i, s])
                zs = []
                for h, terms in byh.items():
                    z = m.NewBoolVar('')
                    m.Add(sum(terms) <= tot * z + MF['min_kids'])
                    msf_z[s, h] = z
                    zs.append(z)
                    obj.append(MF['w_split'] * z)
                o = m.NewBoolVar('')
                if zs:
                    m.Add(sum(zs) <= 1).OnlyEnforceIf(o)
                msf_one[s] = o
            need = int(math.ceil(MF['min_share'] * MF['n_zoned'] - 1e-9))
            msf_sl = m.NewIntVar(0, P.S, '')
            if need > 0:      # (Paul 2026-10-12 ~15:15) soft rule: min_share 0 -> no floor, penalty only
                m.Add(sum(msf_one.values()) + msf_sl >= need)
                obj.append(MF['w_floor'] * msf_sl)
            else:
                m.Add(msf_sl == 0)
        # contiguity cuts
        for (s, cm, nbr, anchor) in cuts:
            if s not in sset:
                continue
            rhs = [x[j, s] for j in nbr if (j, s) in x]
            for v in cm:
                if (v, s) not in x:
                    continue
                if anchor is None:
                    m.Add(x[v, s] <= sum(rhs)) if rhs else m.Add(x[v, s] == 0)
                elif (anchor, s) in x:
                    m.Add(x[v, s] + x[anchor, s] - 1 <= sum(rhs)) if rhs else m.Add(x[v, s] + x[anchor, s] <= 1)
        if getattr(P, 'mode', 'full') == 'full':
            obj += soft
        if allow_split and getattr(P, 'split_cap', None) is not None and split_vars:
            m.Add(sum(split_vars.values()) <= P.split_cap)
        m.Minimize(sum(obj))
        for i in blks:
            h = hint.get(i)
            for s in P.cand[i]:
                m.AddHint(x[i, s], 1 if s == h else 0)
        if yopen:
            used = {hint.get(i) for i in blks}
            for s, v in yopen.items():
                m.AddHint(v, 1 if s in used else 0)
        for (u, d), v in pmv.items():
            m.AddHint(v, 1 if d == u else 0)
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = t_first if rnd == -1 or (rnd == 0 and not rooted) else (
            t_star if rnd == 0 else t_round)
        solver.parameters.num_workers = cfg_solver.get('workers', 6)
        wps = cfg_solver.get('work_per_sec')
        if wps:
            # (Paul 2026-10-13) time limits in units of solver work, not clock time, so a laptop sleep does not use up
            # the budget: deterministic limit = seconds x work_per_sec (calibrated from the det= numbers logged below);
            # the clock limit becomes a loose safety net (x4)
            secs_ = solver.parameters.max_time_in_seconds
            solver.parameters.max_deterministic_time = secs_ * float(wps)
            solver.parameters.max_time_in_seconds = secs_ * 4
        if cfg_solver.get('hint_mode') == 'repair':
            solver.parameters.repair_hint = True
        elif cfg_solver.get('hint_mode') == 'fix':          # diagnostic only: is the hint itself feasible?
            solver.parameters.fix_variables_to_their_hinted_value = True
        solver.parameters.random_seed = 7
        t0 = time.time()
        st = solver.Solve(m)
        dt = time.time() - t0
        try:
            log(f'  (round {rnd}: {dt:.0f}s wall, det={solver.ResponseProto().deterministic_time:.1f} work units)')
        except Exception:
            pass
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            log(f'  round {rnd}: status {solver.StatusName(st)} after {dt:.0f}s')
            info['rounds'].append({'round': rnd, 'status': solver.StatusName(st), 'secs': round(dt, 1)})
            if rnd == -1:
                # relaxation found nothing in time (larger models, e.g. optional schools): fall back to the
                # star-repaired reference hint and go on to the contiguity rounds
                full = np.array(P.hint, dtype=object)
                if P.group is None or allow_split:
                    h, nviol = star_repair(P, full, blks)
                    hint = {i: h[i] for i in blks}
                    log(f'  relaxation skipped; reference hint star-repaired ({nviol} violations left)')
                continue
            if best is None:
                raise RuntimeError('no feasible solution (slack makes this impossible unless a fixed var conflicts)')
            break
        asg = {}
        for i in blks:
            for s in P.cand[i]:
                if solver.Value(x[i, s]):
                    asg[i] = s
                    break
        objv, bound = solver.ObjectiveValue(), solver.BestObjectiveBound()
        gap = (objv - bound) / max(abs(objv), 1e-9)
        sl = {f'{P.names[s]}:{side}': solver.Value(v) / KID for (s, side), v in slack.items() if solver.Value(v)}
        for y, v in dur_slack.items():
            if solver.Value(v):
                sl[f'durability_count_short:{y}'] = solver.Value(v)
        dur_info = None
        if dur_d:
            dur_info = {'durable_through_2040': sorted(P.names[s] for s, v in dur_d.items() if solver.Value(v)),
                        'at_target_by_year': {y: sum(solver.Value(dur_b[s, y]) for s in dur_d) for y in D['ratios']},
                        'required_by_year': D['required']}
        nsplit = sum(solver.Value(z) for z in split_vars.values())
        if msf_one:
            fed = defaultdict(list)
            for (s_, h), z in msf_z.items():
                if solver.Value(z):
                    fed[P.names[s_]].append(h)
            multi = {k: v for k, v in fed.items() if len(v) > 1}
            log(f'   middle zones feeding one high school: {sum(1 for s_ in msf_one if sum(solver.Value(z) for (a, h), z in msf_z.items() if a == s_) <= 1)}/{MF["n_zoned"]}'
                f' (floor {MF["min_share"]:.0%}); split: {multi}')
            if solver.Value(msf_sl):
                sl['ms_to_one_hs_short'] = solver.Value(msf_sl)
        if parent_u:
            pn = defaultdict(int)
            for (p, h), u in parent_u.items():
                pn[p] += solver.Value(u)
            nps = {p: n for p, n in pn.items() if n > 1}
            log(f'   parent zones split across high schools: {nps}')
        full = np.array(P.hint, dtype=object)
        for i, s in asg.items():
            full[i] = s
        isl = find_islands(P, full, blks, rooted)
        if rnd == -1:
            relax = {'objective': objv, 'bound': bound, 'secs': round(dt, 1), 'islands': len(isl),
                     'slack': sl, 'splits': int(nsplit)}
            info['relaxation'] = relax
            log(f'  relaxation (no contiguity): {solver.StatusName(st)} {dt:.0f}s obj={objv:.0f} '
                f'bound={bound:.0f} islands={len(isl)} slack={sl}')
            if P.group is not None and not allow_split:
                h, nviol = full, 'n/a (zone-level rule; relaxed solution used as hint)'
            else:
                h, nviol = star_repair(P, full, blks)
            log(f'  star-feasible warm start: {nviol} violations left after greedy repair')
            hint = {i: h[i] for i in blks}
            continue
        r = {'round': rnd, 'status': solver.StatusName(st), 'secs': round(dt, 1), 'objective': objv,
             'bound': bound, 'gap': round(gap, 4), 'islands': len(isl),
             'relaxation_bound': relax['bound'] if relax else None,
             'gap_vs_relaxation_bound': round((objv - relax['bound']) / max(abs(objv), 1e-9), 4) if relax else None,
             'island_kids': round(float(sum(P.kids[k] for _, cm, _ in isl for k in cm)), 1),
             'cuts_total': len(cuts), 'slack': sl, 'splits': int(nsplit),
             'range_excess': (solver.Value(rng) / KID) if rng is not None else None,
             'durability': dur_info,
             'opened_optional': sorted(P.names[s] for s, v in yopen.items() if solver.Value(v)) if yopen else None,
             'program_dest': {P.names[u]: P.names[d] for (u, d), v in pmv.items() if solver.Value(v)} if pmv else None}
        info['rounds'].append(r)
        log(f'  round {rnd}: {r["status"]} {dt:.0f}s obj={objv:.0f} bound={bound:.0f} gap={gap:.2%} '
            f'islands={len(isl)} ({r["island_kids"]} kids) slack={sl} splits={nsplit}')
        if dur_info:
            log(f'   at target in every modeled year ({D.get("horizon", "psu2041")}): {len(dur_info["durable_through_2040"])}/{len(dur_d)}; at target by year '
                f'{list(dur_info["at_target_by_year"].values())} (required {list(D["required"].values())})')
        if best is not None and r['islands'] == 0 and best[1].get('islands', 1) == 0 and \
                sum(v for k, v in best[1]['slack'].items() if k.endswith((':lo', ':hi'))) < \
                sum(v for k, v in sl.items() if k.endswith((':lo', ':hi'))) - 1e-9:
            log('  improvement round did not reduce size slack; keeping the earlier solution')
            break
        best = (asg, r)
        size_sl = sum(v for k, v in sl.items() if k.endswith((':lo', ':hi')))
        if not isl:
            # (v2) a clean solution that still leaves size slack gets improvement rounds, warm-started from itself
            extra = cfg_solver.get('slack_rounds', 0)
            if size_sl > 0.5 and rnd < extra:
                log(f'  {size_sl:.1f} kids of size slack left -> improvement round {rnd + 1} of {extra}')
                hint = {i: full[i] for i in blks}
                continue
            break
        NB = C.adjacency()[0]
        for s, cm, anchor in isl:
            cms = set(cm)
            nbr = sorted({j for k in cm for j in NB[k] if j not in cms and j in bset})
            cuts.append((s, cm, nbr, anchor))
        # next hint: previous solution with islands greedily repaired
        h = full.copy()
        h, _ = repair_islands(P, h, blks, rooted)
        hint = {i: h[i] for i in blks}
    asg, r = best
    full = np.array(P.hint, dtype=object)
    for i, s in asg.items():
        full[i] = s
    left = find_islands(P, full, blks, rooted)
    if left:
        full, still = repair_islands(P, full, blks, rooted)
        info['heuristic_repair'] = {'islands_before': len(left), 'islands_after': still}
        log(f'  contiguity not closed by cuts; greedy repair of {len(left)} islands -> {still} left')
        asg = {i: full[i] for i in blks}
    info['final'] = r
    return asg, info


def star_repair(P, asg, blks, passes=300):
    """Greedy repair of an assignment into one satisfying the star-contiguity rule (each
    non-root block has a same-school neighbour with smaller geodesic potential).  In grouped
    levels whole groups move.  Falls back to the geodesic-Voronoi school for stubborn blocks
    (that assignment always satisfies the rule).  Returns (asg, violations left)."""
    NB = C.adjacency()[0]
    asg = asg.copy()
    INF = float('inf')

    def ok(i, s):
        if P.root[s] == i:
            return True
        ph = P.phi.get(s)
        if ph is None:
            return True
        pi = ph.get(i)
        if pi is None:
            return False
        return any(asg[j] == s and ph.get(j, INF) < pi for j in NB[i])

    def unit(i):
        if P.group is None:
            return [i]
        return P.group_members[P.group[i]]
    if P.group is not None and not hasattr(P, 'group_members'):
        gm = defaultdict(list)
        for k in range(P.n):
            gm[P.group[k]].append(k)
        P.group_members = gm
    bl = list(blks)
    viol = []
    for it in range(passes):
        viol = [i for i in bl if not ok(i, asg[i])]
        if not viol:
            return asg, 0
        for i in viol:
            if ok(i, asg[i]):
                continue
            k = P.cand_idx[i]
            opts = [t for t in P.cand[i] if t != asg[i] and ok(i, t)]
            if not opts and it > passes // 2:
                opts = [min(P.cand[i], key=lambda t: P.phi.get(t, {}).get(i, INF))]
            if opts:
                t = min(opts, key=lambda t: P.cost[i][k[t]])
                for u in unit(i):
                    if t in P.cand_set[u]:
                        asg[u] = t
    return asg, len(viol)


def prune_unreachable(P, log):
    """Drop candidate s from blocks that cannot connect to s's building through blocks that
    also have s as a candidate (on the zone-connected adjacency).  For grouped levels a school is
    dropped from a whole group only if none of the group's blocks can reach it.  Blocks left with
    no candidate get their next-nearest eligible school (P.order) and the loop repeats."""
    NB = C.adjacency()[0]
    dropped = 0
    for _ in range(40):
        cs = [set(c) for c in P.cand]
        changed = False
        for s in range(P.S):
            r = P.root[s]
            if r is None:
                continue
            seen = {r}
            stack = [r]
            while stack:
                k = stack.pop()
                for j in NB[k]:
                    if j not in seen and s in cs[j]:
                        seen.add(j)
                        stack.append(j)
            un = [i for i in range(P.n) if s in cs[i] and i not in seen]
            if P.group is not None and un:
                reach_g = {P.group[i] for i in seen}
                un = [i for i in un if P.group[i] not in reach_g]
            for i in un:
                if len(P.cand[i]) > 1 or P.order is not None:
                    P.cand[i] = [t for t in P.cand[i] if t != s]
                    dropped += 1
                    changed = True
        for i in range(P.n):
            if not P.cand[i]:
                tried = cs[i]
                nxt = [t for t in (P.order[i] if P.order is not None else []) if t not in tried]
                P.cand[i] = [nxt[0]] if nxt else sorted(tried)[:1]
                changed = True
        if not changed:
            break
    log(f' pruned {dropped} unreachable (block, school) candidates')
    P.hint = [h if h in c else c[0] for h, c in zip(P.hint, P.cand)]


def geodesic_potentials(P):
    """phi[s][i]: shortest-path length (km, centroid-to-centroid) from s's building block to
    block i, over blocks that have s as a candidate (zone-connected adjacency)."""
    import heapq
    NB = C.adjacency()[0]
    b = C.blocks()
    X = b['x'].values * 78.7   # km per degree lon at 45.5N
    Y = b['y'].values * 111.1
    cs = [set(c) for c in P.cand]
    phi = {}
    for s in range(P.S):
        r = P.root[s]
        if r is None:
            continue
        dist = {r: 0.0}
        pq = [(0.0, r)]
        while pq:
            d, k = heapq.heappop(pq)
            if d > dist[k]:
                continue
            for j in NB[k]:
                if s not in cs[j]:
                    continue
                nd = d + math.hypot(X[k] - X[j], Y[k] - Y[j]) + 1e-6
                if nd < dist.get(j, float('inf')):
                    dist[j] = nd
                    heapq.heappush(pq, (nd, j))
        phi[s] = dist
    return phi


def unit_potentials(P):
    """Units = connected pieces of each feeder group.  uphi[s][u]: geodesic distance on the
    unit graph (kid-weighted centroid to centroid, km) from the unit holding s's building."""
    import heapq
    NB = C.adjacency()[0]
    b = C.blocks()
    X = b['x'].values * 78.7
    Y = b['y'].values * 111.1
    uid = -np.ones(P.n, dtype=int)
    units = []
    for i in range(P.n):
        if uid[i] >= 0:
            continue
        g = P.group[i]
        stack = [i]
        uid[i] = len(units)
        mem = []
        while stack:
            k = stack.pop()
            mem.append(k)
            for j in NB[k]:
                if uid[j] < 0 and P.group[j] == g:
                    uid[j] = len(units)
                    stack.append(j)
        units.append(mem)
    w = P.kids + 1e-3
    cx = np.array([np.average(X[m], weights=w[m]) for m in units])
    cy = np.array([np.average(Y[m], weights=w[m]) for m in units])
    uadj = [set() for _ in units]
    for i in range(P.n):
        for j in NB[i]:
            if uid[j] != uid[i]:
                uadj[uid[i]].add(int(uid[j]))
    P.units, P.uadj, P.uid = units, uadj, uid
    P.units_of_school = defaultdict(list)
    for u, m in enumerate(units):
        for s in P.cand[m[0]]:
            P.units_of_school[s].append(u)
    P.uphi, P.uroot = {}, {}
    for s in range(P.S):
        r = P.root[s]
        if r is None:
            continue
        ur = int(uid[r])
        P.uroot[s] = ur
        allowed = set(P.units_of_school[s])
        dist = {ur: 0.0}
        pq = [(0.0, ur)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v in uadj[u]:
                if v not in allowed:
                    continue
                nd = d + math.hypot(cx[u] - cx[v], cy[u] - cy[v]) + 1e-6
                if nd < dist.get(v, float('inf')):
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
        P.uphi[s] = dist


def run_problem(P, rooted, cfg_solver, log):
    prune_unreachable(P, log)
    if getattr(P, 'fb_extra', None):
        phi0 = geodesic_potentials(P)
        bad = [i for i in P.fb_extra if not any(P.root[s] == i or (s in phi0 and i in phi0[s]) for s in P.cand[i])]
        if bad:
            for i in bad:
                P.cand[i] = list(dict.fromkeys(P.cand[i] + P.fb_extra[i]))
                P.fallback_blocks.append(i)
            prune_unreachable(P, log)
            if getattr(P, 'recost', None) is None:
                raise RuntimeError('walk-cap fallback needs a v2 recost')
            b_ = C.blocks()
            log(' EDGE CASE (walk-cap fallback): blocks left with no reachable school inside the cap get their '
                'nearest-walk schools and their neighbours\' nearest in-cap school as candidates: '
                + '; '.join(f'{b_["GEOID"].values[i]} ({P.kids[i]:.1f} kids; candidates now {[P.names[t] for t in P.cand[i]]})'
                            for i in bad))
    if getattr(P, 'recost', None) is not None:
        # model v2: costs and sizes are per candidate POSITION, so rebuild them after pruning (v1 kept the
        # pre-pruning lists, which misaligned walk costs for blocks that lost a candidate)
        P.recost()
    if getattr(P, 'dur', None) and P.dur.get('_v2_build') is not None:
        P.dur['_v2_build']()
    if getattr(P, 'unit_alts', None) and not getattr(P, 'punits', None):
        # program units (capstone): take each unit host's fixed population out of its building's constant size;
        # the model adds it back at whichever school the unit is placed
        D_ = getattr(P, 'dur', None)
        P.punits = {}
        for u, alts in P.unit_alts.items():
            P.punits[u] = {'alts': alts, 'size': P.fixed[u],
                          'size_y': {y: D_['fixed_y'][y][u] for y in D_['ratios']} if D_ and D_.get('fixed_y') else {}}
            P.fixed[u] = 0
            if D_ and D_.get('fixed_y'):
                for y in D_['ratios']:
                    D_['fixed_y'][y][u] = 0
    P.phi = geodesic_potentials(P) if rooted else {}
    if rooted and P.group is not None:
        unit_potentials(P)
    P.cand_set = [set(c) for c in P.cand]
    P.cand_idx = [{s: k for k, s in enumerate(c)} for c in P.cand]
    P.blocks_of = defaultdict(list)
    for i, c in enumerate(P.cand):
        for s in c:
            P.blocks_of[s].append(i)
    asg = np.array([None] * P.n, dtype=object)
    infos = []
    for schools, blks in components_by_school(P):
        log(f' component: {len(schools)} schools, {len(blks)} blocks')
        phase1, info1 = solve_component(P, schools, blks, rooted, False, cfg_solver, log)
        info1['phase'] = 'whole groups' if P.group is not None else 'blocks'
        chosen, info = phase1, info1
        # (2026-10-13, capstone) solver.phase2_always: run the split phase even when whole zones fit, so a few
        # penalized splits can buy shorter walks or keep another (optional) school open
        if P.group is not None and (info1['final']['slack'] or cfg_solver.get('phase2_always')):
            log('  whole-zone feeders leave a size violation -> phase 2: allow penalized splits'
                if info1['final']['slack'] else '  phase 2 (phase2_always): allow penalized splits')
            for i in blks:
                P.hint[i] = phase1[i]
            # lexicographic: (a) fewest splits that remove the violation, (b) full objective with that cap
            P.mode, P.split_cap = 'splits', getattr(P, 'max_splits', None)
            quick = dict(cfg_solver, time_first=cfg_solver.get('time_first_2a', 60), time_star=cfg_solver.get('time_star_2a', 180))
            if cfg_solver.get('phase2_hint_mode'):
                quick['hint_mode'] = cfg_solver['phase2_hint_mode']
            warm = cfg_solver.get('phase2_warm')
            if warm:
                # (2026-10-12) start 2a from the phase-1 plan instead of a fresh relaxation hint (the relaxation's
                # star-repaired hint left dozens of violations and 2a timed out or got worse).  Phase 1 satisfies the
                # ZONE-level contiguity rule; 2a uses the stricter BLOCK-level rule, so repair the hint block by block
                # first (a repaired block becomes a penalized split)
                P.skip_relax = True
                full1 = np.array(P.hint, dtype=object)
                hf = cfg_solver.get('phase2_hint_file')
                if hf:
                    # (2026-10-13) start 2a from a given assignment file instead of phase 1 (e.g. the lead plan's
                    # middle lines with Sellwood's old area handed back, when 2a times out from phase 1)
                    import pandas as pd_
                    ha = pd_.read_parquet(hf if os.path.isabs(hf) else os.path.join(C.SOLVER, hf))["school"].values
                    nidx_ = {n: k for k, n in enumerate(P.names)}
                    for i in blks:
                        k_ = nidx_.get(ha[i])
                        if k_ is not None and k_ in P.cand[i]:
                            full1[i] = k_
                g_ = P.group
                P.group = None
                h_, nv_ = star_repair(P, full1, blks)
                P.group = g_
                for i in blks:
                    P.hint[i] = h_[i]
                nmv = sum(1 for i in blks if h_[i] != full1[i])
                log(f'  phase-2a warm start: phase-1 plan repaired to the block-level rule ({nmv} blocks moved, '
                    f'{nv_} violations left)')
            log('  phase 2a: minimise size slack + number of splits only'
                + (f' (at most {P.split_cap} splits)' if P.split_cap is not None else '')
                + (' (warm start from phase 1)' if warm else ''))
            try:
                pa, infoa = solve_component(P, schools, blks, rooted, True, quick, log)
                P.skip_relax = False
            except RuntimeError as e:
                # (v2, 2026-10-12) phase 2 is an improvement step: if it finds nothing in time, keep phase 1
                log(f'  phase 2a found no solution ({e}); keeping the whole-zone phase-1 assignment')
                P.mode, P.split_cap = 'full', None
                info1['phase2_failed'] = str(e)
                for i, s in phase1.items():
                    asg[i] = s
                infos.append(info1)
                continue
            P.mode, P.split_cap = 'full', infoa['final'].get('splits', None)
            if P.split_cap is not None and cfg_solver.get('phase2b_extra_splits'):
                # (2026-10-13) let 2b trade a few more splits for walking (2a only finds the fewest that fix sizes)
                P.split_cap += int(cfg_solver['phase2b_extra_splits'])
            for i in blks:
                P.hint[i] = pa[i]
            log(f'  phase 2b: full objective with splits <= {P.split_cap}, warm-started from 2a')
            P.skip_relax = True
            phase2, info2 = solve_component(P, schools, blks, rooted, True, cfg_solver, log)
            P.skip_relax = False
            if sum(info2['final']['slack'].values()) > sum(infoa['final']['slack'].values()) + 1e-9:
                log('  phase 2b ended with more slack than 2a -> keeping the 2a assignment')
                phase2, info2 = pa, dict(infoa, note='2b did not improve on 2a slack; 2a kept')
            info2['phase2a_min_splits'] = infoa['final']
            P.split_cap = None
            info2['phase'] = 'splits allowed'
            info2['phase1'] = info1
            chosen, info = phase2, info2
            s1_, s2_ = sum(info1['final']['slack'].values()), sum(info2['final']['slack'].values())
            # (2026-10-16) with phase2_always the split step is run for walking, not slack: keep it unless it is worse on
            # slack (both are often 0; the old rule then threw away the better-walking split plan)
            keep2 = cfg_solver.get('phase2_always') and s2_ <= s1_ + 1e-9
            if warm and not keep2 and s2_ >= s1_ - 1e-9:
                log('  phase 2 did not reduce slack below phase 1 -> keeping the whole-zone phase-1 assignment')
                chosen, info = phase1, dict(info1, phase2_rejected=info2['final'])
        for i, s in chosen.items():
            asg[i] = s
        infos.append(info)
    return asg, infos


# =========================================================================================
# Level builders
# =========================================================================================
def _base(cfg, lev, prev, refs):
    lc = cfg['levels'][lev]
    names = sorted(lc['zoned'])
    sidx = {n: k for k, n in enumerate(names)}
    P = Problem(lev, names)
    K = MX.level_kids(cfg, '2031')
    P.kids = K[lev]
    P.K_all = K
    W = C.dist('walk', names)
    ref_plans = [refs[r][lev] for r in ('today', 'status_quo')]
    E = MX.eligible_mask(lev, names, ref_plans, lc.get('same_side', ()))
    nh = lc.get('nest_hard')
    if nh:
        # (2026-10-15, Paul: fewer middle->high and elementary->high splits) hard nesting: blocks only to schools whose
        # building lies in the block's PPS A high-school area (metrics.apply_nest_hard; allow / free exceptions)
        before = int(E.sum())
        E = MX.apply_nest_hard(E, names, nh)
        print(f' {lev}: nest_hard on {nh.get("column", "A_hs")}: {before} -> {int(E.sum())} eligible (block, school) pairs',
              flush=True)
    return lc, names, sidx, P, W, E


def _costs(cfg, P, W, E, sq_names, sidx):
    """Per (block, candidate) cost in COST units: walk + past-closer + move-vs-SQ."""
    # optional per-level override (2026-10-12, Paul: closeness matters most at K-5): levels.<lev>.weights
    w = dict(cfg['weights'], **cfg['levels'][P.level].get('weights', {}))
    margin = cfg.get('past_margin_miles', 0.25)
    Wm = np.where(E, W, np.inf)
    dmin = Wm.min(axis=1)
    sq_idx = np.array([sidx.get(s, -1) for s in sq_names])
    K = P.kids
    # (2026-10-19, Paul: lines that follow busy streets) kid-miles per unsignalized busy-street crossing on the
    # shortest walk (build/safe_routes/FOR_MODELS.md). Charged out to 1.5 walk miles at every level, not just to the
    # bus line, so the solver can't dodge it by pushing kids just past 1.0 mi; NaN (not routed, >1.5 mi) = 0
    hx = w.get('hard_crossing', 0.0)
    if hx:
        sys.path.insert(0, os.path.join(C.SOLVER, '..', 'safe_routes'))
        import crossings as X
        H = np.nan_to_num(X.hard(P.names), nan=0.0)
    cost = []
    for i, c in enumerate(P.cand):
        row = []
        for s in c:
            d = float(W[i, s])
            v = w['walk'] * K[i] * d
            if hx:
                v += hx * K[i] * float(H[i, s])
            if d - dmin[i] >= margin:
                v += w['past'] * K[i]
            if s != sq_idx[i]:
                v += w['move'] * K[i]
            row.append(int(round(v * COST)))
        cost.append(row)
    return cost


def _bounds(cfg, P, lev, lc, sidx, prog, k8, sq_sizes=None):
    caps = cfg.get('capacity_overrides', {})
    exempt = set(cfg.get('exempt_floor', []))
    fl = cfg['floors']
    for n, s in sidx.items():
        P.fixed[s] = int(round(prog.get(n, 0.0) * KID))
        cap = MX.capacity(cfg, n)
        if n in k8:
            floor = fl['K-8']
            ceil = cap
        else:
            floor = fl[lev]
            ceil = cap
            if lev == 'K-5' and cfg.get('ceiling_k5_max'):
                ceil = min(cap, cfg['ceiling_k5_max']) if not math.isnan(cap) else cfg['ceiling_k5_max']
        if n in exempt:
            # exempt from the floor, but (by default) not allowed to shrink below its Status-Quo
            # 2031-32 size, so an exempt school is not drained to prop up its neighbours
            hold = (sq_sizes or {}).get(n) if cfg.get('exempt_hold_status_quo', True) else None
            P.lo[s] = int(round(min(floor, hold) * KID)) + MARGIN if hold else None
        else:
            P.lo[s] = int(round(floor * KID)) + MARGIN
            P.lo_raw[s] = int(round(floor * KID))
        fo = (cfg.get('floor_overrides') or {}).get(lev, {})
        if n in fo:
            # (Paul 2026-10-12 ~22:15) match PPS A's middle-school shortfalls: this school may go down to the given
            # size (its at-target threshold, lo_raw, stays the real floor)
            P.lo[s] = int(round(min(floor, fo[n]) * KID)) + MARGIN
        fb = (cfg.get('floor_buffer') or {}).get(lev, 0)
        if fb and n not in fo and n not in exempt and P.lo[s] is not None:
            # (Paul 2026-10-13, size-buffer robustness run) aim this many kids above the floor in the base year
            # (soft, via the floor slack); the at-target threshold, lo_raw, stays the real floor
            P.lo[s] += int(round(fb * KID))
        P.hi[s] = None if (ceil is None or math.isnan(ceil)) else int(round(ceil * KID)) - MARGIN


def _weights(cfg, P):
    # optional per-level override (2026-10-12): levels.<lev>.weights, e.g. a stronger boundary-length cost at K-5 only
    w = dict(cfg['weights'], **cfg['levels'][P.level].get('weights', {}))
    P.w_slack = int(w['slack'] * COST / KID)          # per 0.1 kid
    P.w_perim = w['perim'] * COST                     # per km
    P.w_split = int(w['split'] * COST)
    P.w_range = int(w['hs_range'] * COST / KID)
    P.w_div = int(w.get('diversity', 0) * COST / KID)


def _hint(lc, sidx, P, fallback_cols):
    b = C.blocks()
    hint = []
    hcol = lc.get('hint')
    for i, c in enumerate(P.cand):
        h = None
        for col in ([hcol] if hcol else []) + fallback_cols:
            v = sidx.get(b[col].values[i]) if col in b.columns else None
            if v is not None and v in c:
                h = v
                break
        hint.append(h if h is not None else c[0])
    return hint


def _divcoef(cfg, P):
    w = cfg['weights']
    if not w.get('diversity'):
        return None
    p = C.poc_share()
    K = P.kids
    Pd = float((K * p).sum() / K.sum())
    band = w.get('diversity_band', 0.15)
    cp_ = [int(round(KID * K[i] * (p[i] - Pd - band))) for i in range(P.n)]
    cm_ = [int(round(KID * K[i] * (Pd - p[i] - band))) for i in range(P.n)]
    return cp_, cm_


def build_k5(cfg, refs):
    lev = 'K-5'
    lc, names, sidx, P, W, E = _base(cfg, lev, None, refs)
    k8 = set(lc.get('k8', []))
    prog = MX.program_totals(cfg, lev)
    prog68 = MX.program_totals(cfg, '6-8')
    for n in k8:
        prog[n] = prog.get(n, 0.0) + prog68.get(n, 0.0)
    ncand = lc.get('n_cand', 7)
    maxw = lc.get('max_walk_mi')
    sq = refs['status_quo'][lev]
    sqi = np.array([sidx.get(s, -1) for s in sq])
    roots = C.school_block()
    rootblk = {}
    for n, s in sidx.items():
        r = roots[n]
        if r in rootblk.values():
            continue
        rootblk[s] = r
    cand = []
    orders = []
    fbn = lc.get('max_walk_fallback_nearest')
    P.fallback_blocks = []
    NBa = C.adjacency()[0] if (maxw and fbn) else None
    for i in range(P.n):
        el = np.where(E[i])[0]
        if len(el) == 0:
            el = np.arange(len(names))
        order = el[np.argsort(W[i, el])]
        orders.append([int(t) for t in order])
        if maxw:
            keep = [s for s in order if W[i, s] <= maxw or s == sqi[i]]
            if fbn and not any(W[i, s] <= maxw for s in order):
                # (2026-10-12, Paul's edge-case rule) no school within the cap: keep the fbn nearest-walk schools,
                # plus each neighbouring block's nearest in-cap school (so the block can join a neighbour's zone)
                nb = []
                for j in NBa[i]:
                    ej = np.where(E[j])[0]
                    inj = [t for t in ej[np.argsort(W[j, ej])] if W[j, t] <= maxw and E[i, t]]
                    if inj:
                        nb.append(int(inj[0]))
                # stored only; applied in run_problem to blocks left with NO reachable candidate after pruning
                P.fb_extra = getattr(P, 'fb_extra', {})
                P.fb_extra[i] = [int(t) for t in order[:fbn]] + nb
            order = np.array(keep if keep else order[:1])
        c = list(order[:ncand])
        if sqi[i] >= 0 and E[i, sqi[i]] and sqi[i] not in c:
            c.append(sqi[i])
        cand.append([int(s) for s in c])
    for s, r in rootblk.items():
        if s not in cand[r]:
            cand[r].append(s)
        P.root[s] = r
    P.cand = cand
    P.order = orders
    sqcfg = C.load_config(os.path.join(cfg.get('_cfgdir', os.path.join(C.SOLVER, 'configs')), 'status_quo.json'))
    sqcfg['lr_nbhd_share'] = cfg.get('lr_nbhd_share', 0.02)
    bt = MX.building_table(sqcfg, refs['status_quo'])
    _bounds(cfg, P, lev, lc, sidx, prog, k8, sq_sizes=dict(zip(bt['school'], bt['total'])))
    # size contribution: K-5 kids; K-8 buildings also carry the zone's 6-8 kids
    K5, K68 = P.K_all['K-5'], P.K_all['6-8']
    k8i = {sidx[n] for n in k8}
    P.sz = [[int(round(KID * (K5[i] + (K68[i] if s in k8i else 0.0)))) for s in c] for i, c in enumerate(cand)]
    P.cost = _costs(cfg, P, W, E, sq, sidx)
    if MX.is_v2(cfg):
        def recost():
            P.sz = [[int(round(KID * (K5[i] + (K68[i] if s in k8i else 0.0)))) for s in c] for i, c in enumerate(P.cand)]
            P.cost = _costs(cfg, P, W, E, sq, sidx)
        P.recost = recost
    _weights(cfg, P)
    P.div = _divcoef(cfg, P)
    P.hint = _hint(lc, sidx, P, ['sq_es'])
    return P


def build_grouped(cfg, refs, lev, prev_asg, ms_k8=()):
    """6-8 (groups = K-5 zones) or 9-12 (groups = 6-8 zones)."""
    lc, names, sidx, P, W, E = _base(cfg, lev, prev_asg, refs)
    k8 = set(lc.get('k8', []))
    prog = MX.program_totals(cfg, lev)
    ncand = lc.get('n_cand', 5)
    K = P.kids
    gnames = sorted(set(prev_asg))
    gid = {g: k for k, g in enumerate(gnames)}
    group = np.array([gid[g] for g in prev_asg])
    sq = refs['status_quo'][lev]
    b = C.blocks()
    hcol = lc.get('hint')
    cand_g = {}
    for g, gi in gid.items():
        mem = np.where(group == gi)[0]
        if g in k8:
            cand_g[gi] = [sidx[g]]
            continue
        wk = K[mem] + 1e-3
        # eligible: not crossing a hard edge for the majority of the group's kids
        elig_share = (E[mem] * wk[:, None]).sum(axis=0) / wk.sum()
        avgw = (W[mem] * wk[:, None]).sum(axis=0) / wk.sum()
        ok = [s for s in range(len(names)) if elig_share[s] >= 0.5 and names[s] not in k8]
        if not ok:
            ok = [s for s in range(len(names)) if names[s] not in k8]
        order = sorted(ok, key=lambda s: avgw[s])
        c = order[:ncand]
        # precedent: Status Quo and hint schools of the group's majority (if open)
        for col_vals in (sq, b[hcol].values if hcol else None):
            if col_vals is None:
                continue
            vals = col_vals[mem]
            tally = defaultdict(float)
            for v, kk in zip(vals, wk):
                tally[v] += kk
            top = max(tally, key=tally.get)
            if top in sidx and sidx[top] not in c and names[sidx[top]] not in k8:
                c.append(sidx[top])
        cand_g[gi] = [int(s) for s in c]
    # roots: each school's building block; its group (zone) must feed it.  If two buildings sit
    # in the same group, only the first is rooted (the other uses unrooted cuts).
    roots = C.school_block()
    used = set()
    for n, s_ in sidx.items():
        r = roots.get(n)
        if r is None:
            continue
        gi = group[r]
        if gi in used:
            continue
        if gnames[gi] in k8 and n != gnames[gi]:
            continue
        if s_ not in cand_g[gi]:
            if gnames[gi] in k8:
                continue
            cand_g[gi].append(s_)
        used.add(gi)
        P.root[s_] = r
    P.cand = [list(cand_g[group[i]]) for i in range(P.n)]
    P.group = group
    gm = defaultdict(list)
    for i in range(P.n):
        gm[group[i]].append(i)
    P.group_members_all = gm
    _bounds(cfg, P, lev, lc, sidx, prog, set())
    for n in k8:            # K-8 sizes were enforced at K-5 (building level)
        P.lo[sidx[n]] = None
        P.lo_raw[sidx[n]] = None
        P.hi[sidx[n]] = None
    P.sz = [[int(round(KID * K[i]))] * len(c) for i, c in enumerate(P.cand)]
    P.cost = _costs(cfg, P, W, E, sq, sidx)
    if MX.is_v2(cfg):
        def recost():
            P.sz = [[int(round(KID * K[i]))] * len(c) for i, c in enumerate(P.cand)]
            P.cost = _costs(cfg, P, W, E, sq, sidx)
        P.recost = recost
    _weights(cfg, P)
    P.div = _divcoef(cfg, P)
    # hint: group majority of the hint column
    hint = []
    hv = b[hcol].values if hcol else sq
    gh = {}
    for g, gi in gid.items():
        mem = np.where(group == gi)[0]
        tally = defaultdict(float)
        for v, kk in zip(hv[mem], K[mem] + 1e-3):
            if v in sidx and sidx[v] in cand_g[gi]:
                tally[sidx[v]] += kk
        gh[gi] = max(tally, key=tally.get) if tally else cand_g[gi][0]
    P.hint = [gh[group[i]] for i in range(P.n)]
    if lev == '9-12' and cfg.get('hs_range_max'):
        P.range_schools = [sidx[n] for n in names]
        P.range_max = int(cfg['hs_range_max'] * KID)
    return P


# =========================================================================================
def run(cfg_path, start_level='K-5'):
    import pandas as pd
    cfg = C.load_config(cfg_path)
    cfg['_cfgdir'] = os.path.dirname(os.path.abspath(cfg_path))
    if str(cfg.get('status', '')).startswith(('needs', 'placeholder')):
        raise SystemExit(f'{cfg["name"]}: {cfg["status"]}')
    out = os.path.join(MX.outdir(cfg), cfg['name'])
    if MX.is_v2(cfg):
        # TRACKS.md write rule (2026-10-12): never write into a folder the site may read.  Solve into
        # <name>.staging; run_queue.py checks it and swaps it into place.
        final = out
        out = final + '.staging'
        os.makedirs(out, exist_ok=True)
        if start_level != 'K-5':
            import shutil
            for f in ['checkpoint.json'] + [f'assign_{l}.parquet' for l in C.LEVELS]:
                if not os.path.exists(os.path.join(out, f)) and os.path.exists(os.path.join(final, f)):
                    shutil.copy2(os.path.join(final, f), os.path.join(out, f))
    os.makedirs(out, exist_ok=True)
    logf = open(os.path.join(out, 'solve_log.txt'), 'w' if start_level == 'K-5' else 'a')

    def log(msg):
        print(msg, flush=True)
        logf.write(msg + '\n')
        logf.flush()
    refs = MX.load_refs(cfg['_cfgdir'] if MX.is_v2(cfg) else None)
    plan = {}
    infos = {}
    times = {}
    ck = os.path.join(out, 'checkpoint.json')
    prev_ck = json.load(open(ck)) if os.path.exists(ck) else {}
    # (option1_full, Paul 2026-10-12 ~17:05) a config may solve levels in feeder order, e.g. K-5 -> 9-12 -> 6-8, so
    # middle zones can nest inside the new high-school lines; --from follows this order
    ORDER = cfg.get('level_order', C.LEVELS)
    for lev in ORDER:
        if ORDER.index(lev) < ORDER.index(start_level):
            plan[lev] = pd.read_parquet(os.path.join(out, f'assign_{lev}.parquet'))['school'].values.astype(object)
            infos[lev] = prev_ck['infos'][lev]
            times[lev] = prev_ck['times'][lev]
            log(f'== {lev}: loaded from checkpoint')
            continue
        t0 = time.time()
        log(f'== {cfg["name"]} {lev}')
        frun = cfg['levels'][lev].get('fixed_run')
        if frun:
            # (option1_nested) this level is copied from a finished run's assignment, not solved
            fp = os.path.join(C.SOLVER, 'out_v2', frun, f'assign_{lev}.parquet')
            plan[lev] = pd.read_parquet(fp)['school'].values.astype(object)
            times[lev] = 0.0
            infos[lev] = [{'final': {'slack': {}, 'splits': 0}, 'phase': f'fixed: copied from {frun} (not solved)'}]
            log(f' {lev}: fixed to {fp} (not solved)')
            continue
        fa = cfg['levels'][lev].get('fixed_assign')
        if fa:
            plan[lev] = C.blocks()[fa].values.astype(object)
            # (2026-10-18, Paul: don't send Skyline over the St. Johns Bridge) levels.<lev>.fixed_reassign: a list of
            # {"by": block column, "area": value, "to": school}; those blocks go to "to" instead of the column's school
            for ra in cfg['levels'][lev].get('fixed_reassign', []):
                m_ = C.blocks()[ra['by']].values == ra['area']
                plan[lev][m_] = ra['to']
                log(f' {lev}: {int(m_.sum())} blocks with {ra["by"]} = {ra["area"]} -> {ra["to"]}')
            times[lev] = 0.0
            infos[lev] = [{'final': {'slack': {}, 'splits': 0}, 'phase': f'fixed: column {fa} (not solved)'}]
            log(f' {lev}: fixed to block column {fa} (not solved)')
            continue
        opt_names = (cfg.get('optional_open') or {}).get(lev) or []
        if opt_names:
            cfg['levels'][lev]['zoned'] = list(cfg['levels'][lev]['zoned']) + [
                n for n in opt_names if n not in cfg['levels'][lev]['zoned']]
            log(f' optional schools (solver may keep open): {opt_names}')
        if lev == 'K-5':
            P = build_k5(cfg, refs)
        elif lev == '6-8':
            gs = cfg['levels'][lev].get('group_split_by')
            if gs:
                # (Paul 2026-10-12 ~22:00, feeders option A) middle zones are built from elementary zones CUT AT the
                # high-school lines in column gs (e.g. A_hs): each piece of a K-5 zone on one side of an HS line is its
                # own unit, so middle zones can follow PPS's HS lines without changing the K-5 lines.  K-8s stay whole.
                k8s = set(cfg['levels']['K-5'].get('k8', []))
                hv = C.blocks()[gs].values
                grp = np.array([s if s in k8s else f'{s}|{h}' for s, h in zip(plan['K-5'], hv)], dtype=object)
                log(f' 6-8: groups = K-5 zones cut at {gs} lines ({len(set(grp))} pieces from '
                    f'{len(set(plan["K-5"]))} K-5 zones)')
                P = build_grouped(cfg, refs, lev, grp)
            else:
                P = build_grouped(cfg, refs, lev, plan['K-5'])
        else:
            gb = cfg['levels'][lev].get('group_by', '6-8')
            P = build_grouped(cfg, refs, lev, plan[gb])
            if cfg['levels'][lev].get('parent_split_by'):
                pb = plan[cfg['levels'][lev]['parent_split_by']]
                P.parent = pb
                P.w_parent_split = int(cfg['weights'].get('ms_split', 5000) * COST)
                if cfg['levels'][lev].get('parent_floor'):
                    pf = dict(cfg['levels'][lev]['parent_floor'])
                    pf['n_zoned'] = len(cfg['levels'][cfg['levels'][lev]['parent_split_by']]['zoned'])
                    pf['w_floor'] = int(cfg['weights'].get('ms_floor', cfg['weights'].get('durability_count_slack', 100000)) * COST)
                    P.parent_floor = pf
                    if pf.get('soft_to'):
                        P.parent_target = {'soft_to': pf['soft_to'], 'w_soft': P.w_parent_split}
                        log(f' 9-12: middle zones on one HS: near-hard floor {pf["min_share"]:.0%} '
                            f'({cfg["weights"].get("ms_floor", cfg["weights"].get("durability_count_slack"))} per zone short), '
                            f'soft push {cfg["weights"].get("ms_split")} per zone short of {pf["soft_to"]:.0%}, none beyond')
        offa = cfg['levels'][lev].get('off_reference') if lev == '9-12' else None
        for nest_key in ('hs_nest', 'ms_nest'):
            # (2026-10-14) ms_nest: the same soft cost for crossing a MIDDLE-school map (a run's 6-8 lines,
            # {'run': r, 'level': '6-8'}), so elementary lines can shift to fit whole into middle zones
            nest = cfg['levels'][lev].get(nest_key)
            if nest and lev != '9-12':
                # (v2, Paul 2026-10-12) K-5 / 6-8 zones should nest inside the high-school lines (A_hs): a kid whose
                # block's high school differs from the high school of the school building's block costs extra
                if nest.get('run') or nest.get('self'):
                    # nest in another run's high-school lines, or (self) in this run's own 9-12, solved first
                    if nest.get('self'):
                        hsv = np.asarray(plan['9-12'], dtype=object)
                        nest = dict(nest, column='this plan\'s 9-12')
                    else:
                        nl_ = nest.get('level', '9-12')
                        rp_ = os.path.join(C.SOLVER, 'out_v2', nest['run'] + ('.staging' if nest.get('staging') else ''))
                        hsv = pd.read_parquet(os.path.join(rp_, f'assign_{nl_}.parquet'))['school'].values
                        nest = dict(nest, column=f'{nest["run"]} {nl_}')
                    if P.group is not None and nest.get('hard'):
                        # grouped level: every block of an elementary zone takes the zone's majority high school, so the
                        # zone's blocks keep the same candidate set (whole zones move together)
                        import collections
                        Kg = P.kids
                        tally = collections.defaultdict(lambda: collections.defaultdict(float))
                        for i in range(P.n):
                            tally[P.group[i]][hsv[i]] += Kg[i] + 1e-6
                        gh = {g: max(t, key=t.get) for g, t in tally.items()}
                        hsv = np.array([gh[P.group[i]] for i in range(P.n)], dtype=object)
                else:
                    hsv = C.blocks()[nest['column']].values
                roots_ = C.school_block()
                bhs = {k: hsv[roots_[n]] for k, n in enumerate(P.names) if n in roots_}
                wn = float(nest['kid_miles_per_kid']) * COST

                def _add_nest(P=P, hsv=hsv, bhs=bhs, wn=wn):
                    for i, c in enumerate(P.cand):
                        for k, s_ in enumerate(c):
                            if s_ in bhs and bhs[s_] != hsv[i]:
                                P.cost[i][k] += int(round(wn * P.kids[i]))
                base_rc = getattr(P, 'recost', None)

                def _rc(base_rc=base_rc, f=_add_nest):
                    if base_rc:
                        base_rc()
                    f()
                P.recost = _rc
                if base_rc is None:
                    _add_nest()
                log(f' {lev}: each kid placed across a {nest["column"]} line ({nest_key}) costs {nest["kid_miles_per_kid"]} kid-miles')
                if nest.get('hard'):
                    # keep only candidates whose building is in the block's own high-school area (as PPS's Scenario A
                    # K-5 lines do, 36 of 37 zones); a block with no such candidate keeps its list
                    kept = 0
                    for i, c in enumerate(P.cand):
                        same = [s_ for s_ in c if bhs.get(s_) == hsv[i]]
                        if same and len(same) < len(c):
                            P.cand[i] = same
                            kept += 1
                        if P.hint[i] not in P.cand[i]:
                            P.hint[i] = P.cand[i][0]
                    log(f' {lev}: hard nesting in {nest["column"]}: {kept} blocks lost cross-line candidates')
        if offa:
                ref = C.blocks()[offa['column']].values
                wk = float(offa['kid_miles_per_kid']) * COST

                def _add_offa(P=P, ref=ref, wk=wk):
                    for i, c in enumerate(P.cand):
                        for k, s_ in enumerate(c):
                            if P.names[s_] != ref[i]:
                                P.cost[i][k] += int(round(wk * P.kids[i]))
                base_recost = getattr(P, 'recost', None)

                def _recost(base_recost=base_recost, f=_add_offa):
                    if base_recost:
                        base_recost()
                    f()
                P.recost = _recost
                if base_recost is None:
                    _add_offa()
                log(f' {lev}: each kid assigned off {offa["column"]} costs {offa["kid_miles_per_kid"]} kid-miles')
        if lev == '9-12' and cfg['levels'][lev].get('parent_split_by'):
                log(f' 9-12 groups = whole {gb} zones; each extra high school a {cfg["levels"][lev]["parent_split_by"]} '
                    f'zone feeds costs {cfg["weights"].get("ms_split", 5000)}')
        st = cfg['levels'][lev].get('start')
        if st:
            # tactical plans (Paul 2026-10-12): start from a given assignment; each kid moved off it costs
            # kid_miles_per_kid, and at most max_kids (2031-32 band kids) may move (hard budget)
            if 'column' in st:
                start = C.blocks()[st['column']].values
            else:
                start = pd.read_parquet(os.path.join(C.SOLVER, 'out_v2', st['run'], f'assign_{lev}.parquet'))['school'].values
            P.start = start
            P.budget_max = int(round(KID * st['max_kids']))
            ws = float(st.get('kid_miles_per_kid', 0.5)) * COST

            def _add_start(P=P, start=start, ws=ws):
                for i, c in enumerate(P.cand):
                    for k, s_ in enumerate(c):
                        if P.names[s_] != start[i]:
                            P.cost[i][k] += int(round(ws * P.kids[i]))
            base_st = getattr(P, 'recost', None)

            def _rcs(base_st=base_st, f=_add_start):
                if base_st:
                    base_st()
                f()
            P.recost = _rcs
            if base_st is None:
                _add_start()
            nidx = {n: k for k, n in enumerate(P.names)}
            for i in range(P.n):
                k = nidx.get(start[i])
                if k is not None and k in P.cand[i]:
                    P.hint[i] = k
            if lev == 'K-5':
                P.skip_relax = True    # warm-start round 0 from the start plan itself (it meets the budget)
            log(f' {lev}: start from {st.get("run", st.get("column"))}; <= {st["max_kids"]} kids may move '
                f'({st.get("kid_miles_per_kid", 0.5)} kid-miles each)')
        ws_ = cfg['levels'][lev].get('warm_start')
        if ws_ and not st:
            # (2026-10-12) warm start from another run's assignment at this level (same schools/candidates), e.g.
            # option2 K-5 from option1_durable when the star round finds nothing in time from the relaxation's hint.
            # Only a hint: every rule and cost is unchanged.  Skips the relaxation round.
            wp = os.path.join(C.SOLVER, 'out_v2', ws_['run'] + ('.staging' if ws_.get('staging') else ''),
                              f'assign_{lev}.parquet')
            if not os.path.exists(wp):     # staging already promoted -> the final folder holds the same file
                wp = os.path.join(C.SOLVER, 'out_v2', ws_['run'], f'assign_{lev}.parquet')
            wa = pd.read_parquet(wp)['school'].values
            nidx = {n: k for k, n in enumerate(P.names)}
            hit = 0
            for i in range(P.n):
                k = nidx.get(wa[i])
                if k is not None and k in P.cand[i]:
                    P.hint[i] = k
                    hit += 1
            P.skip_relax = True
            log(f' {lev}: warm start from {wp} ({hit}/{P.n} blocks hinted); relaxation round skipped')
        if opt_names:
            # a building that carries a fixed population (DLI strand, lottery group) is never optional
            fixed_hosts = [n for n in opt_names if n in P.names and P.fixed[P.names.index(n)] > 0]
            pc = (cfg.get('program_choice') or {}).get(lev)
            if pc:
                # (capstone) these hosts may close: their program unit moves to one of the n nearest schools
                bb_ = C.blocks()
                xy_ = {k: (bb_['x'].values[P.root[k]], bb_['y'].values[P.root[k]]) for k in range(P.S) if P.root[k] is not None}
                k8x_ = set(cfg['levels'][lev].get('k8', []))
                P.unit_alts = {}
                for n in fixed_hosts:
                    u = P.names.index(n)
                    if u not in xy_:
                        continue
                    ux, uy = xy_[u]
                    near = sorted((((xy_[k][0] - ux) * 0.70) ** 2 + (xy_[k][1] - uy) ** 2, k) for k in xy_
                                  if k != u and P.names[k] not in k8x_)
                    P.unit_alts[u] = [k for _, k in near[:int(pc.get('n_alts', 3))]]
                    # straight-line miles between the two buildings (deg lat ~ 69 mi; lon already scaled by 0.70)
                    P.unit_dist = getattr(P, 'unit_dist', {})
                    P.unit_dist[u] = {k: round(69.0 * d2 ** 0.5, 2) for d2, k in near[:int(pc.get('n_alts', 3))]}
                P.w_pm = float(cfg['weights'].get('program_move', 1.0)) * COST / KID
                log(f' program units may move (whole unit, to one of the {pc.get("n_alts", 3)} nearest schools; '
                    f'{cfg["weights"].get("program_move", 1.0)} kid-miles per student per mile moved, min 1 mi): '
                    + '; '.join(f'{P.names[u]} -> {[P.names[k] for k in a]}' for u, a in P.unit_alts.items()))
                fixed_hosts = []
            if fixed_hosts:
                log(f' not optional (fixed program/lottery population): {fixed_hosts}')
            opt_names = [n for n in opt_names if n not in fixed_hosts]
            P.optional = {P.names.index(n) for n in opt_names if n in P.names}
            P.w_open = int(cfg['weights'].get('open_school', 0) * COST)
            P.cap_receivers = cfg.get('cap_receivers_per_closure')
            area_col = {'K-5': 'es_cur', '6-8': 'ms_cur', '9-12': 'sq_hs'}[lev]
            ac = C.blocks()[area_col].values
            P.closure_area = {s: list(np.nonzero(ac == P.names[s])[0]) for s in P.optional}
            cvc = cfg['levels'][lev].get('coverage')
            if cvc:
                Dc = np.nan_to_num(C.dist(cvc.get('mode', 'walk'), P.names), nan=99.0)
                tiers = cvc.get('tiers') or [[cvc['miles'], cvc['kid_miles_per_kid']]]
                P.cov_tiers = [([list(np.nonzero(Dc[i] <= mi)[0]) for i in range(len(Dc))], float(w) * COST) for mi, w in tiers]
                log(f' {lev}: spacing cost per kid with no open school within (miles, kid-miles): {tiers} ({cvc.get("mode", "walk")})')
                hv = cvc.get('hard_vs')
                if hv:
                    import pandas as _pd
                    ref_ = _pd.read_csv(os.path.join(C.SOLVER, 'out_v2', hv['run'], 'schools.csv'))
                    ref_ = sorted(ref_[ref_['zoned_K-5'] == True].school)
                    dref = np.nan_to_num(C.dist(cvc.get('mode', 'walk'), ref_), nan=99.0).min(1)
                    lim = np.maximum(hv.get('min_mi', 1.25), dref + hv.get('slack_mi', 0.25))
                    P.cov_hard = {i: list(np.nonzero(Dc[i] <= lim[i])[0]) for i in range(len(Dc)) if P.kids[i] > 0}
                    log(f' {lev}: hard spacing rule: every block keeps an open school within max({hv.get("min_mi", 1.25)} mi, '
                        f'its distance under {hv["run"]} + {hv.get("slack_mi", 0.25)} mi)')
        mf = cfg.get('ms_hs_feeder')
        if lev == '6-8' and mf:
            K912 = MX.level_kids(cfg, '2031')['9-12']
            hcol = cfg['levels']['9-12'].get('fixed_assign') or mf.get('hs_column', 'A_hs')
            P.msfeed = {'hs': C.blocks()[hcol].values, 'w': [int(round(KID * v)) for v in K912],
                        'min_kids': int(KID * mf.get('min_kids', 5)), 'min_share': mf.get('min_share', 0.7),
                        'n_zoned': len(cfg['levels'][lev]['zoned']), 'allow': mf.get('allow_split', {}),
                        'w_split': int(cfg['weights'].get('ms_split', 5000) * COST),
                        'w_floor': int(cfg['weights'].get('ms_floor', cfg['weights'].get('durability_count_slack', 100000)) * COST)}
            log(f' middle->high feeders vs {hcol}: {mf.get("ms_split_note", "")} penalty {cfg["weights"].get("ms_split", 5000)} '
                f'per high school fed; floor {P.msfeed["min_share"]:.0%} of {P.msfeed["n_zoned"]} middle zones feed one HS')
        if lev == '9-12' and cfg['levels'][lev].get('ms_need_feedback'):
            K68 = MX.level_kids(cfg, '2031')['6-8']
            roots_ = C.school_block()
            p68 = MX.program_totals(cfg, '6-8')
            exempt = set(cfg.get('exempt_floor', []))
            k8s = set(cfg['levels']['6-8'].get('k8', []))
            mzon = [q for q in cfg['levels']['6-8']['zoned'] if q not in k8s]   # K-8s sized at K-5
            P.ms_need = {'k68': [int(round(KID * v)) for v in K68],
                         'root': {q: roots_[q] for q in mzon},
                         'net_floor': {q: (0 if q in exempt else int(round(KID * max(0.0, cfg['floors']['6-8'] - p68.get(q, 0.0)))))
                                       for q in mzon},
                         'net_cap': {q: (int(round(KID * max(0.0, MX.capacity(cfg, q) - p68.get(q, 0.0))))
                                         if not np.isnan(MX.capacity(cfg, q)) else 10 ** 6) for q in mzon},
                         'w': int(cfg['weights'].get('ms_need', 2000) * COST)}
            log(f' 9-12: 6-8 size need fed back: each HS area holds >= the middle-school floors (500 less programs) of '
                f'the {len(mzon)} middle schools whose buildings it takes, <= their capacity '
                f'({cfg["weights"].get("ms_need", 2000)} kid-miles per kid short; sizes 2031-32)')
        if cfg['levels'][lev].get('max_splits') is not None:
            P.max_splits = int(cfg['levels'][lev]['max_splits'])
        if cfg['levels'][lev].get('coarse_ties'):
            # (2026-10-13, capstone stage 1) tie blocks into connected pieces of (Status Quo zone, census block group,
            # PPS A high-school area); school buildings' own blocks stay free
            bb_ = C.blocks()
            sqz = refs['status_quo'][lev]
            lab = np.array([f'{z}|{g[:12]}|{h}' for z, g, h in zip(sqz, bb_['GEOID'].astype(str).values,
                                                                   bb_[cfg['levels']['9-12'].get('fixed_assign') or 'A_hs'].values)], dtype=object)  # (2026-10-16) the run's own HS lines
            rts = {P.root[s] for s in range(P.S) if P.root[s] is not None}
            NBt = C.adjacency()[0]
            seen_, ties = set(), []
            for i in range(P.n):
                if i in seen_ or i in rts:
                    continue
                comp_, st_ = [], [i]
                seen_.add(i)
                while st_:
                    k = st_.pop()
                    comp_.append(k)
                    for j in NBt[k]:
                        if j not in seen_ and j not in rts and lab[j] == lab[i]:
                            seen_.add(j)
                            st_.append(j)
                if len(comp_) > 1:
                    ties.append(comp_)
            P.ties = ties
            nfree = P.n - sum(len(t) for t in ties)
            log(f' {lev}: coarse ties: {len(ties)} pieces + {nfree} free blocks (from {P.n} blocks)')
        attach_durability(cfg, P, lev, log)
        ncv = sum(len(c) for c in P.cand)
        log(f' {len(P.names)} schools, {P.n} blocks, {ncv} assignment vars, avg {ncv / P.n:.1f} candidates/block')
        asg_idx, info = run_problem(P, cfg['levels'][lev].get('rooted', lev == 'K-5'), cfg['solver'], log)
        plan[lev] = np.array([P.names[s] for s in asg_idx], dtype=object)
        pdst = {}
        for inf_ in (info if isinstance(info, list) else [info]):
            pdst.update(((inf_ or {}).get('final') or {}).get('program_dest') or {})
        moved_units = {u: d for u, d in pdst.items() if u != d}
        if moved_units:
            # write the chosen unit moves into the plan's config, so scoring (v2 population: follow rates, non-followers)
            # and the outputs place each program at its new host
            progs = cfg['levels'][lev].setdefault('programs', {})
            fl_ = (cfg.get('v2') or {}).get('focus_lottery') or {}
            # (2026-10-13) pop every moving unit first, so a chain (George -> West Sylvan, West Sylvan -> Gray) moves
            # each host's own programs once instead of carrying the first unit along the chain
            popped = {u: progs.pop(u) for u in moved_units if u in progs}
            for u, d in moved_units.items():
                if u in popped:
                    progs[d] = progs.get(d, []) + popped[u]
                if u in fl_:
                    fl_[u].setdefault('placement', {})[lev] = {d: 1.0}
            cfg.setdefault('program_result', {})[lev] = moved_units
            log(f' {lev}: program units moved {moved_units}')
        if opt_names:
            used = set(plan[lev])
            closed = [n for n in opt_names if n not in used]
            cfg['levels'][lev]['zoned'] = [n for n in cfg['levels'][lev]['zoned'] if n not in closed]
            cfg.setdefault('optional_result', {})[lev] = {'kept_open': sorted(set(opt_names) & used),
                                                          'closed': sorted(closed)}
            log(f' {lev}: kept open {sorted(set(opt_names) & used)}; closed {sorted(closed)}')
        times[lev] = round(time.time() - t0, 1)
        infos[lev] = info
        log(f' {lev} done in {times[lev]}s')
        b = C.blocks()
        pd.DataFrame({'idx': np.arange(len(b)), 'GEOID': b['GEOID'].values, 'school': plan[lev]}).to_parquet(
            os.path.join(out, f'assign_{lev}.parquet'), index=False)
        with open(ck, 'w') as f:
            json.dump({'infos': infos, 'times': times}, f, default=float)
    extra = {'solve': {'seconds': times, 'components': infos}}
    if cfg.get('optional_result'):
        extra['optional_schools'] = cfg['optional_result']
    if cfg.get('program_result'):
        extra['program_moves'] = cfg['program_result']
    sc = MX.write_plan(out, cfg, plan, refs, extra=extra)
    write_infeasibility(out, cfg, plan, infos)
    log(MX.headline(sc).to_string())
    return sc


def attach_durability(cfg, P, lev, log):
    """Durability mode: require, every year 2031-32..2040-41, at least as many zoned non-exempt
    schools at target as Scenario A has (PSU medium ratios), and reward schools that stay at target
    in every year.  2031-32 floors stay hard (they are the ordinary size bounds)."""
    dcfg = cfg.get('durability') or {}
    if not dcfg.get('mode'):
        P.dur = None
        return
    ref = dcfg.get('reference', 'scenario_A')
    rc = C.load_config(os.path.join(cfg.get('_cfgdir', os.path.join(C.SOLVER, 'configs')), f'{ref}.json'))
    hname, H = C.horizon(cfg)
    # the reference plan is scored on THIS option's horizon (pps2031: required 2027-28 .. 2031-32)
    rd = MX.durability(rc, MX.plan_from_columns(rc), horizon=hname)['levels'][lev]['at_target_zoned']
    YRS = H['required']
    if dcfg['mode'] == 'all' and getattr(P, 'optional', None):
        req = {}          # every OPEN countable school must be durable (solve_component, all_open)
    elif dcfg['mode'] == 'all':
        req = {y: sum(1 for s in range(P.S) if P.lo_raw[s] is not None) for y in YRS}
    else:
        req = {y: rd[y] for y in YRS}
    w = dict(cfg['weights'], **cfg['levels'][lev].get('weights', {}))   # (2026-10-14) per-level prices, e.g. a priced 6-8 target
    # 'ratios' keys = the years the solver models (pps2031: only the required years; the reported years 2032-33 ..
    # 2035-36 are scored afterwards, not optimized).  v2 uses per-year sizes (sz_y), so the ratio values are unused.
    ratios = C.year_ratios(lev) if hname == 'psu2041' else {y: 1.0 for y in YRS}
    if hname != 'psu2041' and not MX.is_v2(cfg):
        raise ValueError('horizon pps2031 needs model v2')
    P.dur = {'ratios': ratios, 'required': req, 'horizon': hname,
             'countable': {s for s in range(P.S) if P.lo_raw[s] is not None},
             'w_durable': int(w.get('durable_school', 3000) * COST),
             'w_year': int(w.get('school_year_at_target', 100) * COST),
             'w_count_slack': int(w.get('durability_count_slack', 100000) * COST),
             'min_durable': (dcfg.get('min_durable') or {}).get(lev),
             'all_open': dcfg['mode'] == 'all' and bool(getattr(P, 'optional', None))}
    if MX.is_v2(cfg):
        # per-year block sizes and fixed populations (model v2, fix 6); built after candidate pruning
        P.dur['_v2_build'] = lambda: _v2_durability_sizes(cfg, P, lev)
    log(f' durability mode ({dcfg["mode"]}, horizon {hname}: {list(YRS)[0]}..{list(YRS)[-1]}): required at target by year {list(req.values())} '
        f'(reference {ref}); {len(P.dur["countable"])} countable schools'
        + (f'; at least {P.dur["min_durable"]} at target in every year' if P.dur['min_durable'] else ''))


def _v2_durability_sizes(cfg, P, lev):
    if True:
        names_idx = {n: k for k, n in enumerate(P.names)}
        k8 = set(cfg['levels'][lev].get('k8', [])) if lev == 'K-5' else set()
        k8i = {names_idx[n] for n in k8 if n in names_idx}
        P.dur['sz_y'], P.dur['fixed_y'] = {}, {}
        for y in P.dur['ratios']:
            K = MX.level_kids(cfg, y[:4])
            Ky = K[lev]
            K68 = K['6-8']
            P.dur['sz_y'][y] = [[int(round(KID * (Ky[i] + (K68[i] if s in k8i else 0.0)))) for s in c]
                                for i, c in enumerate(P.cand)]
            prog = MX.program_totals(cfg, lev, y[:4])
            if lev == 'K-5':
                p68 = MX.program_totals(cfg, '6-8', y[:4])
                for nn in k8:
                    prog[nn] = prog.get(nn, 0.0) + p68.get(nn, 0.0)
            P.dur['fixed_y'][y] = [int(round(prog.get(n, 0.0) * KID)) for n in P.names]


def write_infeasibility(out, cfg, plan, infos):
    bt = MX.building_table(cfg, plan)
    focus = set(cfg.get('focus', []))
    rows = bt[(bt['below_floor'] | bt['above_ceiling']) & ~bt['school'].isin(focus)]
    rep = {'schools_out_of_range_2031_32': [
        {'school': r.school, 'type': r.type, 'size': round(r.total, 1), 'floor': r.floor,
         'ceiling': r.ceiling, 'short_by': round(r.short_by, 1), 'over_by': round(r.over_by, 1),
         'program_only': bool(r.program_only)} for r in rows.itertuples()],
        'solver_slack': {lev: [c['final']['slack'] for c in infos[lev]] for lev in infos},
        'feeder_splits_used': {lev: [c['final'].get('splits', 0) for c in infos[lev]] for lev in infos},
        'exempt_from_floor': cfg.get('exempt_floor', []),
        'note': 'Slack is in kids; non-zero slack means no plan with these schools/programs can meet that bound '
                'given the candidate sets and contiguity. Program-only buildings have fixed sizes set by the '
                'program placement, not by lines.'}
    with open(os.path.join(out, 'infeasibility.json'), 'w') as f:
        json.dump(rep, f, indent=1, default=float)
    return rep


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('config', nargs='?', default=os.path.join(C.SOLVER, 'configs', 'option1.json'))
    ap.add_argument('--from', dest='start', default='K-5', choices=C.LEVELS,
                    help='reuse earlier levels from out/<name>/ checkpoints')
    a = ap.parse_args()
    run(a.config, a.start)
