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

guiTextlist = [
        ["메인 화면", "음성인식 프린트\n시작", "녹음된 음성파일을 이용하여\n프린트", "문서 파일을 이용하여\n프린트", "--기타기능--"],
        ["프린트", "새로 기록", "음성 재안내", "기존파일에 이어서 기록", "뒤로가기"],
        ["녹음파일로 기록", "새로 기록", "음성 재안내", "기존파일에 이어서 기록", "뒤로가기"],
        ["문서파일의 내용을 기록", "문서 선택", "음성 재안내", "기존파일에 이어서 기록", "뒤로가기"],
        ["--기타기능--", "--기타기능--", "--기타기능--", "--기타기능--", "뒤로가기"],
        ["음성프린트", "입력 시작", "음성 재안내", "정정 및 수정", "입력 종료"]
]

class Ui_Dialog(object):
    mod_num = int()
    def __init__(self):
        self.mainDialog = QtWidgets.QDialog()
        self.mainDialog.setObjectName("mainDialog")
        self.mainDialog.resize(1024, 600)
        self.mainDialog.setWindowTitle("음성인식 점자프린터")
        
        # Layout
        self.mainLayout = QtWidgets.QGridLayout() # Buttons
        self.mainLayout.setContentsMargins(75, 0, 75, 50)
        self.mainLayout.setObjectName("mainLayout")
        self.mainLayout_2 = QtWidgets.QGridLayout() # mainInfo and spacer
        self.mainLayout_2.setContentsMargins(250, 30, 250, 30)
        self.mainLayout_2.setObjectName("mainLayout_2")
        self.mainLayout_3 = QtWidgets.QGridLayout(self.mainDialog) # mainLayout and mainLayout_2
        self.mainLayout_3.setObjectName("mainLayout_3")
        self.mainLayout_3.addLayout(self.mainLayout, 1, 0, 1, 1)
        self.mainLayout_3.addLayout(self.mainLayout_2, 0, 0, 1, 1)

        # Button
        self.mainBtnlist = [QtWidgets.QPushButton()] * 4
        for i in range(4):
            self.mainBtnlist[i] = QtWidgets.QPushButton(self.mainDialog)
            self.mainBtnlist[i].setMinimumSize(QtCore.QSize(300, 175))
            self.mainBtnlist[i].setObjectName("mainBtnlist["+str(i)+"]")
            self.mainBtnlist[i].setStyleSheet('font-size:'+str(fontsize_1)+'px;')
            self.mainLayout.addWidget(self.mainBtnlist[i], int(i/2), int(i%2), 1, 1)
        self.mainBtnlist[0].clicked.connect(self.btn_1)
        self.mainBtnlist[1].clicked.connect(self.btn_2)
        self.mainBtnlist[2].clicked.connect(self.btn_3)
        self.mainBtnlist[3].clicked.connect(self.btn_back)

        # mainInfo
        self.mainInfo = QtWidgets.QTextBrowser(self.mainDialog)
        self.mainInfo.setMinimumSize(QtCore.QSize(0, 45))
        self.mainInfo.setMaximumSize(QtCore.QSize(500, 45))
        self.mainInfo.setObjectName("mainInfo")
        self.mainInfo.setStyleSheet('font-size:'+str(fontsize_1)+'px;')
        self.mainLayout_2.addWidget(self.mainInfo, 0, 0, 1, 1)
        
        self.refreshUi(self.mod_num)
        QtCore.QMetaObject.connectSlotsByName(self.mainDialog)

        self.mainDialog.show()

        # printDialog
        self.printDialog = QtWidgets.QDialog()
        self.printDialog.setObjectName("printDialog")
        self.printDialog.resize(1024, 600)
        self.printDialog.setWindowTitle("음성인식 점자프린터")

        self.printLayout = QtWidgets.QGridLayout() # mainInfo and spacer
        self.printLayout.setContentsMargins(20, 30, 20, 30)
        self.printLayout.setObjectName("printLayout")
        self.printInfo = QtWidgets.QTextBrowser(self.printDialog)
        self.printInfo.setMinimumSize(QtCore.QSize(0, 45))
        self.printInfo.setMaximumSize(QtCore.QSize(500, 45))
        self.printInfo.setObjectName("printInfo")
        self.printInfo.setStyleSheet('font-size:'+str(fontsize_1)+'px;')
        self.printLayout.addWidget(self.printInfo, 0, 0, 1, 1)

        self.printLayout_2 = QtWidgets.QGridLayout() # mainInfo
        self.printTextwork = QtWidgets.QTextBrowser(self.printDialog)
        self.printTextwork.setMinimumSize(QtCore.QSize(0, 245))
        self.printTextwork.setMaximumSize(QtCore.QSize(1200, 245))
        self.printTextwork.setObjectName("printTextwork")
        self.printTextwork.setStyleSheet('font-size:'+str(fontsize_1)+'px;')
        self.printLayout_2.addWidget(self.printTextwork, 0, 0, 1, 1)
        self.printLayout_2.setContentsMargins(75, 0, 75, 0)

        self.printLayout_3 = QtWidgets.QGridLayout() # Button
        self.printBtnlist = [QtWidgets.QPushButton()] * 4
        for i in range(4):
            self.printBtnlist[i] = QtWidgets.QPushButton(self.printDialog)
            self.printBtnlist[i].setMinimumSize(QtCore.QSize(300, 75))
            self.printBtnlist[i].setObjectName("mainBtnlist["+str(i)+"]")
            self.printBtnlist[i].setStyleSheet('font-size:'+str(30)+'px;')
            self.printLayout_3.addWidget(self.printBtnlist[i], int(i/2), int(i%2), 1, 1)
        self.printBtnlist[3].clicked.connect(self.btn_back)
        self.printLayout_3.setContentsMargins(75, 0, 75, 30)

        self.gridLayout_7 = QtWidgets.QGridLayout(self.printDialog)
        self.gridLayout_7.setObjectName("printLayout")
        self.gridLayout_7.addLayout(self.printLayout, 0, 0, 1, 1)
        self.gridLayout_7.addLayout(self.printLayout_2, 1, 0, 1, 1)
        self.gridLayout_7.addLayout(self.printLayout_3, 2, 0, 1, 1)

        self.printDialog.hide()

    def refreshUi(self, mod_num):
        for i in range(5):
            if self.mod_num not in mod_list: self.mod_num = 0
            if i == 0 : self.mainInfo.setText(guiTextlist[self.mod_num][i])
            elif self.mod_num >= 5 :
                if i == 0 : self.printInfo.setText(guiTextlist[self.mod_num][i])
                else: self.printBtnlist[i-1].setText(guiTextlist[self.mod_num][i])
            else : self.mainBtnlist[i-1].setText(guiTextlist[self.mod_num][i])
    
    def btn_1(self):
        if self.mod_num not in mod_list:
            self.mod_num = 1
            self.refreshUi(self.mod_num)
        elif (self.mod_num == 1):
            self.mod_num = 5
            self.refreshUi(self.mod_num)
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
        self.mainDialog.hide()
        self.printDialog.show()

    def print_record(self):
        print("녹음프린트 기능을 클릭 하셨습니다.")

    def print_document(self):
        print("문서프린트 기능을 클릭 하셨습니다.")
    
    def others(self):
        print("기타 기능을 클릭 하셨습니다.")
    
    def extend_file(self):
        print("외부파일 기능을 클릭 하셨습니다.")

    def back(self):
        if self.printDialog.isVisible:
            self.mainDialog.show()
            self.printDialog.hide()
        print("뒤로")

    def noone(self):
        return None

def main():
    app = QtWidgets.QApplication(sys.argv)
    # mainDialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    # mainDialog.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()