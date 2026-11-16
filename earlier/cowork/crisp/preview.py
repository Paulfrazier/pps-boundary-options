# Build preview pages: preview_before.html (published page copy) and preview_after.html
# (same page with polygons from crisp.json).  Usage: python3 preview.py [crisp.json] [out.html]
import os as _os  # _PPS_MAP_HDR (added by export: repo-relative paths)
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PPS_MAP = _os.environ.get('PPS_MAP_DIR') or _os.path.join(_HERE, '../../data/pps-map')
import json, sys
S = (_os.environ.get('CRISP_WORKDIR') or _os.path.join(_HERE, '..'))
src = sys.argv[1] if len(sys.argv) > 1 else 'crisp.json'
out = sys.argv[2] if len(sys.argv) > 2 else 'preview_after.html'
f = open(f'{S}/work/pps-walk-redraw.html').read()
open(f'{S}/crisp/preview_before.html', 'w').write(f)
c = json.load(open(src))
i = f.index('const RD=') + 9; j = f.index(';\nconst SCH=', i)
rd = json.loads(f[i:j])
for k in 'A', 'B', 'DA': rd[k]['poly'] = c['F' + k]['poly']
f = f[:i] + json.dumps(rd, separators=(',', ':')) + f[j:]
i = f.index('const OUTL=') + 11; j = f.index(';', i)
f = f[:i] + json.dumps(c['FA']['outline']) + f[j:]
open(out, 'w').write(f)
import subprocess; subprocess.run(['python3', f'{S}/crisp/patch_page.py', out, out], check=True)
print(out, len(f))
