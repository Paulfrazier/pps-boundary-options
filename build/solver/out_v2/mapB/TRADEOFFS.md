# Map B: the Superintendent's school set, lines fixed (promoted 2026-11-15)

Copy of `_lns_lnsBjj5_13.staging`. It keeps the rec's closures and DLI hubs, merges James John into Sitton, redraws
K-5 lines with the regional LNS (lns_rule.py), and keeps the rec's 6-8 and 9-12 lines unchanged.

## How it was built
rec_jjs2 (North only) → lnsBjj4 (move 0.75, block moves of 0.10 mi or less blocked, SW floor-exempt) → lnsBjj5 (adds the
worst-walk penalty: 2.0 per kid sent more than 1 mi past an eligible school within 1 mi; hard cut within ½ mi).

## Scores, 2031-32
| | super_rec | mapB (this) | lower-move alt `_lns_lnsBjj4_19` |
|---|---|---|---|
| K-5 at 360 | 17/40 | 33/39 | 33/39 |
| K-5 past closer | 2,013 | 1,280 | 1,381 |
| Over the bus line | 4,438 | 3,567 | 4,010 |
| Worst walks (within 1 mi / within ½ mi) | 1,216 / 115 | 248 / 0 | 692 / — |
| Moved out of open schools | 124 | 1,594 (618 walk farther) | 1,261 (481 farther) |
| ES zones split across middle schools | 1 | 23 | 22 |

## Known tradeoffs
- **District's plan, left short (floor-exempt):** Maplewood 248, Forest Park 259, Stephenson 260, Markham 345.
  SW doesn't have the kids for those buildings. Skyline (K-8) is at 177.
- **Feeders:** the rec's middle-school lines were drawn around the rec's K-5 zones, so 23 new K-5 zones now split across
  middle schools. Redrawing 6-8 on these lines (mapB_ms) broke feeders worse (BLOCKERS B6) and was rejected.
- **Exclaves:** K-5 is clean. The 6-8 and 9-12 pieces are the rec's own lines, identical to super_rec's list
  (Ockley Green 1 block, Skyline 2 pieces, Astor 5 pieces at 6-8; McDaniel 399 blocks, Jefferson 2, Roosevelt 1 at 9-12).
