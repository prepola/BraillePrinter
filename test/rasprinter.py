# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore, QtGui, QtWidgets

# 1: print_ui
# 2: recording_file_ui
# 3: document_ui
# 4: undefined_ui
# 5: input_ui
# others: main_ui 
mod_num = 1

class Ui_Dialog(object):
    mod_num = 1
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1024, 600)
        self.gridLayout_3 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(75, 40, 75, 50)
        self.gridLayout.setObjectName("gridLayout")
        self.mainbtn_1 = QtWidgets.QPushButton(Dialog)
        self.mainbtn_1.setMinimumSize(QtCore.QSize(300, 175))
        self.mainbtn_1.setObjectName("mainbtn_1")
        self.gridLayout.addWidget(self.mainbtn_1, 0, 0, 1, 1)
        self.mainbtn_4 = QtWidgets.QPushButton(Dialog)
        self.mainbtn_4.setMinimumSize(QtCore.QSize(300, 175))
        self.mainbtn_4.setObjectName("mainbtn_4")
        self.gridLayout.addWidget(self.mainbtn_4, 1, 1, 1, 1)
        self.mainbtn_3 = QtWidgets.QPushButton(Dialog)
        self.mainbtn_3.setMinimumSize(QtCore.QSize(300, 175))
        self.mainbtn_3.setObjectName("mainbtn_3")
        self.gridLayout.addWidget(self.mainbtn_3, 1, 0, 1, 1)
        self.mainbtn_2 = QtWidgets.QPushButton(Dialog)
        self.mainbtn_2.setMinimumSize(QtCore.QSize(300, 175))
        self.mainbtn_2.setObjectName("mainbtn_2")
        self.gridLayout.addWidget(self.mainbtn_2, 0, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setContentsMargins(20, 0, 20, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setMinimumSize(QtCore.QSize(0, 40))
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 60))
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_2.addWidget(self.textBrowser, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(680, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        Dialog.setWindowTitle("음성인식 점자프린터")

        self.retranslateUi(mod_num)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, mod_num):
        if (self.mod_num==1):
            self.textBrowser.setText("프린트")
            self.mainbtn_1.setText("새로 기록")
            self.mainbtn_2.setText("기존파일에 이어서 기록")
            self.mainbtn_3.setText("")
            self.mainbtn_4.setText("뒤로가기")
            self.mainbtn_4.clicked.connect(self.back_btn)
        elif (self.mod_num==2):
            self.textBrowser.setText("녹음파일로 기록")
            self.mainbtn_1.setText("새로 기록")
            self.mainbtn_2.setText("기존파일에 이어서 기록")
            self.mainbtn_3.setText("")
            self.mainbtn_4.setText("뒤로가기")
            self.mainbtn_4.clicked.connect(self.back_btn)
        elif (self.mod_num==3):
            self.textBrowser.setText("문서파일의 내용을 기록")
            self.mainbtn_1.setText("새로 기록")
            self.mainbtn_2.setText("기존파일에 이어서 기록")
            self.mainbtn_3.setText("")
            self.mainbtn_4.setText("뒤로가기")
            self.mainbtn_4.clicked.connect(self.back_btn)
        elif (self.mod_num==4):
            self.textBrowser.setText("--기타기능--")
            self.mainbtn_1.setText("--기타기능--")
            self.mainbtn_2.setText("--기타기능--")
            self.mainbtn_3.setText("--기타기능--")
            self.mainbtn_4.setText("뒤로가기")
            self.mainbtn_4.clicked.connect(self.back_btn)
        else:
            self.textBrowser.setText("메인 화면")
            self.mainbtn_1.setText("음성인식 프린트\n시작")
            self.mainbtn_2.setText("녹음된 음성파일을 이용하여\n프린트")
            self.mainbtn_3.setText("문서 파일을 이용하여\n프린트")
            self.mainbtn_4.setText("--기타기능--")
            self.mainbtn_1.clicked.connect(self.print_btn)
            self.mainbtn_2.clicked.connect(self.record_btn)
            self.mainbtn_3.clicked.connect(self.document_btn)
    
    def print_btn(self):
        self.mod_num = 1
        self.retranslateUi(self.mod_num)

    def record_btn(self):
        self.mod_num = 2
        self.retranslateUi(self.mod_num)

    def document_btn(self):
        self.mod_num = 3
        self.retranslateUi(self.mod_num)
    
    def back_btn(self):
        self.mod_num = 0
        self.retranslateUi(self.mod_num)
    
    #def clicked_print(self, Dialog):


def main():
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()