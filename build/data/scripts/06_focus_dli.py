"""focus_dli.csv + focus_dli_homes.parquet (estimated home blocks of DLI-strand and focus-option students)."""
import pathlib, numpy as np, pandas as pd
D = pathlib.Path(__file__).resolve().parent.parent
s = pd.read_csv(D / "work/schools_base.csv").set_index("name")
b = pd.read_parquet(D / "blocks.parquet")
G = ["g_K"] + [f"g_{i}" for i in range(1, 13)]
BAND = {"K-5": G[:6], "6-8": G[6:9], "9-12": G[9:], "K-8": G[:9], "K-12": G}
RAWB = {"K-5": ["raw_k5"], "6-8": ["raw_m68"], "9-12": ["raw_h912"], "K-8": ["raw_k5", "raw_m68"], "K-12": ["raw_k5", "raw_m68", "raw_h912"]}
# (program id, host, kind, language, grades, enrollment 2025-26, source, service area rule, whole_school)
P = [
 ("DLI Spanish @ Ainsworth","Ainsworth","DLI","Spanish","K-5",287,"PRC T5.5","cluster",0),
 ("DLI Spanish @ Atkinson","Atkinson","DLI","Spanish","K-5",178,"PRC T5.5","cluster",0),
 ("DLI Spanish @ Beach","Beach","DLI","Spanish","K-5",155,"PRC T5.5","cluster",0),
 ("DLI Spanish @ Cesar Chavez","Cesar Chavez","DLI","Spanish","K-8",300,"PRC T5.5","cluster",0),
 ("DLI Mandarin @ Clark","Clark","DLI","Mandarin","K-5",91,"PRC T5.5","cluster",0),
 ("DLI Spanish @ James John","James John","DLI","Spanish","K-5",133,"PRC T5.5","cluster",0),
 ("DLI Russian @ Kelly","Kelly","DLI","Russian","K-5",143,"PRC T5.5","cluster",0),
 ("DLI Spanish @ Lent (whole school)","Lent","DLI","Spanish","K-5",256,"PRC T5.5","own_area",1),
 ("DLI Mandarin @ MLK Jr","MLK Jr","DLI","Mandarin","K-5",193,"PRC T5.5","cluster",0),
 ("DLI Spanish @ Rigler (whole school)","Rigler","DLI","Spanish","K-5",289,"PRC T5.5","own_area",1),
 ("DLI Vietnamese @ Rose City Park","Rose City Park","DLI","Vietnamese","K-5",207,"PRC T5.5","cluster",0),
 ("DLI Spanish @ Scott","Scott","DLI","Spanish","K-5",222,"PRC T5.5","cluster",0),
 ("DLI Spanish @ Sitton","Sitton","DLI","Spanish","K-5",138,"PRC T5.5","cluster",0),
 ("DLI Mandarin @ Woodstock","Woodstock","DLI","Mandarin","K-5",190,"PRC T5.5","cluster",0),
 ("DLI Japanese @ Richmond (whole school, no area)","Richmond","DLI","Japanese","K-5",512,"ODE/PRC","district",1),
 ("DLI Spanish @ Beaumont","Beaumont","DLI","Spanish","6-8",101,"PRC T5.5","cluster",0),
 ("DLI Spanish @ George","George","DLI","Spanish","6-8",109,"PRC T5.5","cluster",0),
 ("DLI Mandarin @ Tubman","Tubman","DLI","Mandarin","6-8",48,"PRC T5.5","cluster",0),
 ("DLI Mandarin @ Harrison Park","Harrison Park","DLI","Mandarin","6-8",111,"PRC T5.5","cluster",0),
 ("DLI Spanish @ Kellogg","Kellogg","DLI","Spanish","6-8",201,"PRC T5.5","cluster",0),
 ("DLI Russian @ Lane (Brentwood)","Lane (Brentwood)","DLI","Russian","6-8",36,"PRC T5.5","cluster",0),
 ("DLI Japanese @ Mt Tabor","Mt Tabor","DLI","Japanese","6-8",222,"PRC T5.5","district",0),
 ("DLI Spanish @ Ockley Green","Ockley Green","DLI","Spanish","6-8",63,"PRC T5.5","cluster",0),
 ("DLI Spanish @ Roseway Heights","Roseway Heights","DLI","Spanish","6-8",93,"PRC T5.5","cluster",0),
 ("DLI Vietnamese @ Roseway Heights","Roseway Heights","DLI","Vietnamese","6-8",64,"PRC T5.5","cluster",0),
 ("DLI Spanish @ West Sylvan","West Sylvan","DLI","Spanish","6-8",116,"PRC T5.5","cluster",0),
 ("DLI Mandarin @ Cleveland","Cleveland","DLI","Mandarin","9-12",115,"PRC T5.5","district",0),
 ("DLI Spanish @ Franklin","Franklin","DLI","Spanish","9-12",173,"PRC T5.5","cluster",0),
 ("DLI Russian @ Franklin","Franklin","DLI","Russian","9-12",29,"PRC T5.5","cluster",0),
 ("DLI Japanese @ Grant","Grant","DLI","Japanese","9-12",265,"PRC T5.5","district",0),
 ("DLI Mandarin @ Jefferson","Jefferson","DLI","Mandarin","9-12",14,"PRC T5.5","cluster",0),
 ("DLI Spanish @ Lincoln","Lincoln","DLI","Spanish","9-12",178,"PRC T5.5","cluster",0),
 ("DLI Spanish @ McDaniel","McDaniel","DLI","Spanish","9-12",205,"PRC T5.5","cluster",0),
 ("DLI Vietnamese @ McDaniel","McDaniel","DLI","Vietnamese","9-12",34,"PRC T5.5","cluster",0),
 ("DLI Spanish @ Roosevelt","Roosevelt","DLI","Spanish","9-12",299,"PRC T5.5","cluster",0),
 ("Focus: Winterhaven K-8 (STEM)","Winterhaven","focus","","K-8",316,"ODE","district",1),
 ("Focus: da Vinci 6-8 (arts)","da Vinci","focus","","6-8",429,"ODE","district",1),
 ("Focus: Odyssey K-8","Odyssey","focus","","K-8",217,"PRC T5.5","district",1),
 ("Focus: ACCESS 1-8 (TAG)","ACCESS","focus","","K-8",324,"PRC T5.5","district",1),
 ("Alt: MLC K-12","MLC","focus","","K-12",275,"ODE","district",1),
 ("Focus: Benson 9-12 (CTE)","Benson","focus","","9-12",1024,"ODE","district",1),
]
# school-level host clusters (2025-26 HS cluster of the host building's own block area)
host_cluster = {}
for n, r in s.iterrows():
    key = r.es_area if isinstance(r.es_area, str) else (r.ms_area if isinstance(r.ms_area, str) else None)
    if key and isinstance(r.es_area, str):
        host_cluster[n] = b[b.es_cur == key].hs_cluster_cur.mode().iloc[0]
    elif isinstance(r.ms_area, str):
        host_cluster[n] = b[b.ms_cur == key].hs_cluster_cur.mode().iloc[0]
    elif isinstance(r.hs_area, str):
        host_cluster[n] = r.hs_area if r.hs_area != "Jefferson" else "Grant"
rows, homes = [], pd.DataFrame({"GEOID": b.GEOID})
for pid, host, kind, lang, grades, enr, src, svc, whole in P:
    r = s.loc[host]
    gc = BAND[grades]
    gd = r[gc].astype(float)
    if gd.isna().all() or gd.sum() == 0:
        gd = pd.Series(1.0, index=gc)
    est = (gd / gd.sum() * enr).round(1)
    w = b[RAWB[grades]].sum(axis=1)
    if svc == "cluster":
        cl = host_cluster.get(host); w = w.where(b.hs_cluster_cur == cl, 0); area = f"HS cluster {cl} (2025-26)"
    elif svc == "own_area":
        w = w.where(b.es_cur == r.es_area, 0); area = f"{host} attendance area"
    else:
        area = "whole district"
    homes[pid] = (w / w.sum() * enr).round(4)
    row = {"program": pid, "kind": kind, "language": lang, "host_building_2025_26": host, "grades": grades,
           "enrollment_2025_26": enr, "enrollment_source": src, "whole_school_program": whole,
           "counted_in_block_neighborhood_kids": "yes (target = whole school)" if svc == "own_area" else "no",
           "home_distribution_assumption": f"proportional to Census band residents (raw_*) in {area}",
           "host_cluster_2025_26": host_cluster.get(host, "")}
    for c in G: row[f"est_{c}"] = est.get(c, 0.0)
    rows.append(row)
df = pd.DataFrame(rows)
df.to_csv(D / "focus_dli.csv", index=False)
homes.to_parquet(D / "focus_dli_homes.parquet", index=False)
print(df[["program", "grades", "enrollment_2025_26", "host_cluster_2025_26"]].to_string())
