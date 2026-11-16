"""Turn extracted boundary paths into georeferenced polygons and list the label words inside each."""
import json, pathlib, sys
import numpy as np, pdfplumber
from shapely.geometry import Polygon, Point
from shapely.validation import make_valid
D = pathlib.Path(__file__).resolve().parent.parent
M = np.array(json.load(open(D / "work/georef_affine.json"))["affine_3x2"])
STYLE = {"K_5": ((0.85409, 0.66987, 0.0), 2.5), "6_8": ((0.0, 0.6125, 0.57128), 2.5), "9_12": ((0.0, 0.32554, 0.5451), 9)}
def close(a, b): return isinstance(a, (list, tuple)) and len(a) == 3 and all(abs(x - y) < 0.01 for x, y in zip(a, b))
def get(name):
    lvl = next(k for k in STYLE if name.endswith(k))
    col, lw = STYLE[lvl]
    pg = pdfplumber.open(D / f"raw/scenario_maps/{name}.pdf").pages[0]
    polys = []
    for o in pg.curves:
        if o.get("stroke") and close(o.get("stroking_color"), col) and (o.get("linewidth") or 0) >= lw:
            p = np.array(o["pts"])
            if len(p) < 4: continue
            inset = (p[:, 0].mean() < 700) and (p[:, 1].mean() > 2100)
            polys.append({"pdf": p.tolist(), "inset": bool(inset)})
    words = json.load(open(D / f"work/pdfpaths_{name}.json"))["words"]
    return polys, words
if __name__ == "__main__":
    for name in sys.argv[1:]:
        polys, words = get(name)
        print("=====", name, len(polys))
        for i, P in enumerate(polys):
            pp = Polygon(P["pdf"])
            if not pp.is_valid: pp = make_valid(pp)
            inside = [w["t"] for w in words if w["size"] >= 8 and pp.contains(Point(w["x"], w["y"])) and w["t"][0].isupper() and len(w["t"]) > 2]
            print(i, "inset" if P["inset"] else "", round(pp.area), " ".join(inside)[:300])
