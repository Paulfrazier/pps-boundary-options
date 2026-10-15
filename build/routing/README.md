# PPS routing (local OSRM)

Files
- `school_points.csv`: 86 CCD 2024 PPS schools (name, ncessch, level, lat, lon, grades_ccd, charter, snap distances). Includes charters (Emerson, Kairos, Le Monde, Arthur Academy, Portland Village), alternative/focus schools, MLC; filter by `charter`/`level` as needed. CCD has no 2025 file yet; 2024 is the latest. Closed or merged schools not in 2024 are absent.
- `walk_miles.parquet`, `bike_miles.parquet`: long format, ALL pairs (9,295 blocks x 86 schools = 799,370 rows). Columns: block_idx (index in BL), geoid, school_idx (row in school_points.csv), ncessch, `<mode>_miles`, `<mode>_seconds`. Pivot: `df.pivot(index='block_idx', columns='school_idx', values='walk_miles')`.
- `validation.md`, `validation_pairs.csv`, `build_matrices.py`, `validate.py`, `run_build.sh`.
- `foot/`, `bike/`: built OSRM graphs (MLD). `osm/portland.osm.pbf`: extract (lon -123.00..-122.40, lat 45.36..45.75).

Runtime: Docker via Colima (no Docker Desktop installed).
```
colima start --cpu 4 --memory 4 --disk 20
cd build/routing
docker run -d --name osrm-foot --restart unless-stopped -p 5001:5000 -v "$PWD/foot:/data" osrm/osrm-backend osrm-routed --algorithm mld --max-table-size 100000 /data/map.osrm
docker run -d --name osrm-bike --restart unless-stopped -p 5002:5000 -v "$PWD/bike:/data" osrm/osrm-backend osrm-routed --algorithm mld --max-table-size 100000 /data/map.osrm
```
If containers already exist: `docker start osrm-foot osrm-bike`. Stop: `docker stop osrm-foot osrm-bike; colima stop`.

Ports: foot = 5001, bicycle = 5002 (lon,lat order).
```
curl "localhost:5001/route/v1/foot/-122.6365,45.5171;-122.6514,45.5058?overview=false"
curl "localhost:5002/table/v1/bicycle/LON,LAT;LON,LAT?annotations=duration,distance"
```
Table distances are metres (divide by 1609.344 for miles).

Rebuild graphs: copy osm/portland.osm.pbf to foot/map.osm.pbf and bike/map.osm.pbf, then `bash run_build.sh foot foot` and `bash run_build.sh bicycle bike`.
