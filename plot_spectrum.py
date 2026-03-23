# Version: 1.0.0
# Author: Roberto Moscetti
# Use: This script is used in Thermo Fisher OMNIC workflows to generate
# a PNG plot for visual monitoring of spectrum background stability.
# It helps the operator verify complete cleaning of the ATR/HATR module.

from pathlib import Path
import csv
import os
import sys
from datetime import datetime

# Load packages installed locally in .deps
sys.path.insert(0, str(Path(__file__).resolve().with_name(".deps")))

import matplotlib  # type: ignore[import-not-found]

# Render directly to PNG without opening a GUI window
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # type: ignore[import-not-found]

base = Path(__file__).resolve().parent
png = base / "current_background.png"
tmp = base / "current_background.tmp.png"
x = []
y = []

with (base / "background_stability.TSV").open(newline="") as f:
    rows = csv.reader(f, delimiter="\t")
    # Skip the TSV header: X<TAB>Y.
    next(rows, None)
    for row in rows:
        x.append(float(row[0].replace(",", ".")))
        y.append(float(row[1].replace(",", ".")))

plt.figure(figsize=(11, 7))
plt.plot(x, y, color="blue", linewidth=0.8)
plt.grid(True, color="lightgray")
plt.xlim(max(x), min(x))
plt.title(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
plt.tight_layout()
# Write to a temporary file first, then replace the final PNG atomically
plt.savefig(tmp, dpi=100)
plt.close()
os.replace(tmp, png)
