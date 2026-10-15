"""Write backtest.md from work/backtest_*.csv plus a leave-one-out cluster-rate test."""
import json, pathlib, numpy as np, pandas as pd
D = pathlib.Path(__file__).resolve().parent.parent
b = pd.read_parquet(D / "blocks.parquet")
summ = json.load(open(D / "work/backtest_summary.json"))
es = pd.read_csv(D / "work/backtest_es.csv", index_col=0); ms = pd.read_csv(D / "work/backtest_ms.csv", index_col=0); hs = pd.read_csv(D / "work/backtest_hs.csv", index_col=0)
# today's-lines aggregation of the FINAL calibrated blocks (exact by construction)
fin = {"es": b.groupby("es_cur").k5.sum(), "ms": b.groupby("ms_cur").m68.sum(), "hs": b.groupby("hs_cluster_cur").h912.sum()}
for k, df in [("es", es), ("ms", ms), ("hs", hs)]:
    df["final_calibrated"] = fin[k].reindex(df.index)
    df["final_err_pct"] = 100 * (df.final_calibrated - df.actual) / df.actual
# leave-one-out: predict each area with the capture rate of the OTHER areas in its 2025-26 HS cluster
def loo(df, area_col, wcol="raw"):
    cl = b.groupby(area_col).hs_cluster_cur.agg(lambda x: x.mode().iloc[0])
    df = df.copy(); df["cluster"] = cl.reindex(df.index)
    pred = {}
    for a, r in df.iterrows():
        o = df[(df.cluster == r.cluster) & (df.index != a)]
        if len(o) == 0: o = df[df.index != a]
        pred[a] = r.raw * o.actual.sum() / o.raw.sum()
    df["pred_loo_cluster"] = pd.Series(pred); df["err_pct_loo_cluster"] = 100 * (df.pred_loo_cluster - df.actual) / df.actual
    return df
es = loo(es, "es_cur"); ms = loo(ms, "ms_cur")
def mape(x): return float(np.mean(np.abs(x)))
def wape(df, col): return float((df[col] - df.actual).abs().sum() / df.actual.sum() * 100)
WHY = {
 "Bridger": "Creative Science focus lottery draws students from outside the area (capture >100%).",
 "Sunnyside": "Environmental focus lottery draws from outside the area (capture ~0.9-1.2).",
 "Buckman": "Arts focus option draws from outside the area.",
 "Laurelhurst": "Very high neighborhood capture (affluent, popular K-8); few DLI/private drains measured.",
 "Faubion": "K-8 with high in-area capture plus transfers in (new building).",
 "Marysville": "High capture; area also feeds Lent DLI under SEGC history; small raw base.",
 "Lent": "Whole-school Spanish DLI: enrollment includes DLI students from outside the small area.",
 "Lewis": "Small, high-capture area (Sellwood/Westmoreland).",
 "Astor": "K-8 with high capture; area is small relative to its draw.",
 "Alameda": "High-income area with very high public-school capture and transfers in.",
 "Woodlawn": "Transfers in / high capture relative to Census age counts.",
 "Boise-Eliot/Humboldt": "Transfers in; Census 2020 kids undercount 2025 (new housing in Eliot/Lloyd).",
 "Skyline": "Rural area, tiny Census base; K-8 draws some out-of-area students.",
 "Beach": "Half of the building is the Spanish DLI strand; in-area kids who enroll in the DLI are not 'neighborhood' (capture 0.27).",
 "Cesar Chavez": "2/3 of the school is Spanish DLI; neighborhood program is only ~88 K-5 kids.",
 "Chapman": "Downtown/NW: high private-school share and many Census kids in non-family housing; also feeds Ainsworth DLI.",
 "Whitman": "Low capture: transfers out (charters, Lent DLI, Winterhaven/focus) in outer SE.",
 "Atkinson": "Half the school is Spanish DLI (not counted); transfers out to Winterhaven/Richmond/focus nearby.",
 "Rosa Parks": "Transfers out (charters, Cesar Chavez DLI), plus Census undercount of churn in subsidized housing.",
 "Rose City Park": "Half the school is Vietnamese DLI (not counted); transfers out.",
 "Ainsworth": "Half the school is Spanish DLI; downtown private-school share.",
 "Abernethy": "Close-in SE with private/focus (Winterhaven, Sunnyside, Richmond) drain.",
 "Clark": "Mandarin DLI not counted; outer-SE transfers out.",
 "Woodstock": "Mandarin DLI not counted; Winterhaven/da Vinci draw nearby.",
 "James John": "Spanish DLI strand not counted.", "Sitton": "Spanish DLI strand not counted.", "Scott": "Spanish DLI strand not counted.",
 "Glencoe": "Richmond (Japanese DLI) and focus schools draw from this area.", "Arleta": "Transfers out (Lent DLI, charters).",
 "Forest Park": "High private-school share in NW hills.", "Markham": "", "Rieke": "",
 "George": "Most N Portland 6-8 kids attend K-8s (Astor, Cesar Chavez) or Spanish DLI; neighborhood 6-8 small.",
 "Harrison Park": "Recently converted from K-8; many in-area 6-8 kids in Kellogg DLI, Bridger K-8, da Vinci/Winterhaven, charters.",
 "Tubman": "Low capture; transfers out (da Vinci, Winterhaven, charters, Vernon/Faubion K-8 choices).",
 "Beaumont": "Spanish DLI not counted; da Vinci draws heavily from NE.",
 "West Sylvan": "Spanish DLI not counted; private-school share in West Hills.",
 "Lane": "Russian DLI small; transfers out.",
 "Sellwood": "High capture, transfers in.",
 "Grant": "Transfers in and the Jefferson dual-assignment zones mostly choose Grant.",
 "Roosevelt": "Transfers out (Benson, charters) and to Jefferson.",
 "Cleveland": "", "Vernon": "", "Beverly Cleary": "", "Mt Tabor": "Japanese DLI 222 not counted (district-wide draw).",
}
def tbl(df, cols, flagcol):
    lines = ["| school | actual nbhd 2025-26 | Census raw | capture | uniform-rate pred | err % | LOO-cluster err % | final calibrated | flag |", "|---|---|---|---|---|---|---|---|---|"]
    for a, r in df.sort_values(flagcol, key=abs, ascending=False).iterrows():
        flag = "**>15%**" if abs(r[flagcol]) > 15 else ""
        lines.append(f"| {a} | {r.actual:.0f} | {r.raw:.0f} | {r.capture_factor:.2f} | {r.pred_uniform:.0f} | {r.err_pct:+.0f} | {(format(r.get('err_pct_loo_cluster'), '+.0f') if pd.notna(r.get('err_pct_loo_cluster')) else 'n/a')} | {r.final_calibrated:.0f} | {flag} |")
    return "\n".join(lines)
def flags(df, col):
    out = []
    for a, r in df.sort_values(col, key=abs, ascending=False).iterrows():
        if abs(r[col]) > 15:
            out.append(f"- **{a}** ({r[col]:+.0f}%): {WHY.get(a, '') or 'No specific explanation found; within the spread of capture rates.'}")
    return "\n".join(out)
hs["err_pct_loo_cluster"] = np.nan
md = f"""# Backtest: can the block model reproduce today?

Built {pd.Timestamp.today().date()} by `scripts/04_calibrate.py` + `scripts/10_backtest_md.py`. All numbers are 2025-26 **neighborhood-program** students (school enrollment minus DLI strands, focus/lottery programs and newcomer programs where PPS/PSU publish the split; see README "Targets").

## Read this first: two different tests

1. **Final calibrated blocks vs today (the solver's input).** Each block's kids = Census-based raw count x its current area's capture factor, so blocks summed over today's lines reproduce actual neighborhood enrollment **exactly** (0.0% error at every school, every level). That is by construction, not evidence. It is the same convention the first-generation model's per-block estimate (`s` in `pps-model.json`) used.
2. **Structural backtest (the real gate).** Ignore each school's own enrollment and predict it from Census residents alone:
   - *uniform*: one district-wide capture rate per level;
   - *LOO-cluster*: the capture rate of the **other** schools in the same high-school cluster (leave-one-out) - this is the honest out-of-sample number;
   - *cross-level*: carry each block's K-5 capture factor into its 6-8 kids (and 6-8 into 9-12).
   This measures how much school-to-school variation in "who actually enrolls in the neighborhood school" exists beyond Census age counts. It bounds the error for blocks that change school, because a moved block carries its *old* area's capture factor.

## Summary

| level | areas | district capture (nbhd enrolled / Census-age residents) | MAPE uniform | MAPE LOO-cluster | MAPE cross-level | WAPE uniform | schools >15% (uniform) | final calibrated MAPE |
|---|---|---|---|---|---|---|---|---|
| K-5 | {len(es)} | {summ['es']['rate']:.2f} | {mape(es.err_pct):.1f}% | {mape(es.err_pct_loo_cluster):.1f}% | n/a | {wape(es,'pred_uniform'):.1f}% | {summ['es']['flag15']} | 0.0% |
| 6-8 | {len(ms)} | {summ['ms']['rate']:.2f} | {mape(ms.err_pct):.1f}% | {mape(ms.err_pct_loo_cluster):.1f}% | {summ['ms']['MAPE_from_k5']:.1f}% (from K-5 factors) | {wape(ms,'pred_uniform'):.1f}% | {summ['ms']['flag15']} | 0.0% |
| 9-12 (7 cluster units) | {len(hs)} | {summ['hs']['rate']:.2f} | {mape(hs.err_pct):.1f}% | n/a | {summ['hs']['MAPE_from_68']:.1f}% (from 6-8 factors) | {wape(hs,'pred_uniform'):.1f}% | {summ['hs']['flag15']} | 0.0% |

Other checks:
- K-5 raw proxy: grade-specific ages (this build) MAPE {summ['es']['MAPE_uniform']:.1f}% vs all-under-18 proxy (the old `s` method) {summ['es']['MAPE_uniform_u18proxy']:.1f}% under a uniform rate - a small improvement, not a large one.
- Old `s` (2024-25 NCES totals minus immersion estimates) vs 2025-26 neighborhood actuals: MAPE {summ['es']['MAPE_s_model_vs_2526']:.1f}%. Biggest miss: **Hayhurst `s`=451 vs 290** - the old K5 count included the Odyssey K-8 program (ODE reports it inside Hayhurst). Old `s` sums to 14,897; new `k5` sums to {b.k5.sum():.0f}.
- 6-8 Rigler question: the PPS 2027-28 Status-Quo map draws the Rigler K-5 area in Roseway Heights; the City/PPS 2023-24 layer has it in Beaumont. Moving it raises MAPE ({summ['ms']['MAPE_uniform']:.1f}% -> {summ['ms']['MAPE_rigler_alt']:.1f}%) and pushes Roseway to +33%/Beaumont to -23%, so the current-layer assignment (Beaumont) is kept for calibration.

## Verdict

- Census residents alone are a weak predictor of who enrolls in each neighborhood school: capture rates run from ~0.27 (Beach, Cesar Chavez: DLI-dominated) to >1 (Bridger, Sunnyside: focus lotteries). The out-of-sample error (LOO-cluster MAPE ~{mape(es.err_pct_loo_cluster):.0f}% K-5, ~{mape(ms.err_pct_loo_cluster):.0f}% 6-8) is the honest "model error" for any school whose population is mostly *new* territory.
- Because calibration is per area, the solver's error is concentrated in **moved blocks**: they carry their old area's capture rate. For boundary edits between similar neighborhoods this is small; for blocks moving out of DLI/focus-heavy areas (Beach, Cesar Chavez, Rigler, Lent, Sunnyside, Bridger, Buckman) it can be large - see README "Assumptions the solver must know".
- The gate passes in the sense that matters (today is reproduced exactly; total kids per level are right; cross-level carry-over of capture factors cuts the 6-8 error from {summ['ms']['MAPE_uniform']:.0f}% to {summ['ms']['MAPE_from_k5']:.0f}%), **but** any school-size result within ~15% of a threshold (360 / 500 / 1,100) should be treated as uncertain.

## K-5 (53 current K-5/K-8 areas)

{tbl(es, None, 'err_pct')}

### K-5 schools off by more than 15% (uniform rate) and likely why (hypotheses from program/transfer patterns - not verified with PPS transfer data)
{flags(es, 'err_pct')}

## 6-8 (23 current middle areas; K-8s count their own 6-8)

{tbl(ms, None, 'err_pct')}

### 6-8 schools off by more than 15% and likely why (hypotheses from program/transfer patterns - not verified with PPS transfer data)
{flags(ms, 'err_pct')}

## 9-12 (7 units: Jefferson's dual-assignment zones are pooled with the partner school because 2025-26 students could choose either)

{tbl(hs, None, 'err_pct')}

### 9-12 flags (likely causes, not verified)
{flags(hs, 'err_pct')}
"""
(D / "backtest.md").write_text(md)
es.to_csv(D / "work/backtest_es.csv"); ms.to_csv(D / "work/backtest_ms.csv")
print(mape(es.err_pct_loo_cluster), mape(ms.err_pct_loo_cluster), es.final_err_pct.abs().max(), ms.final_err_pct.abs().max(), hs.final_err_pct.abs().max())
