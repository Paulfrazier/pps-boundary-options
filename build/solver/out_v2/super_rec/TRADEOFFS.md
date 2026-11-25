# Superintendent's recommendation (2026-11-12), as written: model v2 read

Built by build_super_rec.py from PPS's traced Scenario A lines plus the memo's listed changes (pp. 25-27). Source:
build/pps-texts/superintendent-recommendation-2026-11-12.md. Scored, not solved. Promoted 2026-11-14 as `out_v2/super_rec` (the reference plan for the new site).

## Calibration against the memo (2031-32 unless noted)
| | Model | PPS memo |
|---|---|---|
| Stephenson | 260 | 261 (p. 43) |
| James John / Maplewood / Sitton / Sunrise (= Lee) | 233 / 248 / 208 / 254 | all "<260" (p. 42) |
| MLK Jr with all of Sabin | 574 of 584 seats | 572 projected Fall 2027 (p. 26) |
| K-5 at 360+ | 17 of 38 neighborhood + 4 DLI hubs = 21 of 42 | 50% of 42 (p. 42) |
| Middle at 500+ | 6 of 14 | 47% of 15 (p. 42) |

## What it leaves short (K-5 under 360, 2031-32)
Sitton 208, James John 233, Maplewood 248, Lee/Sunrise 254, Forest Park 258, Stephenson 260, Clark 262, Hayhurst 266*,
Grout 280, Bridger 285, Vernon 289, Woodlawn 290, Glencoe 301, Boise-Eliot/Humboldt 310, Rieke 313, Capitol Hill 320,
Laurelhurst 323, Chapman 336, Markham 345, Abernethy 355. Over building: Whitman 447 / 416 seats, George 673 / 623.
Middle under 500: Sellwood 351, Lane (Brentwood) 357*, Jackson 409, Tubman 423, Beaumont 464, Gray 472, Hosford 495.
(*) model assumptions: Hayhurst gets back A's piece given to Rieke. Kelly's 6-8 stays at Brentwood (corrected 2026-11-25: Scenario A's
Kelly -> Harrison Park move went with Brentwood taking Duniway/Lewis from a closing Sellwood; the memo lists neither for the rec, and its
2027-28 Brentwood 422 / Harrison Park 407 fit Kelly staying; ours 417 / 567, the Harrison Park gap being Bridger's 6-8, which PPS moves in 2028-29).
PPS lists Hosford, Gray, Sellwood under 400.

## Main findings
1. James John and Sitton: the memo keeps James John open because it is "close to the planning floor of 360 through 2031-32"
   (p. 25-26), but the same memo lists it under 260 (p. 42-43). That 360 figure counts the Spanish strand, which the same
   recommendation moves to Chavez. Without the strand, James John (233) and Sitton (208) are two small neighborhood
   schools side by side; together they are ~441. Scenario A merged them (Sitton 433).
2. Boise-Eliot/Humboldt: keeping Mandarin at MLK Jr removes A's fix for BEH (A: 505), so BEH is ~310; the memo
   itself notes BEH fell 3 years running to 285. MLK Jr is then at 98% of its seats.
3. Sabin -> MLK Jr passes Vernon for 107 of 237 Sabin-area K-5 kids. Variant super_rec_sabin (nearest walk of
   MLK / Vernon / BC): MLK 459, Vernon 289 -> 395, K-5 at 360+ 17 -> 18, past closer 2,013 -> 1,983.
4. K-5 at target is 17 of 38 every year 2028-29 to 2035-36 (15 in 2027-28); current best dli_home3_rh is 38/38.
   Fewer kids moved (2,133 K-5 vs SQ) than A (2,935) or the current best (4,749); past closer 2,013 (best 793).


# super_rec: detached pieces (exceptions to the exclave rule)

These pieces are in the Superintendent's recommendation's own lines (PPS's traced Scenario A lines as modified by the memo of 2026-11-12), not drawn by our solver. They are kept as the district's plan. Kids are 2031-32 forecast.

- K-5 Chapman: 1 blocks, 0.3 kids, near 45.5428, -122.7463
- K-5 Chapman: 2 blocks, 0.4 kids, near 45.5319, -122.7309
- K-5 Chief Joseph: 2 blocks, 0.4 kids, near 45.5703, -122.7214
- K-5 Skyline: 7 blocks, 3.5 kids, near 45.5622, -122.7485
- K-5 Skyline: 1 blocks, 0.6 kids, near 45.5456, -122.7448
- K-5 Faubion: 72 blocks, 198.7 kids, near 45.6034, -122.6699
- K-5 Astor: 4 blocks, 4.7 kids, near 45.6242, -122.7532
- K-5 Astor: 1 blocks, 0.4 kids, near 45.6138, -122.7102
- 6-8 Ockley Green: 1 blocks, 0.2 kids, near 45.5669, -122.722
- 6-8 Skyline: 7 blocks, 1.0 kids, near 45.5622, -122.7485
- 6-8 Skyline: 1 blocks, 0.3 kids, near 45.5456, -122.7448
- 6-8 Astor: 4 blocks, 3.1 kids, near 45.6242, -122.7532
- 6-8 Astor: 2 blocks, 1.2 kids, near 45.5644, -122.6379
- 6-8 Astor: 4 blocks, 1.1 kids, near 45.5668, -122.6401
- 6-8 Astor: 1 blocks, 0.3 kids, near 45.6138, -122.7102
- 6-8 Astor: 1 blocks, 1.7 kids, near 45.5695, -122.6451
- 9-12 McDaniel: 399 blocks, 350.5 kids, near 45.5196, -122.5796
- 9-12 Jefferson: 2 blocks, 0.1 kids, near 45.5703, -122.7214
- 9-12 Roosevelt: 1 blocks, 0.2 kids, near 45.6138, -122.7102
