---
title: "PPS School Profiles 2025-26 (Power BI dashboard), per-school text snapshots"
source_url: "https://www.pps.net/departments/dataaccountability/data-and-accountability/data-strategy-and-insights/internal-school-profiles"
powerbi_url: "https://app.powerbi.com/view?r=eyJrIjoiOWZlNmJhYjQtYzc5YS00MzY5LTk3ODYtMWYxMmQ0YWMyMjIxIiwidCI6ImQwOGRmYzk0LWEyM2MtNDRlNC04YjhkLTRhYmM0MGRkYTlhZSIsImMiOjZ9&pageName=52fe3db4b36f375bbf95"
captured_by: "PPS DLI & Rightsizing explorer, scrape_school_profiles.mjs (headless Chrome), commit d9d683eb31370d40a1d9659e4b212e3eb93fb9bb"
retrieved: "2026-10-09 (by pps-dli-explorer); copied into this archive 2026-10-12"
provenance: "PPS-original data (PPS Power BI report), captured second-hand: we did not take these snapshots ourselves"
---

# PPS School Profiles 2025-26: text snapshots

One `.txt` per school (83 files): the visible text of PPS's School Profiles Power BI report with that school selected. Each file begins with `SELECTED`, `RETRIEVED` (UTC time) and `SOURCE` (the Power BI URL).

**What we use:** "Functional Capacity" (current building capacity, 2025-26) for model v2 fix 4. Parsed by `build/data/v2/build_v2_inputs.py` into `build/data/v2/capacity_2025_26.csv`.

**Provenance label: PPS-original, captured second-hand.** The numbers are PPS's own (PPS's dashboard), but the snapshots were taken by a parent-built project (pps-dli-explorer), not by us.

**Checks against PPS-original text we hold ourselves** (PPS Family Guides, Oct 2026, p. 3, `build/pps-texts/family-guide-*.md`):

| School | Profile functional capacity | Family Guide wording | Match |
|---|---|---|---|
| Abernethy | 441 | "Abernethy can hold 441 students" | yes |
| Arleta | 652.65 | "Arleta has room for 653 students" | yes |
| Whitman | 416.1 | "Whitman has room for 416 students" | yes |
| Hayhurst | 525 | "Hayhurst has room for over 500 students" | yes |
| Boise-Eliot/Humboldt | 585.9 | "BEH has room for up to 632 students" | no (guide is 8% higher; unexplained) |

Sanity check (PPS staff, TLE committee, Sept 8 2026, https://youtu.be/S-pk57P6f_o?t=3849): "our current K-5s all have the capacity for at least 360 ... all of our middle schools have functional capacities of at least 500." See `capacity_2025_26.csv` for the result of this check.
