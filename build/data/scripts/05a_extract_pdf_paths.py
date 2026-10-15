"""Extract vector boundary paths + words from PPS scenario map PDFs (pdfplumber).
Output work/pdfpaths_<name>.json : {teal:[pts..], k8:[pts..], fills:[{color,pts}], words:[...]}"""
import json, sys, pathlib, pdfplumber
D = pathlib.Path(__file__).resolve().parent.parent
TEAL = (0.0, 0.6125, 0.57128)
K8 = (0.37255, 0.06275, 0.18824)
def close(a, b): return a is not None and len(a) == 3 and all(abs(x - y) < 0.01 for x, y in zip(a, b))
for name in sys.argv[1:]:
    pg = pdfplumber.open(D / f"raw/scenario_maps/{name}.pdf").pages[0]
    out = {"teal": [], "k8": [], "fills": [], "words": []}
    for o in pg.curves + pg.lines:
        sc = o.get("stroking_color"); sc = tuple(sc) if isinstance(sc, (list, tuple)) else None
        pts = [(round(x, 2), round(y, 2)) for x, y in o["pts"]]
        if o.get("stroke") and close(sc, TEAL) and (o.get("linewidth") or 0) >= 2.5:
            out["teal"].append(pts)
        elif o.get("stroke") and close(sc, K8) and (o.get("linewidth") or 0) >= 2.5:
            out["k8"].append(pts)
        nc = o.get("non_stroking_color")
        if o.get("fill") and isinstance(nc, (list, tuple)) and len(nc) == 3 and abs((o.get("linewidth") or 0) - 0.7) < 0.05 and len(pts) > 20:
            out["fills"].append({"color": [round(c, 4) for c in nc], "pts": pts})
    for w in pg.extract_words(keep_blank_chars=False, use_text_flow=True):
        out["words"].append({"t": w["text"], "x": round((w["x0"] + w["x1"]) / 2, 1), "y": round((w["top"] + w["bottom"]) / 2, 1), "size": round(w["bottom"] - w["top"], 1)})
    out["page"] = [pg.width, pg.height]
    (D / f"work/pdfpaths_{name}.json").write_text(json.dumps(out))
    print(name, {k: len(v) for k, v in out.items()})
