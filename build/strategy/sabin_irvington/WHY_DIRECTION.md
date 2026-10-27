# Why Irvington into Sabin, not Sabin into Irvington

*Analysis by AI (Claude), directed and guided by Paul. Model v2 estimates: 2031-32 PSU-forecast K-5 kids placed on 2020 Census blocks, OSRM walking distances. Figures come from the model runs and block tables named under "Data".*

## Short answer
If one of the two schools stays open, the geography favours keeping Sabin open and moving Irvington's kids. The buildings themselves are evenly matched. What decides it is the other schools nearby: Irvington's families split naturally between Sabin and Beverly Cleary, while Sabin's families have closer options than Irvington. The fair comparison is not "which direction" but "keep Sabin open vs close both".

## The two buildings alone are a wash
| Kids from | Avg walk to Sabin | Avg walk to Irvington |
|---|---|---|
| Sabin area (236 K-5) | 0.46 mi | 1.09 mi |
| Irvington area (223 K-5) | 1.13 mi | 0.54 mi |

Merging either way adds about 0.6 mi for the families who move. Capacity is about the same: Sabin 621, Irvington 618 (PPS school profiles 2025-26).

## What decides it: the neighbouring schools
- **Irvington into Sabin works.** Irvington's families split almost evenly: 114 kids are closer to Sabin and 109 closer to Beverly Cleary. A street line such as NE 15th + Knott gives Sabin about 358 and Beverly Cleary about 354, both near the 360 floor.
- **Sabin into Irvington does not.** Sabin's families are surrounded by schools closer than Irvington: King (MLK Jr), Alameda and Vernon. Only 25 of Sabin's 236 kids are closer to Irvington than to all of those. Even when kids are sent to Irvington unless another school is more than 0.5 mi closer, Irvington reaches only about 335. In the model runs, only 37-71 Sabin kids reach Irvington, and Irvington ends at about 224, far under 360. So "Sabin into Irvington" in practice means closing Sabin and leaving Irvington undersized.

## Other factors point the same way
- **Accessibility:** Sabin has an elevator and a stage lift on the state register. Irvington almost certainly has no elevator or lift (no record on the state register, a 2008 deficiency list and a 2009 study). Irvington is several stories with split levels.
- **Poverty:** Sabin's area has the higher share of kids in poverty (28%, 67 of 236, vs 21% for Irvington). Keeping Sabin open leaves all 67 of them at their school.
- **Feeders:** Sabin's whole zone stays together through Tubman to Jefferson. Irvington's kids follow their new elementary school: the Sabin side to Tubman, the Beverly Cleary side to Beaumont.
- **Plan D** already plans to use the Irvington building as the swing site while Beverly Cleary is retrofitted.

## The honest costs
- **Every Irvington family moves.** Their elementary walk grows about 0.3 mi (0.54 to about 0.86-0.89 mi, depending on the line).
- **Keeping Irvington open would give the two areas shorter walks** (about 0.55 mi vs 0.65 mi on average), but leaves an undersized Irvington and scatters Sabin's families across three schools.
- **District-wide, closing both schools scores slightly better.** It sends about 300 fewer kids past a closer school and has fewer bus-eligible kids. Keeping either one open spreads some cost to the neighbouring schools.

## What could change this
If Vernon's elementary closes (for example, if Tubman's middle school moves into the Vernon building), about 60 Vernon-area kids are closest to Sabin. Sabin would then not need Irvington's kids to reach 360, and Irvington could stay together at Beverly Cleary. Run `tubman_at_vernon_irvbc` tests this.

## Data
- Walk distances and kid counts: `build/solver/out_v2/irvington_map/blocks.csv`, `summary.json`.
- Model runs: `irv_sabin_15th`, `irv_sabin_15th_grant`, `irv_sabin_thompson21` (Sabin open); `sabin_all`, `sabin_all_keepbc`, `sabin_irv_noala` (Irvington open); `equity_noswap_alameda_rig_hs`, `dli_home3_rh` (both close). All in `build/solver/out_v2/`.
- Accessibility research: `build/pps-texts/ada-sabin-irvington/SUMMARY.md` and `IRVINGTON_DEEP_DIVE.md`.
