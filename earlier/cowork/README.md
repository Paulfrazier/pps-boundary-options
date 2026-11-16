# Cowork working files (synced 2026-10-11)

Everything behind the published pages, from the cloud session. This fills the gap noted in CLAUDE.md §4: the block-level assignments are here.

## model/ (Node, run from this folder; core.js expects pps-model.json and pps-race.csv — edit the two paths at the top of core.js to data/pps-map/)
- **final_asg.json** — block-level assignments, keys `A` (walk redraw A, after the Rigler/Scott/Bridger group redraw), `B` (walk redraw B), `DA` (walk + diversity A). Arrays of school name, same order as `BL` in pps-model.json.
- core.js (model loading, race shares, `wmetrics`), algo.js (Lagrangian redraw, cleanup, contiguity, rebalance), ls.js (diversity local search), shape.js (boundary-length/compactness local search with hard 360–600 bounds, crossing locks), region.js (group re-solve used on Rigler/Scott/Bridger/Abernethy), final.js (produces final_asg.json + div2.json + wb2.json), tables.js (walk-band tables), wbcalc.js.
- edges.json — shared Voronoi edge length (km) between neighbouring blocks; 0 across zone lines.
- ls_final.json (`a100w0.5` = diversity A before smoothing), region_runs.json (`G8` = walk A final).

## geo/ (Python + `npx mapshaper`)
dpoly.py (block Voronoi → school polygons) → mapshaper -explode → step2g.py (sliver reassignment) → mapshaper -dissolve to topojson → step3g.py (smoothing, encoding). Output smoothF.json (keys FA, FB, FDA) is what the published map uses. pp.py = Polsby-Popper compactness per school.

## build/
b6.py makes walkmap5_tpl.html from walkmap4_tpl.html; b8.py fills it with data → pps-walk-redraw.html. wt_tpl.html + tables.json → pps-walk-tables.html. div2.json (diversity + summary metrics), wb2.json (walk bands), enc.txt (today's PPS lines), streets.txt (OSM streets).

## crisp/ (new, not yet published)
Street-following boundaries: same assignments, lines snapped to streets/today's lines with square corners. crisp.json is a drop-in replacement for smoothF.json (+ patch_page.py for the page). Compare before_ne_A.png vs after_ne_A.png. See crisp/README.md.

## Encoding
Polygon strings: rings joined by `|`; each ring `X0,Y0 dx,dy …` with lon=(X−1229300)/1e4, lat=(Y+454300)/1e4.
