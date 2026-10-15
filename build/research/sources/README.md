# Research sources (linked, not copied)

The working copy of this analysis kept plain-text extracts of PPS documents here so quotes in
`../targets.md` could be re-checked offline. Those extracts are **not** redistributed in this repo.
Read the originals at PPS's own sites:

| Extract (not included) | Original document |
|---|---|
| `board_worksession_2026-03-31.txt` | PPS Board work session book, Mar 31 2026 (Policy 4.10.045-P quoted): https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3988980 |
| `resolution_7307.txt` | PPS Board Resolution 7307, Rightsizing guiding principles (May 26 2026): https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3997273 |
| `tle_focus_options_2026-06.txt` | TLE Committee, "Alternative & Focus School Overview", June 2026: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3997345 |
| `board_memo_2026-08-04.txt` | Board memo "Rightsizing Update: Equity Audit Evaluation", Aug 4 2026: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3997426 |
| (equity audit, school-by-school volume) | https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3997428 |
| `board_deck_2026-09-01.txt` | Board deck, Sept 1 2026: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14357211 |
| `board_deck_2026-09-15.txt`, `jefferson_is_rising_kpis_slide21.png` | Board deck, Sept 15 2026 (slides 16-21): https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14430171 |
| `scenarios_overview_2026-10-04.txt`, `scenarios_region_{cf,gm,jr,wl}.txt` | PPS Rightsizing scenarios overview and four regional PDFs, linked from https://www.pps.net/about/portland-public-schools-information/rightsize/scenarios (overview: https://drive.google.com/file/d/1ueJVC-Jo6MRKw56Jedihc6YbVdBlSB2z/view) |
| `scenarioA_6-8_map_crop_north.png` | PPS attendance-area map PDFs for SY 2027-28 (Status Quo / A / B x K-5 / 6-8 / 9-12), BoardBook org 915, files 14505795-14505805: `https://meetings.boardbook.org/Documents/DownloadPDF/<id>?org=915` |
| `hs_feeder_patterns_current.txt` | PPS High School Feeder Patterns: https://resources.finalsite.net/images/v1790894228/ppsnet/f2u6fbkysoabacyo484j/PPS_High_School_Feeder_Patterns_Eng.pdf |
| `lrfp_2021_capacity_excerpts.txt` | PPS Long-Range Facility Plan 2021, Vol 1: https://www.pps.net/fs/resource-manager/view/84245cbd-4298-4803-8ba9-d26fb13a9c7a |
| `pps_transport_service_guidelines_2024.txt` | PPS Service Guidelines - Student Transportation (rev. 08/07/2024): https://resources.finalsite.net/images/v1751562292/ppsnet/thzskadliar1v7qds4yc/Service_Guidelines_Student_Transportation_2024.pdf |
| `k_lottery_results_2026-27.txt`, `lottery_slots_ms_hs_2026-27.txt` | PPS enrollment & transfer (school choice) lottery results and slot sheets for 2026-27, pps.net Enrollment & Transfer pages |

## Included

`psu_forecast_table5_5_by_school_program.json` is a machine-readable transcription of Table 5.5
(enrollment by school and program, 2025-26 and 2031-32) from Portland State University Population
Research Center, *PPS Enrollment Forecasts 2026-27 to 2035-36* (July 2026), published by PPS:
https://resources.finalsite.net/images/v1785171463/ppsnet/ejdr22voeddvux8qwlob/PPS_Forecast_2026_27.pdf .
The solver reads it (`build/solver/common.py`). Check numbers against the PDF.
