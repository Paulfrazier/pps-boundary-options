"""Fill gaps in the digitized scenario block assignments and write work/scenario_block_assign.parquet.
Rules (documented in README):
 - K-8 schools are drawn with dashed lines that are not digitized as polygons. Blocks not inside any
   digitized polygon whose K-5 school is a K-8 in that scenario keep that K-8 (Status Quo: today's K-8s;
   A/B: Astor and Skyline, the only neighborhood K-8s left) for K-5 and 6-8.
 - Skyline-area blocks (outside the main map frame, drawn only in the NW inset): K-5/6-8 Skyline; 9-12 Lincoln
   (Status Quo) or Roosevelt (A/B, per the Skyline/Lincoln/Roosevelt family guides).
 - A/B: uncovered blocks of today's Faubion area (Bybee Lake Shelter) -> Astor for K-5 and 6-8.
 - Any other uncovered block (slivers along rivers/edges): nearest digitized block of the same map."""
import pathlib, numpy as np, pandas as pd, geopandas as gpd
from scipy.spatial import cKDTree
D = pathlib.Path(__file__).resolve().parent.parent
c = pd.read_parquet(D / "work/blocks_raw.parquet"); r = pd.read_parquet(D / "work/scenario_block_assign_raw.parquet")
xy = np.c_[(c.x + 122.6) * 0.70, c.y - 45.5]  # cheap local metric (cos 45.5deg)
K8_SQ = {"Astor", "Beverly Cleary", "Bridger", "Cesar Chavez", "Faubion", "Laurelhurst", "Skyline", "Sunnyside", "Vernon"}
K8_AB = {"Astor", "Skyline"}
out = pd.DataFrame({"g": c.g})
for s in ["sq", "A", "B"]:
    k8 = K8_SQ if s == "sq" else K8_AB
    for lvl in ["es", "ms", "hs"]:
        lab = r[f"{s}_{lvl}_map"].copy(); how = pd.Series(np.where(lab.notna(), "map", ""), index=lab.index, dtype=object)
        miss = lab.isna()
        if lvl in ("es", "ms"):
            # K-8 rule keyed on today's K-5 area (K-8 areas are unchanged except Astor's small Bybee Lake shelter gain)
            rule = miss & c.a.isin(k8)
            lab[rule] = c.a[rule]; how[rule] = "k8_rule"
            if s != "sq":  # Bybee Lake Shelter area: Faubion -> Astor K-8 (Astor/Faubion family guides); it sits inside Astor's dashed K-8 line
                rule = lab.isna() & (c.a == "Faubion")
                lab[rule] = "Astor"; how[rule] = "bybee_rule"
        if lvl == "hs":
            rule = miss & (c.a == "Skyline")
            lab[rule] = "Lincoln" if s == "sq" else "Roosevelt"; how[rule] = "skyline_rule"
        miss = lab.isna()
        if miss.any():
            t = cKDTree(xy[~miss.values]); _, ix = t.query(xy[miss.values])
            lab[miss] = lab[~miss].values[ix]; how[miss] = "nearest"
        out[f"{s}_{lvl}"] = lab.values; out[f"{s}_{lvl}_how"] = how.values
        print(s, lvl, how.value_counts().to_dict())
out.to_parquet(D / "work/scenario_block_assign.parquet")
