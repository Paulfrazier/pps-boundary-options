# How our model compares with PPS's own projections

PPS published projected enrollment for every school under its plans, for 2027-28 to 2031-32. They appear in the "How many students are expected?" table on page 4 of each school's Family Guide (dated October 8, 2026). PPS's "No changes" row is the Portland State University forecast (PSU Population Research Center, July 24, 2026, Table 5.5).

Our model estimates students block by block, so it can score any set of lines, including plans PPS hasn't drawn. To check it, the model was run on PPS's own lines (No changes, Scenario A and Scenario B) and compared with PPS's projections, school by school.

## Summary

| PPS plan | Schools compared | Within 10% of PPS, 2031-32 | Within 5% | Median difference | Within 10%, 2027-28 |
|---|---:|---:|---:|---:|---:|
| No changes (PPS Status Quo) | 76 | 74 | 74 | 0.0% | 74 |
| Scenario A | 62 | 58 | 46 | 1.6% | 51 |
| Scenario B | 65 | 61 | 50 | 1.6% | 56 |

Focus and alternative schools (Winterhaven, da Vinci, Odyssey, ACCESS, MLC, Benson) aren't compared, because both PPS and our model hold them fixed. 2031-32 is the main test, because PPS measures its size targets in that year.

## Example: middle schools under Scenario A

| School | PPS 2027-28 | PPS 2028-29 | PPS 2029-30 | PPS 2030-31 | PPS 2031-32 | Our model 2031-32 |
|---|---:|---:|---:|---:|---:|---:|
| Jackson | 618 | 564 | 486 | 428 | 404 | 408 |
| Tubman | 608 | 546 | 492 | 465 | 455 | 423 |
| Lane (Brentwood) | 384 | 586 | 525 | 480 | 457 | 448 |
| Gray | 481 | 518 | 551 | 508 | 490 | 472 |
| Beaumont | 506 | 502 | 501 | 490 | 498 | 464 |
| Ockley Green | 552 | 486 | 497 | 490 | 507 | 521 |
| Mt Tabor | 645 | 647 | 599 | 580 | 546 | 574 |
| Hosford | 602 | 747 | 610 | 575 | 557 | 566 |
| Kellogg | 507 | 548 | 582 | 556 | 579 | 613 |
| Harrison Park | 642 | 625 | 614 | 578 | 591 | 645 |
| West Sylvan | 687 | 647 | 670 | 645 | 620 | 622 |
| Roseway Heights | 655 | 642 | 671 | 655 | 628 | 731 |
| George | 604 | 637 | 669 | 649 | 636 | 673 |

PPS's middle-school size goal is "more than 500 students" (Family Guide glossary). Building capacities come from PPS's 2025-26 school profiles; Hosford's is 711 and George's 623. By PPS's own numbers, 5 of these 13 schools stay between 500 and capacity in every year from 2027-28 to 2031-32. Our model gives the same count.

## Why some schools differ

- **PPS's documents disagree with each other (Roseway Heights, and Beaumont under No changes).** PPS's middle-school map puts the Rigler elementary area, about 104 middle schoolers, inside Roseway Heights. PPS's numbers keep those students at Beaumont. Our model follows the map. Under No changes, Beaumont and Roseway Heights together match PPS to within 0.2% (ours 914, PPS 916).
- **PPS phases some changes in; our model applies them all in 2027-28.** This explains most 2027-28 differences: Lane, Kellogg, Hosford, George, Gray, Tubman, Jackson, Arleta, Llewellyn and Duniway. PPS lets current students finish where they are and moves some groups a year or two later. PPS's guides state the reasons, for example the Marysville guide, p. 3: "Delaying full implementation ensures students previously impacted by Southeast Guiding Coalition changes do not experience multiple school moves during elementary school." By 2031-32 the two mostly agree.
- **Stated modeling choices (Sunnyside +19%, Atkinson +12%, Scenario A, 2031-32).**
  - **Sunnyside:** it includes focus-lottery students in their last grandfathered year, following the Sunnyside guide (p. 3, lottery students "permitted to remain through 5th grade").
  - **Atkinson:** it keeps the immersion families who don't follow the program's move, an estimate PPS doesn't state.
- **Small, unexplained (Vernon, −11%, 35 students).** Vernon becomes K-5. The gap comes from how a K-8's students split between K-5 and 6-8. Our model uses Census age shares; PPS uses its own grade data.

## Why plan comparisons use our model, not PPS's numbers

PPS has published numbers only for its own plans. To compare our options with PPS A fairly, every plan, PPS A included, is scored by the same model on the same basis (2031-32, PSU forecast). When the site describes PPS A on its own, it quotes PPS's figures.

Full school-by-school table: `build/solver/out_v2/calibration_table.csv`. Working notes with every difference explained: `build/solver/out_v2/CALIBRATION.md`.
