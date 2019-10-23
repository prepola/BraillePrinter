import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, Qt

from python_raspberry.mainwindow import Ui_Dialog as mainDialog
from python_raspberry.printwindow import Ui_Dialog as printDialog
from python_raspberry.extendwindow import Ui_Dialog as extendDialog

# from python_rasberry.mainwindow import Ui_Dialog as mainDialog
# import python_rasberry.printwindow as printDialog
# from python_rasberry.extendwindow import Ui_Dialog as extendDialog

def main():
    place_display = mainDialog
    next_mode = 'main'
    app = QtWidgets.QApplication(sys.argv)


    change_display = {
        'print':printDialog,
        'extend':extendDialog,
        'main':mainDialog
    }

    while 1:
        ui = place_display(next_mode, 30)
        app.exec_()
        next_mode = ui.mode
        print('*'*5, next_mode, '로 화면이 전환됩니다.', '*'*5)

        place_display = change_display.get(next_mode, change_display['main'])

if __name__ == '__main__':
    main()