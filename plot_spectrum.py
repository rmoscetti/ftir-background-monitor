# FT-IR Background Monitor - plot_spectrum.py
# Version: 1.1.1
# Roberto Moscetti - University of Tuscia, Italy
# Contact: rmoscetti@unitus.it
# License: MIT
#
# Script for OMNIC workflow use.
# background_stability.TSV is read, the first spectrum is stored as
# background_stability_old.TSV, and current_background.png is written.
# The old spectrum is plotted in red, the current one in blue.

from pathlib import Path
import csv
import os
import sys
from datetime import datetime

# Local packages are loaded from the .deps folder.
sys.path.insert(0, str(Path(__file__).resolve().with_name(".deps")))

import matplotlib  # type: ignore[import-not-found]

# The plot is written to a PNG file without opening a window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # type: ignore[import-not-found]

base = Path(__file__).resolve().parent
current_tsv = base / "BG_ATR_UNITUS_TESI_HATR_BG.BG_snapshot.Background.TSV"
old_tsv = base / "BG_ATR_UNITUS_TESI_HATR_BG.BG_snapshot.Background_old.TSV"
png = base / "current_background.png"
tmp = base / "current_background.tmp.png"

if not old_tsv.exists():
    old_tsv.write_bytes(current_tsv.read_bytes())

old_x = []
old_y = []
new_x = []
new_y = []

for path, x, y in ((old_tsv, old_x, old_y), (current_tsv, new_x, new_y)):
    with path.open(newline="") as f:
        rows = csv.reader(f, delimiter="\t")
        # The first line contains the X and Y header.
        next(rows, None)
        for row in rows:
            x.append(float(row[0].replace(",", ".")))
            y.append(float(row[1].replace(",", ".")))

plt.figure(figsize=(11, 7))
plt.plot(old_x, old_y, color="red", linewidth=0.8, label="Old")
plt.plot(new_x, new_y, color="blue", linewidth=0.8, label="New")
plt.grid(True, color="lightgray")
plt.xlim(max(max(old_x), max(new_x)), min(min(old_x), min(new_x)))
plt.title(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
plt.legend()
plt.tight_layout()
# A temporary file is written first so the viewer never sees a partial PNG.
plt.savefig(tmp, dpi=100)
plt.close()
os.replace(tmp, png)
