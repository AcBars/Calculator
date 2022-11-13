import sys

from PyQt6.QtWidgets import QApplication

import gui

app = QApplication(sys.argv)

window = gui.MainWindow()
window.show()

app.exec()
