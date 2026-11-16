"""Georeference PPS scenario-map PDFs (all share one page layout/extent) by fitting an
affine PDF-points -> EPSG:2913 transform:
  1. initial fit: school-name labels -> school coordinates (pps_schools.csv)
  2. ICP refinement: Status-Quo 6-8 teal boundary vertices -> current (City/PPS 2023-24 FINAL)
     middle-school boundaries.
Writes work/georef_affine.json with residual stats."""
import json, pathlib
import numpy as np, pandas as pd, geopandas as gpd
from scipy.spatial import cKDTree
from shapely.geometry import LineString, Point
D = pathlib.Path(__file__).resolve().parent.parent
d = json.load(open(D / "work/pdfpaths_Status_Quo_6_8.json"))
sch = pd.read_csv(D / "raw/meub-pps-data/data/pps_schools.csv")
sch = gpd.GeoDataFrame(sch, geometry=gpd.points_from_xy(sch.longitude, sch.latitude), crs=4326).to_crs(2913)
key = {"Beaumont": "Beaumont Middle", "Kellogg": "Kellogg", "George": "George Middle", "Harrison": "Harrison Park",
       "Brentwood": "Lane Middle", "Sylvan": "West Sylvan", "Tabor": "Mt Tabor", "Ockley": "Ockley Green",
       "Tubman": "Harriet Tubman", "Roseway": "Roseway", "Gray": "Gray Middle", "Faubion": "Faubion",
       "Astor": "Astor", "Sunnyside": "Sunnyside", "Jackson": "Jackson", "Vinci": "da Vinci",
       "Winterhaven": "Winterhaven", "Laurelhurst": "Laurelhurst", "Hosford": "Hosford", "Vernon": "Vernon",
       "Bridger": "Bridger", "Sellwood": "Sellwood", "Cleary": "Beverly Cleary", "Chávez": "Chávez"}
src, dst = [], []
for w in d["words"]:
    if w["t"] in key:
        m = sch[sch.school_name.str.contains(key[w["t"]], regex=False)]
        if len(m) == 1 and w["y"] < 2950 and not (w["x"] < 700 and w["y"] > 2100):
            src.append((w["x"], w["y"])); dst.append((m.geometry.x.iloc[0], m.geometry.y.iloc[0]))
src, dst = np.array(src), np.array(dst)
def fit(s, t):
    A = np.c_[s, np.ones(len(s))]
    M, *_ = np.linalg.lstsq(A, t, rcond=None)
    return M  # 3x2
def apply(M, s): return np.c_[s, np.ones(len(s))] @ M
M = fit(src, dst)
r = np.linalg.norm(apply(M, src) - dst, axis=1)
print("label fit pairs", len(src), "median resid ft", np.median(r).round(0))
# current middle boundaries, densely sampled
cells = gpd.read_file(D / "raw/boundaries/city_school_attendance_cells.geojson").to_crs(2913)
ms = cells.dissolve("Grade_6_Choice1_Name")
pts = []
for g in ms.geometry.boundary:
    for ln in getattr(g, "geoms", [g]):
        L = ln.length; n = max(2, int(L / 50))
        pts += [ln.interpolate(t).coords[0] for t in np.linspace(0, L, n)]
tgt = np.array(pts); tree = cKDTree(tgt)
# teal vertices (main frame only; drop inset), densify segments
sv = []
for poly in d["teal"]:
    p = np.array(poly)
    for a, b in zip(p[:-1], p[1:]):
        n = max(1, int(np.hypot(*(b - a)) / 3))
        sv += [a + (b - a) * t for t in np.linspace(0, 1, n, endpoint=False)]
sv = np.array(sv)
sv = sv[~((sv[:, 0] < 700) & (sv[:, 1] > 2100))]
for thr in [3000, 1500, 800, 400, 250, 150, 100, 100, 100]:
    T = apply(M, sv)
    dist, idx = tree.query(T)
    k = dist < thr
    M = fit(sv[k], tgt[idx[k]])
T = apply(M, sv); dist, _ = tree.query(T)
print("ICP: vertices", len(sv), "median dist ft", np.median(dist).round(1), "p90", np.percentile(dist, 90).round(1), "share<100ft", (dist < 100).mean().round(3))
print("scale ft/pt", np.hypot(*M[0]).round(3), np.hypot(*M[1]).round(3))
json.dump({"affine_3x2": M.tolist(), "crs": "EPSG:2913", "median_resid_ft": float(np.median(dist)),
           "p90_resid_ft": float(np.percentile(dist, 90)), "inset_excluded": "x<700 & y>2100 (PDF pts)"},
          open(D / "work/georef_affine.json", "w"), indent=1)
