# ============================================================
# FT-IR Background Monitor
# ============================================================
# Purpose:
#   Display the latest generated PNG in a persistent on-screen window.
#   Used for visual monitoring of background stability and ATR/HATR cleaning.
#
# Runtime:
#   Software: Thermo Fisher OMNIC
#   Platform: Windows
#   Python: 3.14
#
# I/O:
#   Input: current_background.png
#   Output: on-screen plot window
#
# Metadata:
#   Author: Roberto Moscetti
#   Affiliation: University of Tuscia, Italy
#   Contact: rmoscetti@unitus.it
#   License: MIT
#   Version: 1.0.0

from pathlib import Path
import sys

# Load packages installed locally in .deps
sys.path.insert(0, str(Path(__file__).resolve().with_name(".deps")))

from PySide6.QtCore import QTimer, Qt  # type: ignore[import-not-found]
from PySide6.QtGui import QPixmap  # type: ignore[import-not-found]
from PySide6.QtWidgets import QApplication, QLabel  # type: ignore[import-not-found]

png = Path(__file__).resolve().with_name("current_background.png")

app = QApplication([])
label = QLabel("In attesa di current_background.png")
label.setWindowTitle("Background monitor")
label.setAlignment(Qt.AlignCenter)
label.resize(1100, 700)

# Remember the last loaded file timestamp to avoid useless reloads
last = -1


def refresh() -> None:
    global last
    if not png.exists():
        return
    mtime = png.stat().st_mtime_ns
    if mtime == last:
        return
    pixmap = QPixmap(str(png))
    # If the image is not readable yet, keep showing the previous one
    if pixmap.isNull():
        return
    label.setPixmap(pixmap)
    last = mtime


# Check periodically whether the PNG has been updated
timer = QTimer()
timer.timeout.connect(refresh)
timer.start(1000)
refresh()
label.show()
app.exec()
