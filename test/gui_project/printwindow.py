import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, Qt

from display import generate_display

class Ui_Dialog(generate_display):
    def __init__(self, fontsize):
        return super().__init__(fontsize)

    def create_worktable(self):
        self.workTable = QtWidgets.QTextBrowser(self.mainDialog)
        self.workTable.setMinimumSize(QtCore.QSize(0, 245))
        self.workTable.setMaximumSize(QtCore.QSize(1200, 245))
        self.workTable.setStyleSheet('font-size:'+str(self.fontsize)+'px;')

    def set_buttonsize(self) :
        for i in range(4):
            self.mainBtnlist[i].setMinimumSize(QtCore.QSize(300, 75))
    
    def set_layout(self):
        self.mainLayout_2.setContentsMargins(20, 30, 20, 30)
        self.mainLayout_4.addLayout(self.mainLayout_3, 1, 0, 1, 1)
        self.mainLayout_4.addLayout(self.mainLayout, 2, 0, 1, 1)
        self.mainLayout_3.addWidget(self.workTable, 0, 0, 1, 1)

def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Dialog('print', 30)
    ui.create_worktable()
    ui.set_buttonsize()
    ui.set_layout()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()