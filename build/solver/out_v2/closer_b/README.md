# Closer schools in Scenario B (K-5)

Data and scripts behind `pages/closer-b.html`.

Question: with Scenario B's ten closures held fixed, how many K-5 kids are sent past a closer open school, and does that have to be so?

- **PPS Scenario B** = `out_v2/scenario_B` (our digitized copy of PPS's B maps).
- **Walk-first lines** = run `bscale_B_ref`: Scenario B's closures and immersion moves, K-5 lines re-solved for walking distance and size, held to keep at least as many schools at 360 each year as B does. The solve stopped at a feasible plan (K-5 gap 31%), so a better plan may exist. Its config, scorecard and K-5 assignment are copied here (`bscale_B_ref_*`).
- "Past a closer school" uses `metrics.py` unchanged: assigned walk at least 0.25 mi longer than the nearest open school reachable without a new I-84 or Willamette crossing; 2031-32 projected kids (model v2).

Rebuild (from `build/solver/out_v2/closer_b`, with the project venv):

    python blocks_b.py blocks_b.json      # per-block walks, both plans (not shipped; ~1 MB)
    python agg.py blocks_b.json vizdata.json
    python build_site_page.py             # writes pages/closer-b.html

`blocks_b.py` reads the walk-first assignment from `bscale_B_ref_assign_K-5.parquet` here when the run's staging folder is not present.
