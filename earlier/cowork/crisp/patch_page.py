# Two small page-code changes that crisp (street-following, few-vertex) boundaries need.
# Works on the built page or on walkmap5_tpl.html.  Usage: python3 patch_page.py IN OUT
#  1. colorize(): adjacency was detected from polygon vertices only; long straight edges have few
#     vertices, so neighbours could get the same colour.  Sample points along every edge instead.
#  2. (+ selection outline moved to that layer too) Boundaries now run down streets, so the street layer (drawn above the areas) hid the white
#     area edges.  Draw a stroke-only copy of every area outline above the street layer.
import sys
t = open(sys.argv[1]).read()
def R(old, new):
    global t
    assert t.count(old) == 1, old[:70]
    t = t.replace(old, new)
R('pts[n]=dec(polys[n]).flat().map(([x,y])=>[x*kx,y])',
  'pts[n]=dec(polys[n]).flatMap(r=>r.flatMap((p,i)=>{const q=r[(i+1)%r.length],k=Math.max(1,Math.ceil(Math.hypot((q[0]-p[0])*kx,q[1]-p[1])/0.0005));return Array.from({length:k},(_,j)=>[(p[0]+(q[0]-p[0])*j/k)*kx,p[1]+(q[1]-p[1])*j/k])}))')
R('const gB=mk("g"),gSt=mk("g");svg.append(gA,gSt,', 'const gB=mk("g"),gSt=mk("g"),gE=mk("g");svg.append(gA,gSt,gE,')
R('function drawAreas(){gA.replaceChildren();', 'function drawAreas(){gA.replaceChildren();gE.replaceChildren();')
R('p.addEventListener("keydown",e=>{if(e.key==="Enter")select(n)});gA.append(p)});',
  'p.addEventListener("keydown",e=>{if(e.key==="Enter")select(n)});gA.append(p);gE.append(mk("path",{d:p.getAttribute("d"),class:"edge","fill-rule":"evenodd"}))});')
R('.area:hover{', '.edge{fill:none;stroke:var(--edge);stroke-width:1.6;stroke-linejoin:miter;vector-effect:non-scaling-stroke;pointer-events:none}\n.area:hover{')
R('function select(n){sel=n;gA.querySelectorAll(".area").forEach(p=>{p.classList.toggle("sel",p.dataset.n===n);if(p.dataset.n===n)gA.append(p)});',
  'function select(n){sel=n;gA.querySelectorAll(".area").forEach(p=>{p.classList.toggle("sel",p.dataset.n===n);if(p.dataset.n===n)gA.append(p)});gE.querySelectorAll(".edge").forEach(p=>{p.classList.toggle("sel",p.dataset.n===n);if(p.dataset.n===n)gE.append(p)});')
R('gE.append(mk("path",{d:p.getAttribute("d"),class:"edge",', 'gE.append(mk("path",{d:p.getAttribute("d"),class:"edge","data-n":n,')
R('.area:hover{', '.edge.sel{stroke:var(--ink);stroke-width:2.6}\n.area:hover{')
open(sys.argv[2], 'w').write(t)
print('patched', sys.argv[2])
