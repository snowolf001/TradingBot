# this file is responsible for all the graphics
# importing modules used here
import sys
from qtpy import QtWidgets
from ui.mainwindow import Ui_MainWindow
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import numpy as np
import random


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Studierendenverwaltung")

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.tab.pushButton.clicked.connect(self.update_graph())

    def update_graph(self):
        fs = 500
        f = random.randint(1, 100)
        ts = 1 / fs
        length_of_signal = 100
        t = np.linspace(0, 1, length_of_signal)

        cosinus_signal = np.cos(2 * np.pi * f * t)
        sinus_signal = np.sin(2 * np.pi * f * t)

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(t, cosinus_signal)
        self.MplWidget.canvas.axes.plot(t, sinus_signal)
        self.MplWidget.canvas.axes.legend(('cosinus', 'sinus'), loc='upper right')
        self.MplWidget.canvas.axes.set_title('Cosinus - Sinus Signal')
        self.MplWidget.canvas.draw()


if __name__ == "__main__":
   app = QtWidgets.QApplication(sys.argv)

   window = MainWindow()

   window.show()

   sys.exit(app.exec_())
