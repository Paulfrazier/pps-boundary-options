"""Public trade-off write-ups (2026-10-13, site review 6).  python public_tradeoffs.py

For each live plan, writes out_v2/<plan>/TRADEOFFS_public.md from its working TRADEOFFS.md: a short plain intro
(below), then the generated tables with internal notes taken out:
  - the reference column/rows for the old walkable baseline (or another of our runs) dropped: PPS A vs this plan only
  - "Scenario A" -> "PPS A"; floats like 1083.0 -> 1,083
  - solver-slack dump, script names, dated attributions and superseded-run notes left out
  - a section repeated in the working file (appended re-runs) is kept once: the last copy, the current numbers
The working TRADEOFFS.md files are unchanged."""
import json, os, re

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out_v2')

INTRO = {
    'option2': ("Boundary changes, same closures",
                "PPS A's closures, programs and high-school lines. Elementary and middle-school lines are redrawn for the "
                "shortest walks that keep every school in range and at least PPS A's at-target count every year "
                "2027-28 to 2031-32. Two of PPS A's immersion moves are avoided: MLK Jr Mandarin stays at MLK Jr (PPS A "
                "moves it to Boise-Eliot/Humboldt) and Beaumont Spanish 6-8 stays at Beaumont (PPS A moves it to Roseway "
                "Heights). Two are kept because they're needed: without them Lent would have 274 kids and Rigler 321, "
                "both below 360. This spares 341 immersion students a program move in 2031-32 (about 326 counting only "
                "families PPS's own projections imply would have followed; inferred from the PPS Family Guide, not stated "
                "by PPS). 1,226 program students still move (PPS A 1,567)."),
    'option2_ms460': ("Boundary changes, balanced middle schools",
                      "The same closures, immersion programs, high-school lines and elementary lines as Boundary changes, "
                      "same closures. The only difference is middle school: the minimum middle-school size is lowered "
                      "from 500 (PPS's goal) to 460 so fewer elementary schools are split between middle schools (3 "
                      "instead of 13) and no middle school is over capacity. At PPS's 500 minimum, 9 of 13 middle "
                      "schools are at target every year; at 460, all 13."),
    'option1_durable': ("Redrawn K-8 lines",
                        "PPS A's closures, programs (every immersion move kept) and high-school lines. Elementary and "
                        "middle-school lines are redrawn for the shortest walks that keep every school in range and at "
                        "least PPS A's at-target count every year 2027-28 to 2031-32."),
    'option4': ("Rebalanced PPS A",
                "PPS A's closures and programs. Lines change as little as possible from PPS Status Quo while every school "
                "is brought into range, with a 2-mile K-5 walk cap. Three schools still miss in 2031-32: Forest Park "
                "(also short under PPS A; geography under the 2-mile cap), Jackson and Roseway Heights. One small block "
                "on the Columbia River edge has no school within 2 miles' walk and keeps its nearest option."),
    'option3a': ("Close 2 focus options (Winterhaven, da Vinci) — a what-if",
                 "PPS A's closures, programs and high-school lines, plus Winterhaven (K-8 STEM) and da Vinci (6-8 arts) "
                 "close. Their students return to their neighborhood schools by the catchment they live in, from a "
                 "per-catchment sheet of 2025-26 focus students (second-hand: its first columns match PPS's October 2025 "
                 "Enrollment Summary, but the per-program columns' source isn't stated). 21 students who live outside PPS "
                 "aren't returned. It assumes every returning student attends their neighborhood school. Elementary and "
                 "middle lines are redrawn under the same rules as the redraws."),
}

CLEANUP = ("**Line cleanup.** After the solve, the elementary lines were cleaned: re-solved with a higher cost on boundary "
           "length and on passing a closer school, then one-block notches moved to the school around them and small "
           "detached pieces swapped back, only where no school gets further outside its range in any year. Every rule "
           "still holds. Before/after line counts: `out_v2/LINES_QA.md`.")

NOCLEAN = ("**Lines.** The elementary lines come from a longer re-solve that keeps Sunnyside's and Abernethy's areas "
           "entirely south of I-84. They were not put through the line cleanup: a cleanup re-solve made them worse (one "
           "more school short of its minimum, more kids sent past a closer school), so they have more one-block notches "
           "than the earlier lines (147 vs 100). Line counts: `out_v2/LINES_QA.md`.")
MS460 = ("**Middle-school minimum.** This plan uses 460, not 500, as the middle-school minimum, so its middle-school "
         "\"at target\" counts below use 460. Four middle schools dip below 500 in their low year: Harrison Park 461 "
         "(2030-31), Ockley Green 461 (2028-29), West Sylvan 460 (2031-32) and George 498 (2031-32). At 500, 9 of 13 are at "
         "target every year 2027-28 to 2031-32. West Sylvan falls to 443 in 2032-33, a year PPS doesn't project.")

BASIS = ("**Basis.** Our model (v2) on PSU's per-school forecast (PSU July 2026, Table 5.5) [inferred: our model on PPS/PSU "
         "numbers, not PPS figures]. \"At target\" = a school between its minimum (360 K-5; 500 K-8 and 6-8; 1,100 9-12) "
         "and its building capacity (PPS 2025-26 school profiles). Required years are 2027-28 to 2031-32, PPS's projection "
         "window (PPS Family Guide p. 1: \"Estimates cover 2027-28 through 2031-32\"); 2032-33 to 2035-36 are reported only "
         "(last year of PSU Table 5.5). Comparisons are with PPS Scenario A (\"PPS A\").")


def _float(m):
    v = float(m.group(0))
    return f'{v:,.0f}' if v >= 100 else m.group(0)


NAMES = {'Redrawn walkable K-8 lines, PPS high schools': 'Redrawn K-8 lines', 'Redrawn K-8, PPS HS': 'Redrawn K-8 lines',
         'Fewest kids moved': 'Rebalanced PPS A: every school in range',
         'Fewest moves, every school in range': 'Rebalanced PPS A: every school in range',   # renamed 2026-10-14 (Paul)
         'Redrawn K-8, MLK Jr + Beaumont DLI stay': 'Boundary changes, same closures',   # renamed 2026-10-14 (Paul)
         'Redrawn K-8, 2 DLI stay': 'Boundary changes, same closures',
         'Same closures, better lines': 'Boundary changes, same closures'}   # renamed 2026-10-14 evening (Paul)


def clean_line(s):
    s = s.replace('PPS Scenario A', 'PPS A').replace('Scenario A', 'PPS A')
    for a, b in NAMES.items():
        s = s.replace(a, b)
    s = s.replace('| Past a closer school |', '| Assigned to a farther school, past a closer one |')
    s = s.replace('. Past a closer school =', '. Assigned to a farther school, past a closer one =')   # site wording, 2026-10-14 (Paul)
    s = re.sub(r'\b\d{3,}\.0\b', _float, s)
    return s


def tables(text):
    """the generated '## ' sections (last copy of each), cleaned"""
    secs, cur = {}, None
    order = []
    for ln in text.splitlines():
        if ln.startswith('## '):
            cur = ln
            if cur not in order:
                order.append(cur)
            secs[cur] = []          # a repeated heading restarts the section: the last copy wins
            continue
        if cur:
            secs[cur].append(ln)
    out = []
    for h in order:
        body = secs[h]
        res, drop_col = [], None
        for ln in body:
            if ln.startswith('Solver slack left') or 'infeasibility.json' in ln:
                continue
            if ln.startswith('**Line cleanup') or ln.startswith('**Headline') or ln.startswith('Line quality is from'):
                break               # appended re-run notes after the tables: covered by the intro
            if ln.startswith('`*` = required year'):
                ln = '`*` = required year.'
            if ln.startswith('|'):
                cells = ln.strip().strip('|').split('|')
                hdr = [c.strip() for c in cells]
                ref = [k for k, c in enumerate(hdr) if 'msfeed_off' in c or c == 'Walkable baseline'
                       or c.startswith('Redrawn walkable K-8 lines, PPS high schools') and 'option4' in CURRENT]
                if ref and ln.startswith('| Level | Measure'):
                    drop_col = ref[0]
                if CURRENT == 'option4' and len(hdr) > 1 and hdr[1].startswith('Redrawn walkable K-8 lines') \
                        or CURRENT == 'option4' and hdr and hdr[0].startswith('Redrawn walkable K-8 lines'):
                    continue        # option4's reference rows (an older copy of option1_durable)
                if any('msfeed_off' in c for c in hdr) and not ln.startswith('| Level | Measure'):
                    continue        # a baseline row in a per-plan table
                if drop_col is not None and len(cells) > drop_col:
                    cells = cells[:drop_col] + cells[drop_col + 1:]
                    ln = '|' + '|'.join(cells) + '|'
            elif 'msfeed_off' in ln or CURRENT == 'option4' and ln.startswith('- Redrawn walkable K-8 lines'):
                continue
            res.append(clean_line(ln))
        while res and not res[-1].strip():
            res.pop()
        out.append(clean_line(h))
        out += res
        out.append('')
    return '\n'.join(out)


def pps_official_rows(txt):
    """Paul 2026-10-14 ("use the official PPS data to represent their models"): in the at-target table, PPS A gets a row
    from PPS's own Family Guide figures (out_v2/PPS_OFFICIAL_DURABILITY.json, written by durability_vs_pps.py) above
    our model's row.  PPS publishes no figures past 2031-32."""
    f = os.path.join(OUT, 'PPS_OFFICIAL_DURABILITY.json')
    if not os.path.exists(f):
        return txt
    L = json.load(open(f))['plans']['scenario_A']['durability']['levels']
    out, sec = [], None
    for ln in txt.split('\n'):
        if ln.startswith('## '):
            sec = ln
        cells = [c.strip() for c in ln.strip().strip('|').split('|')] if ln.startswith('|') else []
        if sec == '## Schools at target, year by year' and len(cells) == 13 and cells[1] == 'PPS A':
            lev = cells[0].split(' (')[0]
            o = L[lev]
            fig = [str(v) for v in o['at_target_zoned'].values()] + ['—'] * 4 + [str(o['at_target_all_required_years']), '—']
            out.append(f'| {cells[0]} | PPS A, PPS figures | ' + ' | '.join(fig) + ' |')
            out.append('|  | PPS A, our model | ' + ' | '.join(cells[2:]) + ' |')
            continue
        if sec == '## Schools at target, year by year' and ln.startswith('`*` = required year'):
            ln = ('`*` = required year. "PPS figures" = PPS\'s own enrollment estimates (Family Guide p. 4, guides dated '
                  '2026-10-08), counted with the same targets; PPS publishes none past 2031-32. "Our model" = PPS A\'s '
                  'lines scored the same way as this plan. High-school lines are PPS A\'s in every plan, so a 9-12 '
                  'difference between the two PPS A rows comes from the estimates, not the lines.')
        if sec == '## Schools at target, year by year' and 'meets or beats PPS A in every required year' in ln:
            ln = ln.replace('meets or beats PPS A in every', 'meets or beats PPS A (our model) in every')
        out.append(ln)
    return '\n'.join(out)


CURRENT = ''
if __name__ == '__main__':
    for plan, (title, intro) in INTRO.items():
        CURRENT = plan
        src = open(os.path.join(OUT, plan, 'TRADEOFFS.md')).read()
        body = tables(src)
        parts = [f'# {title}: trade-offs', '', BASIS, '', f'**What this plan is.** {intro}', '']
        if plan in ('option2', 'option2_ms460'):
            parts += [NOCLEAN, '']
        elif plan != 'option4':
            parts += [CLEANUP, '']
        if plan == 'option2_ms460':
            parts += [MS460, '']
        parts += [body.strip(), '', 'Plain-language summary of every plan: `out_v2/BRIEFS.md`.', '']
        txt = '\n'.join(parts)
        txt = re.sub(r'\n{3,}', '\n\n', txt)
        txt = pps_official_rows(txt)
        open(os.path.join(OUT, plan, 'TRADEOFFS_public.md'), 'w').write(txt)
        print(plan, len(txt.splitlines()), 'lines')
