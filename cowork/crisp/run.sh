#!/bin/sh
# Rebuild crisp polygons: faces -> assign -> dissolve -> fragment fix -> topology -> crisp.json
set -e
cd "$(dirname "$0")"
MS=../geo/node_modules/.bin/mapshaper
[ -f faces.pkl ] || python3 faces.py
python3 assign.py FA FB FDA
for X in FA FB FDA; do
  $MS -i ${X}_atoms.json snap -clean -dissolve fields=name -explode -o ${X}_cparts.json >/dev/null 2>&1
done
python3 frag.py FA FB FDA
for X in FA FB FDA; do
  $MS -i ${X}_cfix.json snap -clean -dissolve fields=name -o ${X}_ctopo.json format=topojson no-quantization >/dev/null 2>&1
done
[ -f topo2crisp.py ] && python3 topo2crisp.py crisp.json FA FB FDA || true
