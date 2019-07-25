import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, Qt

class generate_display(object):
    def __init__(self, mode, fontsize):
        self.fontsize = fontsize
        self.mode = mode

        self.mainDialog = QtWidgets.QDialog()
        self.mainDialog.resize(1024, 600)
        self.mainDialog.setWindowTitle("음성인식 점자프린터")
        
        # Layout
        self.mainLayout = QtWidgets.QGridLayout() # Buttons
        self.mainLayout_2 = QtWidgets.QGridLayout() # mainInfo and spacer
        self.mainLayout_3 = QtWidgets.QGridLayout() # workTable and listView
        self.mainLayout_4 = QtWidgets.QGridLayout(self.mainDialog) # mainLayout and mainLayout_2
        self.mainLayout.setContentsMargins(75, 0, 75, 50)
        self.mainLayout_3.setContentsMargins(75, 0, 75, 0)
        self.mainLayout_4.addLayout(self.mainLayout_2, 0, 0, 1, 1)

        # Button
        self.mainBtnlist = [QtWidgets.QPushButton()] * 4
        for i in range(4):
            self.mainBtnlist[i] = QtWidgets.QPushButton(self.mainDialog)
            self.mainBtnlist[i].setStyleSheet('font-size:'+str(self.fontsize)+'px;')
            self.mainLayout.addWidget(self.mainBtnlist[i], int(i//2), int(i%2), 1, 1)

        # mainInfo
        self.mainInfo = QtWidgets.QTextBrowser(self.mainDialog)
        self.mainInfo.setMinimumSize(QtCore.QSize(0, 45))
        self.mainInfo.setMaximumSize(QtCore.QSize(500, 45))
        self.mainInfo.setStyleSheet('font-size:'+str(self.fontsize)+'px;')
        self.mainLayout_2.addWidget(self.mainInfo, 0, 0, 1, 1)       

        QtCore.QMetaObject.connectSlotsByName(self.mainDialog)
        self.mainDialog.show()        

    def set_clickevent(self, *args):
        i = 0
        for func in args:
            self.mainBtnlist[i].clicked.connect(func)
            i = i + 1

    def set_infotext(self, data):
        if len(self.workTable.toPlainText()) < 1 :
            self.workTable.setText(data)
        else:
            self.workTable.append(data)

    def refresh_ui(self, text_list):
        print(text_list)
        for i in range(5):
            if i == 0 : self.mainInfo.setText(text_list[i])          
            else : self.mainBtnlist[i-1].setText(text_list[i])
            print(i, text_list[i])
    

def main():
    # app = QtWidgets.QApplication(sys.argv)
    # ui = generate_display("extend",30)
    # ui.set_buttonsize()
    # ui.create_listview()
    # ui.set_layout()
    # sys.exit(app.exec_())
    pass

if __name__ == "__main__":
    main()