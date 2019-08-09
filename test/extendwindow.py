import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, Qt

from display import generate_display

class Ui_Dialog(generate_display):
    def __init__(self, mode, fontsize):
        super().__init__(mode, fontsize)
        self.set_buttonsize()
        self.create_listview()
        self.set_layout()

    def create_listview(self):
        self.itemList = os.listdir('C://')
        self.listView = QtWidgets.QListView()
        self.model = QtGui.QStandardItemModel()
        for item in self.itemList:
            self.model.appendRow(QtGui.QStandardItem(item))
        self.listView.setModel(self.model)
        self.listView.setStyleSheet('font-size:'+str(self.fontsize)+'px;')

    def set_buttonsize(self) :
        for i in range(4):
            self.mainBtn[i].setMinimumSize(QtCore.QSize(300, 75))
    
    def set_layout(self):
        self.mainLayout_2.setContentsMargins(20, 30, 20, 30)
        self.mainLayout_4.addLayout(self.mainLayout_3, 1, 0, 1, 1)
        self.mainLayout_4.addLayout(self.mainLayout, 2, 0, 1, 1)
        self.mainLayout_3.addWidget(self.listView, 0, 0, 1, 1)

def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Dialog(30)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()