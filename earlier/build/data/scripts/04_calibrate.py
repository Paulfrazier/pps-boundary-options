"""Calibrate block kids by grade band to 2025-26 neighborhood enrollment; run the backtest; write
blocks.parquet / blocks.csv and work/backtest_tables.json."""
import json, pathlib, numpy as np, pandas as pd
D = pathlib.Path(__file__).resolve().parent.parent
b = pd.read_parquet(D / "work/blocks_raw.parquet")
sc = pd.read_parquet(D / "work/scenario_block_assign.parquet")
s = pd.read_csv(D / "work/schools_base.csv")
b["bg"] = b.g.str[:12]; b["tract"] = b.g.str[:11]
b["u18"] = b.a0_4 + b.a5_9 + b.a10_14 + b.a15_17
POP = b["pop"]
# --- smoothed raw counts: block pop x block-group band rate (same smoothing the first-generation model's per-block estimate, `s` in pps-model.json, used for under-18)
for band in ["k5", "m68", "h912"]:
    rate = b.groupby("bg")[f"raw_{band}"].transform("sum") / b.groupby("bg")["pop"].transform("sum")
    b[f"w_{band}"] = POP * rate
b["w_u18"] = POP * b.groupby("bg").u18.transform("sum") / b.groupby("bg")["pop"].transform("sum")
# --- targets (2025-26 neighborhood-program enrollment)
S = s.set_index("name")
def nb(name, band):
    r = S.loc[name]; col = {"k5": "enr_k5", "m68": "enr_68"}[band]
    if name == "Cesar Chavez":  # PRC: 143 neighborhood K-8 of 443; split by ODE grade-band shares
        return 143 * r[col] / r.enr_total
    if not np.isnan(r.prc_neighborhood_2526) and r.level in ("K-5", "6-8"):
        return r.prc_neighborhood_2526
    return r[col]
es_name = {r.es_area: n for n, r in S.iterrows() if isinstance(r.es_area, str)}
ms_name = {r.ms_area: n for n, r in S.iterrows() if isinstance(r.ms_area, str)}
T_es = {a: nb(n, "k5") for a, n in es_name.items()}
T_ms = {a: nb(n, "m68") for a, n in ms_name.items()}
HSN = {"Cleveland": 1336, "Franklin": 1578, "Grant": 1809, "Ida B. Wells": 1574, "Jefferson": 377, "Lincoln": 1469, "McDaniel": 1325, "Roosevelt": 1082}
b["hs_cluster"] = b.hs_zone_cur.str.replace("Jefferson / ", "", regex=False)
jz = b.hs_zone_cur.str.startswith("Jefferson")
jshare = b[jz].groupby("hs_cluster").w_h912.sum() / b[jz].w_h912.sum()
T_hs = {k: v + (HSN["Jefferson"] * jshare.get(k, 0)) for k, v in HSN.items() if k != "Jefferson"}
# --- calibrate
def calib(area_col, wcol, T):
    raw = b.groupby(area_col)[wcol].sum()
    f = pd.Series({a: T[a] / raw[a] for a in T})
    return b[wcol] * b[area_col].map(f), f, raw
b["k5"], f_es, raw_es = calib("a", "w_k5", T_es)
b["m68"], f_ms, raw_ms = calib("ms_cur", "w_m68", T_ms)
b["h912"], f_hs, raw_hs = calib("hs_cluster", "w_h912", T_hs)
assert abs(b.k5.sum() - sum(T_es.values())) < 1e-6
# --- backtests
def table(raw, T, extra=None):
    df = pd.DataFrame({"actual": pd.Series(T), "raw": raw.reindex(list(T))})
    rate = df.actual.sum() / df.raw.sum()
    df["pred_uniform"] = df.raw * rate
    df["err_pct"] = 100 * (df.pred_uniform - df.actual) / df.actual
    df["capture_factor"] = df.actual / df.raw
    return df, rate
bt = {}
es_df, es_rate = table(raw_es, T_es)
u18_raw = b.groupby("a").w_u18.sum(); es_u18, _ = table(u18_raw, T_es)
es_df["err_pct_u18proxy"] = es_u18.err_pct
s_model = b.groupby("a").s.sum(); es_df["s_model"] = s_model
es_df["err_pct_s_model_vs_2526"] = 100 * (es_df.s_model - es_df.actual) / es_df.actual
ms_df, ms_rate = table(raw_ms, T_ms)
# cross-level: carry each block's K-5 capture factor into its 6-8 / 9-12 kids
b["xm"] = b.w_m68 * b.a.map(f_es); xm = b.groupby("ms_cur").xm.sum(); xm *= sum(T_ms.values()) / xm.sum()
ms_df["pred_from_k5_factors"] = xm; ms_df["err_pct_from_k5"] = 100 * (xm - ms_df.actual) / ms_df.actual
# alt middle line: SQ 2027-28 map puts the Rigler area in Roseway Heights instead of Beaumont
alt = b.ms_cur.where(~((b.ms_cur == "Beaumont") & (sc.sq_ms == "Roseway Heights")), "Roseway Heights")
raw_alt = b.groupby(alt).w_m68.sum(); ms_alt, _ = table(raw_alt, T_ms); ms_df["err_pct_rigler_to_roseway"] = ms_alt.err_pct
hs_df, hs_rate = table(raw_hs, T_hs)
b["xh"] = b.w_h912 * b.ms_cur.map(f_ms); xh = b.groupby("hs_cluster").xh.sum(); xh *= sum(T_hs.values()) / xh.sum()
hs_df["pred_from_68_factors"] = xh; hs_df["err_pct_from_68"] = 100 * (xh - hs_df.actual) / hs_df.actual
def mape(x): return float(np.mean(np.abs(x)))
summ = {"es": {"MAPE_uniform": mape(es_df.err_pct), "MAPE_uniform_u18proxy": mape(es_df.err_pct_u18proxy), "MAPE_s_model_vs_2526": mape(es_df.err_pct_s_model_vs_2526), "n": len(es_df), "rate": es_rate, "flag15": int((es_df.err_pct.abs() > 15).sum())},
        "ms": {"MAPE_uniform": mape(ms_df.err_pct), "MAPE_from_k5": mape(ms_df.err_pct_from_k5), "MAPE_rigler_alt": mape(ms_df.err_pct_rigler_to_roseway), "n": len(ms_df), "rate": ms_rate, "flag15": int((ms_df.err_pct.abs() > 15).sum())},
        "hs": {"MAPE_uniform": mape(hs_df.err_pct), "MAPE_from_68": mape(hs_df.err_pct_from_68), "n": len(hs_df), "rate": hs_rate, "flag15": int((hs_df.err_pct.abs() > 15).sum())}}
print(json.dumps(summ, indent=1))
for n, df in [("es", es_df), ("ms", ms_df), ("hs", hs_df)]:
    df.round(3).to_csv(D / f"work/backtest_{n}.csv")
json.dump(summ, open(D / "work/backtest_summary.json", "w"), indent=1)
# --- write blocks
out = pd.DataFrame({"idx": b.idx, "GEOID": b.g, "x": b.x, "y": b.y, "pop": b["pop"], "hu": b.hu,
    "es_cur": b.a, "es_cur_polygon": b.es_cur, "ms_cur": b.ms_cur, "hs_zone_cur": b.hs_zone_cur, "hs_cluster_cur": b.hs_cluster,
    "k5": b.k5.round(4), "m68": b.m68.round(4), "h912": b.h912.round(4), "s_model": b.s,
    "raw_k5": b.w_k5.round(4), "raw_m68": b.w_m68.round(4), "raw_h912": b.w_h912.round(4),
    "dhc_age5_9": b.a5_9, "dhc_age10_14": b.a10_14, "dhc_age15_17": b.a15_17, "dhc_under18": b.u18,
    "f_es": b.a.map(f_es).round(4), "f_ms": b.ms_cur.map(f_ms).round(4), "f_hs": b.hs_cluster.map(f_hs).round(4)})
for c in [c for c in sc.columns if c != "g"]:
    out[c] = sc[c].values
out.to_parquet(D / "blocks.parquet", index=False); out.to_csv(D / "blocks.csv", index=False)
print(out[["k5", "m68", "h912", "s_model"]].sum().round(1))
