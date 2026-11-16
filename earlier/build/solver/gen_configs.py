"""Write the plan/option configs in configs/*.json.

A config describes one plan:
  levels.<L>.zoned      schools that have an attendance area at that level
  levels.<L>.k8         K-8 buildings (their 6-8 area = their K-5 area; building size = K-8 total)
  levels.<L>.programs   {host building: [program keys from common.PROGRAMS]}  (fixed populations)
  levels.<L>.assign     (baselines only) block column holding the plan's assignment
  floors / ceilings / exemptions / weights / solver settings
Baselines (today, status_quo, scenario_A, scenario_B) are evaluated, not solved.
Options are solved by solve.py.
"""
import json
import os

import common as C

OUT = os.path.join(C.SOLVER, 'configs')
os.makedirs(OUT, exist_ok=True)
b = C.blocks()

K8_TODAY = ['Astor', 'Beverly Cleary', 'Bridger', 'Cesar Chavez', 'Faubion', 'Laurelhurst',
            'Skyline', 'Sunnyside', 'Vernon']
K8_AB = ['Astor', 'Skyline']

PROG_TODAY = {
    'K-5': {'Ainsworth': ['Ainsworth|Spanish'], 'Atkinson': ['Atkinson|Spanish'], 'Beach': ['Beach|Spanish'],
            'Cesar Chavez': ['Cesar Chavez|Spanish K-5'], 'Clark': ['Clark|Mandarin'],
            'James John': ['James John|Spanish'], 'Kelly': ['Kelly|Russian'], 'Lent': ['Lent|Spanish'],
            'MLK Jr': ['MLK Jr|Mandarin'], 'Rigler': ['Rigler|Spanish'],
            'Rose City Park': ['Rose City Park|Vietnamese'], 'Scott': ['Scott|Spanish'],
            'Sitton': ['Sitton|Spanish'], 'Woodstock': ['Woodstock|Mandarin'], 'Richmond': ['Richmond|Japanese']},
    '6-8': {'Cesar Chavez': ['Cesar Chavez|Spanish 6-8'], 'West Sylvan': ['West Sylvan|Spanish'],
            'Kellogg': ['Kellogg|Spanish'], 'George': ['George|Spanish'], 'Beaumont': ['Beaumont|Spanish'],
            'Roseway Heights': ['Roseway Heights|Spanish', 'Roseway Heights|Vietnamese'],
            'Ockley Green': ['Ockley Green|Spanish'], 'Harrison Park': ['Harrison Park|Mandarin'],
            'Tubman': ['Tubman|Mandarin'], 'Mt Tabor': ['Mt Tabor|Japanese'], 'Lane': ['Lane|Russian']},
    '9-12': {'Lincoln': ['Lincoln|Spanish'], 'Roosevelt': ['Roosevelt|Spanish', 'Roosevelt|PISA'],
             'McDaniel': ['McDaniel|Spanish', 'McDaniel|Vietnamese', 'McDaniel|PISA'],
             'Franklin': ['Franklin|Spanish', 'Franklin|Russian'], 'Cleveland': ['Cleveland|Mandarin'],
             'Jefferson': ['Jefferson|Mandarin'], 'Grant': ['Grant|Japanese']},
}
PROG_A = {
    'K-5': {'Ainsworth': ['Ainsworth|Spanish'],
            'Cesar Chavez': ['Cesar Chavez|Spanish K-5', 'Beach|Spanish', 'James John|Spanish', 'Sitton|Spanish'],
            'Lent': ['Lent|Spanish', 'Atkinson|Spanish'], 'Rigler': ['Rigler|Spanish', 'Scott|Spanish'],
            'Boise-Eliot/Humboldt': ['MLK Jr|Mandarin'], 'Woodstock': ['Woodstock|Mandarin', 'Clark|Mandarin'],
            'Kelly': ['Kelly|Russian'], 'Vestal': ['Rose City Park|Vietnamese'], 'Richmond': ['Richmond|Japanese']},
    '6-8': {'West Sylvan': ['West Sylvan|Spanish'], 'Kellogg': ['Kellogg|Spanish'],
            'George': ['George|Spanish', 'Ockley Green|Spanish', 'Cesar Chavez|Spanish 6-8'],
            'Roseway Heights': ['Roseway Heights|Spanish', 'Beaumont|Spanish', 'Roseway Heights|Vietnamese'],
            'Harrison Park': ['Harrison Park|Mandarin'], 'Tubman': ['Tubman|Mandarin'],
            'Mt Tabor': ['Mt Tabor|Japanese'], 'Lane': ['Lane|Russian']},
    '9-12': PROG_TODAY['9-12'],
}
PROG_B = json.loads(json.dumps(PROG_A))
PROG_B['K-5'].pop('Vestal')
PROG_B['K-5']['Rose City Park'] = ['Rose City Park|Vietnamese']

FOCUS = ['Winterhaven', 'da Vinci', 'Odyssey', 'ACCESS', 'MLC', 'Benson']

COMMON = {
    'basis': '2031-32 (PSU forecast; block kids scaled by area, see METHOD.md)',
    'lr_nbhd_share': 0.02,
    'floors': {'K-5': 360, 'K-8': 500, '6-8': 500, '9-12': 1100},
    'ceiling_k5_max': 600,
    'exempt_floor': ['Astor', 'Skyline'],
    'exempt_hold_status_quo': True,   # exempt K-8s may not shrink below their Status-Quo 2031-32 size
    'capacity_overrides': {
        # HS: Sept 15 2026 deck slide 21 (2025 'Jefferson is Rising') where given, else LRFP 2021
        'Jefferson': 1773, 'Grant': 1935, 'McDaniel': 1735, 'Roosevelt': 1404,
        # Harrison Park was a K-8 in 2021 (1006 at the 100% K-8 rate); PPS 2025 utilization model
        # value (85% MS rate) via meub/pps-data
        'Harrison Park': 890,
    },
    'hs_range_max': 350,
    'focus': FOCUS,
    'past_margin_miles': 0.25,
}


def zoned(col):
    return sorted(b[col].unique().tolist())


def baseline(name, label, cols, k8, prog):
    cfg = dict(COMMON)
    cfg.update({'name': name, 'label': label, 'kind': 'baseline', 'levels': {}})
    for lev, col in zip(C.LEVELS, cols):
        cfg['levels'][lev] = {'assign': col, 'zoned': zoned(col), 'programs': prog[lev],
                              'k8': [s for s in k8 if s in zoned(col)] if lev != '9-12' else []}
    return cfg


cfgs = [
    baseline('today', 'Today (2025-26 lines, today\'s programs)', ['es_cur', 'ms_cur', 'hs_cluster_cur'],
             K8_TODAY, PROG_TODAY),
    baseline('status_quo', 'Status Quo 2027-28 (PPS map; Jefferson dual assignment ended)',
             ['sq_es', 'sq_ms', 'sq_hs'], K8_TODAY, PROG_TODAY),
    baseline('scenario_A', 'PPS Scenario A (digitized PPS maps)', ['A_es', 'A_ms', 'A_hs'], K8_AB, PROG_A),
    baseline('scenario_B', 'PPS Scenario B (digitized PPS maps)', ['B_es', 'B_ms', 'B_hs'], K8_AB, PROG_B),
]
# Today's 9-12: in 2025-26 the Jefferson dual zones chose Jefferson or the partner school;
# hs_cluster_cur pools them with the partner, so Jefferson has no neighborhood area in 'today'.

opt1 = dict(COMMON)
opt1.update({
    'name': 'option1_2031only',
    'label': 'Option 1 (2031-only): district-like (Scenario A closures, conversions, DLI placements; only the lines change), sized to 2031-32 floors only',
    'kind': 'option',
    'move_baseline': 'status_quo',
    'levels': {
        'K-5': {'zoned': zoned('A_es'), 'k8': K8_AB, 'programs': PROG_A['K-5'], 'hint': 'A_es',
                'n_cand': 7, 'rooted': True},
        '6-8': {'zoned': zoned('A_ms'), 'k8': K8_AB, 'programs': PROG_A['6-8'], 'hint': 'A_ms',
                'n_cand': 5, 'rooted': True},
        '9-12': {'zoned': zoned('A_hs'), 'k8': [], 'programs': PROG_A['9-12'], 'hint': 'A_hs',
                 'n_cand': 4, 'rooted': True},
    },
    # objective weights, in kid-miles per unit (walk = 1 per kid-mile)
    'weights': {
        'walk': 1.0,            # per kid-mile of walking (K-5, 6-8 and 9-12 all use walk miles)
        'past': 0.25,           # per kid assigned >= past_margin_miles beyond the nearest eligible open school
        'move': 0.15,           # per kid reassigned vs the 2027-28 Status Quo
        'perim': 3.0,           # per km of attendance-area boundary (shared Voronoi edge length)
        'diversity': 0.0,       # per kid of deviation beyond a +/- band from the district kids-of-color share
        'diversity_band': 0.15,
        'split': 5000.0,        # per split feeder (phase 2 only, when whole-zone feeders are infeasible); large so splits are minimised first
        'hs_range': 2.0,        # per kid of HS enrollment range above 350
        'slack': 10000.0,       # per kid outside a size bound (infeasibility)
    },
    'solver': {'time_first': 120, 'time_round': 60, 'time_star': 300, 'max_rounds': 10, 'workers': 6},
})
cfgs.append(opt1)

for c in cfgs:
    with open(os.path.join(OUT, c['name'] + '.json'), 'w') as f:
        json.dump(c, f, indent=1)
    print('wrote', c['name'])


# ------------------------------------------------------------------------------------------
# Durability mode (default for every option after Option 1 (2031-only)):
#   every year 2031-32..2040-41, at least as many zoned schools at target as Scenario A has
#   (PSU medium district ratios), 2031-32 floors still hard, heavy reward per school that
#   stays at target through 2040-41.
# ------------------------------------------------------------------------------------------
DUR = {'mode': 'meet_reference', 'reference': 'scenario_A',
       'note': 'count of zoned non-exempt schools at target >= reference count, each year 2031-32..2040-41'}
DUR_W = {'durable_school': 3000.0,          # per school at target every year 2031-32..2040-41
         'school_year_at_target': 100.0,    # per school-year at target
         'durability_count_slack': 100000.0}


def variant(base, **kw):
    c = json.loads(json.dumps(base))
    for k, v in kw.items():
        c[k] = v
    return c


opt1d = variant(opt1, name='option1_durable',
                label='Option 1-durable: Scenario A schools and programs; lines drawn so at least as many schools as A stay at target every year to 2040-41',
                durability=DUR)
opt1d['weights'].update(DUR_W)
opt1d['weights']['split'] = 20000.0   # above the durability reward, so splits stay a feasibility-only device
opt1d['solver'].update({'time_first': 180, 'time_star': 600})
# 9-12 rule (Paul, 2026-10-12): whole ELEMENTARY zones go to high schools, so a middle school may split
# between high schools but no elementary zone does; each extra high school a middle zone feeds costs
# ms_split (above the per-school durability reward, so splits are bought only by hard requirements).
opt1d['levels']['9-12'].update({'group_by': 'K-5', 'parent_split_by': '6-8', 'n_cand': 5})
opt1d['weights']['ms_split'] = 5000.0

# Option 2: DLI stays put.  A strand stays in its 2025-26 building when the building stays open
# and the strand is viable (2031-32 >= 132 K-5 / 60 6-8, targets.md 2.3); otherwise A's destination.
PROG_2 = {
    'K-5': {'Ainsworth': ['Ainsworth|Spanish'], 'Atkinson': ['Atkinson|Spanish'], 'Scott': ['Scott|Spanish'],
            'MLK Jr': ['MLK Jr|Mandarin'], 'Kelly': ['Kelly|Russian'], 'Lent': ['Lent|Spanish'],
            'Rigler': ['Rigler|Spanish'], 'Richmond': ['Richmond|Japanese'],
            'Cesar Chavez': ['Cesar Chavez|Spanish K-5', 'Beach|Spanish', 'James John|Spanish', 'Sitton|Spanish'],
            'Woodstock': ['Woodstock|Mandarin', 'Clark|Mandarin'],
            'Vestal': ['Rose City Park|Vietnamese']},
    '6-8': {'West Sylvan': ['West Sylvan|Spanish'], 'Kellogg': ['Kellogg|Spanish'],
            'George': ['George|Spanish', 'Ockley Green|Spanish', 'Cesar Chavez|Spanish 6-8'],
            'Beaumont': ['Beaumont|Spanish'],
            'Roseway Heights': ['Roseway Heights|Spanish', 'Roseway Heights|Vietnamese'],
            'Harrison Park': ['Harrison Park|Mandarin'], 'Tubman': ['Tubman|Mandarin'],
            'Mt Tabor': ['Mt Tabor|Japanese'], 'Lane': ['Lane|Russian']},
    '9-12': PROG_A['9-12'],
}
opt2 = variant(opt1d, name='option2', label='Option 2: DLI stays put (Scenario A closures; viable strands stay in open buildings)')
for lev in C.LEVELS:
    opt2['levels'][lev]['programs'] = PROG_2[lev]
opt2['todo'] = ('Strands are placed by the viability rule up front.  PLAN also allows moving a strand when that is '
                'the only way to keep a school in range; the engine has no program-placement variables yet, so '
                'that case shows up as size slack in infeasibility.json and must be resolved by hand or by adding '
                'placement variables.')

# Option 3a: Winterhaven (K-8) and da Vinci (6-8) close; their students return to neighborhood schools.
opt3a = variant(opt1d, name='option3a', label='Option 3a: as Option 1 (A closure list) but Winterhaven and da Vinci close',
                dissolve_programs=['Winterhaven', 'da Vinci'],
                focus=[f for f in FOCUS if f not in ('Winterhaven', 'da Vinci')])
opt3b = variant(opt3a, name='option3b', label='Option 3b: as 3a, and the solver may keep open neighborhood schools that A closes',
                optional_open={'K-5': ['Beach', 'Buckman', 'Creston', 'Irvington', 'James John', 'Lewis', 'Maplewood',
                                       'Marysville', 'Peninsula', 'Rose City Park', 'Sabin', 'Stephenson', 'Woodmere'],
                               '6-8': ['Sellwood']},
                status='needs engine feature: open/close variables y_s (x[i,s] <= y_s, size bounds scaled by y_s, '
                       'objective term per open school); not runnable yet')

# Option 4: fewest moves vs today, every school in range, walk cap.
opt4 = variant(opt1d, name='option4', label='Option 4: fewest moves (A closures/programs; minimise kids reassigned vs today, walk cap)',
               move_baseline='today')
opt4['weights'].update({'walk': 0.3, 'past': 0.1, 'move': 2.0})
opt4['levels']['K-5']['max_walk_mi'] = 1.5
opt4['todo'] = ('move weight is applied vs Status Quo 2027-28 in solve._costs (SQ = today except the Jefferson '
                'sunset and ~20 K-5 kids); switch the reference column if moves vs today are wanted exactly.  '
                'max_walk_mi only filters K-5 candidates (each block keeps its SQ school).')

# Option 5 placeholder: built to last.
opt5 = variant(opt1d, name='option5', label='Option 5 (placeholder): built to last - every school at target through 2040-41; solver chooses closures',
               durability={'mode': 'all', 'reference': 'scenario_A',
                           'note': 'every zoned non-exempt school at target every year 2031-32..2040-41'},
               optional_open={'K-5': 'all current K-5/K-8 buildings', '6-8': 'all current 6-8 buildings'},
               status='placeholder: needs open/close variables (as 3b) and a closure-count / cost objective; do not run yet')

for c in (opt1d, opt2, opt3a, opt3b, opt4, opt5):
    with open(os.path.join(OUT, c['name'] + '.json'), 'w') as f:
        json.dump(c, f, indent=1)
    print('wrote', c['name'])
