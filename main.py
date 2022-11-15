import sys
from log import log_startend as se
from PyQt6.QtWidgets import QApplication

import gui

app = QApplication(sys.argv)

window = gui.MainWindow()
window.show()
se(1)

app.exec()
se(0)