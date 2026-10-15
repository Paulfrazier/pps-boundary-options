# Routing validation

Router: OSRM MLD, foot and bicycle profiles, Geofabrik Oregon extract (2026-10-11) clipped to lon -123.00..-122.40, lat 45.36..45.75. Walk speed is the OSRM default (5 km/h).

## Walk vs existing BL[i].w (public OSRM foot router)
Compared every (block, elementary) pair in BL[i].w: 65,065 pairs, 53 schools, all matched to a CCD point within 300 m.

| Metric | Value |
|---|---|
| Pearson r | 0.998 |
| Median abs diff | 0.022 mi |
| Mean abs diff | 0.046 mi |
| 95th percentile abs diff | 0.169 mi |
| 99th percentile abs diff | 0.310 mi |
| Median signed diff (new - old) | -0.018 mi (ours slightly shorter; ratio 0.989) |
| Pairs differing by > 0.25 mi | 1,220 (1.9%); > 0.5 mi: 148 |

Full pair list: `validation_pairs.csv`.

### Outliers
- Block 3813 (410510043001102, Linnton/Forest Park edge, -122.7336, 45.5516) and block 5262 (410510043001107): old values 2.0-3.3 mi to Beach/Astor/Cesar Chavez; ours 6-8 mi. Our route goes via Hwy 30 / St. Johns Bridge (the only real river/rail crossing). The old value is about the straight-line distance, so the public router likely snapped to a path or the wrong side of the rail/river. Ours is the defensible one.
- Block 3668 (410510072023043, Columbia Slough / Smith-Bybee, -122.7034, 45.6035): old 1.9-3.1 mi to Astor/James John/Sitton/Rosa Parks, ours 4.9-6.6 mi. Route goes around the slough and rail yards.
- Block 2813 (410510043001086, -122.7616, 45.5702, Forest Park): ours is 1.2-1.4 mi SHORTER than old (e.g. Astor 5.2 vs 6.5). Likely uses Forest Park trails (Leif Erikson / firelanes) that the old router either lacked or snapped differently. Population there is near zero.
- Blocks 9203, 9159, 9056, 6345: shorter by about 1 mi to several schools; scattered, single-block differences, probably snapping/path differences.
- An earlier build clipped at lon -122.90 produced 7 mi errors for 9 blocks west of that line (Skyline area); the final extract is widened to -123.00 and those are gone.

## Hard-edge spot checks (foot router)
Five north-of-I-84 blocks routed to schools south of the freeway (I84 line from pps-model.json):

| Block | To | Route mi | Straight mi | I-84 crossing at |
|---|---|---|---|---|
| 4535 | Abernethy | 2.46 | 2.18 | NE 28th Ave |
| 4576 | Buckman | 1.84 | 1.63 | NE Sandy Blvd |
| 6498 | Glencoe | 2.23 | 1.66 | NE Campesinos Blvd, NE 47th Ave, Banfield Expressway Path (the polyline is approximate; all are real overpasses/path) |
| 7736 | Grout | 3.43 | 2.93 | NE 21st Ave |
| 357 | Sunnyside | 1.89 | 1.39 | NE 53rd Ave |

All crossings are on named bridges/overpasses. Willamette: Buckman to Chapman uses Burnside Bridge, Abernethy to Chapman uses Hawthorne Bridge, Woodstock to Ainsworth uses Ross Island Bridge; Forest Park to Astor uses St. Johns Bridge. Rail lines and freeways are barriers in OSM because only mapped crossings connect; the detour ratios above (1.1-1.35x) are consistent with that. Rail was not exhaustively audited.

## Other checks
- No null pairs in either matrix (799,370 pairs each); every block routes to every school.
- Bike/walk median distance ratio 1.02 (bike can use roads walkers cannot and vice versa).
- School snap distances (school point to nearest routable way): median 30 m, max 70 m (Benson); stored as `walk_snap_m` / `bike_snap_m` in school_points.csv. Snapped to the street network, not building entrances.
- Block centroid snap is not stored; centroids inside parks or industrial areas may snap a few hundred metres.
