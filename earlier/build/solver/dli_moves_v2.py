"""DLI (immersion) strand moves for a run, read from THAT run's own program placement.

  python dli_moves_v2.py <run> [<run> ...] [--write]      (a run name, or name.staging)

Baseline = configs/v2/status_quo.json (its program hosts equal today's). For each run, configs/v2/<run>.json
levels.<lev>.programs is compared strand by strand; a strand counts as moved only if its host building differs from
the Status Quo host. Sizes: PSU July 2026 Table 5.5 strand rows (v2.program_series), 2025-26 and 2031-32. Arrival share
= the share implied by PPS's Family Guide projections (v2.follow_rate; 1.0 where PPS implies none). Prints a markdown
table; --write saves <run folder>/dli_moves.json (the previous file is kept as dli_moves.json.bak_buggy).

Fixed 2026-10-26: the old version (dli_moves_v2.py.bak_dli) ignored its argument's run and always wrote Scenario A vs
option2 moves into whatever folder it was given, so e.g. out_v2/dli_home3_rh/dli_moves.json listed strands that run
keeps at home (Clark, Sitton, Atkinson, Scott ...) as moved."""
import json, os, sys
import common as C, v2 as V2

OUT = os.path.join(C.SOLVER, 'out_v2')


def hosts(cfg, lev):
    return {k: h for h, keys in (cfg['levels'][lev].get('programs') or {}).items() for k in keys}


def served(cfg, lev):
    L = cfg['levels'][lev]
    return set(L['zoned']) | {h for h, keys in (L.get('programs') or {}).items() if keys}


def moves(run):
    name = run.replace('.staging', '')
    cfg = C.load_config(os.path.join(C.SOLVER, 'configs', 'v2', f'{name}.json'))
    sq = C.load_config(os.path.join(C.SOLVER, 'configs', 'v2', 'status_quo.json'))
    open_any = set().union(*(served(cfg, l) for l in C.LEVELS))
    out = []
    for lev in ('K-5', '6-8'):
        h0, h1 = hosts(sq, lev), hosts(cfg, lev)
        for k, src in h0.items():
            dst = h1.get(k)
            if dst == src:
                continue
            s = V2.program_series(k)
            f = V2.follow_rate(k, 2031) if dst else 0.0
            if dst is None:
                why = 'strand dropped'
            elif src not in open_any:
                why = 'building closes'
            elif src not in served(cfg, lev):
                why = 'building drops these grades'
            else:
                why = 'program moves (building stays open at this level)'
            out.append({'strand': k, 'level': lev, 'from': src, 'to': dst, 'why': why,
                        'n_2025_26': round(s[2025]), 'n_2031_32': round(s[2031]),
                        'arrival_share_2031_implied': round(f, 4), 'arrive_2031': round(f * s[2031]),
                        'non_followers_2031': round((1 - f) * s[2031])})
    return out


def summary(ms):
    t = {k: sum(m[k] for m in ms) for k in ('n_2025_26', 'n_2031_32', 'arrive_2031', 'non_followers_2031')}
    t['strands'] = len(ms)
    t['by_level'] = {lev: {k: sum(m[k] for m in ms if m['level'] == lev) for k in ('n_2025_26', 'n_2031_32')}
                     for lev in ('K-5', '6-8')}
    return t


def folder(run):
    for d in (run, run.replace('.staging', ''), run.replace('.staging', '') + '.staging'):
        if os.path.exists(os.path.join(OUT, d, 'scorecard.json')):
            return os.path.join(OUT, d)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    for r in args:
        ms = moves(r)
        res = {'run': r.replace('.staging', ''), 'baseline': 'status_quo', 'moves': ms, 'summary': summary(ms),
               'source': 'configs/v2/<run>.json levels.<lev>.programs vs configs/v2/status_quo.json; sizes PSU Table 5.5 '
                         'strand rows (v2.program_series); arrival share v2.follow_rate (implied by PPS Family Guides)'}
        print(f'\n### {r}\n\n| Strand | Level | From -> to | Why | 2025-26 | 2031-32 | Arrival share | Arrive 2031-32 |')
        print('|---|---|---|---|---|---|---|---|')
        for m in ms:
            print(f"| {m['strand']} | {m['level']} | {m['from']} -> {m['to']} | {m['why']} | {m['n_2025_26']} | "
                  f"{m['n_2031_32']} | {m['arrival_share_2031_implied']:.2f} | {m['arrive_2031']} |")
        print(json.dumps(res['summary']))
        if '--write' in sys.argv:
            d = folder(r)
            p = os.path.join(d, 'dli_moves.json')
            if os.path.exists(p) and not os.path.exists(p + '.bak_buggy'):
                os.rename(p, p + '.bak_buggy')
            json.dump(res, open(p, 'w'), indent=1)
