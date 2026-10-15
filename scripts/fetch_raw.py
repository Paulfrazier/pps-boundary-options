#!/usr/bin/env python3
"""Fetch the raw inputs that this repo does not redistribute, into build/data/raw/ and build/routing/osm/.

Best effort: public URLs move. Each step is independent; re-run with step names to retry one.

    export CENSUS_API_KEY=...            # free key: https://api.census.gov/data/key_signup.html
    python scripts/fetch_raw.py          # all steps
    python scripts/fetch_raw.py meub boundaries maps guides census osm

Steps
  meub        git clone https://github.com/meub/pps-data -> build/data/raw/meub-pps-data
              (ODE fall membership 2025-26, PSU forecast CSV/PDF, PPS school list + capacities, immersion details)
  boundaries  City of Portland School_Boundaries layer (PPS cells) -> build/data/raw/boundaries/
  maps        PPS 2027-28 attendance-area map PDFs from BoardBook (org 915, files 14505795-14505805)
              -> build/data/raw/scenario_maps/{Status_Quo,Scenario_A,Scenario_B}_{K_5,6_8,9_12}.pdf
  guides      PPS per-school Family Guides (Google Drive ids in scripts/family_guides_index.tsv)
              -> build/data/raw/family_guides/*.pdf + all_text.txt (what build/data/scripts/07 parses)
  census      2020 DHC P12 (blocks) + PCT12 (tracts) via build/data/scripts/01_fetch_census.py
  osm         Oregon extract from Geofabrik, clipped to Portland with osmium -> build/routing/osm/portland.osm.pbf
"""
import os
import re
import subprocess
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'build' / 'data' / 'raw'
UA = {'User-Agent': 'pps-boundary-options fetch (independent research)'}


def get(url, dest, **kw):
    dest.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, headers=UA, timeout=120, **kw)
    r.raise_for_status()
    dest.write_bytes(r.content)
    print(f'  {dest.relative_to(ROOT)} ({len(r.content):,} bytes)')
    return dest


def meub():
    d = RAW / 'meub-pps-data'
    if d.exists():
        subprocess.check_call(['git', '-C', str(d), 'pull', '--ff-only'])
    else:
        subprocess.check_call(['git', 'clone', '--depth', '1', 'https://github.com/meub/pps-data', str(d)])
    print('  note: the analysis used meub/pps-data at commit 80ec323 (2026-10-05); check out that commit to reproduce exactly.')


def boundaries():
    base = 'https://services.arcgis.com/quVN97tn06YNGj9s/arcgis/rest/services/School_Boundaries/FeatureServer/0/query'
    params = {'where': "Unified_SD_Name='Portland SD 1J'", 'outFields': '*', 'outSR': '4326', 'f': 'geojson'}
    get(base, RAW / 'boundaries' / 'city_school_attendance_cells.geojson', params=params)


def maps():
    import pdfplumber
    out = RAW / 'scenario_maps'
    for fid in range(14505795, 14505806):
        p = out / f'boardbook_{fid}.pdf'
        try:
            get(f'https://meetings.boardbook.org/Documents/DownloadPDF/{fid}?org=915', p)
        except Exception as e:  # some ids in the range are not maps
            print(f'  {fid}: {e}')
            continue
        try:
            txt = pdfplumber.open(p).pages[0].extract_text() or ''
        except Exception:
            continue
        scen = 'Status_Quo' if re.search(r'Status\s*Quo', txt, re.I) else ('Scenario_A' if re.search(r'Scenario\s*A\b', txt) else ('Scenario_B' if re.search(r'Scenario\s*B\b', txt) else None))
        lvl = next((k for k, rx in (('K_5', r'K\s*[-–]\s*5'), ('6_8', r'6\s*[-–]\s*8'), ('9_12', r'9\s*[-–]\s*12')) if re.search(rx, txt)), None)
        if scen and lvl:
            p.rename(out / f'{scen}_{lvl}.pdf')
            print(f'    -> {scen}_{lvl}.pdf')
        else:
            print(f'    could not identify {p.name}; rename it by its title by hand')


def guides():
    import pdfplumber
    out = RAW / 'family_guides'
    idx = ROOT / 'scripts' / 'family_guides_index.tsv'
    parts = []
    for line in idx.read_text().splitlines():
        if not line.strip():
            continue
        name, fid = line.split('\t')[:2]
        p = out / f'{name}.pdf'
        if not p.exists():
            try:
                get(f'https://drive.google.com/uc?export=download&id={fid}', p)
            except Exception as e:
                print(f'  {name}: {e}')
                continue
        with pdfplumber.open(p) as pdf:
            text = '\n'.join((pg.extract_text() or '') for pg in pdf.pages)
            parts.append(f'######## {p.name} pages={len(pdf.pages)}\n{text}\n')
    (out / 'all_text.txt').write_text(''.join(parts))
    print(f'  all_text.txt from {len(parts)} guides')


def census():
    if not os.environ.get('CENSUS_API_KEY'):
        sys.exit('set CENSUS_API_KEY first')
    subprocess.check_call([sys.executable, str(ROOT / 'build' / 'data' / 'scripts' / '01_fetch_census.py')])


def osm():
    osm_dir = ROOT / 'build' / 'routing' / 'osm'
    pbf = osm_dir / 'oregon-latest.osm.pbf'
    if not pbf.exists():
        osm_dir.mkdir(parents=True, exist_ok=True)
        subprocess.check_call(['curl', '-L', '-o', str(pbf), 'https://download.geofabrik.de/north-america/us/oregon-latest.osm.pbf'])
    subprocess.check_call(['osmium', 'extract', '-b', '-123.00,45.36,-122.40,45.75', str(pbf),
                           '-o', str(osm_dir / 'portland.osm.pbf'), '--overwrite'])


STEPS = {'meub': meub, 'boundaries': boundaries, 'maps': maps, 'guides': guides, 'census': census, 'osm': osm}

if __name__ == '__main__':
    for name in (sys.argv[1:] or list(STEPS)):
        print(f'== {name}')
        try:
            STEPS[name]()
        except Exception as e:
            print(f'  FAILED: {e}')
