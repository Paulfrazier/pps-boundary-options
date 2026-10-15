"""Current attendance areas (GeoJSON) + rename digitized scenario polygons."""
import pathlib, geopandas as gpd, pandas as pd
D = pathlib.Path(__file__).resolve().parent.parent
cells = gpd.read_file(D / "raw/boundaries/city_school_attendance_cells.geojson")
VINT = "City of Portland School_Boundaries FeatureServer (lastEdit 2025-11-03) = PPS 'Boundaries_All_Grades_23_24_FINAL' (board-approved SEGC lines, effective 2023-24; unchanged through 2025-26)"
K8 = {"Astor", "Beverly Cleary", "Bridger", "Cesar Chavez", "Faubion", "Laurelhurst", "Skyline", "Sunnyside", "Vernon"}
OUT = D / "boundaries"; OUT.mkdir(exist_ok=True)
es = cells.dissolve("Grade_1_Choice1_Name").reset_index()[["Grade_1_Choice1_Name", "geometry"]].rename(columns={"Grade_1_Choice1_Name": "school"})
es["config"] = es.school.map(lambda s: "K-8" if s in K8 else "K-5"); es["vintage"] = VINT
es.to_file(OUT / "current_K-5_K-8.geojson", driver="GeoJSON")
ms = cells.dissolve("Grade_6_Choice1_Name").reset_index()[["Grade_6_Choice1_Name", "geometry"]].rename(columns={"Grade_6_Choice1_Name": "school"})
ms["config"] = ms.school.map(lambda s: "K-8 (own 6-8)" if s in K8 else "6-8"); ms["vintage"] = VINT
ms.to_file(OUT / "current_6-8.geojson", driver="GeoJSON")
hs = cells.dissolve("Grade_10_Choice1_Name").reset_index()[["Grade_10_Choice1_Name", "geometry"]].rename(columns={"Grade_10_Choice1_Name": "zone"})
hs["cluster_2025_26"] = hs.zone.str.replace("Jefferson / ", "", regex=False)
hs["note"] = hs.zone.map(lambda z: "Jefferson dual-assignment zone in 2025-26 (choose Jefferson or the other HS); PPS 2027-28 Status Quo map shows it as Jefferson-only" if z.startswith("Jefferson /") else "")
hs["vintage"] = VINT
hs.to_file(OUT / "current_9-12.geojson", driver="GeoJSON")
cells.to_file(OUT / "current_cells_all_levels.geojson", driver="GeoJSON")
# rename digitized scenario polygons
SM = D / "scenario_maps"
for f in SM.glob("*.geojson"):
    if f.name.startswith(("Status_Quo_", "Scenario_")):
        scen = "status_quo" if f.name.startswith("Status") else "scenario_" + f.name.split("_")[1]
        lvl = {"K_5": "K-5", "6_8": "6-8", "9_12": "9-12"}[next(k for k in ["K_5", "6_8", "9_12"] if f.stem.endswith(k))]
        g = gpd.read_file(f); g["note"] = "digitized from PPS 2027-28 map PDF; K-8 (dashed) areas and inset (Skyline) not included as polygons - use blocks.parquet assignment"
        g.to_file(SM / f"{scen}_{lvl}.geojson", driver="GeoJSON"); f.unlink()
print(sorted(p.name for p in OUT.glob("*")), sorted(p.name for p in SM.glob("*")))
