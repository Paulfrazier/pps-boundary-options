"""Digitize PPS Oct-2026 scenario attendance maps (Status Quo / A / B x K-5 / 6-8 / 9-12).
Vector boundary paths from the PDFs -> georeferenced polygons (affine fitted in 05b) -> labelled
-> block assignment by centroid. Outputs:
  scenario_maps/<scen>_<level>.geojson  (labelled polygons, WGS84)
  work/scenario_block_assign.parquet    (per block: sq/A/B x es/ms/hs + method flags)"""
import json, re, pathlib
import numpy as np, pandas as pd, geopandas as gpd
from shapely.geometry import Polygon, Point, box
from shapely.validation import make_valid
import importlib.util
D = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("p", D / "scripts/05c_polys.py"); P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
M = np.array(json.load(open(D / "work/georef_affine.json"))["affine_3x2"])
Minv = np.linalg.inv(np.r_[M.T, [[0, 0, 1]]])
# canonical names (K-5 names = pps-model NAMES; MS/HS = City layer names)
ALIAS = {
 "K_5": {"Abernethy": "Abernethy", "Ainsworth": "Ainsworth", "Alameda": "Alameda", "Arleta": "Arleta", "Astor": "Astor", "Atkinson": "Atkinson",
   "Beach": "Beach", "Beverly Cleary": "Beverly Cleary", "Boise-Eliot/Humboldt": "Boise-Eliot/Humboldt", "Bridger( Creative Science)?": "Bridger",
   "Bridlemile": "Bridlemile", "Buckman": "Buckman", "Capitol Hill": "Capitol Hill", "C[ée]sar Ch[áa]vez": "Cesar Chavez", "Chapman": "Chapman",
   "Chief Joseph": "Chief Joseph", "Clark": "Clark", "Creston": "Creston", "Duniway": "Duniway", "Faubion": "Faubion", "Forest Park": "Forest Park",
   "Glencoe": "Glencoe", "Grout": "Grout", "Hayhurst": "Hayhurst", "Irvington": "Irvington", "James John": "James John", "Kelly": "Kelly",
   "Laurelhurst": "Laurelhurst", "Lee": "Lee", "Sunrise": "Lee", "Lent": "Lent", "Lewis": "Lewis", "Llewellyn": "Llewellyn", "(Dr\\. )?(MLK|Martin Luther King)( Jr\\.?)?": "MLK Jr",
   "Maplewood": "Maplewood", "Markham": "Markham", "Marysville": "Marysville", "Peninsula": "Peninsula", "Rieke": "Rieke", "Rigler": "Rigler",
   "Rosa Parks": "Rosa Parks", "Rose City Park": "Rose City Park", "Sabin": "Sabin", "Scott": "Scott", "Sitton": "Sitton", "Skyline": "Skyline",
   "Stephenson": "Stephenson", "Sunnyside( Environmental)?": "Sunnyside", "Vernon": "Vernon", "Vestal": "Vestal", "Whitman": "Whitman",
   "Woodlawn": "Woodlawn", "Woodmere": "Woodmere", "Woodstock": "Woodstock"},
 "6_8": {"Beaumont": "Beaumont", "Brentwood": "Lane", "Lane": "Lane", "George": "George", "(Robert )?Gray": "Gray", "Harrison Park": "Harrison Park",
   "Hosford": "Hosford", "Jackson": "Jackson", "Kellogg": "Kellogg", "(Mt\\.? )?Tabor": "Mt Tabor", "Ockley Green": "Ockley Green",
   "Roseway Heights": "Roseway Heights", "Sellwood": "Sellwood", "(Harriet )?Tubman": "Tubman", "West Sylvan": "West Sylvan"},
 "9_12": {"Cleveland": "Cleveland", "Franklin": "Franklin", "Grant": "Grant", "(Ida B\\.? )?Wells(-Barnett)?": "Ida B. Wells", "Jefferson": "Jefferson",
   "Lincoln": "Lincoln", "McDaniel": "McDaniel", "Roosevelt": "Roosevelt"}}
SUFFIX = {"K_5": r"K-[58]", "6_8": r"Middle School", "9_12": r"High School"}
DLI_ONLY = {"Lent", "Rigler", "Cesar Chavez", "Richmond"}  # whole-school DLI under the scenarios: never the neighborhood label
def label(text, lvl):
    hits = []
    for pat, canon in ALIAS[lvl].items():
        for m in re.finditer(r"(?<![A-Za-z])" + pat + r"\s+" + SUFFIX[lvl] + r"\s*(\S+)?", text):
            nxt = (m.groups()[-1] or "")
            hits.append((m.start(), canon, nxt))
    good = [h for h in hits if not h[2].startswith(("Focus", "Closed"))]
    nb = [h for h in good if h[2].startswith("Neighborhood") and h[1] not in DLI_ONLY]
    imm = [h for h in good if h[1] not in DLI_ONLY]
    pick = nb or imm
    return (pick[0][1] if pick else None), sorted({h[1] for h in hits})
cur = pd.read_parquet(D / "work/blocks_raw.parquet")
pts = gpd.GeoSeries(gpd.points_from_xy(cur.x, cur.y), crs=4326).to_crs(2913)
bxy = np.c_[pts.x, pts.y]
pdfxy = np.c_[bxy, np.ones(len(bxy))] @ Minv.T[:, :2]
frame = (pdfxy[:, 0] > 40) & (pdfxy[:, 0] < 2550) & (pdfxy[:, 1] > 40) & (pdfxy[:, 1] < 2985) & ~((pdfxy[:, 0] < 700) & (pdfxy[:, 1] > 2100))
print("blocks outside main map frame (inset/off-sheet):", (~frame).sum(), "current ES there:", cur.a[~frame].value_counts().to_dict())
OUT = D / "scenario_maps"; OUT.mkdir(exist_ok=True)
CURCOL = {"K_5": "a", "6_8": "ms_cur", "9_12": "hs_zone_cur"}
res = {}
report = []
for scen in ["Status_Quo", "Scenario_A", "Scenario_B"]:
    for lvl in ["K_5", "6_8", "9_12"]:
        name = f"{scen}_{lvl}"
        polys, words = P.get(name)
        feats = []
        for i, Pp in enumerate(polys):
            if Pp["inset"]: continue
            pp = Polygon(Pp["pdf"]); pp = pp if pp.is_valid else make_valid(pp)
            if pp.area < 500: continue
            ws = [w for w in words if pp.contains(Point(w["x"], w["y"]))]
            text = " ".join(w["t"] for w in ws)
            lab, cands = label(text, lvl)
            g = np.array(Pp["pdf"]); g = np.c_[g, np.ones(len(g))] @ M
            geo = Polygon(g); geo = geo if geo.is_valid else make_valid(geo)
            feats.append({"i": i, "label": lab, "cands": ",".join(cands), "pdf_area": pp.area, "geometry": geo})
        gdf = gpd.GeoDataFrame(feats, crs=2913)
        # assign blocks: smallest containing polygon
        bp = gpd.GeoDataFrame({"bi": range(len(cur))}, geometry=pts.values, crs=2913)
        j = gpd.sjoin(bp, gdf[["i", "label", "pdf_area", "geometry"]], predicate="within").sort_values("pdf_area")
        j = j[~j.bi.duplicated()].set_index("bi")
        lab = pd.Series(j.label, index=j.index).reindex(range(len(cur)))
        # unlabelled polygons: name by majority current school of the blocks inside (only for polygons with no label text)
        for i in gdf.i[gdf.label.isna()]:
            ids = j.index[j.i == i]
            if len(ids):
                maj = cur.loc[ids, CURCOL[lvl]].mode().iloc[0]
                gdf.loc[gdf.i == i, "label"] = maj; gdf.loc[gdf.i == i, "cands"] = f"(unlabelled; majority-current={maj})"
                lab[ids] = maj
        method = pd.Series(np.where(lab.notna(), "map", ""), index=lab.index)
        res[(scen, lvl)] = (lab, method)
        gdf.to_crs(4326).to_file(OUT / f"{scen}_{lvl}.geojson", driver="GeoJSON")
        report.append((name, len(gdf), int(lab.notna().sum()), sorted(gdf.label.dropna().unique().tolist())))
for r in report: print(r[0], "polys", r[1], "blocks mapped", r[2], r[3])
# assemble
out = pd.DataFrame({"g": cur.g})
for (scen, lvl), (lab, method) in res.items():
    s = {"Status_Quo": "sq", "Scenario_A": "A", "Scenario_B": "B"}[scen]; l = {"K_5": "es", "6_8": "ms", "9_12": "hs"}[lvl]
    out[f"{s}_{l}_map"] = lab.values
out["in_frame"] = frame
out.to_parquet(D / "work/scenario_block_assign_raw.parquet")
