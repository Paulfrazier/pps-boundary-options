"""Write model-v2 configs to configs/v2/*.json from the v1 configs (run gen_configs.py first).

v1 configs are untouched, so  `python solve.py configs/option1_durable.json`  still reproduces v1 into out/.
v2:  `python metrics.py --v2 status_quo scenario_A scenario_B`  -> out_v2/<name>/
     `python solve.py configs/v2/option1_durable.json`           -> out_v2/option1_durable/
"""
import json
import os

import common as C

SRC = os.path.join(C.SOLVER, 'configs')
OUT = os.path.join(SRC, 'v2')
os.makedirs(OUT, exist_ok=True)

CAPTURE = ('PPS Enrollment Summary Oct 2025 by neighborhood and type of school attended, p. 1 '
           '(build/pps-texts/boardbook-2026-10/pps-enrollment-summary-oct-2025-capture-rates.md)')
ENROLL = 'ODE Fall Membership 2025-26 (build/data/schools.csv enr_total)'


def lottery(placement):
    """fix 1. in_zone = own-neighborhood-school students living in the area (PPS capture report);
    enrollment = 2025-26 building enrollment.  placement per band: 'host' (focus runs) or 'home' (returns)."""
    return {
        'Sunnyside': {'in_zone_2025_26': 219, 'enrollment_2025_26': 485, 'source': f'{CAPTURE}; {ENROLL}',
                      'placement': placement['Sunnyside']},
        'Bridger': {'in_zone_2025_26': 143, 'enrollment_2025_26': 446, 'source': f'{CAPTURE}; {ENROLL}',
                    'placement': placement['Bridger']},
        'Buckman': {'in_zone_2025_26': 133, 'enrollment_2025_26': 283, 'source': f'{CAPTURE}; {ENROLL}',
                    'placement': placement['Buckman']},
    }


HOST_ALL = {'Sunnyside': {'K-5': 'host', '6-8': 'host'}, 'Bridger': {'K-5': 'host', '6-8': 'host'},
            'Buckman': {'K-5': 'host'}}
# Scenario A/B (memo + Family Guides p.3): Sunnyside focus discontinued (K-8 -> K-5 neighborhood); Bridger keeps its
# Creative Science focus as a K-5 (6-8 students go to Harrison Park "or return to their neighborhood middle school");
# Buckman closes and its arts focus closes with it.  Focus students return to their neighborhood schools
# (Family Guide p.2 footnote).
# Revised 2026-10-12 (Paul): a school's OWN change follows PPS's stated rule for it; the footnote ("students return to
# their neighborhood school") covers only schools with no change of their own.
#  - Buckman closes: enrolled students split 50/50 Abernethy/Sunnyside (Oct 6 memo, file 14509719, p. 2).  In-zone kids
#    follow the traced line (Sunnyside guide p. 3: "the area north of Burnside"); lottery kids are a fixed 50/50.
#  - Sunnyside K-5 lottery kids "permitted to remain through 5th grade" (Sunnyside guide p. 3), no new lottery:
#    phase out at the host, then home.  Sunnyside 6-8 lottery kids go home: the guide sends "Neighborhood 6th-8th
#    graders" to Hosford, and PPS's Hosford projection (557 in 2031-32) has no room for them.
#  - Bridger 6-8 students "would be reassigned to Harrison Park Middle School or could choose to return to their
#    neighborhood middle school" (Bridger guide p. 3): lottery 6-8 kids -> Harrison Park (the stated default).
AFTER_A = {'Sunnyside': {'K-5': 'phase_out', '6-8': 'home'},
           'Bridger': {'K-5': 'host', '6-8': {'Harrison Park': 1.0}},
           'Buckman': {'K-5': {'Abernethy': 0.5, 'Sunnyside': 0.5}}}

LENT = {'kids_2025_26': 117,
        'source': (f'{CAPTURE}: Lent row, 117 Lent-area PPS students attend another neighborhood school '
                   '(Marysville by design; Closure Commutes cites ~115). Marysville closure memo: "pre-SEGC Lent non-DLI '
                   'area -> Kelly" (build/data/scenarios.json closures)')}

V2_COMMON_CAPS = {
    # fix 4: PPS School Profiles 2025-26 functional capacity for every school (v2.capacity); only override kept:
    # Jefferson post-modernization capacity, PPS Sept 15 2026 deck slide 21 (2025 "Jefferson is Rising" KPIs):
    # 1,590 now -> 1,773 modernized.  Profiles give Jefferson 1,590.
    'Jefferson': 1773,
}


def to_v2(c, placement, today_like=False):
    c = json.loads(json.dumps(c))
    c['model_version'] = 'v2'
    c['capacity_overrides'] = dict(V2_COMMON_CAPS)
    c['v2'] = {'focus_lottery': lottery(placement), 'lent_nondli': LENT,
               'dli_follow': 'build/data/v2/dli_follow.json',
               'capacity': 'build/data/v2/capacity_2025_26.csv',
               'psu_by_year': 'build/data/v2/psu_table5_5_by_year.csv',
               # fix 1 returners live where Census band residents live in the host's 2025-26 HS cluster (the
               # build/data convention for all focus homes); 'other_nbhd' (first pass) over-weighted Whitman/Kellogg
               'returner_weighting': 'residents'}
    if today_like:
        # Lent is whole-school DLI today; its area's non-DLI kids attend Marysville.  Lent becomes program-only.
        c['v2']['reassign_K5'] = {'Lent': 'Marysville'}
        for lev in ('K-5',):
            c['levels'][lev]['zoned'] = [s for s in c['levels'][lev]['zoned'] if s != 'Lent']
    if 'solver' in c:
        c['solver']['workers'] = 4
        # v2 solver budget.  Paul 2026-10-12 (speed-up B): per-round limits roughly halved vs the first v2 runs
        # (rounds were hitting their limits with little objective change); hard constraints unchanged.
        c['solver'].update(time_first=90, time_star=300, time_round=30, time_first_2a=30, time_star_2a=300,
                           slack_rounds=0)
    # middle -> high feeders (Paul 2026-10-12): penalize each high school a middle zone feeds (ms_split) and require
    # >= 70% of middle zones to feed one high school (Scenario A: 80%; PPS KPI target 100%)
    if 'solver' in c:
        c['ms_hs_feeder'] = {'min_share': 0.7, 'min_kids': 5}
        # our K-5 zones must nest in the fixed HS lines or no middle plan can reach 70% (first rerun: 5/15 at best
        # with the earlier K-5 zones, proven optimal) -> each kid placed across an A_hs line costs 1 kid-mile
        # soft (1 kid-mile) still left 7 of 37 K-5 zones across HS lines and 6/15 middle zones on one HS -> hard
        c['levels']['K-5']['hs_nest'] = {'column': 'A_hs', 'kid_miles_per_kid': 1.0, 'hard': True}
    return c


def load(n):
    return json.load(open(os.path.join(SRC, f'{n}.json')))


out = {
    'today': to_v2(load('today'), HOST_ALL, today_like=True),
    'status_quo': to_v2(load('status_quo'), HOST_ALL, today_like=True),
    'scenario_A': to_v2(load('scenario_A'), AFTER_A),
    'scenario_B': to_v2(load('scenario_B'), AFTER_A),
}
# PPS baselines follow PPS's Marysville phase-in (Paul 2026-10-12, revised decision 1): the Lent-area non-DLI kids now
# at Marysville stay with Marysville's student body at Arleta ("Avoiding multiple moves: Delaying full
# implementation ...", Marysville Family Guide p. 3).  Options assign them by where they live.
for n in ('scenario_A', 'scenario_B'):
    out[n]['v2']['lent_nondli'] = dict(LENT, baseline_to='Arleta')
# PPS baselines: Sellwood MS closes in 2028 (Hosford Family Guide p. 3; Sellwood guide shows 523 in 2027-28), so its
# Status Quo 6-8 area stays at Sellwood in 2027-28 (Paul 2026-10-20).  Options assign by their own lines.
SELLWOOD_2028 = [{'level': '6-8', 'through': 2027, 'area_col': 'sq_ms', 'area': 'Sellwood', 'school': 'Sellwood',
                  'source': 'PPS Family Guide, Hosford p. 3 ("planned closure in 2028"); Sellwood guide 2027-28 = 523'},
                 # enrolled 7th/8th graders stay when a 6-8 line moves between open middle schools; new 6th graders
                 # follow the new line (fitted to PPS's 2027-32 guide numbers, Paul 2026-10-20 "do it like PPS does")
                 {'level': '6-8', 'kind': 'enrolled_stay', 'area_col': 'sq_ms', 'schedule': {'2027': 2 / 3, '2028': 1 / 3},
                  'source': 'fitted to PPS Family Guide 6-8 projections 2027-28..2031-32 (A and B): cuts squared '
                            'gap vs PPS 78% (Jackson->Gray, Kellogg/Harrison Park, Ockley Green->George, Hosford->Kellogg)'}]
for n in ('scenario_A', 'scenario_B'):
    out[n]['phase_in'] = SELLWOOD_2028
A_HS = {'fixed_assign': 'A_hs', 'note': ('Paul 2026-10-12: keep Scenario A\'s official 9-12 lines in all options '
                                          '(feeder splits did not pay in v1 Option 1-durable)')}
for n in ('option1_durable', 'option2', 'option3a', 'option3b', 'option4', 'option5'):
    c = to_v2(load(n), AFTER_A)
    c['levels']['9-12'] = dict(c['levels']['9-12'], **A_HS)
    out[n] = c
# option 2: Paul 2026-10-12 (late): no longer on hold for the Oct 13 TLE meeting; runs right after option1_durable.

for n, c in out.items():
    with open(os.path.join(OUT, f'{n}.json'), 'w') as f:
        json.dump(c, f, indent=1)
    print('wrote v2', n)

# Frontier (Paul 2026-10-12): walkability vs durability on Scenario A's schools/programs and 9-12 lines, same hard
# rule (meet or beat A's count at target every year).  k17 = no durability reward (most walkable plan exactly as
# durable as PPS); k19/k21 = at least N K-5 schools at target in all ten years (A has 17 on model v2), no reward
# beyond that; 6-8 gets A+1 / A+2 (A has 6).  End point = option1_durable.
FRONTIER = {'frontier_k17': {'K-5': None, '6-8': None}, 'frontier_k19': {'K-5': 19, '6-8': 7},
            'frontier_k21': {'K-5': 21, '6-8': 8}}
for n, mins in FRONTIER.items():
    c = json.loads(json.dumps(out['option1_durable']))
    c['name'] = n
    c['label'] = (f'Frontier {n[-3:]}: Scenario A schools/programs/9-12 lines; meet A\'s count every year; '
                  + ('no durability reward (most walkable)' if not mins['K-5'] else
                     f'at least {mins["K-5"]} K-5 and {mins["6-8"]} 6-8 schools at target all ten years, no reward beyond'))
    c['weights']['durable_school'] = 0.0
    c['weights']['school_year_at_target'] = 0.0
    c['durability']['min_durable'] = {k: v for k, v in mins.items() if v}
    c['kind'] = 'frontier'
    with open(os.path.join(OUT, f'{n}.json'), 'w') as f:
        json.dump(c, f, indent=1)
    print('wrote v2', n)

# Options 3b and 5 (engine feature added 2026-10-12: optional schools with open/close variables, solve.py)
A_CLOSED = {'K-5': ['Beach', 'Buckman', 'Creston', 'Irvington', 'James John', 'Lewis', 'Maplewood', 'Marysville',
                    'Peninsula', 'Rose City Park', 'Sabin', 'Stephenson', 'Woodmere'], '6-8': ['Sellwood']}
o3b = out['option3b']
o3b.pop('status', None)
o3b['optional_open'] = A_CLOSED

o3b['optional_note'] = ('Solver may keep open any neighborhood school Scenario A closes, if every open school stays in '
                        'range (2031-32 hard, durability count rule as Option 1).  Programs stay where A puts them.')
with open(os.path.join(OUT, 'option3b.json'), 'w') as f:
    json.dump(o3b, f, indent=1)
o5 = out['option5']
o5.pop('status', None)
PROGRAM_HOSTS = {lev: set(o5['levels'][lev].get('programs', {})) for lev in ('K-5', '6-8')}
o5['optional_open'] = {}
for lev in ('K-5', '6-8'):
    allz = list(o5['levels'][lev]['zoned']) + [n for n in A_CLOSED[lev] if n not in o5['levels'][lev]['zoned']]
    o5['optional_open'][lev] = [n for n in allz if n not in PROGRAM_HOSTS[lev] and n not in o5['exempt_floor']]
o5['cap_receivers_per_closure'] = 2

o5['label'] = ('Option 5: built to last - solver chooses which neighborhood schools stay open; every open school at '
               'target every year 2031-32..2040-41; at most 2 receiving schools per closure')
o5['optional_note'] = ('Program hosts (A placement), exempt K-8s (Astor, Skyline) and buildings with a fixed lottery/'
                       'program population stay open.  Receiving cap: PPS deck 2026-10-06 p. 11 / '
                       'https://youtu.be/zOUH2Jq7Owo?t=5941.  9-12 keeps A\'s lines (not solved).')
with open(os.path.join(OUT, 'option5.json'), 'w') as f:
    json.dump(o5, f, indent=1)
print('wrote v2 option3b, option5 (runnable)')


# Options 3c / 3d (Paul 2026-10-12): as 3a, plus more focus options closed; students return to neighborhood schools by
# home location (focus_dli_homes.parquet).  Benson and MLC stay open in both.  ACCESS = grades 1-8 TAG (services not
# modeled).  Odyssey is a program inside a building, so closing it changes no building.
for n, extra, lab in (('option3c', ['Odyssey', 'ACCESS'], 'Option 3c: as 3a, and Odyssey and ACCESS also close (no focus options except Benson and MLC)'),
                      ('option3d', ['Odyssey'], 'Option 3d: as 3a, and Odyssey also closes; ACCESS stays')):
    c = json.loads(json.dumps(out['option3a']))
    c['name'], c['label'] = n, lab
    c['dissolve_programs'] = ['Winterhaven', 'da Vinci'] + extra
    c['focus'] = [f for f in c['focus'] if f not in c['dissolve_programs']]
    with open(os.path.join(OUT, f'{n}.json'), 'w') as f:
        json.dump(c, f, indent=1)
    print('wrote v2', n)


# option1_durable_hs (Paul 2026-10-12): "tactical HS".  Same K-5 and 6-8 plan as option1_durable WITHOUT the feeder
# floor (its first v2 solve, kept in out_v2/option1_durable_msfeed_off/), and 9-12 lines that may leave A's only by
# moving whole elementary zones (so whole middle zones too), at a cost per kid moved off A; high schools in range, A's
# count at target every year, each extra HS a middle zone feeds costs ms_split, >= 70% of middle zones feed one HS.
hs = json.loads(json.dumps(out['option1_durable']))
hs['name'] = 'option1_durable_hs'
hs['label'] = 'Option 1-durable with tactical HS lines: 9-12 bends to follow our middle zones (whole elementary zones)'
hs.pop('ms_hs_feeder', None)
hs['levels']['K-5'].pop('hs_nest', None)
L = hs['levels']['9-12']
for k in ('fixed_assign', 'note'):
    L.pop(k, None)
L.update({'group_by': 'K-5', 'parent_split_by': '6-8', 'hint': 'A_hs',
          'parent_floor': {'min_share': 0.7},
          'off_reference': {'column': 'A_hs', 'kid_miles_per_kid': 2.0,
                            'note': 'moving a kid off Scenario A\'s high school must buy >= 2 kid-miles of objective'}})
hs['reuse_levels_from'] = 'option1_durable_msfeed_off'
# Paul's rule: a level that ends with new slack under the shortened limits is rerun with the original limits
hs['solver'].update(time_first=180, time_star=600, time_round=60, time_first_2a=60, time_star_2a=600)
with open(os.path.join(OUT, 'option1_durable_hs.json'), 'w') as f:
    json.dump(hs, f, indent=1)
print('wrote v2 option1_durable_hs')

# option 4 keeps a 1.5-mile K-5 candidate filter, which together with hard HS nesting leaves no contiguous plan
# (INFEASIBLE at once, 2026-10-12): option 4 uses the soft nesting cost only.
o4 = json.load(open(os.path.join(OUT, 'option4.json')))
o4['levels']['K-5']['hs_nest'] = {'column': 'A_hs', 'kid_miles_per_kid': 1.0}
with open(os.path.join(OUT, 'option4.json'), 'w') as f:
    json.dump(o4, f, indent=1)

# Tactical family (Paul 2026-10-12, "move a little on all 3 layers").  Start: K-5 and 6-8 of
# option1_durable_msfeed_off (the walkable v2 solve), 9-12 = Scenario A (A_hs).  Each level may move kids off its start
# at 0.5 kid-mile each, under a hard budget; K-5 gets the soft HS-nesting cost; 6-8 the feeder penalty/floor vs A_hs;
# 9-12 moves whole elementary zones only, each extra HS a middle zone feeds costs ms_split, and >= 70% of middle zones
# must feed one HS (very large penalty).  Objective otherwise as option1_durable.  Solved K-5 -> 6-8 -> 9-12 in sequence:
# tactical, not proven optimal.
TACT = {'tactical_s': (300, 500, 400), 'tactical_m': (600, 1000, 800), 'tactical_l': (1000, 1500, 1200)}
for n, (b5, b8, b12) in TACT.items():
    t = json.loads(json.dumps(out['option1_durable']))
    t['name'] = n
    t['label'] = f'Tactical: move a little on all three levels (K-5 <= {b5}, 6-8 <= {b8}, 9-12 <= {b12} kids moved)'
    t['kind'] = 'tactical'
    t['levels']['K-5']['hs_nest'] = {'column': 'A_hs', 'kid_miles_per_kid': 1.0}
    t['levels']['K-5']['start'] = {'run': 'option1_durable_msfeed_off', 'max_kids': b5, 'kid_miles_per_kid': 0.5}
    t['levels']['6-8']['start'] = {'run': 'option1_durable_msfeed_off', 'max_kids': b8, 'kid_miles_per_kid': 0.5}
    L = t['levels']['9-12']
    for k in ('fixed_assign', 'note'):
        L.pop(k, None)
    L.update({'group_by': 'K-5', 'parent_split_by': '6-8', 'hint': 'A_hs', 'parent_floor': {'min_share': 0.7},
              'start': {'column': 'A_hs', 'max_kids': b12, 'kid_miles_per_kid': 0.5}})
    t['weights']['ms_floor'] = 1e6
    with open(os.path.join(OUT, f'{n}.json'), 'w') as f:
        json.dump(t, f, indent=1)
    print('wrote v2', n)


# =====================================================================================================================
# Horizon + feeders (Paul 2026-10-12 ~15:15).  Config switch "horizon": "pps2031" (common.HORIZONS):
#  - REQUIRED: meet or beat Scenario A's count at target every year 2027-28 .. 2031-32 at every level (PPS Family Guide
#    p. 1, "Estimates cover 2027-28 through 2031-32"; per-school sizes from PSU Table 5.5); REPORTED to 2035-36 (last
#    Table 5.5 year); the 2036-41 district-trend extension is dropped.  The durable reward (3,000 kid-miles) counts a
#    school at target in all required years.
#  - Feeders SOFT: ms_split = 200 kid-miles per high school a middle zone feeds (so ~200 per EXTRA one); no floor.
#  - Walkable K-5: no hard nesting in A's HS lines; a tiny soft nesting cost (NEST_PPS2031 kid-miles per kid placed
#    across an A high-school line) only breaks near-ties.  Tested against no nesting (_diag_nonest_pps2031).
#  - Original (not halved) solver limits.
# The earlier configs of the reruns are kept as <name>_psu2041.json so the older v2 results stay reproducible.
# =====================================================================================================================
NEST_PPS2031 = 0.1
ORIG_LIMITS = dict(time_first=180, time_star=600, time_round=60, time_first_2a=60, time_star_2a=600, slack_rounds=0,
                   workers=4)
PPS2031_NOTE = ('count of zoned non-exempt schools at target >= Scenario A\'s count, each REQUIRED year 2027-28..2031-32 '
                '(PPS Family Guide window); 2032-33..2035-36 reported only (PSU Table 5.5); no extension past 2035-36')


def pps2031(c, nest=NEST_PPS2031):
    c = json.loads(json.dumps(c))
    c['horizon'] = 'pps2031'
    if 'solver' in c:
        c['solver'].update(ORIG_LIMITS)
        c['durability'] = dict(c.get('durability') or {}, note=PPS2031_NOTE)
        c['ms_hs_feeder'] = {'min_share': 0.0, 'min_kids': 5,
                             'ms_split_note': 'soft (Paul 2026-10-12 ~15:15): ~200 kid-miles per extra HS, no floor'}
        c['weights']['ms_split'] = 200.0
        c['levels']['K-5'].pop('hs_nest', None)
        if nest:
            c['levels']['K-5']['hs_nest'] = {'column': 'A_hs', 'kid_miles_per_kid': nest}
    return c


for n in ('option1_durable', 'option2', 'option4'):
    with open(os.path.join(OUT, f'{n}_psu2041.json'), 'w') as f:
        json.dump(dict(out[n] if n != 'option4' else o4, name=n), f, indent=1)
for n in ('today', 'status_quo', 'scenario_A', 'scenario_B'):
    with open(os.path.join(OUT, f'{n}.json'), 'w') as f:
        json.dump(pps2031(out[n]), f, indent=1)

p1 = pps2031(out['option1_durable'])
p1['label'] = ('Option 1-durable: Scenario A schools and programs; lines drawn so at least as many schools as A are at '
               'target every year 2027-28..2031-32 (reported to 2035-36)')
# Option 2 (Paul 2026-10-12 ~15:15): Atkinson->Lent and Scott->Rigler are NECESSARY moves (Lent 274 / Rigler 321,
# below 360, if their strands stay home; whole-school DLI buildings with no neighborhood area in A).  The avoidable
# moves stay put: MLK Jr Mandarin stays at MLK Jr (A: -> Boise-Eliot/Humboldt), Beaumont Spanish 6-8 stays at Beaumont
# (A: -> Roseway Heights).  Every other strand is placed as in Scenario A.
p2 = json.loads(json.dumps(p1))
p2['name'] = 'option2'
p2['label'] = ('Option 2: immersion programs stay put where avoidable (Scenario A closures and program moves, except '
               'MLK Jr Mandarin and Beaumont Spanish stay)')
pk = p2['levels']['K-5']['programs']
pk['Boise-Eliot/Humboldt'] = [k for k in pk['Boise-Eliot/Humboldt'] if k != 'MLK Jr|Mandarin']
if not pk['Boise-Eliot/Humboldt']:
    del pk['Boise-Eliot/Humboldt']
pk['MLK Jr'] = ['MLK Jr|Mandarin']
pm = p2['levels']['6-8']['programs']
pm['Roseway Heights'] = [k for k in pm['Roseway Heights'] if k != 'Beaumont|Spanish']
pm['Beaumont'] = ['Beaumont|Spanish']
# option2's first original-limits K-5 solve stalled (relaxation hint left 23 star violations; round 0 found no plan in
# 600 s), so its K-5 is warm-started from option1_durable's pps2031 K-5 (same schools and candidates; hint only)
p2['levels']['K-5']['warm_start'] = {'run': 'option1_durable', 'staging': True}
p2['program_note'] = ('necessary moves (kept): Atkinson Spanish -> Lent, Scott Spanish -> Rigler; avoided: MLK Jr '
                      'Mandarin, Beaumont Spanish 6-8 (Paul 2026-10-12 ~15:15)')
p4 = pps2031(o4)
p4['solver']['phase2_warm'] = True    # 6-8 phase 2a timed out from the relaxation hint (Jackson -79, Roseway Heights -35)
# 6-8 split search found nothing in 600 s three times (whole-zone plan left Jackson -79, Roseway Heights -35): last
# try with a small split cap (Paul: "small splits where needed") and a longer 2a limit
p4['levels']['6-8']['max_splits'] = 6
p4['solver']['time_star_2a'] = 1200
p4['levels']['K-5']['max_walk_fallback_nearest'] = 3   # edge case (Paul 2026-10-12): 1 block, 2 kids, nearest 3.83 mi
p4['levels']['K-5']['max_walk_mi'] = 2.0     # Paul 2026-10-12 ~15:15: walk cap 2.0 mi (1.5 was infeasible)
p4['label'] = 'Option 4: fewest moves (A closures/programs; minimise kids reassigned vs today; 2.0-mile K-5 walk cap)'
for n, c in (('option1_durable', p1), ('option2', p2), ('option4', p4)):
    with open(os.path.join(OUT, f'{n}.json'), 'w') as f:
        json.dump(c, f, indent=1)
# diagnostic: the same option1_durable with no nesting at all (is the tiny nesting cost immaterial?)
d = pps2031(out['option1_durable'], nest=0)
d['name'] = '_diag_nonest_pps2031'
with open(os.path.join(OUT, '_diag_nonest_pps2031.json'), 'w') as f:
    json.dump(d, f, indent=1)
print('wrote v2 pps2031: baselines, option1_durable, option2, option4 (+ *_psu2041 archives, _diag_nonest_pps2031)')

# option1_full (Paul via coordinator, 2026-10-12 evening): "PPS is closing 14 schools; redraw ALL the lines, high
# schools included".  As option1_durable (pps2031) for K-5/6-8, warm-started from its finished K-5 (not frozen); 9-12
# REDRAWN from WHOLE middle zones (group_by 6-8), so every middle zone feeds one high school by construction; split of a
# middle zone across high schools only in phase 2 (last resort, `split` = 20,000 kid-miles each).  HS: floor 1,100,
# capacity ceiling (Jefferson 1,773), >= A's 9-12 count at target each required year, HS range soft (KPI < 350), no new
# I-84/Willamette crossings (eligible_mask, as other levels).  The A_hs-relative rules (feeder penalty vs A's lines,
# K-5 nesting in A's lines) don't apply, because A's high-school lines are not kept.
f1 = json.loads(json.dumps(p1))
f1['name'] = 'option1_full'
f1['label'] = ('Option 1-full: Scenario A schools and programs; K-5, 6-8 AND 9-12 lines redrawn (high schools from whole '
               'elementary zones; 75-85% of middle zones feed one HS); at least as many schools at target as A every '
               'year 2027-28..2031-32')
f1.pop('ms_hs_feeder', None)
f1['levels']['K-5'].pop('hs_nest', None)
f1['levels']['K-5']['warm_start'] = {'run': 'option1_durable'}
L = f1['levels']['9-12']
for k in ('fixed_assign', 'note', 'parent_split_by', 'parent_floor', 'off_reference', 'start'):
    L.pop(k, None)
# REVISED (Paul via coordinator, same evening): don't force 100%.  9-12 from WHOLE ELEMENTARY zones (no elementary
# zone split at 9-12), so a middle zone may feed two high schools; >= 75% of middle zones on one HS is near-hard
# (ms_floor = 100,000 kid-miles per zone short, durability-count scale); a soft push of ms_split = 200 kid-miles per
# zone short of 85%, and nothing beyond 85% (A: 80%).
L['group_by'] = 'K-5'
L['parent_split_by'] = '6-8'
L['parent_floor'] = {'min_share': 0.75, 'soft_to': 0.85}
L['hint'] = 'A_hs'
L['note'] = ('redrawn from whole elementary zones (option1_full); 75% one-HS near-hard, soft push to 85%; '
             'A_hs is only the solver hint')
# (Paul ~16:55, "yes allow small splits where needed"): split elementary zones at 9-12 only where needed for size or
# durability, at most 5 (else stop and surface); phase 2 warm-starts from the whole-zone plan (engine fix)
L['max_splits'] = 5
f1['solver']['phase2_warm'] = True
f1['weights']['ms_split'] = 200.0
f1['weights']['ms_floor'] = 100000.0
with open(os.path.join(OUT, 'option1_full.json'), 'w') as f:
    json.dump(f1, f, indent=1)
print('wrote v2 option1_full')

# frontier_k17 under the CURRENT rules (Paul ~16:50): pps2031 horizon, meet A's count every required year, NO durability
# reward (walk-max end), walkable K-5 with 0.1 kid-mile soft nesting, soft feeders 200 per extra HS, A's 9-12 fixed,
# original limits, phase-2 warm start (engine fix).  Old config kept as frontier_k17_psu2041.json.
import shutil as _sh
_sh.copyfile(os.path.join(OUT, 'frontier_k17.json'), os.path.join(OUT, 'frontier_k17_psu2041.json'))   # old rules, as run
fk = json.loads(json.dumps(p1))
fk['name'] = 'frontier_k17'
fk['kind'] = 'frontier'
fk['label'] = ('Frontier k17 (current rules): Scenario A schools/programs/9-12 lines; meet A\'s count every required year '
               '2027-28..2031-32; no durability reward (most walkable)')
fk['weights']['durable_school'] = 0.0
fk['weights']['school_year_at_target'] = 0.0
fk['durability']['min_durable'] = {}
fk['solver']['phase2_warm'] = True
# first current-rules K-5 solve from the relaxation hint (29 violations) ended with ~630 kids of 2031-32 slack, gap
# 99.8%: warm-start K-5 from option1_durable (hint only), as for option2
fk['levels']['K-5']['warm_start'] = {'run': 'option1_durable'}
fk['solver']['workers'] = 3          # third parallel slot (Paul: "lets expand to 3 slots")
with open(os.path.join(OUT, 'frontier_k17.json'), 'w') as f:
    json.dump(fk, f, indent=1)
print('wrote v2 frontier_k17 (pps2031)')

# option1_nested was folded into option1_full (Paul ~17:05): see the feeder-order block below.  (configs/v2/
# option1_nested.json is a leftover from the brief standalone version; not run.)

# option1_full, FEEDER ORDER (Paul ~17:05, "stick with our plan"): K-5 (warm-started from option1_durable, as solved)
# -> 9-12 from whole elementary zones of that K-5, <= 5 penalized splits only where size/durability needs them, NO
# middle-zone feeder term -> 6-8 from whole elementary zones, HARD-nested in the new 9-12 lines (each elementary zone
# takes its majority high school), <= 5 penalized ES->MS splits only where needed.
f1['level_order'] = ['K-5', '9-12', '6-8']
L = f1['levels']['9-12']
for k in ('parent_split_by', 'parent_floor'):
    L.pop(k, None)
L['note'] = ('redrawn from whole elementary zones (option1_full, feeder order K-5 -> 9-12 -> 6-8); <= 5 splits; '
             'A_hs is only the solver hint')
# HARD nesting proved infeasible on sizes (2026-10-12 ~17:50): inside the new lines the Ida B. Wells area has 734
# middle-school kids for Gray + Jackson (floors 1,000) and the Grant area 445 for Beaumont (500); whole-zone plan left
# Gray -165, Jackson -102, Beaumont -56, Tubman -46 (proven optimal), and splits cannot cross a hard line.  So nesting is
# SOFT: 5 kid-miles per middle schooler placed across a new high-school line; the solver crosses only where size needs.
f1['levels']['6-8']['hs_nest'] = {'self': True, 'kid_miles_per_kid': 5.0}
# That soft-nested plan (kept as scratch out_v2/_option1_full_softnest_attempt) still left Gray -25, Roseway Heights -37,
# George +5 and only 47% of middle zones on one HS.  Paul's step (a): feed the 6-8 size need back into 9-12 (each HS
# area must hold the middle-school floors of the buildings in it, <= their capacity; 5,000 kid-miles per kid short),
# then 6-8 nested more strongly (20 kid-miles per middle schooler across a line).
f1['levels']['9-12']['ms_need_feedback'] = True
f1['weights']['ms_need'] = 5000.0
f1['levels']['6-8']['hs_nest'] = {'self': True, 'kid_miles_per_kid': 20.0}
f1['levels']['6-8']['max_splits'] = 5
f1['label'] = ('Option 1-full: Scenario A schools and programs; all lines redrawn in feeder order K-5 -> 9-12 (whole '
               'elementary zones) -> 6-8 (nested in the new high-school lines); at least as many schools at target as '
               'A every year 2027-28..2031-32')
with open(os.path.join(OUT, 'option1_full.json'), 'w') as f:
    json.dump(f1, f, indent=1)
print('wrote v2 option1_full (feeder order)')

# Split re-solves (Paul ~16:55, "if you can fix elem zones, sure"): option1_durable and option2 6-8 re-solved
# (`solve.py configs/v2/<n>_p2fix.json --from 6-8`, K-5 reused from the done run) with the phase-2 warm start.  They
# write to <n>.staging (same run name); swapped in only if A's count holds every required year, every school is in
# range in 2031-32 and there are FEWER ES->MS splits.  Otherwise the current runs stay.
for n, c in (('option1_durable', p1), ('option2', p2)):
    q = json.loads(json.dumps(c))
    q['solver']['phase2_warm'] = True
    q['solver']['workers'] = 3
    q['levels']['K-5'].pop('warm_start', None)
    with open(os.path.join(OUT, f'{n}_p2fix.json'), 'w') as f:
        json.dump(q, f, indent=1)
print('wrote v2 option1_durable_p2fix, option2_p2fix')

# phase-2a hint: CP-SAT repair_hint on (2026-10-12): the block-level repair of the whole-zone plan can leave a few
# star violations (option4: 3), and a hint with any violation gave no 2a solution in 600 s
for _n in os.listdir(OUT):
    if _n.endswith('.json'):
        _p = os.path.join(OUT, _n)
        _c = json.load(open(_p))
        if (_c.get('solver') or {}).get('phase2_warm') and not _c['solver'].get('phase2_hint_mode'):
            _c['solver']['phase2_hint_mode'] = 'repair'
            json.dump(_c, open(_p, 'w'), indent=1)
print('phase2_hint_mode=repair set on phase2_warm configs')
