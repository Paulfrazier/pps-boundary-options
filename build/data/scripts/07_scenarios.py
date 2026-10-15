"""scenarios.json: PPS Rightsizing Scenarios A and B (Oct 2026) at every level, from the board memo,
regional summaries, per-school Family Guides and the digitized attendance maps."""
import json, re, pathlib, numpy as np, pandas as pd
D = pathlib.Path(__file__).resolve().parent.parent
b = pd.read_parquet(D / "blocks.parquet")
dli = pd.read_csv(D / "focus_dli.csv").set_index("program")
qa = json.load(open(D / "work/georef_affine.json"))
# ---- family-guide projections (PPS's own, 2027-28..2031-32)
txt = open(D / "raw/family_guides/all_text.txt").read()
proj = {}
for blk in txt.split("######## ")[1:]:
    fname = blk.split()[0].replace(".pdf", "")
    m = re.search(r"School year 2027-28 2028-29 2029-30 2030-31 2031-32\n(.*?)\n(?:Programs, school size|Measure)", blk, re.S)
    if not m: continue
    rows = {}
    for ln in m.group(1).split("\n"):
        mm = re.match(r"^(No changes|Options A and B|Option A|Option B|Scenario A/B Note:)\s+((?:[\d,]+\s*){5})$", ln.strip())
        if mm:
            rows[mm.group(1).replace("Scenario A/B Note:", "Options A and B")] = [int(x.replace(",", "")) for x in mm.group(2).split()]
        elif ln.startswith(("Options A and B:", "Option A:", "Options A & B:")) and "clos" in ln:
            rows[ln.split(":")[0].replace("&", "and")] = "closes"
        elif re.match(r"^Options A and B \d+ School would", ln):
            rows["Options A and B"] = "closes"
    def get(k):
        for key in ([k, "Options A and B"]):
            if key in rows: return rows[key]
        return None
    proj[fname.replace("_", " ")] = {"no_change": rows.get("No changes"), "A": get("Option A"), "B": get("Option B")}
# ---- block-level flows (calibrated 2025-26 neighborhood kids; digitized scenario lines)
LV = {"K-5": ("es_cur", "k5", "es"), "6-8": ("ms_cur", "m68", "ms"), "9-12": ("hs_cluster_cur", "h912", "hs")}
def flows(scen):
    out = {}
    for lvl, (cur, kids, pre) in LV.items():
        f = b.groupby([cur, f"{scen}_{pre}"])[kids].sum().round(1)
        f = f[f > 0.5]
        moved = float(b.loc[b[cur] != b[f"{scen}_{pre}"], kids].sum())
        size = b.groupby(f"{scen}_{pre}")[kids].sum().round(1)
        out[lvl] = {"flows_current_to_scenario": [{"from": a, "to": t, "kids_2025_26": v} for (a, t), v in f.items()],
                    "neighborhood_kids_by_school_2025_26_basis": size.to_dict(),
                    "kids_changing_school_2025_26_basis": round(moved, 1),
                    "block_assignment_method_counts": b[f"{scen}_{pre}_how"].value_counts().to_dict()}
    return out
def d(p): return int(dli.loc[p, "enrollment_2025_26"])
common_conv = [
 {"school": "Beverly Cleary", "from": "K-8", "to": "K-5", "grades_6_8_to": "Beaumont", "students_6_8_2025_26": 204},
 {"school": "Laurelhurst", "from": "K-8", "to": "K-5", "grades_6_8_to": "Mt Tabor", "students_6_8_2025_26": 235},
 {"school": "Sunnyside", "from": "K-8 (neighborhood + environmental focus)", "to": "K-5 neighborhood; focus discontinued, no new lottery transfers (current lottery students may stay through grade 5)", "grades_6_8_to": "Hosford", "students_6_8_2025_26": 193, "hs_change": "Sunnyside area moves Franklin -> Cleveland"},
 {"school": "Bridger", "from": "K-8", "to": "K-5 (keeps neighborhood area and Creative Science focus)", "grades_6_8_to": "Harrison Park (or return to neighborhood middle school)", "students_6_8_2025_26": 140},
 {"school": "Cesar Chavez", "from": "K-8 (neighborhood + Spanish DLI)", "to": "K-5 regional Spanish DLI only; neighborhood K-5 -> Rosa Parks", "grades_6_8_to": "George", "students_6_8_2025_26": 170},
 {"school": "Faubion", "from": "K-8", "to": "K-5", "grades_6_8_to": "Ockley Green", "students_6_8_2025_26": 223, "note": "Bybee Lake Shelter area moves Faubion -> Astor (K-8) and Jefferson -> Roosevelt"},
 {"school": "Vernon", "from": "K-8", "to": "K-5", "grades_6_8_to": "Tubman", "students_6_8_2025_26": 195},
 {"school": "MLC", "from": "K-12 alternative", "to": "K-8 alternative (9-12 to neighborhood HS / other options; Odyssey co-locates)", "students_9_12_2025_26": 40},
]
dli_common = [
 {"program": "Spanish DLI K-5", "from": ["Beach", "James John", "Sitton"], "to": "Cesar Chavez (K-5 regional Spanish DLI hub)", "students_2025_26": {"Beach": d("DLI Spanish @ Beach"), "James John": d("DLI Spanish @ James John"), "Sitton": d("DLI Spanish @ Sitton")}},
 {"program": "Spanish DLI 6-8", "from": ["Cesar Chavez 6-8", "Ockley Green"], "to": "George (regional 6-8 Spanish DLI)", "students_2025_26": {"Cesar Chavez 6-8 (est. = 300 x 170/443)": 115, "Ockley Green": d("DLI Spanish @ Ockley Green")}},
 {"program": "Spanish DLI K-5", "from": ["Atkinson"], "to": "Lent (whole-school Spanish DLI; Lent's neighborhood area -> Kelly)", "students_2025_26": {"Atkinson": d("DLI Spanish @ Atkinson")}},
 {"program": "Spanish DLI K-5", "from": ["Scott"], "to": "Rigler (becomes regional Spanish DLI school; Rigler's non-DLI neighborhood area -> Scott)", "students_2025_26": {"Scott": d("DLI Spanish @ Scott")}},
 {"program": "Spanish DLI 6-8", "from": ["Beaumont"], "to": "Roseway Heights", "students_2025_26": {"Beaumont": d("DLI Spanish @ Beaumont")}},
 {"program": "Mandarin DLI K-5", "from": ["Clark"], "to": "Woodstock", "students_2025_26": {"Clark": d("DLI Mandarin @ Clark")}},
 {"program": "Mandarin DLI K-5", "from": ["MLK Jr"], "to": "Boise-Eliot/Humboldt", "students_2025_26": {"MLK Jr": d("DLI Mandarin @ MLK Jr")}},
 {"program": "Deaf/Hard of Hearing (regional, CRIS)", "from": ["Creston"], "to": "Glencoe", "students_2025_26": None},
 {"program": "Odyssey K-8 focus", "from": ["Odyssey (East Sylvan bldg)"], "to": "MLC site", "students_2025_26": {"Odyssey": 217}},
]
A_only_dli = [{"program": "Vietnamese DLI K-5", "from": ["Rose City Park"], "to": "Vestal (6-8 Vietnamese stays at Roseway Heights)", "students_2025_26": {"Rose City Park": d("DLI Vietnamese @ Rose City Park")}}]
closures_common = [
 {"school": "Beach", "level": "K-5", "receivers": [{"to": "Chief Joseph", "group": "neighborhood K-5 (100% of area)"}, {"to": "Cesar Chavez", "group": "Spanish DLI"}]},
 {"school": "Buckman", "level": "K-5", "receivers": [{"to": "Abernethy", "group": "neighborhood, south of Burnside / north of Hawthorne (~50%)"}, {"to": "Sunnyside", "group": "neighborhood, north of Burnside (~50%)"}], "note": "Arts focus option closes"},
 {"school": "Creston", "level": "K-5", "receivers": [{"to": "Atkinson", "group": "neighborhood K-5"}, {"to": "Glencoe", "group": "DHH program"}], "note": "Building stays as preschool (Creston Annex)"},
 {"school": "Irvington", "level": "K-5", "receivers": [{"to": "Beverly Cleary", "group": "K-5"}, {"to": "Beaumont", "group": "6-8 area (was Tubman)"}]},
 {"school": "James John", "level": "K-5", "receivers": [{"to": "Sitton", "group": "neighborhood K-5"}, {"to": "Cesar Chavez", "group": "Spanish DLI"}]},
 {"school": "Maplewood", "level": "K-5", "receivers": [{"to": "Hayhurst", "share": 0.7}, {"to": "Rieke", "share": 0.3}], "note": "6-8 area Jackson -> Gray"},
 {"school": "Marysville", "level": "K-5", "receivers": [{"to": "Arleta", "group": "pre-SEGC Marysville area"}, {"to": "Kelly", "group": "pre-SEGC Lent non-DLI area"}]},
 {"school": "Peninsula", "level": "K-5", "receivers": [{"to": "Rosa Parks", "group": "100% of area"}], "note": "6-8 area Ockley Green -> George"},
 {"school": "Sabin", "level": "K-5", "receivers": [{"to": "MLK Jr", "group": "100% of area"}]},
 {"school": "Woodmere", "level": "K-5", "receivers": [{"to": "Whitman", "group": "100% of area"}], "note": "combined area -> Lane/Brentwood 6-8, Franklin 9-12"},
 {"school": "Sellwood", "level": "6-8", "receivers": [{"to": "Hosford", "group": "Llewellyn area"}, {"to": "Lane (Brentwood)", "group": "Duniway and Lewis areas"}], "note": "closes 2028"},
]
closures_A_only = [
 {"school": "Lewis", "level": "K-5", "receivers": [{"to": "Duniway", "group": "100% of area"}]},
 {"school": "Rose City Park", "level": "K-5", "receivers": [{"to": "Scott", "group": "neighborhood K-5 (100%)"}, {"to": "Vestal", "group": "Vietnamese DLI"}]},
 {"school": "Stephenson", "level": "K-5", "receivers": [{"to": "Markham", "share": 0.7}, {"to": "Capitol Hill", "share": 0.3}]},
]
ms_changes_common = [
 "Beaumont: + Beverly Cleary 6-8 (incl. former Irvington area, which leaves Tubman); Spanish DLI -> Roseway Heights",
 "Mt Tabor: + Laurelhurst 6-8",
 "Hosford: + Sunnyside 6-8 + Llewellyn area (from Sellwood) [+ Duniway-west-of-McLoughlin area in A]",
 "Lane (Brentwood): + Duniway and Lewis areas (from Sellwood); Kelly neighborhood 6-8 -> Harrison Park; Russian DLI stays",
 "Harrison Park: + Lent and Kelly areas; Atkinson area -> Kellogg; Bridger 6-8 (from K-8); Mandarin DLI stays",
 "Kellogg: + Atkinson and Creston areas; Lent area -> Harrison Park; all SE Spanish DLI 6-8 stays at Kellogg",
 "Tubman: + Vernon 6-8; Irvington area -> Beaumont",
 "Ockley Green: + Faubion 6-8; Peninsula area -> George; Spanish DLI -> George; all Ockley Green feeds Jefferson",
 "George: + Cesar Chavez 6-8, Peninsula area, Spanish DLI from Ockley Green and Chavez (regional 6-8 Spanish DLI)",
 "Gray: + Maplewood area (from Jackson); Jackson loses Maplewood area",
 "Roseway Heights: + Spanish DLI from Beaumont; keeps Vietnamese DLI",
 "Sellwood: closes (2028)",
]
hs_changes_common = [
 "Cleveland: + Sunnyside area (from Franklin); remaining Woodmere/Whitman pieces -> Franklin",
 "Franklin: + expanded Whitman area (former Whitman+Woodmere); Sunnyside area -> Cleveland; small Vestal piece -> McDaniel",
 "McDaniel: + small part of Vestal area (from Franklin)",
 "Lincoln: Skyline area -> Roosevelt",
 "Roosevelt: + Skyline area; + Bybee Lake Shelter area (from Jefferson)",
 "Jefferson: own neighborhood boundary already phasing in under Status Quo (dual assignment ending); minor Bybee Lake Shelter change",
 "MLC 9-12 program closes; students to neighborhood HS (not counted as a closure)",
 "Grant, Ida B. Wells, Benson: no change",
]
def side(scen):
    S = {"closures": closures_common + (closures_A_only if scen == "A" else []),
         "k8_conversions_and_grade_changes": common_conv,
         "dli_and_program_moves": dli_common + (A_only_dli if scen == "A" else []),
         "focus_option_changes": ["Sunnyside environmental focus discontinued", "Buckman arts focus closes with the building",
                                  "Odyssey moves to MLC site (East Sylvan building closes)", "MLC becomes K-8", "Winterhaven, da Vinci, ACCESS, Richmond, Benson unchanged"],
         "middle_school_changes": ms_changes_common, "high_school_changes": hs_changes_common,
         "k8_remaining": ["Astor (gains Bybee Lake Shelter area)", "Skyline (HS pathway Lincoln -> Roosevelt)"],
         "block_level": flows(scen)}
    if scen == "B":
        S["scenario_B_differences"] = ["Lewis stays open and receives part of Whitman's area (Lewis/Duniway still go to Lane/Brentwood for 6-8)",
            "Rose City Park stays open with its area and Vietnamese DLI (Scott does not receive RCP area; Vietnamese DLI not moved)",
            "Stephenson stays open with no change", "Duniway's area west of McLoughlin stays with Duniway (moves to Llewellyn only in A)"]
    return S
out = {"source": {
    "board_memo": "PPS 'Rightsizing Update: Scenario Release' memo, Oct 5 2026 (meub/pps-data data/raw/pps_rightsizing_board_2026-10-06/)",
    "regional_summaries": "PPS Regional summaries (4), updated Oct 3-4 2026",
    "family_guides": "Per-school Family Guides via https://www.pps.net/about/portland-public-schools-information/rightsize/how-could-your-school-be-impacted (Awesome Table -> Google Drive PDFs), saved in raw/family_guides/",
    "maps": "Attendance boundary map PDFs (Status Quo/A/B x K-5, 6-8, 9-12; School Year 2027-28) from BoardBook org 915 files 14505795-14505805; Scenario A 6-8 also from the user's Downloads. Digitized from vector paths (raw/scenario_maps/)",
    "scenario_page": "https://www.pps.net/about/portland-public-schools-information/rightsize/scenarios"},
  "thresholds": {"k5": 360, "k8_and_middle": 500, "high": 1100, "space_use_goal": "70-100% of building capacity"},
  "renames": {"Lee": "Sunrise", "Lane Middle School": "Brentwood Middle School", "Gray": "Robert Gray"},
  "digitization_qa": {"georeference": "affine PDF->EPSG:2913 fitted on Status-Quo 6-8 lines vs current lines (ICP)", "median_line_offset_ft": round(qa["median_resid_ft"]), "p90_line_offset_ft": round(qa["p90_resid_ft"]),
                      "status_quo_k5_block_agreement_with_current": "99.9% of digitized blocks", "status_quo_6_8_block_agreement": "98.7% (all 100 disagreements = Rigler K-5 area drawn in Roseway Heights on the 2027-28 SQ map vs Beaumont in the City/PPS 2023-24 layer)",
                      "status_quo_9_12": "matches current except dual-assignment zones, which the 2027-28 map shows as Jefferson-only"},
  "pps_projections_2027_28_to_2031_32": proj,
  "status_quo_2027_28": {"block_level": flows("sq"), "note": "PPS's own 'No Change' map for 2027-28: same lines as today except Jefferson HS dual-assignment zones become Jefferson (phase-in) and the Rigler K-5 area is shown feeding Roseway Heights."},
  "scenarios": {"A": side("A"), "B": side("B")}}
json.dump(out, open(D / "scenarios.json", "w"), indent=1, default=float)
for s_ in ["A", "B"]:
    print(s_, {l: v["kids_changing_school_2025_26_basis"] for l, v in out["scenarios"][s_]["block_level"].items()})
print("projections parsed:", len(proj), sum(1 for v in proj.values() if v["A"] is None))
print([k for k, v in proj.items() if v["A"] is None or v["B"] is None])
