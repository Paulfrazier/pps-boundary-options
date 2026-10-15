"""Fetch 2020 Census DHC P12 (sex by age, 5-yr bands) at BLOCK level and
PCT12 (sex by single year of age) at TRACT level for the PPS counties.
The API key is read at runtime from the CENSUS_API_KEY environment variable and never written."""
import json, os, pathlib, time, requests
OUT = pathlib.Path(__file__).resolve().parent.parent / "raw" / "census"
KEY = os.environ["CENSUS_API_KEY"]  # export the key; never commit it
BASE = "https://api.census.gov/data/2020/dec/dhc"
COUNTIES = ["051", "067", "005"]
# P12: 003-006 male <5,5-9,10-14,15-17 ; 027-030 female same
P12 = ["P12_001N"] + [f"P12_{i:03d}N" for i in (3, 4, 5, 6, 27, 28, 29, 30)]
# PCT12: male ages 0..17 = PCT12_003N..PCT12_020N ; female PCT12_107N..PCT12_124N
PCT12 = [f"PCT12_{i:03d}N" for i in range(3, 21)] + [f"PCT12_{i:03d}N" for i in range(107, 125)]

def get(params):
    for a in range(5):
        r = requests.get(BASE, params={**params, "key": KEY}, timeout=120)
        if r.status_code == 200:
            return r.json()
        time.sleep(3 * (a + 1))
    raise RuntimeError(f"{r.status_code} {r.text[:300]}")

blocks, tracts = [], []
for c in COUNTIES:
    rows = get({"get": ",".join(P12), "for": "block:*", "in": f"state:41 county:{c} tract:*"})
    blocks += rows if not blocks else rows[1:]
    rows = get({"get": "NAME," + ",".join(PCT12), "for": "tract:*", "in": f"state:41 county:{c}"})
    tracts += rows if not tracts else rows[1:]
    print(c, len(blocks), len(tracts))
(OUT / "dhc_p12_blocks.json").write_text(json.dumps(blocks))
(OUT / "dhc_pct12_tracts.json").write_text(json.dumps(tracts))
