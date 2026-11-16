"""Per-block grade-band raw resident counts (2020 DHC) + current attendance-area join.
Output: work/blocks_raw.parquet"""
import os as _os  # _PPS_MAP_HDR (added by export: repo-relative paths)
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PPS_MAP = _os.environ.get('PPS_MAP_DIR') or _os.path.join(_HERE, '../../../data/pps-map')
import json, pathlib
import numpy as np, pandas as pd, geopandas as gpd
D = pathlib.Path(__file__).resolve().parent.parent
m = json.load(open(_os.path.join(_PPS_MAP, 'pps-model.json')))
bl = pd.DataFrame([{k: b[k] for k in ("g", "x", "y", "a", "s", "pop", "hu")} for b in m["BL"]])
bl["idx"] = range(len(bl))

# --- block P12 bands
rows = json.load(open(D / "raw/census/dhc_p12_blocks.json"))
p = pd.DataFrame(rows[1:], columns=rows[0])
p["g"] = p.state + p.county + p.tract + p.block
for c in [c for c in p.columns if c.startswith("P12")]:
    p[c] = p[c].astype(int)
p["a0_4"] = p.P12_003N + p.P12_027N
p["a5_9"] = p.P12_004N + p.P12_028N
p["a10_14"] = p.P12_005N + p.P12_029N
p["a15_17"] = p.P12_006N + p.P12_030N
p = p[["g", "P12_001N", "a0_4", "a5_9", "a10_14", "a15_17"]].rename(columns={"P12_001N": "pop_dhc"})

# --- tract single-year ages -> within-band shares
rows = json.load(open(D / "raw/census/dhc_pct12_tracts.json"))
t = pd.DataFrame(rows[1:], columns=rows[0])
t["tract"] = t.state + t.county + t.tract
ages = np.zeros((len(t), 18))
for a in range(18):
    ages[:, a] = t[f"PCT12_{3+a:03d}N"].astype(int).values + t[f"PCT12_{107+a:03d}N"].astype(int).values
# grade g occupies age g+5 (5/12) and g+6 (7/12) on Census day (Apr 1) with a Sep 1 cutoff
def wvec(grades):
    w = np.zeros(19)  # ages 0..18
    for g in grades:
        w[g + 5] += 5 / 12; w[g + 6] += 7 / 12
    return w
W = {"k5": wvec(range(0, 6)), "m68": wvec(range(6, 9)), "h912": wvec(range(9, 13))}
bands = {"a5_9": range(5, 10), "a10_14": range(10, 15), "a15_17": range(15, 18)}
coef = {}  # coef[(tract, out_band, census_band)] = expected kids per census-band kid
for i, tr in enumerate(t.tract):
    a = ages[i]
    for ob, w in W.items():
        for cb, rg in bands.items():
            tot = a[list(rg)].sum()
            if tot > 0:
                share = a[list(rg)] / tot
            else:
                share = np.ones(len(rg)) / len(rg)
            c = float((share * w[list(rg)]).sum())
            if cb == "a15_17" and ob == "h912":
                # age 18 (7/12 of grade 12) is outside P12 <18 bands: approximate with age-17 count
                c += (share[-1]) * 7 / 12
            coef[(tr, ob, cb)] = c
p["tract"] = p.g.str[:11]
for ob in W:
    p[f"raw_{ob}"] = sum(p[cb] * p.tract.map(lambda tr, cb=cb, ob=ob: coef.get((tr, ob, cb), np.nan)) for cb in bands)
bl = bl.merge(p, on="g", how="left")
print("blocks w/o DHC:", bl.pop_dhc.isna().sum(), " pop match:", (bl.pop == bl.pop_dhc).mean())

# --- current attendance areas (City of Portland School_Boundaries cells = PPS 2023-24 FINAL board-approved)
cells = gpd.read_file(D / "raw/boundaries/city_school_attendance_cells.geojson")
pts = gpd.GeoDataFrame(bl[["idx"]], geometry=gpd.points_from_xy(bl.x, bl.y), crs=4326)
j = gpd.sjoin(pts, cells[["Grade_1_Choice1_Name", "Grade_6_Choice1_Name", "Grade_10_Choice1_Name", "geometry"]], how="left", predicate="within")
j = j[~j.idx.duplicated()]
miss = j.Grade_1_Choice1_Name.isna()
if miss.any():  # centroid just outside (river edge etc.): nearest cell
    near = gpd.sjoin_nearest(pts[miss.values].to_crs(2913), cells.to_crs(2913)[["Grade_1_Choice1_Name", "Grade_6_Choice1_Name", "Grade_10_Choice1_Name", "geometry"]])
    near = near[~near.idx.duplicated()]
    j = pd.concat([j[~miss], near.to_crs(4326)])
    print("nearest-cell fallback blocks:", miss.sum())
j = j.set_index("idx").sort_index()
bl["es_cur"] = j.Grade_1_Choice1_Name.values
bl["ms_cur"] = j.Grade_6_Choice1_Name.values
bl["hs_zone_cur"] = j.Grade_10_Choice1_Name.values
print("ES label agreement with model 'a':", (bl.es_cur == bl.a).mean())
print(bl[bl.es_cur != bl.a][["g", "a", "es_cur", "s"]].groupby(["a", "es_cur"]).s.agg(["count", "sum"]))
(D / "work").mkdir(exist_ok=True)
bl.to_parquet(D / "work/blocks_raw.parquet")
print(bl[["a0_4", "a5_9", "a10_14", "a15_17", "raw_k5", "raw_m68", "raw_h912"]].sum())
