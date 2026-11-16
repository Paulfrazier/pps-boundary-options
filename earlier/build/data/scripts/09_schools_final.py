"""schools.csv (final)."""
import json, pathlib, numpy as np, pandas as pd
D = pathlib.Path(__file__).resolve().parent.parent
s = pd.read_csv(D / "work/schools_base.csv", dtype={"nces_id": str})
b = pd.read_parquet(D / "blocks.parquet")
sj = json.load(open(D / "scenarios.json")); proj = sj["pps_projections_2027_28_to_2031_32"]
GUIDE = {"Boise-Eliot/Humboldt": "Boise-Eliot Humboldt", "Bridger": "Bridger Creative Science", "MLK Jr": "Dr  Martin Luther King Jr ",
         "Lee (Sunrise)": "Sunrise", "Lane (Brentwood)": "Brentwood", "Tubman": "Harriet Tubman", "Ida B. Wells": "Ida B Wells",
         "Mt Tabor": "Mt  Tabor", "MLC": "Metropolitan Learning Center"}
def pj(n, k):
    v = proj.get(GUIDE.get(n, n), {}).get(k)
    return v if isinstance(v, str) else (v[-1] if v else np.nan)
s["pps_proj_2031_32_no_change"] = [pj(n, "no_change") for n in s.name]
s["pps_proj_2031_32_A"] = [pj(n, "A") for n in s.name]
s["pps_proj_2031_32_B"] = [pj(n, "B") for n in s.name]
# neighborhood 2025-26 (= calibration targets) and model block sums
s["nbhd_k5_2526"] = s.es_area.map(b.groupby("es_cur").k5.sum()).round(1)
s["nbhd_68_2526"] = s.ms_area.map(b.groupby("ms_cur").m68.sum()).round(1)
s["nbhd_912_2526_cluster"] = s.hs_area.map(b.groupby("hs_cluster_cur").h912.sum()).round(1)
s.loc[s.name == "Jefferson", "nbhd_912_2526_cluster"] = 377  # Jefferson draws from dual zones; included in Grant/McDaniel/Roosevelt cluster sums
s["has_current_attendance_area"] = s.es_area.notna() | s.ms_area.notna() | s.hs_area.notna()
s["whole_school_dli"] = s.name.isin(["Lent", "Rigler", "Richmond"])
s["dli_languages"] = s.dli_languages.fillna("")
s.loc[s.name == "Woodstock", "dli_languages"] = "Mandarin"; s.loc[s.name == "Richmond", "dli_languages"] = "Japanese"
s.loc[s.name == "Richmond", "prc_dli_2526"] = 512
fd = pd.read_csv(D / "focus_dli.csv")
s["dli_strands_detail_2526"] = [";".join(f"{r.language}:{r.enrollment_2025_26}" for r in fd[(fd.host_building_2025_26 == n) & (fd.kind == "DLI")].itertuples()) for n in s.name]
G = ["g_K"] + [f"g_{i}" for i in range(1, 13)]
cols = ["name", "level", "grades", "focus_option", "has_current_attendance_area", "es_area", "ms_area", "hs_area", "ode_id", "nces_id", "ode_name", "lat", "lon",
        "capacity_functional_2021", "capacity_functional_model", "utilization_pct_2526_meub", "seismic_status", "is_urm_building",
        "enr_total", "enr_k5", "enr_68", "enr_912"] + G + ["prc_total_2526", "prc_neighborhood_2526", "prc_dli_2526", "prc_pisa_2526", "dli_languages", "dli_strands_detail_2526", "whole_school_dli",
        "nbhd_k5_2526", "nbhd_68_2526", "nbhd_912_2526_cluster", "forecast_2031_32_prc", "pps_proj_2031_32_no_change", "pps_proj_2031_32_A", "pps_proj_2031_32_B", "notes"]
s[cols].rename(columns={"g_K": "enr_gK", **{f"g_{i}": f"enr_g{i}" for i in range(1, 13)}}).to_csv(D / "schools.csv", index=False)
print(s[["name", "pps_proj_2031_32_no_change", "pps_proj_2031_32_A", "pps_proj_2031_32_B", "nbhd_k5_2526", "nbhd_68_2526"]].head(12).to_string())
print(s.pps_proj_2031_32_A.isna().sum(), s.name[s.pps_proj_2031_32_A.isna()].tolist())
