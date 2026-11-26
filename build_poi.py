#!/usr/bin/env python3
"""يبني ملفات رادارات/مطبات مصر من OSM: data/meta.json + data/cells/<i>_<j>.json (مربعات 0.1°، نفس تقسيم الوركر)."""
import json, math, os, sys, time, shutil
import osmium

CELL = 0.1
BUMP = {"bump", "hump", "table", "cushion", "dip"}

class H(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.cells = {}
    def node(self, n):
        t = n.tags
        rad = t.get("highway") == "speed_camera" or t.get("enforcement") == "maxspeed"
        bmp = t.get("traffic_calming") in BUMP
        if not (rad or bmp) or not n.location.valid():
            return
        la, lo = n.location.lat, n.location.lon
        k = f"{math.floor(la / CELL)}_{math.floor(lo / CELL)}"
        c = self.cells.setdefault(k, {"rad": [], "bmp": []})
        if bmp:
            c["bmp"].append([round(la, 5), round(lo, 5)])
        else:
            try:
                mx = int(str(t.get("maxspeed", "0")).split()[0])
            except ValueError:
                mx = 0
            c["rad"].append([round(la, 5), round(lo, 5), mx])

def main(pbf, out):
    h = H()
    h.apply_file(pbf)  # العُقد بس: مفيش locations=True محتاجة
    shutil.rmtree(os.path.join(out, "cells"), ignore_errors=True)
    os.makedirs(os.path.join(out, "cells"))
    for k, c in h.cells.items():
        with open(os.path.join(out, "cells", k + ".json"), "w") as f:
            json.dump(c, f, separators=(",", ":"))
    with open(os.path.join(out, "meta.json"), "w") as f:
        json.dump({"t": int(time.time() * 1000), "cells": len(h.cells),
                   "radars": sum(len(c["rad"]) for c in h.cells.values()),
                   "bumps": sum(len(c["bmp"]) for c in h.cells.values()),
                   "source": "OpenStreetMap contributors (ODbL) via Geofabrik"}, f, ensure_ascii=False)
    print("cells", len(h.cells))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
