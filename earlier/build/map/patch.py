#!/usr/bin/env python
"""Build pages/pps-walk-redraw-v2.html from the original page.
Prereqs (cached in work/): diffs.py -> work/compare.json ; streets.py -> work/street_labels.txt ; fonts/*.woff2
Usage: ../../.venv/bin/python patch.py   (runs diffs.py/streets.py first if their outputs are missing)"""
import base64, json, os, re, subprocess, sys
from common import *

for out, script in (('official_poly.json', 'official.py'), ('official.json', 'official_stats.py'), ('compare.json', 'diffs.py'), ('street_labels.txt', 'streets.py')):
    if not os.path.exists(os.path.join(WORK, out)):
        subprocess.check_call([sys.executable, os.path.join(HERE, script)], cwd=HERE)

t = load_page()
def rep(old, new, count=1):
    global t
    assert t.count(old) == count, (t.count(old), old[:80])
    t = t.replace(old, new)


# 0. official PPS Scenario A/B (traced maps) replace the page's old reconstruction: polygons, sizes, stats, tables
OFF = json.load(open(os.path.join(WORK, 'official_poly.json'))); OS = json.load(open(os.path.join(WORK, 'official.json')))
def set_const(name, nxt, value, raw=False):
    global t
    pre = 'const %s=' % name
    i = t.index(pre) + len(pre); j = t.index(nxt, i)
    t = t[:i] + (value if raw else json.dumps(value, separators=(',', ':'), ensure_ascii=False)) + t[j:]
RDd = json.loads(grab(t, 'const RD=', ';\nconst SCH='))
for s in 'AB':
    RDd[s]['pps'] = OS['sizes_' + s]; RDd[s]['pfrom'] = OS['pfrom'][s]
RDd['DA']['pps'] = OS['sizes_A']
set_const('RD', ';\nconst SCH=', RDd)
set_const('PPSP', ';\nconst STREETS', {'A': OFF['A'], 'B': OFF['B']})
DIVd = json.loads(grab(t, 'const DIV=', ';\nconst shareKey'))
for s in 'AB':
    k = 'P' + s; m = OS['metrics'][s + 'new']
    DIVd['share'][k] = OS['share_' + s]
    DIVd['summ'][k] = dict(D=m['D'], within=m['within'], n=m['nsh'], min=round(m['min'] * 100), max=round(m['max'] * 100), avg=m['avg'],
                           o1=m['o1'], o15=m['o15'], past=m['past'], full=m['full'], nn=m['n'], moved=m['moved'])
set_const('DIV', ';\nconst shareKey', DIVd)
CMPd = json.loads(grab(t, 'const CMP=', ';\nconst DET='))
def R_(m): return ['%.3f' % m['avg'], f"{m['o1']:,}", f"{m['o15']:,}", f"{m['past']:,}", f"{m['full']} of {m['n']}", f"{m['moved']:,}"]
for r in CMPd:
    if r[0] == 'A · PPS plan': r[0] = 'A · PPS Scenario A (official map)'; r[1:] = R_(OS['metrics']['Anew'])
    if r[0] == 'B · PPS plan': r[0] = 'B · PPS Scenario B (official map)'; r[1:] = R_(OS['metrics']['Bnew'])
set_const('CMP', ';\nconst DET=', CMPd)
set_const('DET', ';\nconst PPSP=', OS['det'])
WBd = json.loads(grab(t, 'const WB=', ';\nconst OUTL='))
for key in 'SH':
    bnd = OS['bands']['A'][key]
    for row in WBd[key]:
        x = bnd.get(row[0]) if row[0] != '__ALL' else bnd['__ALL']
        row[6:11] = x if x else [None] * 5
set_const('WB', ';\nconst OUTL=', WBd)
rep("the PPS plan buttons show PPS's proposed boundaries", "the PPS Scenario buttons show PPS's own proposed boundaries (traced from its published maps)")
rep('data-s="PA" aria-pressed="false">PPS plan · A</button><button data-s="PB" aria-pressed="false">PPS plan · B</button>', 'data-s="PA" aria-pressed="false">PPS Scenario A (official map)</button><button data-s="PB" aria-pressed="false">PPS Scenario B (official map)</button>')
rep('data-k="2">PPS plan A</th>', 'data-k="2">PPS Scenario A</th>')
rep("<h2>Walking from each closing school's area under PPS plan A</h2>", "<h2>Walking from each closing school's area under PPS Scenario A (official map)</h2>")
rep('<th>Assigned in PPS plan (A)</th>', '<th>Assigned in PPS Scenario A</th>')
rep('["A · PPS plan","PA"]', '["A · PPS Scenario A (official map)","PA"]'); rep('["B · PPS plan","PB"]', '["B · PPS Scenario B (official map)","PB"]')
# side panel for PPS scenario areas: students by today's area (the old text described the halfway-split approximation)
i = t.index('<div class="from"><div class="tag">Area under PPS\'s plan</div>'); j = t.index('</p></div>', i) + len('</p></div>')
t = t[:i] + '${pbars(s,n)}' + t[j:]
i = t.index('<p class="hint">Where PPS splits'); j = t.index('</p>', i) + 4
t = t[:i] + '<p class="hint">Lines are traced from PPS\'s published 2027-28 scenario map and may be off by about 70 feet. Thin dark lines are today\'s boundaries.</p>' + t[j:]
rep('Students, PPS plan</span><span>${RD[s].pps[n]??"—"}</span>', 'Students, PPS map</span><span>${RD[s].pps[n]??"—"}</span>')
note = ("<p><b>PPS Scenario lines.</b> The PPS Scenario A and B boundaries are traced from the 2027-28 K-5 scenario maps PPS published (BoardBook, October 2026), "
        "and may be off by about 70 feet (median trace error). Each Census block follows the traced map, and K-8 areas such as Astor and Skyline, which PPS draws dashed, follow nearest-block rules. "
        "Sizes, stats and comparison counts treat the whole-school immersion areas of Lent and Rigler as staying with their program (as PPS's own projections do), while the map still shows the official lines, which draw those areas as part of Kelly and Scott. Cesar Chavez has no neighborhood area under PPS A or B, so its neighborhood students go to Rosa Parks and it appears as a program-only school."
        "</p>\n  ")
rep('<p>Map data © OpenStreetMap contributors', note + '<p>Map data © OpenStreetMap contributors')

# 1. fonts: embedded variable woff2 (latin subset), no network
def b64(f): return base64.b64encode(open(os.path.join(HERE, 'fonts', f), 'rb').read()).decode()
fonts = f"""<style>
/* Overpass + Overpass Mono, latin subset, variable woff2 embedded (Google Fonts, OFL). No network needed; font-display:swap + system fallbacks. */
@font-face{{font-family:"Overpass";font-style:normal;font-weight:400 800;font-display:swap;src:url(data:font/woff2;base64,{b64('ov.woff2')}) format("woff2")}}
@font-face{{font-family:"Overpass";font-style:italic;font-weight:400 800;font-display:swap;src:url(data:font/woff2;base64,{b64('ovi.woff2')}) format("woff2")}}
@font-face{{font-family:"Overpass Mono";font-style:normal;font-weight:400 700;font-display:swap;src:url(data:font/woff2;base64,{b64('ovm.woff2')}) format("woff2")}}
html{{-webkit-text-size-adjust:100%;text-size-adjust:100%}}
</style>"""
i = t.index('<link rel="stylesheet" href="https://fonts.googleapis.com'); j = t.index('>', i) + 1
t = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n<title>PPS Walk-Based Redraw</title>\n' + fonts + t[j:]
rep('--sans:"Overpass",system-ui,-apple-system,"Segoe UI",sans-serif; --mono:"Overpass Mono",ui-monospace,Menlo,monospace;',
    '--sans:"Overpass",system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Roboto,Arial,sans-serif; --mono:"Overpass Mono",ui-monospace,"SF Mono",SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;')

# 2. CSS
css = open(os.path.join(HERE, 'v2_head.css')).read() + '\n.legend [hidden]{display:none}\n.legend .dvl:not(.on){display:none}\n'
rep('</style>\n<div class="wrap">', css + '</style>\n<body>\n<div class="wrap">')

# 3. controls
rep('<div class="seg" role="group" aria-label="Map view">',
    '<div class="seg" role="group" aria-label="Compare mode"><button data-m="single" aria-pressed="true">Single plan</button><button data-m="swipe" aria-pressed="false">Swipe compare</button><button data-m="overlay" aria-pressed="false">Overlay compare</button></div>\n  <div class="seg" id="segS" role="group" aria-label="Map view">')
rep('''  <label class="chk"><input type="checkbox" id="lst" checked> Neighborhood streets <span style="opacity:.7">(zoom in)</span></label>''',
'''  <label class="chk"><input type="checkbox" id="lst" checked> Collector streets <button type="button" class="zh" data-z="1.6" hidden>zoom in</button></label>
  <label class="chk"><input type="checkbox" id="lloc" checked> Local streets <button type="button" class="zh" data-z="3" hidden>zoom in</button></label>
  <label class="chk"><input type="checkbox" id="lnm" checked> Street names <button type="button" class="zh" data-z="4" hidden>zoom in</button></label>''')
rep(' </div>\n <div class="grid">', ''' </div>
 <div class="cmpbar" id="cmpbar" hidden role="group" aria-label="Choose two plans to compare">
  <label class="sel">Plan 1 (left / fill)<select id="sel1"></select></label>
  <button type="button" class="swap" id="swapb" aria-label="Swap plan 1 and plan 2" title="Swap">⇄</button>
  <label class="sel">Plan 2 (right / outline)<select id="sel2"></select></label>
  <label class="chk"><input type="checkbox" id="ldf" checked> Outline changed schools</label>
  <label class="chk"><input type="checkbox" id="lhf"> Hatch changed areas</label>
  <p class="cnote" id="cnote" aria-live="polite"></p>
 </div>
 <div class="grid">''')
rep('<div class="zoom"><button id="zin"', '''<div class="tip" id="tip" hidden></div><div class="cchip l" id="chipL" hidden></div><div class="cchip r" id="chipR" hidden></div>
    <div class="swipe" id="swipe" hidden><button type="button" role="slider" aria-orientation="horizontal" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50">◂▸</button></div>
    <div class="zoom"><button id="zin"''')
rep('stroke-width="0.6"/></svg>Neighborhood street</span>', 'stroke-width="0.6" stroke-opacity=".6"/></svg>Local street</span>')
rep('<span class="dvl" id="dvl">', '''<span class="lg2" id="lg2" hidden><span id="lgO" hidden><svg width="26" height="10"><line x1="1" y1="5" x2="25" y2="5" stroke="var(--cmp-case)" stroke-width="5"/><line x1="1" y1="5" x2="25" y2="5" stroke="var(--cmp)" stroke-width="2.4"/></svg>Plan 2 boundary</span><span id="lgS" hidden>◂ plan 1 | plan 2 ▸</span><span><i class="chgsw"></i>Changed school (plan 1 → plan 2)</span></span>
<span class="dvl" id="dvl">''')

# 4. data + js
cmpd = open(os.path.join(WORK, 'compare.json')).read()
slbl = open(os.path.join(WORK, 'street_labels.txt')).read()
from model_port import SC as _SC
import pandas as _pd
_sc = _pd.read_csv(os.path.join(KIT, 'build', 'data', 'schools.csv')).set_index('name')
PROG = {s: {n: (int(_sc.loc[n, 'pps_proj_2031_32_' + s]) if n in _sc.index and _pd.notna(_sc.loc[n, 'pps_proj_2031_32_' + s]) else None) for n, v in _SC[s]['imm'].items() if v > 0} for s in 'AB'}
data = 'const PROG=' + json.dumps(PROG) + ';\nconst CMPD=' + cmpd + ';\nconst SLBL=' + json.dumps(slbl, ensure_ascii=False).replace('</', '<\\/') + ';\n'
rep('<script>\nconst BASE=', '<script>\n' + data + 'const BASE=')

rep('const gA=mk("g"),gPri=mk("g"),gRail=mk("g"),gRiv=mk("g"),gFwy=mk("g"),gCur=mk("g"),gS=mk("g");const gB=mk("g"),gSt=mk("g");svg.append(gA,gSt,gPri,gRail,gRiv,gFwy,gB,gCur,gS);',
'''const gA=mk("g"),gPri=mk("g"),gRail=mk("g"),gRiv=mk("g"),gFwy=mk("g"),gCur=mk("g"),gS=mk("g");const gB=mk("g"),gSt=mk("g");
const gA2=mk("g"),gDiff=mk("g"),gOv=mk("g"),gStN=mk("g");
{const defs=mk("defs");const c1=mk("clipPath",{id:"swc"});c1.append(mk("rect",{id:"swr",x:0,y:0,width:1,height:1}));const c2=mk("clipPath",{id:"swcL"});c2.append(mk("rect",{id:"swrL",x:0,y:0,width:1,height:1}));
 const pt=mk("pattern",{id:"hatch",patternUnits:"userSpaceOnUse",width:6,height:6});pt.append(mk("path",{d:"M-1,1 L1,-1 M0,6 L6,0 M5,7 L7,5",style:"stroke:var(--ink);stroke-width:1.2;opacity:.6;fill:none"}));defs.append(c1,c2,pt);svg.append(defs)}
svg.append(gA,gA2,gDiff,gSt,gPri,gRail,gRiv,gFwy,gB,gCur,gOv,gStN,gS);''')
rep('"stroke-width":"0.7","stroke-opacity":"0.9","vector-effect":"non-scaling-stroke"});\ngSt.append', '"stroke-width":"0.6","stroke-opacity":"0.6","vector-effect":"non-scaling-stroke"});\ngSt.append')

# replace drawAreas, rename select
i = t.index('function drawAreas(){'); j = t.index('function select(n){')
t = t[:i] + t[j:]
rep('function select(n){sel=n;gA.querySelectorAll', 'function selectOne(n){sel=n;gA.querySelectorAll')
rep('document.getElementById("lcur").onchange=e=>gCur.style.display=(e.target.checked&&scn!=="T")?"":"none";\n', '')
rep('gS.querySelectorAll("circle").forEach(c=>c.setAttribute("r",(3.6*k).toFixed(2)));','gS.querySelectorAll("circle").forEach(c=>c.setAttribute("r",((+c.dataset.rm||1)*3.6*k).toFixed(2)));')
rep('const stOn=document.getElementById("lst").checked;stS.style.display=stOn&&z>=1.6?"":"none";stR.style.display=stOn&&z>=3?"":"none";', 'streetState(z);viewHook();')
rep('document.getElementById("lst").onchange=updateLabels;', 'document.getElementById("lst").onchange=updateLabels;')
js = open(os.path.join(HERE, 'v2_main.js')).read()
rep('drawAreas();\nwindow.addEventListener("resize",updateLabels);', js + '\ninitCompare();\nwindow.addEventListener("resize",()=>{nmReg=null;updateLabels()});')

rep('tap an area for its numbers.</p>', 'tap an area for its numbers. New: pick two plans and compare them with a swipe slider or an overlay, and zoom in for local streets and street names.</p>')
open(OUT, 'w', encoding='utf-8').write(t)
print(OUT, len(t.encode()))
