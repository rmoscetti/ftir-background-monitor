# FT-IR Background Monitor - view_plot.py
# Version: 1.0.0
# Roberto Moscetti - University of Tuscia, Italy
# Contact: rmoscetti@unitus.it
# License: MIT
#
# Small viewer for current_background.png.
# The window is intended to remain open while the OMNIC workflow updates the plot.

from pathlib import Path
import sys

# Local packages are loaded from the .deps folder.
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

# The last file timestamp is stored to avoid needless reloads.
last = -1


def refresh() -> None:
    global last
    if not png.exists():
        return
    mtime = png.stat().st_mtime_ns
    if mtime == last:
        return
    pixmap = QPixmap(str(png))
    # If the file is being replaced, the previous image remains visible.
    if pixmap.isNull():
        return
    label.setPixmap(pixmap)
    last = mtime


# The PNG is checked once per second.
timer = QTimer()
timer.timeout.connect(refresh)
timer.start(1000)
refresh()
label.show()
app.exec()
