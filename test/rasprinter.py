# -*- coding: utf-8 -*-

import sys
import io
from PyQt5 import QtCore, QtGui, QtWidgets

# 1: print_ui
# 2: recording_file_ui
# 3: document_ui
# 4: undefined_ui
# 5: input_ui
# others: main_ui
mod_list = [1, 2, 3, 4, 5]
fontsize_1 = 30

class Ui_Dialog(object):
    mod_num = int()
    def __init__(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1024, 600)
        Dialog.setWindowTitle("음성인식 점자프린터")
        
        # Layout
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(75, 40, 75, 50)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setContentsMargins(20, 0, 20, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_3.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        # Button
        self.btn_list = [QtWidgets.QPushButton()] * 4
        for i in range(4):
            self.btn_list[i] = QtWidgets.QPushButton(Dialog)
            self.btn_list[i].setMinimumSize(QtCore.QSize(300, 175))
            self.btn_list[i].setObjectName("btn_list["+str(i)+"]")
            self.btn_list[i].setStyleSheet('font-size:'+str(fontsize_1)+'px;')
        self.gridLayout.addWidget(self.btn_list[0], 0, 0, 1, 1)
        self.gridLayout.addWidget(self.btn_list[1], 0, 1, 1, 1)
        self.gridLayout.addWidget(self.btn_list[2], 1, 0, 1, 1)
        self.gridLayout.addWidget(self.btn_list[3], 1, 1, 1, 1)

        # textBrowser
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setMinimumSize(QtCore.QSize(0, 40))
        self.textBrowser.setMaximumSize(QtCore.QSize(500, 60))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setStyleSheet('font-size:'+str(fontsize_1)+'px;')
        self.gridLayout_2.addWidget(self.textBrowser, 0, 0, 1, 1)

        # spacerItem
        spacerItem = QtWidgets.QSpacerItem(680, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        
        self.refreshUi(self.mod_num)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def refreshUi(self, mod_num):
        self.btn_list[0].clicked.connect(self.btn_1)
        self.btn_list[1].clicked.connect(self.btn_2)
        self.btn_list[2].clicked.connect(self.btn_3)
        self.btn_list[3].clicked.connect(self.btn_back)
        if (self.mod_num==1):
            self.textBrowser.setText("프린트")
            self.btn_list[0].setText("새로 기록")
            self.btn_list[1].setText("기존파일에 이어서 기록")
            self.btn_list[2].setText("")
            self.btn_list[3].setText("뒤로가기")
        elif (self.mod_num==2):
            self.textBrowser.setText("녹음파일로 기록")
            self.btn_list[0].setText("새로 기록")
            self.btn_list[1].setText("기존파일에 이어서 기록")
            self.btn_list[2].setText("")
            self.btn_list[3].setText("뒤로가기")
        elif (self.mod_num==3):
            self.textBrowser.setText("문서파일의 내용을 기록")
            self.btn_list[0].setText("새로 기록")
            self.btn_list[1].setText("기존파일에 이어서 기록")
            self.btn_list[2].setText("")
            self.btn_list[3].setText("뒤로가기")
        elif (self.mod_num==4):
            self.textBrowser.setText("--기타기능--")
            self.btn_list[0].setText("--기타기능--")
            self.btn_list[1].setText("--기타기능--")
            self.btn_list[2].setText("--기타기능--")
            self.btn_list[3].setText("뒤로가기")
        else:
            self.textBrowser.setText("메인 화면")
            self.btn_list[0].setText("음성인식 프린트\n시작")
            self.btn_list[1].setText("녹음된 음성파일을 이용하여\n프린트")
            self.btn_list[2].setText("문서 파일을 이용하여\n프린트")
            self.btn_list[3].setText("--기타기능--")
    
    def btn_1(self):
        if self.mod_num not in mod_list:
            self.mod_num = 1
            self.refreshUi(self.mod_num)
            self.print_voice()
        elif (self.mod_num == 1):
            self.print_voice()
        elif (self.mod_num == 2):
            self.print_record()
        elif (self.mod_num == 3):
            self.print_document()
        elif (self.mod_num == 4):
            self.others()

    def btn_2(self):
        if self.mod_num not in mod_list:
            self.mod_num = 2
            self.refreshUi(self.mod_num)
            self.print_record()
        elif (self.mod_num == 1):
            self.extend_file()
        elif (self.mod_num == 2):
            self.extend_file()
        elif (self.mod_num == 3):
            self.extend_file()
        elif (self.mod_num == 4):
            self.others()
            

    def btn_3(self):
        if self.mod_num not in mod_list:
            self.mod_num = 3
            self.refreshUi(self.mod_num)
            self.print_document()
        elif (self.mod_num == 1):
            self.noone()
        elif (self.mod_num == 2):
            self.noone()
        elif (self.mod_num == 3):
            self.noone()
        elif (self.mod_num == 4):
            self.others()

    def btn_back(self):
        if self.mod_num in mod_list:
            self.mod_num = 0
            self.refreshUi(self.mod_num)
            self.back()
    
    def print_voice(self):
        print("음성프린트 기능을 클릭 하셨습니다.")

    def print_record(self):
        print("녹음프린트 기능을 클릭 하셨습니다.")

    def print_document(self):
        print("문서프린트 기능을 클릭 하셨습니다.")
    
    def others(self):
        print("기타 기능을 클릭 하셨습니다.")
    
    def extend_file(self):
        print("외부파일 기능을 클릭 하셨습니다.")

    def back(self):
        print("뒤로")

    def noone(self):
        return None


def main():
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()