window.SABIN_DATA = {
 "available": true,
 "note": "Model v2 estimates, 2031-32 projected kids, by today's attendance area. pov = students experiencing poverty (Census <185% of poverty anchored to each school's direct-certification rate in PPS's Status Quo dashboard; rough for areas this small), oth = all other students. mv/in1/bus/sust/pps are percents; walk/dwalk are miles. Render only plans whose status is \"done\".",
 "source": "build/solver/out_v2/SABIN_OPTIONS.json",
 "source_md": "build/solver/out_v2/SABIN_POVERTY.md",
 "script": "build/solver/sabin_poverty.py",
 "areas": [
  "Sabin",
  "Irvington"
 ],
 "plans": [
  {
   "run": "status_quo",
   "label": "PPS Status Quo",
   "data_label": "Today (Status Quo)",
   "note": "No closures: today's school areas (2027-28 lines).",
   "caveat": null,
   "on_map": true,
   "scorecard": "build/solver/out_v2/status_quo/scorecard.json",
   "schools_csv": "build/solver/out_v2/status_quo/schools.csv",
   "tradeoffs": null,
   "district": {
    "schools_open": 76,
    "pct_sustainable_schools": 27.6,
    "pct_students_in_sustainable": 50.0
   },
   "neighbor_schools": {
    "Sabin": {
     "total_2031": 236,
     "at_target_every_year": false
    },
    "Irvington": {
     "total_2031": 223,
     "at_target_every_year": false
    },
    "MLK Jr": {
     "total_2031": 337,
     "at_target_every_year": false
    },
    "Alameda": {
     "total_2031": 490,
     "at_target_every_year": true
    },
    "Vernon": {
     "total_2031": 451,
     "at_target_every_year": false
    },
    "Beverly Cleary": {
     "total_2031": 394,
     "at_target_every_year": false
    },
    "Boise-Eliot/Humboldt": {
     "total_2031": 309,
     "at_target_every_year": false
    },
    "Rigler": {
     "total_2031": 327,
     "at_target_every_year": false
    },
    "Woodlawn": {
     "total_2031": 289,
     "at_target_every_year": false
    }
   },
   "school_years": {
    "Sabin": {
     "type": "K-5",
     "years": {
      "2027-28": 236.9,
      "2028-29": 248.9,
      "2029-30": 240.9,
      "2030-31": 234.9,
      "2031-32": 235.9,
      "2032-33": 232.9,
      "2033-34": 229.9,
      "2034-35": 223.8,
      "2035-36": 220.8
     }
    },
    "Irvington": {
     "type": "K-5",
     "years": {
      "2027-28": 240.0,
      "2028-29": 236.0,
      "2029-30": 229.0,
      "2030-31": 220.0,
      "2031-32": 223.0,
      "2032-33": 222.0,
      "2033-34": 218.0,
      "2034-35": 213.0,
      "2035-36": 210.0
     }
    },
    "Beverly Cleary": {
     "type": "K-8",
     "years": {
      "2027-28": 435.6,
      "2028-29": 417.5,
      "2029-30": 412.5,
      "2030-31": 403.4,
      "2031-32": 394.4,
      "2032-33": 397.4,
      "2033-34": 384.3,
      "2034-35": 382.2,
      "2035-36": 379.2
     }
    },
    "MLK Jr": {
     "type": "K-5",
     "years": {
      "2027-28": 337.0,
      "2028-29": 343.0,
      "2029-30": 346.0,
      "2030-31": 350.0,
      "2031-32": 337.0,
      "2032-33": 330.0,
      "2033-34": 320.0,
      "2034-35": 307.0,
      "2035-36": 303.0
     }
    },
    "Boise-Eliot/Humboldt": {
     "type": "K-5",
     "years": {
      "2027-28": 315.1,
      "2028-29": 334.1,
      "2029-30": 325.1,
      "2030-31": 323.1,
      "2031-32": 309.0,
      "2032-33": 293.0,
      "2033-34": 279.9,
      "2034-35": 267.9,
      "2035-36": 265.9
     }
    },
    "Vernon": {
     "type": "K-8",
     "years": {
      "2027-28": 490.2,
      "2028-29": 486.2,
      "2029-30": 475.2,
      "2030-31": 461.3,
      "2031-32": 451.3,
      "2032-33": 446.3,
      "2033-34": 442.4,
      "2034-35": 445.3,
      "2035-36": 442.4
     }
    },
    "Alameda": {
     "type": "K-5",
     "years": {
      "2027-28": 495.7,
      "2028-29": 500.7,
      "2029-30": 504.6,
      "2030-31": 499.7,
      "2031-32": 489.7,
      "2032-33": 483.7,
      "2033-34": 473.8,
      "2034-35": 462.8,
      "2035-36": 458.9
     }
    },
    "Beaumont": {
     "type": "6-8",
     "years": {
      "2027-28": 296.9,
      "2028-29": 281.1,
      "2029-30": 288.7,
      "2030-31": 291.7,
      "2031-32": 313.2,
      "2032-33": 316.5,
      "2033-34": 320.7,
      "2034-35": 327.9,
      "2035-36": 323.2
     }
    },
    "Tubman": {
     "type": "6-8",
     "years": {
      "2027-28": 457.0,
      "2028-29": 414.0,
      "2029-30": 389.0,
      "2030-31": 368.0,
      "2031-32": 374.0,
      "2032-33": 377.0,
      "2033-34": 386.0,
      "2034-35": 391.0,
      "2035-36": 381.0
     }
    },
    "Jefferson": {
     "type": "9-12",
     "years": {
      "2027-28": 564.0,
      "2028-29": 805.0,
      "2029-30": 981.0,
      "2030-31": 1158.0,
      "2031-32": 1183.0,
      "2032-33": 1178.0,
      "2033-34": 1173.0,
      "2034-35": 1159.0,
      "2035-36": 1175.0
     }
    },
    "Grant": {
     "type": "9-12",
     "years": {
      "2027-28": 1935.0,
      "2028-29": 1822.0,
      "2029-30": 1713.0,
      "2030-31": 1576.0,
      "2031-32": 1487.0,
      "2032-33": 1394.0,
      "2033-34": 1332.0,
      "2034-35": 1263.0,
      "2035-36": 1237.0
     }
    }
   },
   "areas": {
    "Sabin": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 66.6409,
        "mv": 0.0,
        "walk": 0.477,
        "dwalk": 0.0,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 0.0,
        "pps": 0.0
       },
       "oth": {
        "n": 169.2329,
        "mv": 0.0,
        "walk": 0.4456,
        "dwalk": 0.0,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 0.0,
        "pps": 0.0
       }
      },
      "6-8": {
       "pov": {
        "n": 23.0294,
        "mv": 0.0,
        "walk": 1.7432,
        "dwalk": 0.0,
        "in1": 0.0,
        "bus": 69.857,
        "sust": 0.0,
        "pps": 0.0
       },
       "oth": {
        "n": 70.1338,
        "mv": 0.0,
        "walk": 1.817,
        "dwalk": 0.0,
        "in1": 0.0,
        "bus": 74.8626,
        "sust": 0.0,
        "pps": 0.0
       }
      },
      "9-12": {
       "pov": {
        "n": 70.6614,
        "mv": 0.0,
        "walk": 1.5527,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       },
       "oth": {
        "n": 149.8511,
        "mv": 0.0,
        "walk": 1.7818,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Sabin": {
        "kids": 236,
        "poverty": 67
       }
      },
      "6-8": {
       "Tubman": {
        "kids": 93,
        "poverty": 23
       }
      },
      "9-12": {
       "Jefferson": {
        "kids": 221,
        "poverty": 71
       }
      }
     }
    },
    "Irvington": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 46.4941,
        "mv": 0.0,
        "walk": 0.5997,
        "dwalk": 0.0,
        "in1": 87.2829,
        "bus": 12.7171,
        "sust": 0.0,
        "pps": 0.0
       },
       "oth": {
        "n": 176.5054,
        "mv": 0.0,
        "walk": 0.5211,
        "dwalk": 0.0,
        "in1": 93.9852,
        "bus": 6.0148,
        "sust": 0.0,
        "pps": 0.0
       }
      },
      "6-8": {
       "pov": {
        "n": 32.067,
        "mv": 0.0,
        "walk": 1.1978,
        "dwalk": 0.0,
        "in1": 33.1396,
        "bus": 31.0805,
        "sust": 0.0,
        "pps": 0.0
       },
       "oth": {
        "n": 81.8647,
        "mv": 0.0,
        "walk": 1.2683,
        "dwalk": 0.0,
        "in1": 20.637,
        "bus": 29.2609,
        "sust": 0.0,
        "pps": 0.0
       }
      },
      "9-12": {
       "pov": {
        "n": 50.8122,
        "mv": 0.0,
        "walk": 1.2861,
        "dwalk": 0.0,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 277.1536,
        "mv": 0.0,
        "walk": 1.2693,
        "dwalk": 0.0,
        "sust": 100.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Irvington": {
        "kids": 223,
        "poverty": 46
       }
      },
      "6-8": {
       "Tubman": {
        "kids": 114,
        "poverty": 32
       }
      },
      "9-12": {
       "Grant": {
        "kids": 328,
        "poverty": 51
       }
      }
     }
    }
   }
  },
  {
   "run": "scenario_A",
   "label": "PPS Scenario A",
   "data_label": "PPS Scenario A",
   "note": null,
   "caveat": null,
   "on_map": true,
   "scorecard": "build/solver/out_v2/scenario_A/scorecard.json",
   "schools_csv": "build/solver/out_v2/scenario_A/schools.csv",
   "tradeoffs": null,
   "district": {
    "schools_open": 62,
    "pct_sustainable_schools": 69.4,
    "pct_students_in_sustainable": 81.4
   },
   "neighbor_schools": {
    "Sabin": {
     "total_2031": 0,
     "at_target_every_year": false
    },
    "Irvington": {
     "total_2031": 0,
     "at_target_every_year": false
    },
    "MLK Jr": {
     "total_2031": 377,
     "at_target_every_year": true
    },
    "Alameda": {
     "total_2031": 490,
     "at_target_every_year": true
    },
    "Vernon": {
     "total_2031": 288,
     "at_target_every_year": false
    },
    "Beverly Cleary": {
     "total_2031": 451,
     "at_target_every_year": true
    },
    "Boise-Eliot/Humboldt": {
     "total_2031": 505,
     "at_target_every_year": true
    },
    "Rigler": {
     "total_2031": 505,
     "at_target_every_year": true
    },
    "Woodlawn": {
     "total_2031": 292,
     "at_target_every_year": false
    }
   },
   "school_years": {
    "Beverly Cleary": {
     "type": "K-5",
     "years": {
      "2027-28": 491.7,
      "2028-29": 477.4,
      "2029-30": 467.6,
      "2030-31": 453.4,
      "2031-32": 451.1,
      "2032-33": 451.7,
      "2033-34": 440.2,
      "2034-35": 433.9,
      "2035-36": 429.2
     }
    },
    "MLK Jr": {
     "type": "K-5",
     "years": {
      "2027-28": 373.8,
      "2028-29": 392.0,
      "2029-30": 385.0,
      "2030-31": 382.0,
      "2031-32": 377.8,
      "2032-33": 370.8,
      "2033-34": 360.8,
      "2034-35": 346.7,
      "2035-36": 340.7
     }
    },
    "Boise-Eliot/Humboldt": {
     "type": "K-5",
     "years": {
      "2027-28": 516.6,
      "2028-29": 535.7,
      "2029-30": 528.7,
      "2030-31": 527.7,
      "2031-32": 505.6,
      "2032-33": 486.5,
      "2033-34": 470.5,
      "2034-35": 453.4,
      "2035-36": 450.4
     }
    },
    "Vernon": {
     "type": "K-5",
     "years": {
      "2027-28": 313.3,
      "2028-29": 310.9,
      "2029-30": 303.9,
      "2030-31": 295.0,
      "2031-32": 288.6,
      "2032-33": 285.4,
      "2033-34": 282.8,
      "2034-35": 284.7,
      "2035-36": 282.8
     }
    },
    "Alameda": {
     "type": "K-5",
     "years": {
      "2027-28": 495.8,
      "2028-29": 500.8,
      "2029-30": 504.8,
      "2030-31": 499.8,
      "2031-32": 489.9,
      "2032-33": 483.9,
      "2033-34": 473.9,
      "2034-35": 463.0,
      "2035-36": 459.0
     }
    },
    "Beaumont": {
     "type": "6-8",
     "years": {
      "2027-28": 427.9,
      "2028-29": 443.3,
      "2029-30": 467.9,
      "2030-31": 454.2,
      "2031-32": 463.7,
      "2032-33": 468.8,
      "2033-34": 469.3,
      "2034-35": 471.8,
      "2035-36": 463.2
     }
    },
    "Tubman": {
     "type": "6-8",
     "years": {
      "2027-28": 586.3,
      "2028-29": 505.0,
      "2029-30": 439.9,
      "2030-31": 422.7,
      "2031-32": 423.3,
      "2032-33": 424.9,
      "2033-34": 430.7,
      "2034-35": 434.3,
      "2035-36": 426.8
     }
    },
    "Jefferson": {
     "type": "9-12",
     "years": {
      "2027-28": 563.0,
      "2028-29": 803.6,
      "2029-30": 979.2,
      "2030-31": 1155.9,
      "2031-32": 1180.9,
      "2032-33": 1175.9,
      "2033-34": 1170.9,
      "2034-35": 1156.9,
      "2035-36": 1172.9
     }
    },
    "Grant": {
     "type": "9-12",
     "years": {
      "2027-28": 1935.0,
      "2028-29": 1822.0,
      "2029-30": 1713.0,
      "2030-31": 1576.0,
      "2031-32": 1487.0,
      "2032-33": 1394.0,
      "2033-34": 1332.0,
      "2034-35": 1263.0,
      "2035-36": 1237.0
     }
    }
   },
   "areas": {
    "Sabin": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 66.6409,
        "mv": 100.0,
        "walk": 0.7979,
        "dwalk": 0.321,
        "in1": 74.0581,
        "bus": 25.9419,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 169.2329,
        "mv": 100.0,
        "walk": 0.9835,
        "dwalk": 0.5379,
        "in1": 46.2286,
        "bus": 53.7714,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "6-8": {
       "pov": {
        "n": 23.0294,
        "mv": 0.0,
        "walk": 1.7432,
        "dwalk": 0.0,
        "in1": 0.0,
        "bus": 69.857,
        "sust": 0.0,
        "pps": 0.0
       },
       "oth": {
        "n": 70.1338,
        "mv": 0.0,
        "walk": 1.817,
        "dwalk": 0.0,
        "in1": 0.0,
        "bus": 74.8626,
        "sust": 0.0,
        "pps": 0.0
       }
      },
      "9-12": {
       "pov": {
        "n": 70.6614,
        "mv": 0.0,
        "walk": 1.5527,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       },
       "oth": {
        "n": 149.8511,
        "mv": 0.0,
        "walk": 1.7818,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "MLK Jr": {
        "kids": 236,
        "poverty": 67
       }
      },
      "6-8": {
       "Tubman": {
        "kids": 93,
        "poverty": 23
       }
      },
      "9-12": {
       "Jefferson": {
        "kids": 221,
        "poverty": 71
       }
      }
     }
    },
    "Irvington": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 46.4941,
        "mv": 100.0,
        "walk": 1.0342,
        "dwalk": 0.4345,
        "in1": 50.8415,
        "bus": 49.1585,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 176.5054,
        "mv": 100.0,
        "walk": 1.0827,
        "dwalk": 0.5617,
        "in1": 41.622,
        "bus": 58.378,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "6-8": {
       "pov": {
        "n": 32.067,
        "mv": 100.0,
        "walk": 2.0384,
        "dwalk": 0.8406,
        "in1": 0.0,
        "bus": 94.4728,
        "sust": 0.0,
        "pps": 0.0
       },
       "oth": {
        "n": 81.8647,
        "mv": 100.0,
        "walk": 1.825,
        "dwalk": 0.5566,
        "in1": 0.0,
        "bus": 81.4632,
        "sust": 0.0,
        "pps": 0.0
       }
      },
      "9-12": {
       "pov": {
        "n": 50.8122,
        "mv": 0.0,
        "walk": 1.2861,
        "dwalk": 0.0,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 277.1536,
        "mv": 0.0,
        "walk": 1.2693,
        "dwalk": 0.0,
        "sust": 100.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Beverly Cleary": {
        "kids": 223,
        "poverty": 46
       }
      },
      "6-8": {
       "Beaumont": {
        "kids": 114,
        "poverty": 32
       }
      },
      "9-12": {
       "Grant": {
        "kids": 328,
        "poverty": 51
       }
      }
     }
    }
   }
  },
  {
   "run": "planD_updated",
   "label": "Plan D (current draft, Sabin stays open)",
   "data_label": "Scenario D as written (current draft, Sabin stays open)",
   "note": "A board member's current draft, as written: five elementary schools close, Sabin stays open with today's area, and Irvington goes to Beverly Cleary. Lines are not redrawn.",
   "caveat": null,
   "on_map": true,
   "scorecard": "build/solver/out_v2/planD_updated/scorecard.json",
   "schools_csv": "build/solver/out_v2/planD_updated/schools.csv",
   "tradeoffs": "build/solver/out_v2/planD_updated/TRADEOFFS.md",
   "district": {
    "schools_open": 71,
    "pct_sustainable_schools": 39.4,
    "pct_students_in_sustainable": 59.7
   },
   "neighbor_schools": {
    "Sabin": {
     "total_2031": 236,
     "at_target_every_year": false
    },
    "Irvington": {
     "total_2031": 0,
     "at_target_every_year": false
    },
    "MLK Jr": {
     "total_2031": 337,
     "at_target_every_year": false
    },
    "Alameda": {
     "total_2031": 490,
     "at_target_every_year": true
    },
    "Vernon": {
     "total_2031": 288,
     "at_target_every_year": false
    },
    "Beverly Cleary": {
     "total_2031": 451,
     "at_target_every_year": true
    },
    "Boise-Eliot/Humboldt": {
     "total_2031": 309,
     "at_target_every_year": false
    },
    "Rigler": {
     "total_2031": 327,
     "at_target_every_year": false
    },
    "Woodlawn": {
     "total_2031": 289,
     "at_target_every_year": false
    }
   },
   "school_years": {
    "Sabin": {
     "type": "K-5",
     "years": {
      "2027-28": 236.9,
      "2028-29": 248.9,
      "2029-30": 240.9,
      "2030-31": 234.9,
      "2031-32": 235.9,
      "2032-33": 232.9,
      "2033-34": 229.9,
      "2034-35": 223.8,
      "2035-36": 220.8
     }
    },
    "Beverly Cleary": {
     "type": "K-5",
     "years": {
      "2027-28": 491.5,
      "2028-29": 477.2,
      "2029-30": 467.4,
      "2030-31": 453.1,
      "2031-32": 450.9,
      "2032-33": 451.5,
      "2033-34": 440.0,
      "2034-35": 433.7,
      "2035-36": 429.0
     }
    },
    "MLK Jr": {
     "type": "K-5",
     "years": {
      "2027-28": 337.0,
      "2028-29": 343.0,
      "2029-30": 346.0,
      "2030-31": 350.0,
      "2031-32": 337.0,
      "2032-33": 330.0,
      "2033-34": 320.0,
      "2034-35": 307.0,
      "2035-36": 303.0
     }
    },
    "Boise-Eliot/Humboldt": {
     "type": "K-5",
     "years": {
      "2027-28": 315.1,
      "2028-29": 334.1,
      "2029-30": 325.1,
      "2030-31": 323.1,
      "2031-32": 309.0,
      "2032-33": 293.0,
      "2033-34": 279.9,
      "2034-35": 267.9,
      "2035-36": 265.9
     }
    },
    "Vernon": {
     "type": "K-5",
     "years": {
      "2027-28": 312.8,
      "2028-29": 310.3,
      "2029-30": 303.3,
      "2030-31": 294.4,
      "2031-32": 288.0,
      "2032-33": 284.9,
      "2033-34": 282.3,
      "2034-35": 284.2,
      "2035-36": 282.3
     }
    },
    "Alameda": {
     "type": "K-5",
     "years": {
      "2027-28": 495.7,
      "2028-29": 500.7,
      "2029-30": 504.6,
      "2030-31": 499.7,
      "2031-32": 489.7,
      "2032-33": 483.7,
      "2033-34": 473.8,
      "2034-35": 462.8,
      "2035-36": 458.9
     }
    },
    "Beaumont": {
     "type": "6-8",
     "years": {
      "2027-28": 523.9,
      "2028-29": 485.8,
      "2029-30": 467.9,
      "2030-31": 454.2,
      "2031-32": 463.7,
      "2032-33": 468.8,
      "2033-34": 469.3,
      "2034-35": 471.8,
      "2035-36": 463.2
     }
    },
    "Tubman": {
     "type": "6-8",
     "years": {
      "2027-28": 490.3,
      "2028-29": 462.5,
      "2029-30": 439.9,
      "2030-31": 422.7,
      "2031-32": 423.3,
      "2032-33": 424.9,
      "2033-34": 430.7,
      "2034-35": 434.3,
      "2035-36": 426.8
     }
    },
    "Jefferson": {
     "type": "9-12",
     "years": {
      "2027-28": 564.0,
      "2028-29": 805.0,
      "2029-30": 981.0,
      "2030-31": 1158.0,
      "2031-32": 1183.0,
      "2032-33": 1178.0,
      "2033-34": 1173.0,
      "2034-35": 1159.0,
      "2035-36": 1175.0
     }
    },
    "Grant": {
     "type": "9-12",
     "years": {
      "2027-28": 1935.0,
      "2028-29": 1822.0,
      "2029-30": 1713.0,
      "2030-31": 1576.0,
      "2031-32": 1487.0,
      "2032-33": 1394.0,
      "2033-34": 1332.0,
      "2034-35": 1263.0,
      "2035-36": 1237.0
     }
    }
   },
   "areas": {
    "Sabin": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 66.6409,
        "mv": 0.0,
        "walk": 0.477,
        "dwalk": 0.0,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 0.0,
        "pps": 0.0
       },
       "oth": {
        "n": 169.2329,
        "mv": 0.0,
        "walk": 0.4456,
        "dwalk": 0.0,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 0.0,
        "pps": 0.0
       }
      },
      "6-8": {
       "pov": {
        "n": 23.0294,
        "mv": 0.0,
        "walk": 1.7432,
        "dwalk": 0.0,
        "in1": 0.0,
        "bus": 69.857,
        "sust": 0.0,
        "pps": 0.0
       },
       "oth": {
        "n": 70.1338,
        "mv": 0.0,
        "walk": 1.817,
        "dwalk": 0.0,
        "in1": 0.0,
        "bus": 74.8626,
        "sust": 0.0,
        "pps": 0.0
       }
      },
      "9-12": {
       "pov": {
        "n": 70.6614,
        "mv": 0.0,
        "walk": 1.5527,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       },
       "oth": {
        "n": 149.8511,
        "mv": 0.0,
        "walk": 1.7818,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Sabin": {
        "kids": 236,
        "poverty": 67
       }
      },
      "6-8": {
       "Tubman": {
        "kids": 93,
        "poverty": 23
       }
      },
      "9-12": {
       "Jefferson": {
        "kids": 221,
        "poverty": 71
       }
      }
     }
    },
    "Irvington": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 46.4941,
        "mv": 100.0,
        "walk": 1.0342,
        "dwalk": 0.4345,
        "in1": 50.8415,
        "bus": 49.1585,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 176.5054,
        "mv": 100.0,
        "walk": 1.0827,
        "dwalk": 0.5617,
        "in1": 41.622,
        "bus": 58.378,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "6-8": {
       "pov": {
        "n": 32.067,
        "mv": 100.0,
        "walk": 2.0384,
        "dwalk": 0.8406,
        "in1": 0.0,
        "bus": 94.4728,
        "sust": 0.0,
        "pps": 0.0
       },
       "oth": {
        "n": 81.8647,
        "mv": 100.0,
        "walk": 1.825,
        "dwalk": 0.5566,
        "in1": 0.0,
        "bus": 81.4632,
        "sust": 0.0,
        "pps": 0.0
       }
      },
      "9-12": {
       "pov": {
        "n": 50.8122,
        "mv": 0.0,
        "walk": 1.2861,
        "dwalk": 0.0,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 277.1536,
        "mv": 0.0,
        "walk": 1.2693,
        "dwalk": 0.0,
        "sust": 100.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Beverly Cleary": {
        "kids": 223,
        "poverty": 46
       }
      },
      "6-8": {
       "Beaumont": {
        "kids": 114,
        "poverty": 32
       }
      },
      "9-12": {
       "Grant": {
        "kids": 328,
        "poverty": 51
       }
      }
     }
    }
   }
  },
  {
   "run": "equity_noswap_alameda_rig_hs",
   "label": "Previous best: no program swaps",
   "data_label": "Current best: fewer DLI moves, sustainable schools",
   "note": null,
   "caveat": null,
   "on_map": true,
   "scorecard": "build/solver/out_v2/equity_noswap_alameda_rig_hs/scorecard.json",
   "schools_csv": "build/solver/out_v2/equity_noswap_alameda_rig_hs/schools.csv",
   "tradeoffs": "build/solver/out_v2/equity_noswap_alameda_rig_hs/TRADEOFFS.md",
   "district": {
    "schools_open": 62,
    "pct_sustainable_schools": 96.8,
    "pct_students_in_sustainable": 98.3
   },
   "neighbor_schools": {
    "Sabin": {
     "total_2031": 0,
     "at_target_every_year": false
    },
    "Irvington": {
     "total_2031": 0,
     "at_target_every_year": false
    },
    "MLK Jr": {
     "total_2031": 487,
     "at_target_every_year": true
    },
    "Alameda": {
     "total_2031": 436,
     "at_target_every_year": true
    },
    "Vernon": {
     "total_2031": 361,
     "at_target_every_year": true
    },
    "Beverly Cleary": {
     "total_2031": 438,
     "at_target_every_year": true
    },
    "Boise-Eliot/Humboldt": {
     "total_2031": 368,
     "at_target_every_year": true
    },
    "Rigler": {
     "total_2031": 523,
     "at_target_every_year": true
    },
    "Woodlawn": {
     "total_2031": 361,
     "at_target_every_year": true
    }
   },
   "school_years": {
    "Beverly Cleary": {
     "type": "K-5",
     "years": {
      "2027-28": 475.7,
      "2028-29": 458.7,
      "2029-30": 453.1,
      "2030-31": 440.5,
      "2031-32": 437.7,
      "2032-33": 437.6,
      "2033-34": 426.7,
      "2034-35": 419.9,
      "2035-36": 415.3
     }
    },
    "MLK Jr": {
     "type": "K-5",
     "years": {
      "2027-28": 489.1,
      "2028-29": 502.5,
      "2029-30": 501.9,
      "2030-31": 503.2,
      "2031-32": 486.8,
      "2032-33": 474.8,
      "2033-34": 461.0,
      "2034-35": 443.7,
      "2035-36": 437.9
     }
    },
    "Boise-Eliot/Humboldt": {
     "type": "K-5",
     "years": {
      "2027-28": 375.6,
      "2028-29": 391.4,
      "2029-30": 385.0,
      "2030-31": 381.7,
      "2031-32": 367.7,
      "2032-33": 352.4,
      "2033-34": 338.8,
      "2034-35": 325.6,
      "2035-36": 321.3
     }
    },
    "Vernon": {
     "type": "K-5",
     "years": {
      "2027-28": 379.5,
      "2028-29": 384.9,
      "2029-30": 375.2,
      "2030-31": 366.0,
      "2031-32": 360.7,
      "2032-33": 356.0,
      "2033-34": 351.4,
      "2034-35": 348.3,
      "2035-36": 344.8
     }
    },
    "Alameda": {
     "type": "K-5",
     "years": {
      "2027-28": 444.1,
      "2028-29": 449.4,
      "2029-30": 448.6,
      "2030-31": 441.9,
      "2031-32": 435.7,
      "2032-33": 430.8,
      "2033-34": 422.4,
      "2034-35": 412.8,
      "2035-36": 408.8
     }
    },
    "Beaumont": {
     "type": "6-8",
     "years": {
      "2027-28": 626.5,
      "2028-29": 591.2,
      "2029-30": 588.6,
      "2030-31": 578.0,
      "2031-32": 599.9,
      "2032-33": 601.7,
      "2033-34": 607.1,
      "2034-35": 617.6,
      "2035-36": 608.0
     }
    },
    "Tubman": {
     "type": "6-8",
     "years": {
      "2027-28": 596.3,
      "2028-29": 555.8,
      "2029-30": 540.6,
      "2030-31": 522.6,
      "2031-32": 523.4,
      "2032-33": 525.7,
      "2033-34": 529.8,
      "2034-35": 534.3,
      "2035-36": 526.2
     }
    },
    "Jefferson": {
     "type": "9-12",
     "years": {
      "2027-28": 563.0,
      "2028-29": 803.6,
      "2029-30": 979.2,
      "2030-31": 1155.9,
      "2031-32": 1180.9,
      "2032-33": 1175.9,
      "2033-34": 1170.9,
      "2034-35": 1156.9,
      "2035-36": 1172.9
     }
    },
    "Grant": {
     "type": "9-12",
     "years": {
      "2027-28": 1935.0,
      "2028-29": 1822.0,
      "2029-30": 1713.0,
      "2030-31": 1576.0,
      "2031-32": 1487.0,
      "2032-33": 1394.0,
      "2033-34": 1332.0,
      "2034-35": 1263.0,
      "2035-36": 1237.0
     }
    }
   },
   "areas": {
    "Sabin": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 66.6409,
        "mv": 100.0,
        "walk": 0.6393,
        "dwalk": 0.1623,
        "in1": 92.1661,
        "bus": 7.8339,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 169.2329,
        "mv": 100.0,
        "walk": 0.6882,
        "dwalk": 0.2425,
        "in1": 90.1886,
        "bus": 9.8114,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "6-8": {
       "pov": {
        "n": 23.0294,
        "mv": 54.0735,
        "walk": 1.4422,
        "dwalk": -0.3011,
        "in1": 1.4278,
        "bus": 41.4669,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 70.1338,
        "mv": 74.644,
        "walk": 1.3929,
        "dwalk": -0.4241,
        "in1": 3.8939,
        "bus": 35.0981,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 70.6614,
        "mv": 0.0,
        "walk": 1.5527,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       },
       "oth": {
        "n": 149.8511,
        "mv": 0.0,
        "walk": 1.7818,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Vernon": {
        "kids": 105,
        "poverty": 27
       },
       "MLK Jr": {
        "kids": 66,
        "poverty": 29
       },
       "Alameda": {
        "kids": 61,
        "poverty": 10
       },
       "Boise-Eliot/Humboldt": {
        "kids": 5,
        "poverty": 1
       }
      },
      "6-8": {
       "Beaumont": {
        "kids": 65,
        "poverty": 12
       },
       "Tubman": {
        "kids": 28,
        "poverty": 11
       }
      },
      "9-12": {
       "Jefferson": {
        "kids": 221,
        "poverty": 71
       }
      }
     }
    },
    "Irvington": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 46.4941,
        "mv": 100.0,
        "walk": 0.893,
        "dwalk": 0.2933,
        "in1": 58.3577,
        "bus": 41.6423,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 176.5054,
        "mv": 100.0,
        "walk": 0.9013,
        "dwalk": 0.3802,
        "in1": 59.8862,
        "bus": 40.1138,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "6-8": {
       "pov": {
        "n": 32.067,
        "mv": 11.2314,
        "walk": 1.2351,
        "dwalk": 0.0373,
        "in1": 32.2598,
        "bus": 35.9131,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 81.8647,
        "mv": 41.7502,
        "walk": 1.3835,
        "dwalk": 0.1152,
        "in1": 18.4798,
        "bus": 44.4835,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 50.8122,
        "mv": 0.0,
        "walk": 1.2861,
        "dwalk": 0.0,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 277.1536,
        "mv": 0.0,
        "walk": 1.2693,
        "dwalk": 0.0,
        "sust": 100.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Beverly Cleary": {
        "kids": 137,
        "poverty": 32
       },
       "Boise-Eliot/Humboldt": {
        "kids": 50,
        "poverty": 12
       },
       "Alameda": {
        "kids": 36,
        "poverty": 2
       }
      },
      "6-8": {
       "Tubman": {
        "kids": 76,
        "poverty": 28
       },
       "Beaumont": {
        "kids": 38,
        "poverty": 4
       }
      },
      "9-12": {
       "Grant": {
        "kids": 328,
        "poverty": 51
       }
      }
     }
    }
   }
  },
  {
   "run": "sabin_all",
   "label": "Sabin into Irvington, close to home",
   "data_label": "Sabin into Irvington, all ideas",
   "note": "Built on the previous best (no program swaps), with the same Skyline high-school change. Sabin closes; Irvington stays open below 360. Today's King, Boise-Eliot/Humboldt and Vernon areas are unchanged. Irvington feeds Tubman, then Jefferson; Alameda and Beverly Cleary feed Beaumont, then Grant. 13 elementary schools close.",
   "caveat": null,
   "on_map": true,
   "scorecard": "build/solver/out_v2/sabin_all/scorecard.json",
   "schools_csv": "build/solver/out_v2/sabin_all/schools.csv",
   "tradeoffs": "build/solver/out_v2/sabin_all/TRADEOFFS.md",
   "district": {
    "schools_open": 63,
    "pct_sustainable_schools": 92.1,
    "pct_students_in_sustainable": 94.8
   },
   "neighbor_schools": {
    "Sabin": {
     "total_2031": 0,
     "at_target_every_year": false
    },
    "Irvington": {
     "total_2031": 224,
     "at_target_every_year": false
    },
    "MLK Jr": {
     "total_2031": 440,
     "at_target_every_year": true
    },
    "Alameda": {
     "total_2031": 387,
     "at_target_every_year": true
    },
    "Vernon": {
     "total_2031": 362,
     "at_target_every_year": true
    },
    "Beverly Cleary": {
     "total_2031": 361,
     "at_target_every_year": true
    },
    "Boise-Eliot/Humboldt": {
     "total_2031": 369,
     "at_target_every_year": true
    },
    "Rigler": {
     "total_2031": 496,
     "at_target_every_year": true
    },
    "Woodlawn": {
     "total_2031": 361,
     "at_target_every_year": true
    }
   },
   "school_years": {
    "Irvington": {
     "type": "K-5",
     "years": {
      "2027-28": 236.0,
      "2028-29": 235.8,
      "2029-30": 229.5,
      "2030-31": 221.8,
      "2031-32": 223.5,
      "2032-33": 221.7,
      "2033-34": 218.2,
      "2034-35": 212.9,
      "2035-36": 210.0
     }
    },
    "Beverly Cleary": {
     "type": "K-5",
     "years": {
      "2027-28": 393.5,
      "2028-29": 377.8,
      "2029-30": 374.3,
      "2030-31": 364.6,
      "2031-32": 361.1,
      "2032-33": 361.4,
      "2033-34": 351.9,
      "2034-35": 346.8,
      "2035-36": 343.3
     }
    },
    "MLK Jr": {
     "type": "K-5",
     "years": {
      "2027-28": 439.8,
      "2028-29": 449.9,
      "2029-30": 451.5,
      "2030-31": 453.8,
      "2031-32": 439.6,
      "2032-33": 430.6,
      "2033-34": 418.5,
      "2034-35": 402.6,
      "2035-36": 396.8
     }
    },
    "Boise-Eliot/Humboldt": {
     "type": "K-5",
     "years": {
      "2027-28": 374.0,
      "2028-29": 394.6,
      "2029-30": 387.8,
      "2030-31": 386.2,
      "2031-32": 368.8,
      "2032-33": 350.6,
      "2033-34": 335.3,
      "2034-35": 321.1,
      "2035-36": 317.2
     }
    },
    "Vernon": {
     "type": "K-5",
     "years": {
      "2027-28": 386.7,
      "2028-29": 388.0,
      "2029-30": 378.6,
      "2030-31": 367.8,
      "2031-32": 361.7,
      "2032-33": 357.5,
      "2033-34": 354.0,
      "2034-35": 354.1,
      "2035-36": 351.2
     }
    },
    "Alameda": {
     "type": "K-5",
     "years": {
      "2027-28": 392.0,
      "2028-29": 397.4,
      "2029-30": 398.1,
      "2030-31": 393.3,
      "2031-32": 386.6,
      "2032-33": 382.1,
      "2033-34": 374.5,
      "2034-35": 365.8,
      "2035-36": 362.5
     }
    },
    "Beaumont": {
     "type": "6-8",
     "years": {
      "2027-28": 636.2,
      "2028-29": 600.8,
      "2029-30": 600.7,
      "2030-31": 593.0,
      "2031-32": 612.9,
      "2032-33": 618.8,
      "2033-34": 620.4,
      "2034-35": 629.1,
      "2035-36": 619.7
     }
    },
    "Tubman": {
     "type": "6-8",
     "years": {
      "2027-28": 640.4,
      "2028-29": 598.7,
      "2029-30": 578.4,
      "2030-31": 555.9,
      "2031-32": 559.4,
      "2032-33": 558.1,
      "2033-34": 566.3,
      "2034-35": 572.6,
      "2035-36": 563.4
     }
    },
    "Jefferson": {
     "type": "9-12",
     "years": {
      "2027-28": 859.7,
      "2028-29": 1073.6,
      "2029-30": 1224.2,
      "2030-31": 1371.3,
      "2031-32": 1379.1,
      "2032-33": 1357.1,
      "2033-34": 1340.5,
      "2034-35": 1314.3,
      "2035-36": 1324.9
     }
    },
    "Grant": {
     "type": "9-12",
     "years": {
      "2027-28": 1714.0,
      "2028-29": 1625.3,
      "2029-30": 1534.9,
      "2030-31": 1424.8,
      "2031-32": 1350.0,
      "2032-33": 1270.0,
      "2033-34": 1217.6,
      "2034-35": 1158.6,
      "2035-36": 1137.0
     }
    }
   },
   "areas": {
    "Sabin": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 66.6409,
        "mv": 100.0,
        "walk": 0.5993,
        "dwalk": 0.1223,
        "in1": 98.8607,
        "bus": 1.1393,
        "sust": 83.8122,
        "pps": 83.8122
       },
       "oth": {
        "n": 169.2329,
        "mv": 100.0,
        "walk": 0.623,
        "dwalk": 0.1774,
        "in1": 98.798,
        "bus": 1.202,
        "sust": 76.8253,
        "pps": 76.8253
       }
      },
      "6-8": {
       "pov": {
        "n": 23.0294,
        "mv": 12.6977,
        "walk": 1.6536,
        "dwalk": -0.0897,
        "in1": 1.4278,
        "bus": 57.1594,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 70.1338,
        "mv": 22.0952,
        "walk": 1.6383,
        "dwalk": -0.1787,
        "in1": 3.8939,
        "bus": 52.7674,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 70.6614,
        "mv": 14.1876,
        "walk": 1.4455,
        "dwalk": -0.1072,
        "sust": 14.1876,
        "pps": 100.0
       },
       "oth": {
        "n": 149.8511,
        "mv": 23.3555,
        "walk": 1.6231,
        "dwalk": -0.1587,
        "sust": 23.3555,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Vernon": {
        "kids": 73,
        "poverty": 20
       },
       "MLK Jr": {
        "kids": 63,
        "poverty": 27
       },
       "Alameda": {
        "kids": 50,
        "poverty": 9
       },
       "Irvington": {
        "kids": 50,
        "poverty": 11
       }
      },
      "6-8": {
       "Tubman": {
        "kids": 75,
        "poverty": 20
       },
       "Beaumont": {
        "kids": 18,
        "poverty": 3
       }
      },
      "9-12": {
       "Jefferson": {
        "kids": 175,
        "poverty": 61
       },
       "Grant": {
        "kids": 45,
        "poverty": 10
       }
      }
     }
    },
    "Irvington": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 46.4941,
        "mv": 38.9189,
        "walk": 0.4858,
        "dwalk": -0.1138,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 38.9189,
        "pps": 38.9189
       },
       "oth": {
        "n": 176.5054,
        "mv": 28.118,
        "walk": 0.4514,
        "dwalk": -0.0697,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 28.118,
        "pps": 28.118
       }
      },
      "6-8": {
       "pov": {
        "n": 32.067,
        "mv": 41.2287,
        "walk": 1.2951,
        "dwalk": 0.0973,
        "in1": 33.1396,
        "bus": 38.9101,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 81.8647,
        "mv": 28.7671,
        "walk": 1.2748,
        "dwalk": 0.0064,
        "in1": 20.637,
        "bus": 23.8218,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 50.8122,
        "mv": 54.0117,
        "walk": 1.6806,
        "dwalk": 0.3945,
        "sust": 45.9883,
        "pps": 100.0
       },
       "oth": {
        "n": 277.1536,
        "mv": 69.206,
        "walk": 1.8346,
        "dwalk": 0.5652,
        "sust": 30.794,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Irvington": {
        "kids": 155,
        "poverty": 28
       },
       "Beverly Cleary": {
        "kids": 66,
        "poverty": 18
       },
       "Alameda": {
        "kids": 1,
        "poverty": 0
       }
      },
      "6-8": {
       "Tubman": {
        "kids": 77,
        "poverty": 19
       },
       "Beaumont": {
        "kids": 37,
        "poverty": 13
       }
      },
      "9-12": {
       "Jefferson": {
        "kids": 219,
        "poverty": 27
       },
       "Grant": {
        "kids": 109,
        "poverty": 23
       }
      }
     }
    }
   }
  },
  {
   "run": "sabin_all_keepbc",
   "label": "Sabin into Irvington, Beverly Cleary as is",
   "data_label": "Sabin into Irvington, Beverly Cleary keeps its area",
   "note": "Like “close to home”, but Beverly Cleary's area stays with Beverly Cleary. Built on the previous best (no program swaps).",
   "caveat": "Two blocks (about 2 high-school students) cut off from Cleveland by the feeder rule were given to Jefferson, the school around them, after the solve.",
   "on_map": true,
   "scorecard": "build/solver/out_v2/sabin_all_keepbc/scorecard.json",
   "schools_csv": "build/solver/out_v2/sabin_all_keepbc/schools.csv",
   "tradeoffs": "build/solver/out_v2/sabin_all_keepbc/TRADEOFFS.md",
   "district": {
    "schools_open": 63,
    "pct_sustainable_schools": 92.1,
    "pct_students_in_sustainable": 94.8
   },
   "neighbor_schools": {
    "Sabin": {
     "total_2031": 0,
     "at_target_every_year": false
    },
    "Irvington": {
     "total_2031": 224,
     "at_target_every_year": false
    },
    "MLK Jr": {
     "total_2031": 445,
     "at_target_every_year": true
    },
    "Alameda": {
     "total_2031": 382,
     "at_target_every_year": true
    },
    "Vernon": {
     "total_2031": 364,
     "at_target_every_year": true
    },
    "Beverly Cleary": {
     "total_2031": 361,
     "at_target_every_year": true
    },
    "Boise-Eliot/Humboldt": {
     "total_2031": 370,
     "at_target_every_year": true
    },
    "Rigler": {
     "total_2031": 499,
     "at_target_every_year": true
    },
    "Woodlawn": {
     "total_2031": 361,
     "at_target_every_year": true
    }
   },
   "school_years": {
    "Irvington": {
     "type": "K-5",
     "years": {
      "2027-28": 236.8,
      "2028-29": 235.8,
      "2029-30": 229.6,
      "2030-31": 221.8,
      "2031-32": 223.6,
      "2032-33": 221.8,
      "2033-34": 218.2,
      "2034-35": 213.0,
      "2035-36": 210.1
     }
    },
    "Beverly Cleary": {
     "type": "K-5",
     "years": {
      "2027-28": 394.1,
      "2028-29": 377.9,
      "2029-30": 374.7,
      "2030-31": 365.2,
      "2031-32": 361.1,
      "2032-33": 361.8,
      "2033-34": 351.9,
      "2034-35": 347.2,
      "2035-36": 343.7
     }
    },
    "MLK Jr": {
     "type": "K-5",
     "years": {
      "2027-28": 445.1,
      "2028-29": 455.5,
      "2029-30": 456.9,
      "2030-31": 459.1,
      "2031-32": 444.9,
      "2032-33": 435.8,
      "2033-34": 423.6,
      "2034-35": 407.6,
      "2035-36": 401.7
     }
    },
    "Boise-Eliot/Humboldt": {
     "type": "K-5",
     "years": {
      "2027-28": 375.2,
      "2028-29": 395.8,
      "2029-30": 389.1,
      "2030-31": 387.5,
      "2031-32": 370.0,
      "2032-33": 351.7,
      "2033-34": 336.5,
      "2034-35": 322.2,
      "2035-36": 318.4
     }
    },
    "Vernon": {
     "type": "K-5",
     "years": {
      "2027-28": 389.0,
      "2028-29": 390.4,
      "2029-30": 380.9,
      "2030-31": 370.1,
      "2031-32": 363.9,
      "2032-33": 359.8,
      "2033-34": 356.2,
      "2034-35": 356.2,
      "2035-36": 353.3
     }
    },
    "Alameda": {
     "type": "K-5",
     "years": {
      "2027-28": 386.1,
      "2028-29": 392.1,
      "2029-30": 392.7,
      "2030-31": 387.8,
      "2031-32": 381.5,
      "2032-33": 376.9,
      "2033-34": 369.6,
      "2034-35": 360.9,
      "2035-36": 357.5
     }
    },
    "Beaumont": {
     "type": "6-8",
     "years": {
      "2027-28": 629.0,
      "2028-29": 594.5,
      "2029-30": 595.1,
      "2030-31": 587.8,
      "2031-32": 607.3,
      "2032-33": 613.2,
      "2033-34": 614.5,
      "2034-35": 623.1,
      "2035-36": 613.9
     }
    },
    "Tubman": {
     "type": "6-8",
     "years": {
      "2027-28": 644.5,
      "2028-29": 602.1,
      "2029-30": 581.1,
      "2030-31": 558.3,
      "2031-32": 561.8,
      "2032-33": 560.6,
      "2033-34": 568.8,
      "2034-35": 575.3,
      "2035-36": 566.1
     }
    },
    "Jefferson": {
     "type": "9-12",
     "years": {
      "2027-28": 888.3,
      "2028-29": 1099.0,
      "2029-30": 1246.8,
      "2030-31": 1390.6,
      "2031-32": 1396.7,
      "2032-33": 1373.0,
      "2033-34": 1355.3,
      "2034-35": 1327.8,
      "2035-36": 1337.8
     }
    },
    "Grant": {
     "type": "9-12",
     "years": {
      "2027-28": 1685.4,
      "2028-29": 1599.8,
      "2029-30": 1512.3,
      "2030-31": 1405.4,
      "2031-32": 1332.4,
      "2032-33": 1254.1,
      "2033-34": 1202.9,
      "2034-35": 1145.1,
      "2035-36": 1124.1
     }
    }
   },
   "areas": {
    "Sabin": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 66.6409,
        "mv": 100.0,
        "walk": 0.6014,
        "dwalk": 0.1244,
        "in1": 99.1712,
        "bus": 0.8288,
        "sust": 89.6376,
        "pps": 89.6376
       },
       "oth": {
        "n": 169.2329,
        "mv": 100.0,
        "walk": 0.6197,
        "dwalk": 0.174,
        "in1": 99.6277,
        "bus": 0.3723,
        "sust": 82.1925,
        "pps": 82.1925
       }
      },
      "6-8": {
       "pov": {
        "n": 23.0294,
        "mv": 14.2709,
        "walk": 1.6475,
        "dwalk": -0.0957,
        "in1": 1.4278,
        "bus": 55.5862,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 70.1338,
        "mv": 24.9908,
        "walk": 1.6234,
        "dwalk": -0.1936,
        "in1": 3.8939,
        "bus": 49.8718,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 70.6614,
        "mv": 16.19,
        "walk": 1.43,
        "dwalk": -0.1227,
        "sust": 16.19,
        "pps": 100.0
       },
       "oth": {
        "n": 149.8511,
        "mv": 27.1243,
        "walk": 1.5993,
        "dwalk": -0.1825,
        "sust": 27.1243,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Vernon": {
        "kids": 75,
        "poverty": 20
       },
       "MLK Jr": {
        "kids": 68,
        "poverty": 30
       },
       "Alameda": {
        "kids": 56,
        "poverty": 10
       },
       "Irvington": {
        "kids": 37,
        "poverty": 7
       }
      },
      "6-8": {
       "Tubman": {
        "kids": 72,
        "poverty": 20
       },
       "Beaumont": {
        "kids": 21,
        "poverty": 3
       }
      },
      "9-12": {
       "Jefferson": {
        "kids": 168,
        "poverty": 59
       },
       "Grant": {
        "kids": 52,
        "poverty": 11
       }
      }
     }
    },
    "Irvington": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 46.4941,
        "mv": 31.7488,
        "walk": 0.4778,
        "dwalk": -0.1218,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 31.7488,
        "pps": 31.7488
       },
       "oth": {
        "n": 176.5054,
        "mv": 23.7777,
        "walk": 0.441,
        "dwalk": -0.0801,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 23.7777,
        "pps": 23.7777
       }
      },
      "6-8": {
       "pov": {
        "n": 32.067,
        "mv": 32.7875,
        "walk": 1.2468,
        "dwalk": 0.049,
        "in1": 33.1396,
        "bus": 30.5539,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 81.8647,
        "mv": 23.8795,
        "walk": 1.248,
        "dwalk": -0.0203,
        "in1": 20.637,
        "bus": 17.8405,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 50.8122,
        "mv": 63.3337,
        "walk": 1.8472,
        "dwalk": 0.5612,
        "sust": 36.6663,
        "pps": 100.0
       },
       "oth": {
        "n": 277.1536,
        "mv": 74.995,
        "walk": 1.9486,
        "dwalk": 0.6793,
        "sust": 25.005,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Irvington": {
        "kids": 166,
        "poverty": 32
       },
       "Beverly Cleary": {
        "kids": 51,
        "poverty": 14
       },
       "Alameda": {
        "kids": 5,
        "poverty": 0
       }
      },
      "6-8": {
       "Tubman": {
        "kids": 84,
        "poverty": 22
       },
       "Beaumont": {
        "kids": 30,
        "poverty": 11
       }
      },
      "9-12": {
       "Jefferson": {
        "kids": 240,
        "poverty": 32
       },
       "Grant": {
        "kids": 88,
        "poverty": 19
       }
      }
     }
    }
   }
  },
  {
   "run": "irv_sabin",
   "label": "Irvington into Sabin",
   "data_label": "Irvington into Sabin",
   "note": "Built on the previous best (no program swaps). Irvington closes; Sabin's building stays open.",
   "caveat": "Sabin stays open below PPS's 360 (exempt from the size floor), so Sabin-area kids stay close to home but most are not in a school PPS counts as sustainable (see the table below).",
   "on_map": true,
   "scorecard": "build/solver/out_v2/irv_sabin/scorecard.json",
   "schools_csv": "build/solver/out_v2/irv_sabin/schools.csv",
   "tradeoffs": "build/solver/out_v2/irv_sabin/TRADEOFFS.md",
   "district": {
    "schools_open": 63,
    "pct_sustainable_schools": 93.7,
    "pct_students_in_sustainable": 96.2
   },
   "neighbor_schools": {
    "Sabin": {
     "total_2031": 237,
     "at_target_every_year": false
    },
    "Irvington": {
     "total_2031": 0,
     "at_target_every_year": false
    },
    "MLK Jr": {
     "total_2031": 405,
     "at_target_every_year": true
    },
    "Alameda": {
     "total_2031": 361,
     "at_target_every_year": true
    },
    "Vernon": {
     "total_2031": 361,
     "at_target_every_year": true
    },
    "Beverly Cleary": {
     "total_2031": 417,
     "at_target_every_year": true
    },
    "Boise-Eliot/Humboldt": {
     "total_2031": 377,
     "at_target_every_year": true
    },
    "Rigler": {
     "total_2031": 496,
     "at_target_every_year": true
    },
    "Woodlawn": {
     "total_2031": 361,
     "at_target_every_year": true
    }
   },
   "school_years": {
    "Sabin": {
     "type": "K-5",
     "years": {
      "2027-28": 244.1,
      "2028-29": 250.0,
      "2029-30": 242.2,
      "2030-31": 234.8,
      "2031-32": 236.6,
      "2032-33": 234.3,
      "2033-34": 230.8,
      "2034-35": 225.1,
      "2035-36": 222.0
     }
    },
    "Beverly Cleary": {
     "type": "K-5",
     "years": {
      "2027-28": 452.8,
      "2028-29": 436.3,
      "2029-30": 431.4,
      "2030-31": 419.7,
      "2031-32": 416.6,
      "2032-33": 416.5,
      "2033-34": 406.0,
      "2034-35": 399.7,
      "2035-36": 395.4
     }
    },
    "MLK Jr": {
     "type": "K-5",
     "years": {
      "2027-28": 405.0,
      "2028-29": 413.4,
      "2029-30": 416.1,
      "2030-31": 419.3,
      "2031-32": 405.0,
      "2032-33": 396.4,
      "2033-34": 384.8,
      "2034-35": 369.8,
      "2035-36": 364.4
     }
    },
    "Boise-Eliot/Humboldt": {
     "type": "K-5",
     "years": {
      "2027-28": 382.6,
      "2028-29": 403.2,
      "2029-30": 396.6,
      "2030-31": 394.9,
      "2031-32": 377.3,
      "2032-33": 358.8,
      "2033-34": 343.5,
      "2034-35": 329.0,
      "2035-36": 325.1
     }
    },
    "Vernon": {
     "type": "K-5",
     "years": {
      "2027-28": 386.2,
      "2028-29": 387.3,
      "2029-30": 377.6,
      "2030-31": 367.0,
      "2031-32": 360.6,
      "2032-33": 356.3,
      "2033-34": 352.8,
      "2034-35": 352.8,
      "2035-36": 349.9
     }
    },
    "Alameda": {
     "type": "K-5",
     "years": {
      "2027-28": 367.6,
      "2028-29": 370.5,
      "2029-30": 372.2,
      "2030-31": 367.7,
      "2031-32": 361.1,
      "2032-33": 357.1,
      "2033-34": 349.7,
      "2034-35": 341.8,
      "2035-36": 338.7
     }
    },
    "Beaumont": {
     "type": "6-8",
     "years": {
      "2027-28": 650.8,
      "2028-29": 623.5,
      "2029-30": 622.6,
      "2030-31": 616.1,
      "2031-32": 637.8,
      "2032-33": 639.4,
      "2033-34": 643.8,
      "2034-35": 651.8,
      "2035-36": 642.3
     }
    },
    "Tubman": {
     "type": "6-8",
     "years": {
      "2027-28": 619.3,
      "2028-29": 575.9,
      "2029-30": 556.3,
      "2030-31": 536.1,
      "2031-32": 537.2,
      "2032-33": 540.6,
      "2033-34": 544.7,
      "2034-35": 549.3,
      "2035-36": 540.0
     }
    },
    "Jefferson": {
     "type": "9-12",
     "years": {
      "2027-28": 563.0,
      "2028-29": 803.6,
      "2029-30": 979.2,
      "2030-31": 1155.9,
      "2031-32": 1180.9,
      "2032-33": 1175.9,
      "2033-34": 1170.9,
      "2034-35": 1156.9,
      "2035-36": 1172.9
     }
    },
    "Grant": {
     "type": "9-12",
     "years": {
      "2027-28": 1935.0,
      "2028-29": 1822.0,
      "2029-30": 1713.0,
      "2030-31": 1576.0,
      "2031-32": 1487.0,
      "2032-33": 1394.0,
      "2033-34": 1332.0,
      "2034-35": 1263.0,
      "2035-36": 1237.0
     }
    }
   },
   "areas": {
    "Sabin": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 66.6409,
        "mv": 42.1554,
        "walk": 0.4533,
        "dwalk": -0.0236,
        "in1": 99.1979,
        "bus": 0.8021,
        "sust": 42.1554,
        "pps": 42.1554
       },
       "oth": {
        "n": 169.2329,
        "mv": 36.7216,
        "walk": 0.4554,
        "dwalk": 0.0098,
        "in1": 97.6641,
        "bus": 2.3359,
        "sust": 36.7216,
        "pps": 36.7216
       }
      },
      "6-8": {
       "pov": {
        "n": 23.0294,
        "mv": 42.2584,
        "walk": 1.6567,
        "dwalk": -0.0865,
        "in1": 1.4278,
        "bus": 68.5168,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 70.1338,
        "mv": 35.3367,
        "walk": 1.607,
        "dwalk": -0.2099,
        "in1": 3.8939,
        "bus": 61.5506,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 70.6614,
        "mv": 0.0,
        "walk": 1.5527,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       },
       "oth": {
        "n": 149.8511,
        "mv": 0.0,
        "walk": 1.7818,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Sabin": {
        "kids": 146,
        "poverty": 39
       },
       "Vernon": {
        "kids": 52,
        "poverty": 14
       },
       "MLK Jr": {
        "kids": 29,
        "poverty": 12
       },
       "Alameda": {
        "kids": 9,
        "poverty": 2
       }
      },
      "6-8": {
       "Tubman": {
        "kids": 59,
        "poverty": 13
       },
       "Beaumont": {
        "kids": 23,
        "poverty": 5
       },
       "Ockley Green": {
        "kids": 12,
        "poverty": 4
       }
      },
      "9-12": {
       "Jefferson": {
        "kids": 221,
        "poverty": 71
       }
      }
     }
    },
    "Irvington": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 46.4941,
        "mv": 100.0,
        "walk": 0.9143,
        "dwalk": 0.3146,
        "in1": 60.617,
        "bus": 39.383,
        "sust": 69.1556,
        "pps": 69.1556
       },
       "oth": {
        "n": 176.5054,
        "mv": 100.0,
        "walk": 0.8389,
        "dwalk": 0.3178,
        "in1": 75.6549,
        "bus": 24.3451,
        "sust": 56.8309,
        "pps": 56.8309
       }
      },
      "6-8": {
       "pov": {
        "n": 32.067,
        "mv": 2.4384,
        "walk": 1.1952,
        "dwalk": -0.0026,
        "in1": 33.1396,
        "bus": 29.9668,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 81.8647,
        "mv": 10.3287,
        "walk": 1.2572,
        "dwalk": -0.0111,
        "in1": 20.637,
        "bus": 24.5434,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 50.8122,
        "mv": 0.0,
        "walk": 1.2861,
        "dwalk": 0.0,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 277.1536,
        "mv": 0.0,
        "walk": 1.2693,
        "dwalk": 0.0,
        "sust": 100.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Beverly Cleary": {
        "kids": 115,
        "poverty": 31
       },
       "Sabin": {
        "kids": 91,
        "poverty": 14
       },
       "Alameda": {
        "kids": 18,
        "poverty": 1
       }
      },
      "6-8": {
       "Tubman": {
        "kids": 105,
        "poverty": 31
       },
       "Beaumont": {
        "kids": 9,
        "poverty": 1
       }
      },
      "9-12": {
       "Grant": {
        "kids": 328,
        "poverty": 51
       }
      }
     }
    }
   }
  },
  {
   "run": "irv_sabin_keep",
   "label": "Irvington into Sabin, all of Sabin stays, Vernon as today",
   "data_label": "Irvington into Sabin, all of Sabin stays, Vernon as today",
   "note": "Built on the previous best (no program swaps). Irvington closes; every family in today's Sabin area stays at Sabin, and Vernon keeps today's lines.",
   "caveat": "Sabin and Vernon stay open below PPS's 360 (exempt from the size floor), so every Sabin-area kid stays at Sabin but none are in a school PPS counts as sustainable. About 44 Alameda-area middle schoolers zoned to Rigler go to Roseway Heights instead of Beaumont; that is still to be fixed.",
   "on_map": true,
   "scorecard": "build/solver/out_v2/irv_sabin_keep/scorecard.json",
   "schools_csv": "build/solver/out_v2/irv_sabin_keep/schools.csv",
   "tradeoffs": "build/solver/out_v2/irv_sabin_keep/TRADEOFFS.md",
   "district": {
    "schools_open": 63,
    "pct_sustainable_schools": 92.1,
    "pct_students_in_sustainable": 95.1
   },
   "neighbor_schools": {
    "Sabin": {
     "total_2031": 296,
     "at_target_every_year": false
    },
    "Irvington": {
     "total_2031": 0,
     "at_target_every_year": false
    },
    "MLK Jr": {
     "total_2031": 377,
     "at_target_every_year": true
    },
    "Alameda": {
     "total_2031": 361,
     "at_target_every_year": true
    },
    "Vernon": {
     "total_2031": 289,
     "at_target_every_year": false
    },
    "Beverly Cleary": {
     "total_2031": 439,
     "at_target_every_year": true
    },
    "Boise-Eliot/Humboldt": {
     "total_2031": 377,
     "at_target_every_year": true
    },
    "Rigler": {
     "total_2031": 499,
     "at_target_every_year": true
    },
    "Woodlawn": {
     "total_2031": 361,
     "at_target_every_year": true
    }
   },
   "school_years": {
    "Sabin": {
     "type": "K-5",
     "years": {
      "2027-28": 301.7,
      "2028-29": 312.8,
      "2029-30": 302.9,
      "2030-31": 294.5,
      "2031-32": 296.2,
      "2032-33": 292.9,
      "2033-34": 288.8,
      "2034-35": 281.4,
      "2035-36": 277.6
     }
    },
    "Beverly Cleary": {
     "type": "K-5",
     "years": {
      "2027-28": 477.5,
      "2028-29": 460.5,
      "2029-30": 455.0,
      "2030-31": 442.3,
      "2031-32": 439.5,
      "2032-33": 439.3,
      "2033-34": 428.5,
      "2034-35": 421.6,
      "2035-36": 417.0
     }
    },
    "MLK Jr": {
     "type": "K-5",
     "years": {
      "2027-28": 376.5,
      "2028-29": 383.3,
      "2029-30": 387.1,
      "2030-31": 391.0,
      "2031-32": 376.5,
      "2032-33": 368.3,
      "2033-34": 357.0,
      "2034-35": 342.8,
      "2035-36": 337.7
     }
    },
    "Boise-Eliot/Humboldt": {
     "type": "K-5",
     "years": {
      "2027-28": 382.6,
      "2028-29": 403.2,
      "2029-30": 396.6,
      "2030-31": 394.9,
      "2031-32": 377.3,
      "2032-33": 358.8,
      "2033-34": 343.5,
      "2034-35": 329.0,
      "2035-36": 325.1
     }
    },
    "Vernon": {
     "type": "K-5",
     "years": {
      "2027-28": 313.3,
      "2028-29": 310.9,
      "2029-30": 303.9,
      "2030-31": 295.0,
      "2031-32": 288.6,
      "2032-33": 285.4,
      "2033-34": 282.8,
      "2034-35": 284.7,
      "2035-36": 282.8
     }
    },
    "Alameda": {
     "type": "K-5",
     "years": {
      "2027-28": 367.7,
      "2028-29": 370.1,
      "2029-30": 371.8,
      "2030-31": 367.3,
      "2031-32": 360.8,
      "2032-33": 356.8,
      "2033-34": 349.4,
      "2034-35": 341.5,
      "2035-36": 338.4
     }
    },
    "Beaumont": {
     "type": "6-8",
     "years": {
      "2027-28": 648.1,
      "2028-29": 626.0,
      "2029-30": 632.1,
      "2030-31": 629.8,
      "2031-32": 645.6,
      "2032-33": 642.0,
      "2033-34": 642.7,
      "2034-35": 648.4,
      "2035-36": 639.2
     }
    },
    "Tubman": {
     "type": "6-8",
     "years": {
      "2027-28": 657.2,
      "2028-29": 609.5,
      "2029-30": 588.1,
      "2030-31": 565.6,
      "2031-32": 567.2,
      "2032-33": 570.5,
      "2033-34": 575.1,
      "2034-35": 580.3,
      "2035-36": 570.1
     }
    },
    "Jefferson": {
     "type": "9-12",
     "years": {
      "2027-28": 563.0,
      "2028-29": 803.6,
      "2029-30": 979.2,
      "2030-31": 1155.9,
      "2031-32": 1180.9,
      "2032-33": 1175.9,
      "2033-34": 1170.9,
      "2034-35": 1156.9,
      "2035-36": 1172.9
     }
    },
    "Grant": {
     "type": "9-12",
     "years": {
      "2027-28": 1935.0,
      "2028-29": 1822.0,
      "2029-30": 1713.0,
      "2030-31": 1576.0,
      "2031-32": 1487.0,
      "2032-33": 1394.0,
      "2033-34": 1332.0,
      "2034-35": 1263.0,
      "2035-36": 1237.0
     }
    }
   },
   "areas": {
    "Sabin": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 66.6409,
        "mv": 0.0,
        "walk": 0.477,
        "dwalk": 0.0,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 0.0,
        "pps": 0.0
       },
       "oth": {
        "n": 169.2329,
        "mv": 0.0,
        "walk": 0.4456,
        "dwalk": 0.0,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 0.0,
        "pps": 0.0
       }
      },
      "6-8": {
       "pov": {
        "n": 23.0294,
        "mv": 0.0,
        "walk": 1.7432,
        "dwalk": 0.0,
        "in1": 0.0,
        "bus": 69.857,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 70.1338,
        "mv": 0.0,
        "walk": 1.817,
        "dwalk": 0.0,
        "in1": 0.0,
        "bus": 74.8626,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 70.6614,
        "mv": 0.0,
        "walk": 1.5527,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       },
       "oth": {
        "n": 149.8511,
        "mv": 0.0,
        "walk": 1.7818,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Sabin": {
        "kids": 236,
        "poverty": 67
       }
      },
      "6-8": {
       "Tubman": {
        "kids": 93,
        "poverty": 23
       }
      },
      "9-12": {
       "Jefferson": {
        "kids": 221,
        "poverty": 71
       }
      }
     }
    },
    "Irvington": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 46.4941,
        "mv": 100.0,
        "walk": 0.9269,
        "dwalk": 0.3273,
        "in1": 57.7752,
        "bus": 42.2248,
        "sust": 74.7019,
        "pps": 74.7019
       },
       "oth": {
        "n": 176.5054,
        "mv": 100.0,
        "walk": 0.8763,
        "dwalk": 0.3552,
        "in1": 67.5105,
        "bus": 32.4895,
        "sust": 72.883,
        "pps": 72.883
       }
      },
      "6-8": {
       "pov": {
        "n": 32.067,
        "mv": 3.6257,
        "walk": 1.1989,
        "dwalk": 0.0011,
        "in1": 33.1396,
        "bus": 31.1542,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 81.8647,
        "mv": 15.3711,
        "walk": 1.2717,
        "dwalk": 0.0033,
        "in1": 20.637,
        "bus": 29.5857,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 50.8122,
        "mv": 0.0,
        "walk": 1.2861,
        "dwalk": 0.0,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 277.1536,
        "mv": 0.0,
        "walk": 1.2693,
        "dwalk": 0.0,
        "sust": 100.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Beverly Cleary": {
        "kids": 138,
        "poverty": 33
       },
       "Sabin": {
        "kids": 60,
        "poverty": 12
       },
       "Alameda": {
        "kids": 26,
        "poverty": 2
       }
      },
      "6-8": {
       "Tubman": {
        "kids": 100,
        "poverty": 31
       },
       "Beaumont": {
        "kids": 14,
        "poverty": 1
       }
      },
      "9-12": {
       "Grant": {
        "kids": 328,
        "poverty": 51
       }
      }
     }
    }
   }
  },
  {
   "run": "irv_sabin_whole",
   "label": "Irvington into Sabin, all of Sabin stays, then Tubman and Jefferson",
   "data_label": "Irvington into Sabin, all of Sabin stays, then Tubman and Jefferson",
   "note": "As “all of Sabin stays”, but the whole Sabin area goes on to Tubman, then Jefferson. Built on the previous best (no program swaps).",
   "caveat": "Sabin and Vernon stay open below PPS's 360 (exempt from the size floor), so every Sabin-area kid stays at Sabin but none are in a school PPS counts as sustainable. About 44 Alameda-area middle schoolers zoned to Rigler go to Roseway Heights instead of Beaumont; that is still to be fixed.",
   "on_map": true,
   "scorecard": "build/solver/out_v2/irv_sabin_whole/scorecard.json",
   "schools_csv": "build/solver/out_v2/irv_sabin_whole/schools.csv",
   "tradeoffs": "build/solver/out_v2/irv_sabin_whole/TRADEOFFS.md",
   "district": {
    "schools_open": 63,
    "pct_sustainable_schools": 92.1,
    "pct_students_in_sustainable": 95.2
   },
   "neighbor_schools": {
    "Sabin": {
     "total_2031": 296,
     "at_target_every_year": false
    },
    "Irvington": {
     "total_2031": 0,
     "at_target_every_year": false
    },
    "MLK Jr": {
     "total_2031": 377,
     "at_target_every_year": true
    },
    "Alameda": {
     "total_2031": 361,
     "at_target_every_year": true
    },
    "Vernon": {
     "total_2031": 289,
     "at_target_every_year": false
    },
    "Beverly Cleary": {
     "total_2031": 439,
     "at_target_every_year": true
    },
    "Boise-Eliot/Humboldt": {
     "total_2031": 377,
     "at_target_every_year": true
    },
    "Rigler": {
     "total_2031": 499,
     "at_target_every_year": true
    },
    "Woodlawn": {
     "total_2031": 361,
     "at_target_every_year": true
    }
   },
   "school_years": {
    "Sabin": {
     "type": "K-5",
     "years": {
      "2027-28": 301.7,
      "2028-29": 312.8,
      "2029-30": 302.9,
      "2030-31": 294.5,
      "2031-32": 296.2,
      "2032-33": 292.9,
      "2033-34": 288.8,
      "2034-35": 281.4,
      "2035-36": 277.6
     }
    },
    "Beverly Cleary": {
     "type": "K-5",
     "years": {
      "2027-28": 477.5,
      "2028-29": 460.5,
      "2029-30": 455.0,
      "2030-31": 442.3,
      "2031-32": 439.5,
      "2032-33": 439.3,
      "2033-34": 428.5,
      "2034-35": 421.6,
      "2035-36": 417.0
     }
    },
    "MLK Jr": {
     "type": "K-5",
     "years": {
      "2027-28": 376.5,
      "2028-29": 383.3,
      "2029-30": 387.1,
      "2030-31": 391.0,
      "2031-32": 376.5,
      "2032-33": 368.3,
      "2033-34": 357.0,
      "2034-35": 342.8,
      "2035-36": 337.7
     }
    },
    "Boise-Eliot/Humboldt": {
     "type": "K-5",
     "years": {
      "2027-28": 382.6,
      "2028-29": 403.2,
      "2029-30": 396.6,
      "2030-31": 394.9,
      "2031-32": 377.3,
      "2032-33": 358.8,
      "2033-34": 343.5,
      "2034-35": 329.0,
      "2035-36": 325.1
     }
    },
    "Vernon": {
     "type": "K-5",
     "years": {
      "2027-28": 313.3,
      "2028-29": 310.9,
      "2029-30": 303.9,
      "2030-31": 295.0,
      "2031-32": 288.6,
      "2032-33": 285.4,
      "2033-34": 282.8,
      "2034-35": 284.7,
      "2035-36": 282.8
     }
    },
    "Alameda": {
     "type": "K-5",
     "years": {
      "2027-28": 367.7,
      "2028-29": 370.1,
      "2029-30": 371.8,
      "2030-31": 367.3,
      "2031-32": 360.8,
      "2032-33": 356.8,
      "2033-34": 349.4,
      "2034-35": 341.5,
      "2035-36": 338.4
     }
    },
    "Beaumont": {
     "type": "6-8",
     "years": {
      "2027-28": 570.9,
      "2028-29": 536.4,
      "2029-30": 538.9,
      "2030-31": 531.6,
      "2031-32": 546.3,
      "2032-33": 549.6,
      "2033-34": 549.0,
      "2034-35": 558.2,
      "2035-36": 550.1
     }
    },
    "Tubman": {
     "type": "6-8",
     "years": {
      "2027-28": 590.8,
      "2028-29": 554.2,
      "2029-30": 536.3,
      "2030-31": 516.4,
      "2031-32": 519.4,
      "2032-33": 518.3,
      "2033-34": 526.1,
      "2034-35": 531.8,
      "2035-36": 523.7
     }
    },
    "Jefferson": {
     "type": "9-12",
     "years": {
      "2027-28": 675.4,
      "2028-29": 909.2,
      "2029-30": 1078.2,
      "2030-31": 1246.2,
      "2031-32": 1265.5,
      "2032-33": 1254.6,
      "2033-34": 1245.4,
      "2034-35": 1226.9,
      "2035-36": 1241.1
     }
    },
    "Grant": {
     "type": "9-12",
     "years": {
      "2027-28": 1822.6,
      "2028-29": 1716.3,
      "2029-30": 1614.0,
      "2030-31": 1485.7,
      "2031-32": 1402.4,
      "2032-33": 1315.3,
      "2033-34": 1257.5,
      "2034-35": 1193.1,
      "2035-36": 1168.8
     }
    }
   },
   "areas": {
    "Sabin": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 66.6409,
        "mv": 0.0,
        "walk": 0.477,
        "dwalk": 0.0,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 0.0,
        "pps": 0.0
       },
       "oth": {
        "n": 169.2329,
        "mv": 0.0,
        "walk": 0.4456,
        "dwalk": 0.0,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 0.0,
        "pps": 0.0
       }
      },
      "6-8": {
       "pov": {
        "n": 23.0294,
        "mv": 0.0,
        "walk": 1.7432,
        "dwalk": 0.0,
        "in1": 0.0,
        "bus": 69.857,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 70.1338,
        "mv": 0.0,
        "walk": 1.817,
        "dwalk": 0.0,
        "in1": 0.0,
        "bus": 74.8626,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 70.6614,
        "mv": 0.0,
        "walk": 1.5527,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       },
       "oth": {
        "n": 149.8511,
        "mv": 0.0,
        "walk": 1.7818,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Sabin": {
        "kids": 236,
        "poverty": 67
       }
      },
      "6-8": {
       "Tubman": {
        "kids": 93,
        "poverty": 23
       }
      },
      "9-12": {
       "Jefferson": {
        "kids": 221,
        "poverty": 71
       }
      }
     }
    },
    "Irvington": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 46.4941,
        "mv": 100.0,
        "walk": 0.9269,
        "dwalk": 0.3273,
        "in1": 57.7752,
        "bus": 42.2248,
        "sust": 74.7019,
        "pps": 74.7019
       },
       "oth": {
        "n": 176.5054,
        "mv": 100.0,
        "walk": 0.8763,
        "dwalk": 0.3552,
        "in1": 67.5105,
        "bus": 32.4895,
        "sust": 72.883,
        "pps": 72.883
       }
      },
      "6-8": {
       "pov": {
        "n": 32.067,
        "mv": 76.4597,
        "walk": 1.6544,
        "dwalk": 0.4566,
        "in1": 21.2253,
        "bus": 70.9325,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 81.8647,
        "mv": 75.0109,
        "walk": 1.5513,
        "dwalk": 0.283,
        "in1": 12.7786,
        "bus": 56.4741,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 50.8122,
        "mv": 21.7639,
        "walk": 1.3179,
        "dwalk": 0.0318,
        "sust": 78.2361,
        "pps": 100.0
       },
       "oth": {
        "n": 277.1536,
        "mv": 26.5446,
        "walk": 1.3294,
        "dwalk": 0.06,
        "sust": 73.4554,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Beverly Cleary": {
        "kids": 138,
        "poverty": 33
       },
       "Sabin": {
        "kids": 60,
        "poverty": 12
       },
       "Alameda": {
        "kids": 26,
        "poverty": 2
       }
      },
      "6-8": {
       "Beaumont": {
        "kids": 86,
        "poverty": 25
       },
       "Tubman": {
        "kids": 28,
        "poverty": 8
       }
      },
      "9-12": {
       "Grant": {
        "kids": 243,
        "poverty": 40
       },
       "Jefferson": {
        "kids": 85,
        "poverty": 11
       }
      }
     }
    }
   }
  },
  {
   "run": "irv_sabin_noala",
   "label": "Sabin Stays - less moves",
   "data_label": "Sabin Stays - less moves",
   "note": "Built on the previous best (no program swaps), without its big-school relief. Irvington closes; every Alameda- and Sabin-area family stays at its own school, Vernon keeps today's lines, and all of Sabin goes on to Tubman, then Jefferson.",
   "caveat": null,
   "on_map": true,
   "scorecard": "build/solver/out_v2/irv_sabin_noala/scorecard.json",
   "schools_csv": "build/solver/out_v2/irv_sabin_noala/schools.csv",
   "tradeoffs": "build/solver/out_v2/irv_sabin_noala/TRADEOFFS.md",
   "district": {
    "schools_open": 63,
    "pct_sustainable_schools": 92.1,
    "pct_students_in_sustainable": 95.2
   },
   "neighbor_schools": {
    "Sabin": {
     "total_2031": 308,
     "at_target_every_year": false
    },
    "Irvington": {
     "total_2031": 0,
     "at_target_every_year": false
    },
    "MLK Jr": {
     "total_2031": 377,
     "at_target_every_year": true
    },
    "Alameda": {
     "total_2031": 525,
     "at_target_every_year": true
    },
    "Vernon": {
     "total_2031": 289,
     "at_target_every_year": false
    },
    "Beverly Cleary": {
     "total_2031": 385,
     "at_target_every_year": true
    },
    "Boise-Eliot/Humboldt": {
     "total_2031": 377,
     "at_target_every_year": true
    },
    "Rigler": {
     "total_2031": 377,
     "at_target_every_year": true
    },
    "Woodlawn": {
     "total_2031": 361,
     "at_target_every_year": true
    }
   },
   "school_years": {
    "Sabin": {
     "type": "K-5",
     "years": {
      "2027-28": 314.0,
      "2028-29": 324.9,
      "2029-30": 314.7,
      "2030-31": 305.8,
      "2031-32": 307.6,
      "2032-33": 304.3,
      "2033-34": 300.0,
      "2034-35": 292.4,
      "2035-36": 288.4
     }
    },
    "Beverly Cleary": {
     "type": "K-5",
     "years": {
      "2027-28": 421.6,
      "2028-29": 404.3,
      "2029-30": 398.5,
      "2030-31": 386.6,
      "2031-32": 384.7,
      "2032-33": 385.2,
      "2033-34": 375.4,
      "2034-35": 369.8,
      "2035-36": 365.6
     }
    },
    "MLK Jr": {
     "type": "K-5",
     "years": {
      "2027-28": 376.5,
      "2028-29": 383.3,
      "2029-30": 387.1,
      "2030-31": 391.0,
      "2031-32": 376.5,
      "2032-33": 368.3,
      "2033-34": 357.0,
      "2034-35": 342.8,
      "2035-36": 337.7
     }
    },
    "Boise-Eliot/Humboldt": {
     "type": "K-5",
     "years": {
      "2027-28": 382.6,
      "2028-29": 403.2,
      "2029-30": 396.6,
      "2030-31": 394.9,
      "2031-32": 377.3,
      "2032-33": 358.8,
      "2033-34": 343.5,
      "2034-35": 329.0,
      "2035-36": 325.1
     }
    },
    "Vernon": {
     "type": "K-5",
     "years": {
      "2027-28": 313.3,
      "2028-29": 310.9,
      "2029-30": 303.9,
      "2030-31": 295.0,
      "2031-32": 288.6,
      "2032-33": 285.4,
      "2033-34": 282.8,
      "2034-35": 284.7,
      "2035-36": 282.8
     }
    },
    "Alameda": {
     "type": "K-5",
     "years": {
      "2027-28": 534.1,
      "2028-29": 538.3,
      "2029-30": 541.5,
      "2030-31": 535.4,
      "2031-32": 525.4,
      "2032-33": 519.4,
      "2033-34": 508.6,
      "2034-35": 497.0,
      "2035-36": 492.6
     }
    },
    "Beaumont": {
     "type": "6-8",
     "years": {
      "2027-28": 609.7,
      "2028-29": 573.7,
      "2029-30": 574.3,
      "2030-31": 566.3,
      "2031-32": 583.4,
      "2032-33": 587.8,
      "2033-34": 588.2,
      "2034-35": 597.3,
      "2035-36": 588.5
     }
    },
    "Tubman": {
     "type": "6-8",
     "years": {
      "2027-28": 599.1,
      "2028-29": 561.6,
      "2029-30": 543.3,
      "2030-31": 523.0,
      "2031-32": 526.0,
      "2032-33": 524.9,
      "2033-34": 532.8,
      "2034-35": 538.6,
      "2035-36": 530.3
     }
    },
    "Jefferson": {
     "type": "9-12",
     "years": {
      "2027-28": 702.1,
      "2028-29": 934.3,
      "2029-30": 1101.7,
      "2030-31": 1267.6,
      "2031-32": 1285.6,
      "2032-33": 1273.2,
      "2033-34": 1263.1,
      "2034-35": 1243.4,
      "2035-36": 1257.2
     }
    },
    "Grant": {
     "type": "9-12",
     "years": {
      "2027-28": 1795.9,
      "2028-29": 1691.3,
      "2029-30": 1590.5,
      "2030-31": 1464.3,
      "2031-32": 1382.3,
      "2032-33": 1296.7,
      "2033-34": 1239.8,
      "2034-35": 1176.5,
      "2035-36": 1152.7
     }
    }
   },
   "areas": {
    "Sabin": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 66.6409,
        "mv": 0.0,
        "walk": 0.477,
        "dwalk": 0.0,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 0.0,
        "pps": 0.0
       },
       "oth": {
        "n": 169.2329,
        "mv": 0.0,
        "walk": 0.4456,
        "dwalk": 0.0,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 0.0,
        "pps": 0.0
       }
      },
      "6-8": {
       "pov": {
        "n": 23.0294,
        "mv": 0.0,
        "walk": 1.7432,
        "dwalk": 0.0,
        "in1": 0.0,
        "bus": 69.857,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 70.1338,
        "mv": 0.0,
        "walk": 1.817,
        "dwalk": 0.0,
        "in1": 0.0,
        "bus": 74.8626,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 70.6614,
        "mv": 0.0,
        "walk": 1.5527,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       },
       "oth": {
        "n": 149.8511,
        "mv": 0.0,
        "walk": 1.7818,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Sabin": {
        "kids": 236,
        "poverty": 67
       }
      },
      "6-8": {
       "Tubman": {
        "kids": 93,
        "poverty": 23
       }
      },
      "9-12": {
       "Jefferson": {
        "kids": 221,
        "poverty": 71
       }
      }
     }
    },
    "Irvington": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 46.4941,
        "mv": 100.0,
        "walk": 0.9209,
        "dwalk": 0.3213,
        "in1": 58.9483,
        "bus": 41.0517,
        "sust": 72.8726,
        "pps": 72.8726
       },
       "oth": {
        "n": 176.5054,
        "mv": 100.0,
        "walk": 0.8569,
        "dwalk": 0.3358,
        "in1": 70.8561,
        "bus": 29.1439,
        "sust": 66.8672,
        "pps": 66.8672
       }
      },
      "6-8": {
       "pov": {
        "n": 32.067,
        "mv": 74.3173,
        "walk": 1.6402,
        "dwalk": 0.4424,
        "in1": 21.5413,
        "bus": 68.7901,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 81.8647,
        "mv": 67.7558,
        "walk": 1.5076,
        "dwalk": 0.2393,
        "in1": 13.6936,
        "bus": 49.219,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 50.8122,
        "mv": 24.142,
        "walk": 1.3407,
        "dwalk": 0.0547,
        "sust": 75.858,
        "pps": 100.0
       },
       "oth": {
        "n": 277.1536,
        "mv": 33.3446,
        "walk": 1.3931,
        "dwalk": 0.1238,
        "sust": 66.6554,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Beverly Cleary": {
        "kids": 131,
        "poverty": 33
       },
       "Sabin": {
        "kids": 71,
        "poverty": 13
       },
       "Alameda": {
        "kids": 21,
        "poverty": 1
       }
      },
      "6-8": {
       "Beaumont": {
        "kids": 79,
        "poverty": 24
       },
       "Tubman": {
        "kids": 35,
        "poverty": 8
       }
      },
      "9-12": {
       "Grant": {
        "kids": 223,
        "poverty": 39
       },
       "Jefferson": {
        "kids": 105,
        "poverty": 12
       }
      }
     }
    }
   }
  },
  {
   "run": "irv_sabin_thompson21",
   "label": "Irvington line: Thompson / 21st / Knott",
   "data_label": "Irvington line: Thompson / 21st / Knott",
   "note": "Follows the shorter walk: about 7 kids go to the farther school.",
   "caveat": "Not a separate solve: the NE 15th + Knott plan with only Irvington's blocks moved to the Thompson / 21st / Knott line, then re-scored. The rest of the district is the same in both.",
   "on_map": true,
   "scorecard": "build/solver/out_v2/irv_sabin_thompson21/scorecard.json",
   "schools_csv": "build/solver/out_v2/irv_sabin_thompson21/schools.csv",
   "tradeoffs": "build/solver/out_v2/irv_sabin_thompson21/TRADEOFFS.md",
   "district": {
    "schools_open": 63,
    "pct_sustainable_schools": 90.5,
    "pct_students_in_sustainable": 94.0
   },
   "neighbor_schools": {
    "Sabin": {
     "total_2031": 355,
     "at_target_every_year": false
    },
    "Irvington": {
     "total_2031": 0,
     "at_target_every_year": false
    },
    "MLK Jr": {
     "total_2031": 377,
     "at_target_every_year": true
    },
    "Alameda": {
     "total_2031": 505,
     "at_target_every_year": true
    },
    "Vernon": {
     "total_2031": 289,
     "at_target_every_year": false
    },
    "Beverly Cleary": {
     "total_2031": 357,
     "at_target_every_year": false
    },
    "Boise-Eliot/Humboldt": {
     "total_2031": 379,
     "at_target_every_year": true
    },
    "Rigler": {
     "total_2031": 377,
     "at_target_every_year": true
    },
    "Woodlawn": {
     "total_2031": 361,
     "at_target_every_year": true
    }
   },
   "school_years": {
    "Sabin": {
     "type": "K-5",
     "years": {
      "2027-28": 364.8,
      "2028-29": 374.8,
      "2029-30": 363.1,
      "2030-31": 352.3,
      "2031-32": 354.8,
      "2032-33": 351.2,
      "2033-34": 346.1,
      "2034-35": 337.4,
      "2035-36": 332.8
     }
    },
    "Beverly Cleary": {
     "type": "K-5",
     "years": {
      "2027-28": 391.4,
      "2028-29": 374.6,
      "2029-30": 369.6,
      "2030-31": 358.8,
      "2031-32": 356.6,
      "2032-33": 357.2,
      "2033-34": 347.9,
      "2034-35": 342.9,
      "2035-36": 339.1
     }
    },
    "MLK Jr": {
     "type": "K-5",
     "years": {
      "2027-28": 376.5,
      "2028-29": 383.3,
      "2029-30": 387.1,
      "2030-31": 391.0,
      "2031-32": 376.5,
      "2032-33": 368.3,
      "2033-34": 357.0,
      "2034-35": 342.8,
      "2035-36": 337.7
     }
    },
    "Boise-Eliot/Humboldt": {
     "type": "K-5",
     "years": {
      "2027-28": 384.2,
      "2028-29": 404.8,
      "2029-30": 398.2,
      "2030-31": 396.5,
      "2031-32": 378.8,
      "2032-33": 360.3,
      "2033-34": 345.0,
      "2034-35": 330.5,
      "2035-36": 326.5
     }
    },
    "Vernon": {
     "type": "K-5",
     "years": {
      "2027-28": 313.3,
      "2028-29": 310.9,
      "2029-30": 303.9,
      "2030-31": 295.0,
      "2031-32": 288.6,
      "2032-33": 285.4,
      "2033-34": 282.8,
      "2034-35": 284.7,
      "2035-36": 282.8
     }
    },
    "Alameda": {
     "type": "K-5",
     "years": {
      "2027-28": 512.0,
      "2028-29": 516.5,
      "2029-30": 520.4,
      "2030-31": 515.1,
      "2031-32": 504.8,
      "2032-33": 498.9,
      "2033-34": 488.5,
      "2034-35": 477.4,
      "2035-36": 473.3
     }
    },
    "Beaumont": {
     "type": "6-8",
     "years": {
      "2027-28": 577.5,
      "2028-29": 545.1,
      "2029-30": 547.2,
      "2030-31": 541.2,
      "2031-32": 557.9,
      "2032-33": 562.4,
      "2033-34": 562.4,
      "2034-35": 571.0,
      "2035-36": 562.9
     }
    },
    "Tubman": {
     "type": "6-8",
     "years": {
      "2027-28": 631.4,
      "2028-29": 590.1,
      "2029-30": 570.4,
      "2030-31": 548.0,
      "2031-32": 551.5,
      "2032-33": 550.3,
      "2033-34": 558.6,
      "2034-35": 564.9,
      "2035-36": 555.9
     }
    },
    "Jefferson": {
     "type": "9-12",
     "years": {
      "2027-28": 800.5,
      "2028-29": 1026.8,
      "2029-30": 1188.4,
      "2030-31": 1346.7,
      "2031-32": 1359.6,
      "2032-33": 1342.1,
      "2033-34": 1328.3,
      "2034-35": 1304.6,
      "2035-36": 1316.9
     }
    },
    "Grant": {
     "type": "9-12",
     "years": {
      "2027-28": 1697.6,
      "2028-29": 1598.8,
      "2029-30": 1503.9,
      "2030-31": 1385.3,
      "2031-32": 1308.3,
      "2032-33": 1227.8,
      "2033-34": 1174.6,
      "2034-35": 1115.3,
      "2035-36": 1093.0
     }
    }
   },
   "areas": {
    "Sabin": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 66.6409,
        "mv": 0.0,
        "walk": 0.477,
        "dwalk": 0.0,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 0.0,
        "pps": 0.0
       },
       "oth": {
        "n": 169.2329,
        "mv": 0.0,
        "walk": 0.4456,
        "dwalk": 0.0,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 0.0,
        "pps": 0.0
       }
      },
      "6-8": {
       "pov": {
        "n": 23.0294,
        "mv": 0.0,
        "walk": 1.7432,
        "dwalk": 0.0,
        "in1": 0.0,
        "bus": 69.857,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 70.1338,
        "mv": 0.0,
        "walk": 1.817,
        "dwalk": 0.0,
        "in1": 0.0,
        "bus": 74.8626,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 70.6614,
        "mv": 0.0,
        "walk": 1.5527,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       },
       "oth": {
        "n": 149.8511,
        "mv": 0.0,
        "walk": 1.7818,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Sabin": {
        "kids": 236,
        "poverty": 67
       }
      },
      "6-8": {
       "Tubman": {
        "kids": 93,
        "poverty": 23
       }
      },
      "9-12": {
       "Jefferson": {
        "kids": 221,
        "poverty": 71
       }
      }
     }
    },
    "Irvington": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 46.4941,
        "mv": 100.0,
        "walk": 0.9171,
        "dwalk": 0.3174,
        "in1": 60.3541,
        "bus": 39.6459,
        "sust": 0.0,
        "pps": 0.0
       },
       "oth": {
        "n": 176.5054,
        "mv": 100.0,
        "walk": 0.8504,
        "dwalk": 0.3293,
        "in1": 74.8746,
        "bus": 25.1254,
        "sust": 0.0,
        "pps": 0.0
       }
      },
      "6-8": {
       "pov": {
        "n": 32.067,
        "mv": 66.0595,
        "walk": 1.6016,
        "dwalk": 0.4038,
        "in1": 22.7387,
        "bus": 64.0844,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 81.8647,
        "mv": 40.5669,
        "walk": 1.4081,
        "dwalk": 0.1397,
        "in1": 16.3317,
        "bus": 37.0763,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 50.8122,
        "mv": 33.3635,
        "walk": 1.4529,
        "dwalk": 0.1669,
        "sust": 66.6365,
        "pps": 100.0
       },
       "oth": {
        "n": 277.1536,
        "mv": 58.3798,
        "walk": 1.7054,
        "dwalk": 0.4361,
        "sust": 41.6202,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Sabin": {
        "kids": 118,
        "poverty": 16
       },
       "Beverly Cleary": {
        "kids": 105,
        "poverty": 30
       }
      },
      "6-8": {
       "Tubman": {
        "kids": 60,
        "poverty": 11
       },
       "Beaumont": {
        "kids": 54,
        "poverty": 21
       }
      },
      "9-12": {
       "Jefferson": {
        "kids": 179,
        "poverty": 17
       },
       "Grant": {
        "kids": 149,
        "poverty": 34
       }
      }
     }
    }
   }
  },
  {
   "run": "irv_sabin_knott",
   "label": "Irvington line: NE Knott",
   "data_label": "Irvington line: NE Knott",
   "note": "Beverly Cleary grows to about 414, but Sabin stays at about 297, well under 360; about 58 kids walk to the farther school (estimate).",
   "caveat": "Not a separate solve: the NE 15th + Knott plan with only Irvington's blocks moved to the NE Knott line, then re-scored. The rest of the district is the same in both.",
   "on_map": true,
   "scorecard": "build/solver/out_v2/irv_sabin_knott/scorecard.json",
   "schools_csv": "build/solver/out_v2/irv_sabin_knott/schools.csv",
   "tradeoffs": null,
   "district": {
    "schools_open": 63,
    "pct_sustainable_schools": 92.1,
    "pct_students_in_sustainable": 95.2
   },
   "neighbor_schools": {
    "Sabin": {
     "total_2031": 297,
     "at_target_every_year": false
    },
    "Irvington": {
     "total_2031": 0,
     "at_target_every_year": false
    },
    "MLK Jr": {
     "total_2031": 377,
     "at_target_every_year": true
    },
    "Alameda": {
     "total_2031": 505,
     "at_target_every_year": true
    },
    "Vernon": {
     "total_2031": 289,
     "at_target_every_year": false
    },
    "Beverly Cleary": {
     "total_2031": 414,
     "at_target_every_year": false
    },
    "Boise-Eliot/Humboldt": {
     "total_2031": 379,
     "at_target_every_year": true
    },
    "Rigler": {
     "total_2031": 377,
     "at_target_every_year": true
    },
    "Woodlawn": {
     "total_2031": 361,
     "at_target_every_year": true
    }
   },
   "school_years": {
    "Sabin": {
     "type": "K-5",
     "years": {
      "2027-28": 302.5,
      "2028-29": 313.5,
      "2029-30": 303.6,
      "2030-31": 295.2,
      "2031-32": 296.9,
      "2032-33": 293.6,
      "2033-34": 289.5,
      "2034-35": 282.1,
      "2035-36": 278.3
     }
    },
    "Beverly Cleary": {
     "type": "K-5",
     "years": {
      "2027-28": 453.7,
      "2028-29": 435.8,
      "2029-30": 429.1,
      "2030-31": 415.9,
      "2031-32": 414.5,
      "2032-33": 414.8,
      "2033-34": 404.5,
      "2034-35": 398.2,
      "2035-36": 393.7
     }
    },
    "MLK Jr": {
     "type": "K-5",
     "years": {
      "2027-28": 376.5,
      "2028-29": 383.3,
      "2029-30": 387.1,
      "2030-31": 391.0,
      "2031-32": 376.5,
      "2032-33": 368.3,
      "2033-34": 357.0,
      "2034-35": 342.8,
      "2035-36": 337.7
     }
    },
    "Boise-Eliot/Humboldt": {
     "type": "K-5",
     "years": {
      "2027-28": 384.2,
      "2028-29": 404.8,
      "2029-30": 398.2,
      "2030-31": 396.5,
      "2031-32": 378.8,
      "2032-33": 360.3,
      "2033-34": 345.0,
      "2034-35": 330.5,
      "2035-36": 326.5
     }
    },
    "Vernon": {
     "type": "K-5",
     "years": {
      "2027-28": 313.3,
      "2028-29": 310.9,
      "2029-30": 303.9,
      "2030-31": 295.0,
      "2031-32": 288.6,
      "2032-33": 285.4,
      "2033-34": 282.8,
      "2034-35": 284.7,
      "2035-36": 282.8
     }
    },
    "Alameda": {
     "type": "K-5",
     "years": {
      "2027-28": 512.0,
      "2028-29": 516.5,
      "2029-30": 520.4,
      "2030-31": 515.1,
      "2031-32": 504.8,
      "2032-33": 498.9,
      "2033-34": 488.5,
      "2034-35": 477.4,
      "2035-36": 473.3
     }
    },
    "Beaumont": {
     "type": "6-8",
     "years": {
      "2027-28": 613.0,
      "2028-29": 576.5,
      "2029-30": 577.1,
      "2030-31": 568.8,
      "2031-32": 586.0,
      "2032-33": 590.4,
      "2033-34": 590.9,
      "2034-35": 600.0,
      "2035-36": 591.1
     }
    },
    "Tubman": {
     "type": "6-8",
     "years": {
      "2027-28": 595.8,
      "2028-29": 558.7,
      "2029-30": 540.5,
      "2030-31": 520.4,
      "2031-32": 523.4,
      "2032-33": 522.3,
      "2033-34": 530.2,
      "2034-35": 535.9,
      "2035-36": 527.7
     }
    },
    "Jefferson": {
     "type": "9-12",
     "years": {
      "2027-28": 694.7,
      "2028-29": 927.4,
      "2029-30": 1095.2,
      "2030-31": 1261.7,
      "2031-32": 1280.0,
      "2032-33": 1268.1,
      "2033-34": 1258.2,
      "2034-35": 1238.8,
      "2035-36": 1252.8
     }
    },
    "Grant": {
     "type": "9-12",
     "years": {
      "2027-28": 1803.3,
      "2028-29": 1698.2,
      "2029-30": 1597.1,
      "2030-31": 1470.3,
      "2031-32": 1387.9,
      "2032-33": 1301.9,
      "2033-34": 1244.7,
      "2034-35": 1181.1,
      "2035-36": 1157.2
     }
    }
   },
   "areas": {
    "Sabin": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 66.6409,
        "mv": 0.0,
        "walk": 0.477,
        "dwalk": 0.0,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 0.0,
        "pps": 0.0
       },
       "oth": {
        "n": 169.2329,
        "mv": 0.0,
        "walk": 0.4456,
        "dwalk": 0.0,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 0.0,
        "pps": 0.0
       }
      },
      "6-8": {
       "pov": {
        "n": 23.0294,
        "mv": 0.0,
        "walk": 1.7432,
        "dwalk": 0.0,
        "in1": 0.0,
        "bus": 69.857,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 70.1338,
        "mv": 0.0,
        "walk": 1.817,
        "dwalk": 0.0,
        "in1": 0.0,
        "bus": 74.8626,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 70.6614,
        "mv": 0.0,
        "walk": 1.5527,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       },
       "oth": {
        "n": 149.8511,
        "mv": 0.0,
        "walk": 1.7818,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Sabin": {
        "kids": 236,
        "poverty": 67
       }
      },
      "6-8": {
       "Tubman": {
        "kids": 93,
        "poverty": 23
       }
      },
      "9-12": {
       "Jefferson": {
        "kids": 221,
        "poverty": 71
       }
      }
     }
    },
    "Irvington": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 46.4941,
        "mv": 100.0,
        "walk": 0.9731,
        "dwalk": 0.3735,
        "in1": 56.9916,
        "bus": 43.0084,
        "sust": 0.0,
        "pps": 89.3169
       },
       "oth": {
        "n": 176.5054,
        "mv": 100.0,
        "walk": 0.9051,
        "dwalk": 0.384,
        "in1": 65.7897,
        "bus": 34.2103,
        "sust": 0.0,
        "pps": 68.625
       }
      },
      "6-8": {
       "pov": {
        "n": 32.067,
        "mv": 89.2588,
        "walk": 1.9514,
        "dwalk": 0.7535,
        "in1": 4.8004,
        "bus": 87.2837,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 81.8647,
        "mv": 65.7991,
        "walk": 1.6416,
        "dwalk": 0.3732,
        "in1": 6.6194,
        "bus": 62.3085,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 50.8122,
        "mv": 13.1855,
        "walk": 1.3397,
        "dwalk": 0.0536,
        "sust": 86.8145,
        "pps": 100.0
       },
       "oth": {
        "n": 277.1536,
        "mv": 33.351,
        "walk": 1.4687,
        "dwalk": 0.1993,
        "sust": 66.649,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Beverly Cleary": {
        "kids": 163,
        "poverty": 42
       },
       "Sabin": {
        "kids": 60,
        "poverty": 5
       }
      },
      "6-8": {
       "Beaumont": {
        "kids": 82,
        "poverty": 29
       },
       "Tubman": {
        "kids": 31,
        "poverty": 3
       }
      },
      "9-12": {
       "Grant": {
        "kids": 229,
        "poverty": 44
       },
       "Jefferson": {
        "kids": 99,
        "poverty": 7
       }
      }
     }
    }
   }
  },
  {
   "run": "irv_sabin_15th",
   "label": "Irvington line: NE 15th + Knott, Sabin side to Jefferson",
   "data_label": "Irvington line: NE 15th + Knott",
   "note": "About 40 more kids walk to the farther school than on the Thompson line; Irvington's lower-income kids split more evenly between the two schools (estimate).",
   "caveat": null,
   "on_map": true,
   "scorecard": "build/solver/out_v2/irv_sabin_15th/scorecard.json",
   "schools_csv": "build/solver/out_v2/irv_sabin_15th/schools.csv",
   "tradeoffs": "build/solver/out_v2/irv_sabin_15th/TRADEOFFS.md",
   "district": {
    "schools_open": 63,
    "pct_sustainable_schools": 90.5,
    "pct_students_in_sustainable": 94.0
   },
   "neighbor_schools": {
    "Sabin": {
     "total_2031": 358,
     "at_target_every_year": false
    },
    "Irvington": {
     "total_2031": 0,
     "at_target_every_year": false
    },
    "MLK Jr": {
     "total_2031": 377,
     "at_target_every_year": true
    },
    "Alameda": {
     "total_2031": 505,
     "at_target_every_year": true
    },
    "Vernon": {
     "total_2031": 289,
     "at_target_every_year": false
    },
    "Beverly Cleary": {
     "total_2031": 354,
     "at_target_every_year": false
    },
    "Boise-Eliot/Humboldt": {
     "total_2031": 379,
     "at_target_every_year": true
    },
    "Rigler": {
     "total_2031": 377,
     "at_target_every_year": true
    },
    "Woodlawn": {
     "total_2031": 361,
     "at_target_every_year": true
    }
   },
   "school_years": {
    "Sabin": {
     "type": "K-5",
     "years": {
      "2027-28": 367.9,
      "2028-29": 377.9,
      "2029-30": 366.1,
      "2030-31": 355.2,
      "2031-32": 357.7,
      "2032-33": 354.2,
      "2033-34": 349.0,
      "2034-35": 340.2,
      "2035-36": 335.6
     }
    },
    "Beverly Cleary": {
     "type": "K-5",
     "years": {
      "2027-28": 388.2,
      "2028-29": 371.4,
      "2029-30": 366.6,
      "2030-31": 355.9,
      "2031-32": 353.6,
      "2032-33": 354.2,
      "2033-34": 345.0,
      "2034-35": 340.1,
      "2035-36": 336.4
     }
    },
    "MLK Jr": {
     "type": "K-5",
     "years": {
      "2027-28": 376.5,
      "2028-29": 383.3,
      "2029-30": 387.1,
      "2030-31": 391.0,
      "2031-32": 376.5,
      "2032-33": 368.3,
      "2033-34": 357.0,
      "2034-35": 342.8,
      "2035-36": 337.7
     }
    },
    "Boise-Eliot/Humboldt": {
     "type": "K-5",
     "years": {
      "2027-28": 384.2,
      "2028-29": 404.8,
      "2029-30": 398.2,
      "2030-31": 396.5,
      "2031-32": 378.8,
      "2032-33": 360.3,
      "2033-34": 345.0,
      "2034-35": 330.5,
      "2035-36": 326.5
     }
    },
    "Vernon": {
     "type": "K-5",
     "years": {
      "2027-28": 313.3,
      "2028-29": 310.9,
      "2029-30": 303.9,
      "2030-31": 295.0,
      "2031-32": 288.6,
      "2032-33": 285.4,
      "2033-34": 282.8,
      "2034-35": 284.7,
      "2035-36": 282.8
     }
    },
    "Alameda": {
     "type": "K-5",
     "years": {
      "2027-28": 512.0,
      "2028-29": 516.5,
      "2029-30": 520.4,
      "2030-31": 515.1,
      "2031-32": 504.8,
      "2032-33": 498.9,
      "2033-34": 488.5,
      "2034-35": 477.4,
      "2035-36": 473.3
     }
    },
    "Beaumont": {
     "type": "6-8",
     "years": {
      "2027-28": 581.0,
      "2028-29": 548.2,
      "2029-30": 550.1,
      "2030-31": 543.9,
      "2031-32": 560.7,
      "2032-33": 565.2,
      "2033-34": 565.2,
      "2034-35": 573.8,
      "2035-36": 565.6
     }
    },
    "Tubman": {
     "type": "6-8",
     "years": {
      "2027-28": 627.9,
      "2028-29": 587.1,
      "2029-30": 567.4,
      "2030-31": 545.4,
      "2031-32": 548.8,
      "2032-33": 547.6,
      "2033-34": 555.8,
      "2034-35": 562.1,
      "2035-36": 553.1
     }
    },
    "Jefferson": {
     "type": "9-12",
     "years": {
      "2027-28": 777.0,
      "2028-29": 1004.7,
      "2029-30": 1167.7,
      "2030-31": 1327.8,
      "2031-32": 1342.0,
      "2032-33": 1325.7,
      "2033-34": 1312.8,
      "2034-35": 1290.0,
      "2035-36": 1302.7
     }
    },
    "Grant": {
     "type": "9-12",
     "years": {
      "2027-28": 1721.0,
      "2028-29": 1620.9,
      "2029-30": 1524.6,
      "2030-31": 1404.1,
      "2031-32": 1325.9,
      "2032-33": 1244.3,
      "2033-34": 1190.2,
      "2034-35": 1129.9,
      "2035-36": 1107.2
     }
    }
   },
   "areas": {
    "Sabin": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 66.6409,
        "mv": 0.0,
        "walk": 0.477,
        "dwalk": 0.0,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 0.0,
        "pps": 0.0
       },
       "oth": {
        "n": 169.2329,
        "mv": 0.0,
        "walk": 0.4456,
        "dwalk": 0.0,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 0.0,
        "pps": 0.0
       }
      },
      "6-8": {
       "pov": {
        "n": 23.0294,
        "mv": 0.0,
        "walk": 1.7432,
        "dwalk": 0.0,
        "in1": 0.0,
        "bus": 69.857,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 70.1338,
        "mv": 0.0,
        "walk": 1.817,
        "dwalk": 0.0,
        "in1": 0.0,
        "bus": 74.8626,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 70.6614,
        "mv": 0.0,
        "walk": 1.5527,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       },
       "oth": {
        "n": 149.8511,
        "mv": 0.0,
        "walk": 1.7818,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Sabin": {
        "kids": 236,
        "poverty": 67
       }
      },
      "6-8": {
       "Tubman": {
        "kids": 93,
        "poverty": 23
       }
      },
      "9-12": {
       "Jefferson": {
        "kids": 221,
        "poverty": 71
       }
      }
     }
    },
    "Irvington": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 46.4941,
        "mv": 100.0,
        "walk": 0.9519,
        "dwalk": 0.3522,
        "in1": 57.8412,
        "bus": 42.1588,
        "sust": 0.0,
        "pps": 0.0
       },
       "oth": {
        "n": 176.5054,
        "mv": 100.0,
        "walk": 0.8793,
        "dwalk": 0.3582,
        "in1": 69.7451,
        "bus": 30.2549,
        "sust": 0.0,
        "pps": 0.0
       }
      },
      "6-8": {
       "pov": {
        "n": 32.067,
        "mv": 56.1111,
        "walk": 1.4104,
        "dwalk": 0.2126,
        "in1": 33.1396,
        "bus": 54.136,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 81.8647,
        "mv": 47.8517,
        "walk": 1.3939,
        "dwalk": 0.1255,
        "in1": 20.637,
        "bus": 44.3612,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 50.8122,
        "mv": 39.6752,
        "walk": 1.4778,
        "dwalk": 0.1918,
        "sust": 60.3248,
        "pps": 100.0
       },
       "oth": {
        "n": 277.1536,
        "mv": 50.8375,
        "walk": 1.5806,
        "dwalk": 0.3113,
        "sust": 49.1625,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Sabin": {
        "kids": 121,
        "poverty": 23
       },
       "Beverly Cleary": {
        "kids": 102,
        "poverty": 24
       }
      },
      "6-8": {
       "Beaumont": {
        "kids": 57,
        "poverty": 18
       },
       "Tubman": {
        "kids": 57,
        "poverty": 14
       }
      },
      "9-12": {
       "Grant": {
        "kids": 167,
        "poverty": 31
       },
       "Jefferson": {
        "kids": 161,
        "poverty": 20
       }
      }
     }
    }
   }
  },
  {
   "run": "irv_sabin_15th_grant",
   "label": "Irvington line: NE 15th + Knott, Irvington teens stay at Grant",
   "data_label": "Irvington line: NE 15th + Knott, Irvington teens stay at Grant",
   "note": "The NE 15th + Knott line with every Irvington-area teen kept at Grant, as today (161 go to Grant instead of Jefferson); elementary and middle school are unchanged.",
   "caveat": null,
   "on_map": true,
   "scorecard": "build/solver/out_v2/irv_sabin_15th_grant/scorecard.json",
   "schools_csv": "build/solver/out_v2/irv_sabin_15th_grant/schools.csv",
   "tradeoffs": "build/solver/out_v2/irv_sabin_15th_grant/TRADEOFFS.md",
   "district": {
    "schools_open": 63,
    "pct_sustainable_schools": 90.5,
    "pct_students_in_sustainable": 94.0
   },
   "neighbor_schools": {
    "Sabin": {
     "total_2031": 358,
     "at_target_every_year": false
    },
    "Irvington": {
     "total_2031": 0,
     "at_target_every_year": false
    },
    "MLK Jr": {
     "total_2031": 377,
     "at_target_every_year": true
    },
    "Alameda": {
     "total_2031": 505,
     "at_target_every_year": true
    },
    "Vernon": {
     "total_2031": 289,
     "at_target_every_year": false
    },
    "Beverly Cleary": {
     "total_2031": 354,
     "at_target_every_year": false
    },
    "Boise-Eliot/Humboldt": {
     "total_2031": 379,
     "at_target_every_year": true
    },
    "Rigler": {
     "total_2031": 377,
     "at_target_every_year": true
    },
    "Woodlawn": {
     "total_2031": 361,
     "at_target_every_year": true
    }
   },
   "school_years": {
    "Sabin": {
     "type": "K-5",
     "years": {
      "2027-28": 367.9,
      "2028-29": 377.9,
      "2029-30": 366.1,
      "2030-31": 355.2,
      "2031-32": 357.7,
      "2032-33": 354.2,
      "2033-34": 349.0,
      "2034-35": 340.2,
      "2035-36": 335.6
     }
    },
    "Beverly Cleary": {
     "type": "K-5",
     "years": {
      "2027-28": 388.2,
      "2028-29": 371.4,
      "2029-30": 366.6,
      "2030-31": 355.9,
      "2031-32": 353.6,
      "2032-33": 354.2,
      "2033-34": 345.0,
      "2034-35": 340.1,
      "2035-36": 336.4
     }
    },
    "MLK Jr": {
     "type": "K-5",
     "years": {
      "2027-28": 376.5,
      "2028-29": 383.3,
      "2029-30": 387.1,
      "2030-31": 391.0,
      "2031-32": 376.5,
      "2032-33": 368.3,
      "2033-34": 357.0,
      "2034-35": 342.8,
      "2035-36": 337.7
     }
    },
    "Boise-Eliot/Humboldt": {
     "type": "K-5",
     "years": {
      "2027-28": 384.2,
      "2028-29": 404.8,
      "2029-30": 398.2,
      "2030-31": 396.5,
      "2031-32": 378.8,
      "2032-33": 360.3,
      "2033-34": 345.0,
      "2034-35": 330.5,
      "2035-36": 326.5
     }
    },
    "Vernon": {
     "type": "K-5",
     "years": {
      "2027-28": 313.3,
      "2028-29": 310.9,
      "2029-30": 303.9,
      "2030-31": 295.0,
      "2031-32": 288.6,
      "2032-33": 285.4,
      "2033-34": 282.8,
      "2034-35": 284.7,
      "2035-36": 282.8
     }
    },
    "Alameda": {
     "type": "K-5",
     "years": {
      "2027-28": 512.0,
      "2028-29": 516.5,
      "2029-30": 520.4,
      "2030-31": 515.1,
      "2031-32": 504.8,
      "2032-33": 498.9,
      "2033-34": 488.5,
      "2034-35": 477.4,
      "2035-36": 473.3
     }
    },
    "Beaumont": {
     "type": "6-8",
     "years": {
      "2027-28": 581.0,
      "2028-29": 548.2,
      "2029-30": 550.1,
      "2030-31": 543.9,
      "2031-32": 560.7,
      "2032-33": 565.2,
      "2033-34": 565.2,
      "2034-35": 573.8,
      "2035-36": 565.6
     }
    },
    "Tubman": {
     "type": "6-8",
     "years": {
      "2027-28": 627.9,
      "2028-29": 587.1,
      "2029-30": 567.4,
      "2030-31": 545.4,
      "2031-32": 548.8,
      "2032-33": 547.6,
      "2033-34": 555.8,
      "2034-35": 562.1,
      "2035-36": 553.1
     }
    },
    "Jefferson": {
     "type": "9-12",
     "years": {
      "2027-28": 563.0,
      "2028-29": 803.5,
      "2029-30": 979.2,
      "2030-31": 1155.9,
      "2031-32": 1180.8,
      "2032-33": 1175.8,
      "2033-34": 1170.8,
      "2034-35": 1156.9,
      "2035-36": 1172.8
     }
    },
    "Grant": {
     "type": "9-12",
     "years": {
      "2027-28": 1935.0,
      "2028-29": 1822.0,
      "2029-30": 1713.0,
      "2030-31": 1576.0,
      "2031-32": 1487.0,
      "2032-33": 1394.0,
      "2033-34": 1332.0,
      "2034-35": 1263.0,
      "2035-36": 1237.0
     }
    }
   },
   "areas": {
    "Sabin": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 66.6409,
        "mv": 0.0,
        "walk": 0.477,
        "dwalk": 0.0,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 0.0,
        "pps": 0.0
       },
       "oth": {
        "n": 169.2329,
        "mv": 0.0,
        "walk": 0.4456,
        "dwalk": 0.0,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 0.0,
        "pps": 0.0
       }
      },
      "6-8": {
       "pov": {
        "n": 23.0294,
        "mv": 0.0,
        "walk": 1.7432,
        "dwalk": 0.0,
        "in1": 0.0,
        "bus": 69.857,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 70.1338,
        "mv": 0.0,
        "walk": 1.817,
        "dwalk": 0.0,
        "in1": 0.0,
        "bus": 74.8626,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 70.6614,
        "mv": 0.0,
        "walk": 1.5527,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       },
       "oth": {
        "n": 149.8511,
        "mv": 0.0,
        "walk": 1.7818,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Sabin": {
        "kids": 236,
        "poverty": 67
       }
      },
      "6-8": {
       "Tubman": {
        "kids": 93,
        "poverty": 23
       }
      },
      "9-12": {
       "Jefferson": {
        "kids": 221,
        "poverty": 71
       }
      }
     }
    },
    "Irvington": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 46.4941,
        "mv": 100.0,
        "walk": 0.9519,
        "dwalk": 0.3522,
        "in1": 57.8412,
        "bus": 42.1588,
        "sust": 0.0,
        "pps": 0.0
       },
       "oth": {
        "n": 176.5054,
        "mv": 100.0,
        "walk": 0.8793,
        "dwalk": 0.3582,
        "in1": 69.7451,
        "bus": 30.2549,
        "sust": 0.0,
        "pps": 0.0
       }
      },
      "6-8": {
       "pov": {
        "n": 32.067,
        "mv": 56.1111,
        "walk": 1.4104,
        "dwalk": 0.2126,
        "in1": 33.1396,
        "bus": 54.136,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 81.8647,
        "mv": 47.8517,
        "walk": 1.3939,
        "dwalk": 0.1255,
        "in1": 20.637,
        "bus": 44.3612,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 50.8122,
        "mv": 0.0,
        "walk": 1.2861,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       },
       "oth": {
        "n": 277.1536,
        "mv": 0.0,
        "walk": 1.2693,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Sabin": {
        "kids": 121,
        "poverty": 23
       },
       "Beverly Cleary": {
        "kids": 102,
        "poverty": 24
       }
      },
      "6-8": {
       "Beaumont": {
        "kids": 57,
        "poverty": 18
       },
       "Tubman": {
        "kids": 57,
        "poverty": 14
       }
      },
      "9-12": {
       "Grant": {
        "kids": 328,
        "poverty": 51
       }
      }
     }
    }
   }
  },
  {
   "run": "tubman_at_vernon_irvbc_ms",
   "label": "Tubman moves into the Vernon building, no Boise-Eliot/Faubion swap",
   "data_label": "Tubman moves into the Vernon building, no Boise-Eliot/Faubion swap",
   "note": null,
   "caveat": null,
   "on_map": false,
   "scorecard": "build/solver/out_v2/tubman_at_vernon_irvbc_ms/scorecard.json",
   "schools_csv": "build/solver/out_v2/tubman_at_vernon_irvbc_ms/schools.csv",
   "tradeoffs": "build/solver/out_v2/tubman_at_vernon_irvbc_ms/TRADEOFFS.md",
   "district": {
    "schools_open": 62,
    "pct_sustainable_schools": 93.5,
    "pct_students_in_sustainable": 95.5
   },
   "neighbor_schools": {
    "Sabin": {
     "total_2031": 420,
     "at_target_every_year": false
    },
    "Irvington": {
     "total_2031": 0,
     "at_target_every_year": false
    },
    "MLK Jr": {
     "total_2031": 407,
     "at_target_every_year": true
    },
    "Alameda": {
     "total_2031": 580,
     "at_target_every_year": true
    },
    "Vernon": {
     "total_2031": 504,
     "at_target_every_year": false
    },
    "Beverly Cleary": {
     "total_2031": 476,
     "at_target_every_year": false
    },
    "Boise-Eliot/Humboldt": {
     "total_2031": 377,
     "at_target_every_year": true
    },
    "Rigler": {
     "total_2031": 377,
     "at_target_every_year": true
    },
    "Woodlawn": {
     "total_2031": 361,
     "at_target_every_year": true
    }
   },
   "school_years": {
    "Sabin": {
     "type": "K-5",
     "years": {
      "2027-28": 436.3,
      "2028-29": 446.9,
      "2029-30": 434.5,
      "2030-31": 422.8,
      "2031-32": 419.6,
      "2032-33": 414.6,
      "2033-34": 409.9,
      "2034-35": 405.1,
      "2035-36": 400.8
     }
    },
    "Beverly Cleary": {
     "type": "K-5",
     "years": {
      "2027-28": 520.3,
      "2028-29": 501.3,
      "2029-30": 492.7,
      "2030-31": 477.1,
      "2031-32": 476.4,
      "2032-33": 476.4,
      "2033-34": 465.0,
      "2034-35": 457.3,
      "2035-36": 452.0
     }
    },
    "MLK Jr": {
     "type": "K-5",
     "years": {
      "2027-28": 409.5,
      "2028-29": 416.2,
      "2029-30": 419.1,
      "2030-31": 422.1,
      "2031-32": 407.0,
      "2032-33": 398.4,
      "2033-34": 386.9,
      "2034-35": 372.8,
      "2035-36": 367.6
     }
    },
    "Boise-Eliot/Humboldt": {
     "type": "K-5",
     "years": {
      "2027-28": 382.6,
      "2028-29": 403.2,
      "2029-30": 396.6,
      "2030-31": 394.9,
      "2031-32": 377.3,
      "2032-33": 358.8,
      "2033-34": 343.5,
      "2034-35": 329.0,
      "2035-36": 325.1
     }
    },
    "Vernon": {
     "type": "6-8",
     "years": {
      "2027-28": 568.4,
      "2028-29": 533.1,
      "2029-30": 515.1,
      "2030-31": 497.2,
      "2031-32": 503.6,
      "2032-33": 504.4,
      "2033-34": 513.6,
      "2034-35": 518.4,
      "2035-36": 510.3
     }
    },
    "Alameda": {
     "type": "K-5",
     "years": {
      "2027-28": 593.4,
      "2028-29": 597.3,
      "2029-30": 599.4,
      "2030-31": 591.8,
      "2031-32": 579.8,
      "2032-33": 573.1,
      "2033-34": 562.0,
      "2034-35": 551.4,
      "2035-36": 546.8
     }
    },
    "Beaumont": {
     "type": "6-8",
     "years": {
      "2027-28": 700.8,
      "2028-29": 659.3,
      "2029-30": 657.0,
      "2030-31": 644.9,
      "2031-32": 661.6,
      "2032-33": 665.5,
      "2033-34": 666.0,
      "2034-35": 676.1,
      "2035-36": 665.9
     }
    },
    "Jefferson": {
     "type": "9-12",
     "years": {
      "2027-28": 563.0,
      "2028-29": 803.6,
      "2029-30": 979.2,
      "2030-31": 1155.9,
      "2031-32": 1180.9,
      "2032-33": 1175.9,
      "2033-34": 1170.9,
      "2034-35": 1156.9,
      "2035-36": 1172.9
     }
    },
    "Grant": {
     "type": "9-12",
     "years": {
      "2027-28": 1935.0,
      "2028-29": 1822.0,
      "2029-30": 1713.0,
      "2030-31": 1576.0,
      "2031-32": 1487.0,
      "2032-33": 1394.0,
      "2033-34": 1332.0,
      "2034-35": 1263.0,
      "2035-36": 1237.0
     }
    }
   },
   "areas": {
    "Sabin": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 66.6409,
        "mv": 0.0,
        "walk": 0.477,
        "dwalk": 0.0,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 0.0,
        "pps": 100.0
       },
       "oth": {
        "n": 169.2329,
        "mv": 0.0,
        "walk": 0.4456,
        "dwalk": 0.0,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 0.0,
        "pps": 100.0
       }
      },
      "6-8": {
       "pov": {
        "n": 23.0294,
        "mv": 100.0,
        "walk": 1.112,
        "dwalk": -0.6312,
        "in1": 32.5838,
        "bus": 10.4471,
        "sust": 0.0,
        "pps": 100.0
       },
       "oth": {
        "n": 70.1338,
        "mv": 100.0,
        "walk": 1.0921,
        "dwalk": -0.7248,
        "in1": 36.6821,
        "bus": 7.4106,
        "sust": 0.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 70.6614,
        "mv": 0.0,
        "walk": 1.5527,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       },
       "oth": {
        "n": 149.8511,
        "mv": 0.0,
        "walk": 1.7818,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Sabin": {
        "kids": 236,
        "poverty": 67
       }
      },
      "6-8": {
       "Vernon": {
        "kids": 93,
        "poverty": 23
       }
      },
      "9-12": {
       "Jefferson": {
        "kids": 221,
        "poverty": 71
       }
      }
     }
    },
    "Irvington": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 46.4941,
        "mv": 100.0,
        "walk": 1.0342,
        "dwalk": 0.4345,
        "in1": 50.8415,
        "bus": 49.1585,
        "sust": 0.0,
        "pps": 100.0
       },
       "oth": {
        "n": 176.5054,
        "mv": 100.0,
        "walk": 1.0827,
        "dwalk": 0.5617,
        "in1": 41.622,
        "bus": 58.378,
        "sust": 0.0,
        "pps": 100.0
       }
      },
      "6-8": {
       "pov": {
        "n": 32.067,
        "mv": 100.0,
        "walk": 2.0384,
        "dwalk": 0.8406,
        "in1": 0.0,
        "bus": 94.4728,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 81.8647,
        "mv": 100.0,
        "walk": 1.825,
        "dwalk": 0.5566,
        "in1": 0.0,
        "bus": 81.4632,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 50.8122,
        "mv": 0.0,
        "walk": 1.2861,
        "dwalk": 0.0,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 277.1536,
        "mv": 0.0,
        "walk": 1.2693,
        "dwalk": 0.0,
        "sust": 100.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Beverly Cleary": {
        "kids": 223,
        "poverty": 46
       }
      },
      "6-8": {
       "Beaumont": {
        "kids": 114,
        "poverty": 32
       }
      },
      "9-12": {
       "Grant": {
        "kids": 328,
        "poverty": 51
       }
      }
     }
    }
   }
  },
  {
   "run": "tubman_at_vernon_swap",
   "label": "Tubman moves into the Vernon building; Irvington all at Beverly Cleary",
   "data_label": "Tubman moves into the Vernon building; Irvington all at Beverly Cleary",
   "note": null,
   "caveat": null,
   "on_map": false,
   "scorecard": "build/solver/out_v2/tubman_at_vernon_swap/scorecard.json",
   "schools_csv": "build/solver/out_v2/tubman_at_vernon_swap/schools.csv",
   "tradeoffs": "build/solver/out_v2/tubman_at_vernon_swap/TRADEOFFS.md",
   "district": {
    "schools_open": 62,
    "pct_sustainable_schools": 93.5,
    "pct_students_in_sustainable": 95.5
   },
   "neighbor_schools": {
    "Sabin": {
     "total_2031": 420,
     "at_target_every_year": false
    },
    "Irvington": {
     "total_2031": 0,
     "at_target_every_year": false
    },
    "MLK Jr": {
     "total_2031": 407,
     "at_target_every_year": true
    },
    "Alameda": {
     "total_2031": 580,
     "at_target_every_year": true
    },
    "Vernon": {
     "total_2031": 524,
     "at_target_every_year": false
    },
    "Beverly Cleary": {
     "total_2031": 476,
     "at_target_every_year": false
    },
    "Boise-Eliot/Humboldt": {
     "total_2031": 377,
     "at_target_every_year": true
    },
    "Rigler": {
     "total_2031": 377,
     "at_target_every_year": true
    },
    "Woodlawn": {
     "total_2031": 361,
     "at_target_every_year": true
    }
   },
   "school_years": {
    "Sabin": {
     "type": "K-5",
     "years": {
      "2027-28": 436.3,
      "2028-29": 446.9,
      "2029-30": 434.5,
      "2030-31": 422.8,
      "2031-32": 419.6,
      "2032-33": 414.6,
      "2033-34": 409.9,
      "2034-35": 405.1,
      "2035-36": 400.8
     }
    },
    "Beverly Cleary": {
     "type": "K-5",
     "years": {
      "2027-28": 520.3,
      "2028-29": 501.3,
      "2029-30": 492.7,
      "2030-31": 477.1,
      "2031-32": 476.4,
      "2032-33": 476.4,
      "2033-34": 465.0,
      "2034-35": 457.3,
      "2035-36": 452.0
     }
    },
    "MLK Jr": {
     "type": "K-5",
     "years": {
      "2027-28": 409.5,
      "2028-29": 416.2,
      "2029-30": 419.1,
      "2030-31": 422.1,
      "2031-32": 407.0,
      "2032-33": 398.4,
      "2033-34": 386.9,
      "2034-35": 372.8,
      "2035-36": 367.6
     }
    },
    "Boise-Eliot/Humboldt": {
     "type": "K-5",
     "years": {
      "2027-28": 382.6,
      "2028-29": 403.2,
      "2029-30": 396.6,
      "2030-31": 394.9,
      "2031-32": 377.3,
      "2032-33": 358.8,
      "2033-34": 343.5,
      "2034-35": 329.0,
      "2035-36": 325.1
     }
    },
    "Vernon": {
     "type": "6-8",
     "years": {
      "2027-28": 574.5,
      "2028-29": 548.7,
      "2029-30": 531.7,
      "2030-31": 519.1,
      "2031-32": 524.5,
      "2032-33": 525.1,
      "2033-34": 532.2,
      "2034-35": 533.1,
      "2035-36": 524.3
     }
    },
    "Alameda": {
     "type": "K-5",
     "years": {
      "2027-28": 593.4,
      "2028-29": 597.3,
      "2029-30": 599.4,
      "2030-31": 591.8,
      "2031-32": 579.8,
      "2032-33": 573.1,
      "2033-34": 562.0,
      "2034-35": 551.4,
      "2035-36": 546.8
     }
    },
    "Beaumont": {
     "type": "6-8",
     "years": {
      "2027-28": 700.8,
      "2028-29": 659.3,
      "2029-30": 657.0,
      "2030-31": 644.9,
      "2031-32": 661.6,
      "2032-33": 665.5,
      "2033-34": 666.0,
      "2034-35": 676.1,
      "2035-36": 665.9
     }
    },
    "Jefferson": {
     "type": "9-12",
     "years": {
      "2027-28": 563.0,
      "2028-29": 803.6,
      "2029-30": 979.2,
      "2030-31": 1155.9,
      "2031-32": 1180.9,
      "2032-33": 1175.9,
      "2033-34": 1170.9,
      "2034-35": 1156.9,
      "2035-36": 1172.9
     }
    },
    "Grant": {
     "type": "9-12",
     "years": {
      "2027-28": 1935.0,
      "2028-29": 1822.0,
      "2029-30": 1713.0,
      "2030-31": 1576.0,
      "2031-32": 1487.0,
      "2032-33": 1394.0,
      "2033-34": 1332.0,
      "2034-35": 1263.0,
      "2035-36": 1237.0
     }
    }
   },
   "areas": {
    "Sabin": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 66.6409,
        "mv": 0.0,
        "walk": 0.477,
        "dwalk": 0.0,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 0.0,
        "pps": 100.0
       },
       "oth": {
        "n": 169.2329,
        "mv": 0.0,
        "walk": 0.4456,
        "dwalk": 0.0,
        "in1": 100.0,
        "bus": 0.0,
        "sust": 0.0,
        "pps": 100.0
       }
      },
      "6-8": {
       "pov": {
        "n": 23.0294,
        "mv": 100.0,
        "walk": 1.112,
        "dwalk": -0.6312,
        "in1": 32.5838,
        "bus": 10.4471,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 70.1338,
        "mv": 100.0,
        "walk": 1.0921,
        "dwalk": -0.7248,
        "in1": 36.6821,
        "bus": 7.4106,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 70.6614,
        "mv": 0.0,
        "walk": 1.5527,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       },
       "oth": {
        "n": 149.8511,
        "mv": 0.0,
        "walk": 1.7818,
        "dwalk": 0.0,
        "sust": 0.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Sabin": {
        "kids": 236,
        "poverty": 67
       }
      },
      "6-8": {
       "Vernon": {
        "kids": 93,
        "poverty": 23
       }
      },
      "9-12": {
       "Jefferson": {
        "kids": 221,
        "poverty": 71
       }
      }
     }
    },
    "Irvington": {
     "groups": {
      "K-5": {
       "pov": {
        "n": 46.4941,
        "mv": 100.0,
        "walk": 1.0342,
        "dwalk": 0.4345,
        "in1": 50.8415,
        "bus": 49.1585,
        "sust": 0.0,
        "pps": 100.0
       },
       "oth": {
        "n": 176.5054,
        "mv": 100.0,
        "walk": 1.0827,
        "dwalk": 0.5617,
        "in1": 41.622,
        "bus": 58.378,
        "sust": 0.0,
        "pps": 100.0
       }
      },
      "6-8": {
       "pov": {
        "n": 32.067,
        "mv": 100.0,
        "walk": 2.0384,
        "dwalk": 0.8406,
        "in1": 0.0,
        "bus": 94.4728,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 81.8647,
        "mv": 100.0,
        "walk": 1.825,
        "dwalk": 0.5566,
        "in1": 0.0,
        "bus": 81.4632,
        "sust": 100.0,
        "pps": 100.0
       }
      },
      "9-12": {
       "pov": {
        "n": 50.8122,
        "mv": 0.0,
        "walk": 1.2861,
        "dwalk": 0.0,
        "sust": 100.0,
        "pps": 100.0
       },
       "oth": {
        "n": 277.1536,
        "mv": 0.0,
        "walk": 1.2693,
        "dwalk": 0.0,
        "sust": 100.0,
        "pps": 100.0
       }
      }
     },
     "destinations": {
      "K-5": {
       "Beverly Cleary": {
        "kids": 223,
        "poverty": 46
       }
      },
      "6-8": {
       "Beaumont": {
        "kids": 114,
        "poverty": 32
       }
      },
      "9-12": {
       "Grant": {
        "kids": 328,
        "poverty": 51
       }
      }
     }
    }
   }
  }
 ],
 "pending": 1,
 "capacity": {
  "schools": [
   "Sabin",
   "Irvington",
   "MLK Jr",
   "Alameda",
   "Vernon",
   "Beverly Cleary",
   "Boise-Eliot/Humboldt"
  ],
  "year": "2031-32",
  "neighborhood_k5_kids": 1915,
  "program_k5_kids": 196,
  "total_k5_kids": 2111,
  "floor": 360,
  "kids_needed": {
   "5": 1800,
   "6": 2160,
   "7": 2520
  },
  "note": "K-5 kids living in these seven schools' current attendance areas plus the K-5 immersion program housed there (King's Mandarin, as in the featured plan); compares with 360 per open school. Model v2, 2031-32."
 },
 "why_sources": {
  "method": "build/solver/METHOD.md",
  "walk": "build/routing/walk_miles.parquet",
  "big_school": "build/solver/out_v2/equity_noswap_alameda_rig/TRADEOFFS.md"
 },
 "irv": {
  "lines": [
   {
    "label": "Knott only",
    "run": "irv_sabin_knott",
    "streets": "one collector street (NE Knott)",
    "to_sabin": 60,
    "to_bc": 163,
    "sabin": 297,
    "bc": 414,
    "farther": 58,
    "walk": 0.919,
    "pov_s": 0.082,
    "pov_b": 0.255,
    "schools_csv": "build/solver/out_v2/irv_sabin_knott/schools.csv"
   },
   {
    "label": "15th + Knott",
    "run": "irv_sabin_15th",
    "streets": "collector streets only (NE 15th, NE Knott)",
    "to_sabin": 121,
    "to_bc": 102,
    "sabin": 358,
    "bc": 354,
    "farther": 44,
    "walk": 0.894,
    "pov_s": 0.187,
    "pov_b": 0.234,
    "schools_csv": "build/solver/out_v2/irv_sabin_15th/schools.csv"
   },
   {
    "label": "Thompson / 21st / Knott",
    "run": "irv_sabin_thompson21",
    "streets": "mostly residential (NE Thompson), then 21st and Knott",
    "to_sabin": 118,
    "to_bc": 105,
    "sabin": 355,
    "bc": 357,
    "farther": 7,
    "walk": 0.864,
    "pov_s": 0.137,
    "pov_b": 0.289,
    "schools_csv": "build/solver/out_v2/irv_sabin_thompson21/schools.csv"
   }
  ],
  "walk": [
   {
    "plan": "Today",
    "k5": {
     "walk_ok": 442,
     "kids": 459
    },
    "ms": {
     "walk_ok": 105,
     "kids": 207
    },
    "ms_tubman": null,
    "hs": {
     "walk_ok": 311,
     "kids": 548
    },
    "hs_modeled": true
   },
   {
    "plan": "PPS A",
    "k5": {
     "walk_ok": 225,
     "kids": 459
    },
    "ms": {
     "walk_ok": 42,
     "kids": 207
    },
    "ms_tubman": null,
    "hs": {
     "walk_ok": 311,
     "kids": 548
    },
    "hs_modeled": true
   },
   {
    "plan": "PPS B",
    "k5": {
     "walk_ok": 225,
     "kids": 459
    },
    "ms": {
     "walk_ok": 42,
     "kids": 207
    },
    "ms_tubman": null,
    "hs": {
     "walk_ok": 311,
     "kids": 548
    },
    "hs_modeled": true
   },
   {
    "plan": "Plan D",
    "k5": {
     "walk_ok": 333,
     "kids": 459
    },
    "ms": {
     "walk_ok": 42,
     "kids": 207
    },
    "ms_tubman": null,
    "hs": {
     "walk_ok": 311,
     "kids": 548
    },
    "hs_modeled": true
   },
   {
    "plan": "Knott only",
    "k5": {
     "walk_ok": 378,
     "kids": 459
    },
    "ms": {
     "walk_ok": 60,
     "kids": 207
    },
    "ms_tubman": {
     "walk_ok": 105,
     "kids": 207
    },
    "hs": {
     "walk_ok": 311,
     "kids": 548
    },
    "hs_modeled": false
   },
   {
    "plan": "15th + Knott, Sabin side to Jefferson",
    "k5": {
     "walk_ok": 386,
     "kids": 459
    },
    "ms": {
     "walk_ok": 85,
     "kids": 207
    },
    "ms_tubman": {
     "walk_ok": 105,
     "kids": 207
    },
    "hs": {
     "walk_ok": 235,
     "kids": 548
    },
    "hs_modeled": true
   },
   {
    "plan": "15th + Knott, Irvington teens stay at Grant",
    "k5": {
     "walk_ok": 386,
     "kids": 459
    },
    "ms": {
     "walk_ok": 85,
     "kids": 207
    },
    "ms_tubman": {
     "walk_ok": 105,
     "kids": 207
    },
    "hs": {
     "walk_ok": 311,
     "kids": 548
    },
    "hs_modeled": true
   },
   {
    "plan": "Thompson / 21st / Knott",
    "k5": {
     "walk_ok": 396,
     "kids": 459
    },
    "ms": {
     "walk_ok": 88,
     "kids": 207
    },
    "ms_tubman": {
     "walk_ok": 105,
     "kids": 207
    },
    "hs": {
     "walk_ok": 311,
     "kids": 548
    },
    "hs_modeled": false
   }
  ],
  "source": "build/solver/out_v2/irvington_map/summary.json",
  "bus_source": "build/solver/out_v2/irvington_map/line_bus.json",
  "bus_script": "build/solver/out_v2/irvington_map/line_bus.py"
 }
};
