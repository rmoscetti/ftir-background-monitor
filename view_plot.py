# FT-IR Background Monitor - view_plot.py
# Version: 1.1.2
# Roberto Moscetti - University of Tuscia, Italy
# Contact: rmoscetti@unitus.it
# License: MIT
#
# Script used outside the OMNIC workflow.
# The script displays plot_background.png.
# The window stays open while the OMNIC workflow updates the plot.

from pathlib import Path
import sys

# Used to load the packages from the .deps folder
sys.path.insert(0, str(Path(__file__).resolve().with_name(".deps")))

from PySide6.QtCore import QTimer, Qt  # type: ignore[import-not-found]
from PySide6.QtGui import QPixmap  # type: ignore[import-not-found]
from PySide6.QtWidgets import QApplication, QLabel  # type: ignore[import-not-found]

png = Path(__file__).resolve().with_name("plot_background.png")

app = QApplication([])  # Required before creating any Qt window or widget
label = QLabel("In attesa di plot_background.png")  # Simple window used to show the PNG
label.setWindowTitle("Background monitor")
label.setAlignment(Qt.AlignCenter)
label.resize(1100, 700)  # Initial size before the first PNG is loaded

# Used to avoid continuous reloads
last = -1


def refresh() -> None:
    global last
    if not png.exists():  # If the PNG does not exist yet, nothing is updated
        return
    mtime = png.stat().st_mtime_ns  # Used to understand if the image changed
    if mtime == last:
        return
    pixmap = QPixmap(str(png))  # Qt object used to load and display images
    # Avoids loading the image while the file is still being replaced
    if pixmap.isNull():
        return
    label.setPixmap(pixmap)  # Replaces the image currently shown in the window
    label.resize(pixmap.size())  # Resizes the window to the real PNG size
    last = mtime


# Checks the PNG every second
timer = QTimer()
timer.timeout.connect(refresh)  # Calls refresh() every time the timer expires
timer.start(1000)
refresh()  # First update when the script starts
label.show()  # Makes the window visible
app.exec()  # Starts the Qt event loop and keeps the window alive
