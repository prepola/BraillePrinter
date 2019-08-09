import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, Qt

font_color = '#ffffff'
back_color = ['#0091EA','#00B0FF','#40C4FF','#80D8FF']
#['#00BFA5','#1DE9B6','#64FFDA','#A7FFEB']

class generate_display(QtWidgets.QDialog):
    def __init__(self, mode, fontsize, parent=None):
        super(generate_display, self).__init__(parent)
        self.fontsize = str(fontsize)
        self.mode = mode
        self.font_color = font_color
        self.back_color = back_color

        self.mainDialog = QtWidgets.QDialog()
        self.mainDialog.resize(1024, 600)
        self.mainDialog.setWindowTitle("음성인식 점자프린터")
        self.mainDialog.setStyleSheet(
                'background: '+ self.back_color[3] +';'
                )

        # Layout
        self.mainLayout = QtWidgets.QGridLayout() # Buttons
        self.mainLayout_2 = QtWidgets.QGridLayout() # mainInfo and spacer
        self.mainLayout_3 = QtWidgets.QGridLayout() # workTable and listView
        self.mainLayout_4 = QtWidgets.QGridLayout(self.mainDialog) # mainLayout and mainLayout_2
        self.mainLayout.setContentsMargins(75, 0, 75, 50)
        self.mainLayout_3.setContentsMargins(75, 0, 75, 0)
        self.mainLayout_4.addLayout(self.mainLayout_2, 0, 0, 1, 1)

        # Button
        self.mainBtn = [QtWidgets.QPushButton()] * 4
        for i in range(4):
            self.mainBtn[i] = QtWidgets.QPushButton(self.mainDialog)
            self.mainBtn[i].setStyleSheet(
                'color:'+ self.font_color +';' +
                'font-size:'+ self.fontsize +'px;' +
                'background: '+ self.back_color[0] +';' +
                'border-radius: 10px'
                )
            self.mainLayout.addWidget(self.mainBtn[i], int(i//2), int(i%2), 1, 1)

        # mainInfo
        self.mainInfo = QtWidgets.QTextBrowser(self.mainDialog)
        self.mainInfo.setMinimumSize(QtCore.QSize(0, 45))
        self.mainInfo.setMaximumSize(QtCore.QSize(500, 45))
        self.mainInfo.setStyleSheet(
                'font-size:'+ self.fontsize +'px;' +
                'background: '+ self.back_color[1] +';' +
                'border-radius: 10px'
                )
        self.mainLayout_2.addWidget(self.mainInfo, 0, 0, 1, 1)
        

        QtCore.QMetaObject.connectSlotsByName(self.mainDialog)
        self.mainDialog.show()        

    def set_clickevent(self, *args):
        i = 0
        for func in args:
            self.mainBtn[i].clicked.connect(func)
            i = i + 1

    def get_mode(self):
        return self.mode
    
    def set_mode(self, mode):
        self.mode = mode

    def set_infotext(self, data):
        if len(self.workTable.toPlainText()) < 1 :
            self.workTable.setText(data)
        else:
            self.workTable.append(data)

    def refresh_ui(self, text_list):
        print(self.get_mode(), text_list[0])
        for i in range(5):
            if i == 0 : self.mainInfo.setText(text_list[i])          
            else : self.mainBtn[i-1].setText(text_list[i])
    

def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = generate_display(30)
    sys.exit(app.exec_())
    pass

if __name__ == "__main__":
    main()