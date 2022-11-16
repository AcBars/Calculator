import sys

from PyQt6.QtWidgets import QApplication

import gui
from log import log_startend as se

app = QApplication(sys.argv)

window = gui.MainWindow()
window.show()
se(1)

app.exec()
se(0)
