"""Public run manifest (2026-10-14, site go-live review): out_v2/MANIFEST_public.json lists only the plans the site
shows, with status and finish time, and the model changes in plain public wording.  No internal notes, test runs or
dated attributions.  The working MANIFEST.json is unchanged.   python public_manifest.py"""
import json, os, re
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out_v2')
import json as _json, os as _os
_PREV = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'export', 'preview_plans.json')
# local-only preview plans (build/export/preview_plans.json never ships) are added after their 'after' plan
# (2026-10-27) dli_home3_rh = the site's current best (approved); equity_noswap_alameda_rig_hs = previous best;
# option2_ms460 = the best before that
RELEASED = ['status_quo', 'scenario_A', 'scenario_B', 'option2', 'dli_home3_rh', 'equity_noswap_alameda_rig_hs', 'option2_ms460', 'option2_ms460_sellwood_home', 'option1_durable', 'option4', 'option3a']
if _os.path.exists(_PREV):
    for _p in _json.load(open(_PREV)).get('plans', []):
        if _p['name'] not in RELEASED:
            RELEASED.insert(RELEASED.index(_p['after']) + 1 if _p.get('after') in RELEASED else len(RELEASED), _p['name'])
# requested runs on the Requests page (build/export/requests.json, site-owned; read only) are listed after the plans
_REQ = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'export', 'requests.json')
if _os.path.exists(_REQ):
    RELEASED += [_r['name'] for _r in _json.load(open(_REQ)).get('requests', []) if _r['name'] not in RELEASED]
# runs the Sabin options page shows (pages/sabin.html, site track): every run in out_v2/SABIN_OPTIONS.json, listed in
# __main__ only once MANIFEST.json marks it done; not added to the site's main plan lists
_SAB = _os.path.join(OUT, 'SABIN_OPTIONS.json')
SABIN = []
if _os.path.exists(_SAB):
    for _p in _json.load(open(_SAB)).get('plans', []):
        if _p['run'] not in RELEASED and _p['run'] not in SABIN:
            SABIN.append(_p['run'])


def clean(s):
    s = re.sub(r'\s*\(Paul[^)]*\)', '', s)
    s = re.sub(r'Paul[ ,]*20\d\d-\d\d-\d\d[^;:)]*[;:]?\s*', '', s)
    s = s.replace('Scenario A', 'PPS A').replace('IMPLIED', 'implied').replace('REQUIRES', 'requires').replace('REPORTED', 'reported')
    s = re.sub(r'\s*Applies to the baselines.*?\.\s*(?=New scorecard keys|$)', ' ', s)
    s = re.sub(r'\s*New scorecard keys:.*$', '', s)
    s = re.sub(r';\s*configs key "horizon"', '', s)
    s = s.replace(' to 2035-36, extended to 2040-41 with the PSU medium district trend', ' to 2035-36')
    s = s.replace('SOFT:', 'are a soft cost:')
    return re.sub(r'\s{2,}', ' ', s).strip()


if __name__ == '__main__':
    m = json.load(open(os.path.join(OUT, 'MANIFEST.json')))
    pub = {'model_version': m.get('model_version'), 'calibrated': m.get('calibrated'),
           'calibration_report': 'build/solver/out_v2/CALIBRATION_public.md',
           'changes_vs_v1': [clean(c) for c in m.get('changes_vs_v1', []) if not c.startswith('scorecard.json')],
           'runs': {r: {'status': m['runs'][r]['status'], 'finished': m['runs'][r].get('finished')}
                    for r in RELEASED if r in m['runs']}}
    pub['runs'].update({r: {'status': 'done', 'finished': m['runs'][r].get('finished')}
                        for r in SABIN if (m['runs'].get(r) or {}).get('status') == 'done'})
    json.dump(pub, open(os.path.join(OUT, 'MANIFEST_public.json'), 'w'), indent=1)
    print(json.dumps(pub, indent=1)[:3000])
