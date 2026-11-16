# Crisp redraw boundaries

`crisp.json` replaces `geo/smoothF.json`. It uses the same format: keys FA, FB and FDA, each holding {poly, outline}.
Boundaries now follow real streets, rail lines, freeways, the zone edges (river and I-84) and today's PPS lines. They are
straight segments, with no Chaikin rounding.

## Method
1. `faces.py` nodes and polygonizes these lines into about 11.5k "street faces" (roughly city blocks), clipped to the district outline:
   secondary, tertiary and residential streets (`work/streets.txt`); motorway, trunk, primary and rail (BASE in the page);
   today's PPS boundaries (`work/enc.txt`); the district outline; and the W/N/S zone polygons.
2. `assign.py`: each 2020 block centre gets the school of the published unsmoothed polygon (`geo/<X>_fix.json`) that contains it.
   - A face holding centres of only one school goes to that school whole.
   - An empty face goes whole to the school that covers most of its area. Thin or tiny empty slivers go instead to the
     school they share the most border with.
   - A face holding centres of 2 or more schools (about 110 faces, mostly large superblocks in the West Hills, Forest Park and
     industrial areas) is cut along the reference (Voronoi) line.
   - Reconnect pass: when a populated piece ends up cut off from its school, empty faces between them are flipped to that
     school. If that is not enough, the populated faces on the path are cut along the reference line. This keeps the
     students where they are, at the cost of a thin tongue.
3. mapshaper runs `snap -clean -dissolve -explode`. `frag.py` then gives each leftover fragment beyond the reference piece
   count to the neighbour it shares the most border with. Every fragment it moves holds 0 students.
4. mapshaper builds the topology. `topo2crisp.py` is step3g without Chaikin: shared arcs get RDP only (TOL=0.00008°, about 8 m)
   and outer arcs get the same light Visvalingam pass as before. Neighbours share the exact same arcs, and there are no
   overlaps or gaps.

## Page changes required (`patch_page.py`; apply to walkmap5_tpl.html or the built page)
- `colorize()` used to find neighbours from polygon vertices only. Straight edges have few vertices, so neighbouring schools
  could get the same colour. The patch samples points along every edge instead.
- Edges now run down streets, and the street layer drawn above the areas hid the white edges. The patch draws stroke-only
  copies of the area outlines above the streets, and the selection outline moves to that layer too.
- Colours are reassigned by the same greedy colouring as before. Because the neighbours it finds have changed, many
  schools get a different colour than on the published page.

## Rebuild
    ./run.sh                      # faces (cached in faces.pkl) -> assign -> dissolve -> frag -> topology -> crisp.json
    python3 preview.py            # preview_before.html (published copy) + preview_after.html (crisp + patch)
    NODE_PATH=$(npm root -g) node shot.js preview_after.html after A,B,DA
    python3 check.py crisp.json imp_after.json && node metrics.js imp_after.json   # wrong-side check + stats

To use it in the real build, have b8.py read `crisp/crisp.json` instead of `geo/smoothF.json`, and run `patch_page.py` on the
output page.
