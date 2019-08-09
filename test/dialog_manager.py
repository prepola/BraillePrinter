import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, Qt

from mainwindow import Ui_Dialog as mainDialog
from printwindow import Ui_Dialog as printDialog
from extendwindow import Ui_Dialog as extendDialog

if __name__ == '__main__':

    place_display = mainDialog
    next_mode = 'main'
    app = QtWidgets.QApplication(sys.argv)

    while 1:
        ui = place_display(next_mode, 30)
        app.exec_()
        next_mode = ui.mode
        print(next_mode)

        if ui.mode == 'print':
            place_display = printDialog
        elif ui.mode == 'extend':
            place_display = extendDialog
        elif ui.mode == 'main':
            place_display = mainDialog
