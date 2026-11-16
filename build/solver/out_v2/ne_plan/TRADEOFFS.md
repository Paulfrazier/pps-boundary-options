# NE plan on the Superintendent's recommendation (promoted 2026-11-14)

It is a copy of `ne_combo_k5.staging`, built by `build_ne_combo.py`. It uses the recommendation everywhere, with three
changes:
- **Sabin** splits on street lines: west of NE 15th to King, the northern part of the rest to Vernon, the remainder
  to Alameda.
- **The other NE K-5 lines** are re-solved under the move rule and the worst-walk rule: kids at a school that stays
  open move only to lift a short school or for a real walk gain.
- **Middle and high school** lines are the rec's in every year.

## Scores, 2031-32
| | Rec | ne_plan |
|---|---|---|
| NE K-5 schools at 360 (11), 2031-32 | 6 | 10 (Laurelhurst 330) |
| …in every year 2027-28 → 2031-32 | 4 | 9 |
| K-5 at 360, citywide, by year 2027-28 → 2031-32 | see super_rec | 19 / 22 / 21 / 21 / 21 |
| K-5 avg walk / past a closer school | 0.953 / 2,013 | 0.941 / 1,843 |
| Over 1 mi with a school within 1 mi / within ½ mi | 1,216 / 115 | 1,035 / 80 |
| K-5 kids moved out of open schools | 124 | 849 |
| Middle at 500 / high at 1,100, by year | 10/10/8/6/6, 6/7/7/8/8 | same as rec |

NE K-5 sizes: King 437, Vernon 361, Alameda 471, Beverly Cleary 361, Boise-Eliot/Humboldt 361, Faubion 361, Scott 361,
Lee 374, Woodlawn 407, Vestal 360, Laurelhurst 330.

## Known tradeoffs
- Sabin's Alameda piece stays in the Tubman / Jefferson middle and high zones, so it splits from Alameda at 6th grade.
  The ne_combo try at moving that pocket to Beaumont / Grant was dropped. Beaumont only reached 489, and Jefferson
  fell under 1,100 in 2027-28 and 2030-31.
- Schools outside NE that are short under the rec stay short, as the district's plan.

## Exclaves
- K-5: none.
- 6-8 and 9-12: the rec's own pieces, identical to super_rec's list (Astor, Ockley Green, Skyline at 6-8; McDaniel 399
  blocks, Jefferson 2, Roosevelt 1 at 9-12).

The stale copy of super_rec's TRADEOFFS that sat here is kept as TRADEOFFS.md.bak_stale_superrec_copy.
