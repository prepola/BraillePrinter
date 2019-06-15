# -*- coding: utf-8 -*-

import sys
import io
import os
import threading
import subprocess
from PyQt5 import QtWidgets, Qt
import time

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from python_raspberry import stt
import display
import tts
# import docxread

# 1: print_ui
# 2: recording_file_ui
# 3: document_ui
# 4: undefined_ui
# 5: title_input
# 6: body_input
# 7: feedback_ui
# 8: record_input
# 9: extend_file
# others: main_ui
mod_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
fontsize_1 = 30
credential_path = 'C:\\Users\\jk691\\Documents\\hanium project-3d7b2a095e96.json' # 구글 클라우드에서 프로젝트 생성후 JSON파일의 경로를 지정

gui_textlist = [
        ["메인 화면", "음성인식 프린트\n시작", "녹음된 음성파일을 이용하여\n프린트", "문서 파일을 이용하여\n프린트", "--기타기능--"],
        ["프린트", "새로 기록", "음성 재안내", "기존파일에 이어서 기록", "뒤로가기"],
        ["녹음파일로 기록", "새로 기록", "음성 재안내", "기존파일에 이어서 기록", "뒤로가기"],
        ["문서파일의 내용을 기록", "문서 선택", "음성 재안내", "기존파일에 이어서 기록", "뒤로가기"],
        ["--기타기능--", "--기타기능--", "--기타기능--", "--기타기능--", "뒤로가기"],
        ["음성프린트", "입력 시작", "음성 재안내", "정정 및 수정", "입력 종료"],
        ["입력중", "이 내용으로 기록", "음성 재안내", "재입력", "입력 종료"],
        ["입력중", "이 내용으로 기록", "음성 재안내", "재입력", "입력 종료"],
        ["입력중", "이 음성 파일로 기록 시작", "음성 재안내", "", "입력 종료"],
        ["파일선택", "위", "파일선택", "아래", "뒤로가기"]
]
work_textdic = {
        'duplicate':'중복되는 파일이 존재합니다.\n다시 시도해주십시요.',
        'start':'안녕하세요\n입력시작 버튼을 누르면 입력을 시작합니다.',
        'readytitle':'기록을 시작하기전에 제목을 입력해야 합니다.\n준비가 되었다면 좌측 상단 버튼을 눌러 제목을 입력해주세요.',
        'readybody':'본문 입력을 시작합니다.\n좌측 상단 버튼을 눌러 기록을 시작해 주십시오',
        'readyrecord':'해당파일로 입력을 시작합니다.',
        'fatal':'비정상 종료됨\n입력종료 버튼을 눌러주세요.',
        'overtime':'입력 시간이 초과하였거나 입력에 실패하였습니다.\n다시 시도해주십시요.',
        'isright':'다음 내용이 맞습니까?',
        'commit':'입력되었습니다\n다음줄로 이동합니다.'
}

class Ui_Dialog(object):

    def __init__(self):
        self.dis = [
                display.Ui_Dialog("main",fontsize_1), 
                display.Ui_Dialog("print",fontsize_1),
                display.Ui_Dialog("extend",fontsize_1)
        ]

        for i in range(3):
            self.dis[i].mainBtnlist[0].clicked.connect(self.btn_1)
            self.dis[i].mainBtnlist[1].clicked.connect(self.btn_2)
            self.dis[i].mainBtnlist[2].clicked.connect(self.btn_3)
            self.dis[i].mainBtnlist[3].clicked.connect(self.btn_back)

        self.field_init()
        self.change_dialog(self.mod_num, None)   
    
    def field_init(self):
        self.mod_num = int()
        self.from_dialog = int()
        self.dex = int()
        self.title_state = bool()
        self.body_state = bool()
        self.title = None
        self.typing_text = None
        self.select_item = None
        self.dis[1].workTable.setText('')

        self.voice = None

    def btn_1(self):
        if self.mod_num not in mod_list:
            self.mod_num = 1
            self.change_dialog(self.mod_num, None)
        elif (self.mod_num == 1):
            self.mod_num = 5
            self.change_dialog(self.mod_num, 'print')
        elif (self.mod_num == 2):
            self.change_dialog(self.mod_num, 'print')
        elif (self.mod_num == 3):
            self.print_document()
        elif (self.mod_num == 4):
            self.others()
        elif (self.mod_num == 5):
            self.mod_num = 6
            self.menu_guide(work_textdic['start'])
        elif (self.title_state is not True):
            self.change_dialog(self.mod_num, 'print')
            self.menu_guide(work_textdic['readytitle'])
            self.title_state = True
        elif self.title_state:
            self.title = self.print_title()
            self.menu_guide(self.title)
            self.menu_guide(work_textdic['isright'])
        elif (self.body_state is not True):
            self.menu_guide(work_textdic['readybody'])
            self.body_state = True
        elif self.body_state:
            self.body = self.print_body()
            self.menu_guide(self.body)
            self.menu_guide(work_textdic['isright'])
        elif (self.title_state & self.body_state):
            self.commit_text(self.title, self.body)
            self.menu_guide(work_textdic['commit'])
        # elif (self.mod_num == 6):
        #     self.mod_num = 7
        #     self.body = self.print_body()
        # elif (self.mod_num == 7):
        #     self.mod_num = 6
        #     self.commit_text(self.title, self.body)
        elif (self.mod_num == 9):
            if self.dex > 0:
                self.dex = self.dex - 1
                self.set_listfocus(self.dex)
        
    def btn_2(self):
        if self.mod_num not in mod_list:
            self.mod_num = 3
            self.change_dialog(self.mod_num, None)
            self.print_document()
        elif (self.mod_num == 1):
            self.noone()
        elif (self.mod_num == 2):
            self.noone()
        elif (self.mod_num == 3):
            self.noone()
        elif (self.mod_num == 4):
            self.others()
        elif (self.mod_num == 9):
            if self.from_dialog == 1:
                print(self.select_item, '을 전달합니다.')
                self.mod_num = 6
                self.change_dialog(self.mod_num, 'print')
                self.title = self.print_title()

    def btn_3(self):
        if self.mod_num not in mod_list:
            self.mod_num = 2
            self.change_dialog(self.mod_num, None)
            # self.print_record()
        elif (self.mod_num in [1, 2, 3]):
            self.from_dialog = self.mod_num
            self.mod_num = 9
            self.change_dialog(self.mod_num, 'extend')
            self.set_listfocus(self.dex)
        elif (self.mod_num == 4):
            self.others()
        elif (self.mod_num == 9):
            if self.dex < (len(self.dis[2].itemList) - 1):
                self.dex = 1 + self.dex
                self.set_listfocus(self.dex)

    def btn_back(self):
        if self.mod_num in mod_list:
            self.field_init()
            self.change_dialog(self.mod_num, None)             
            print("뒤로")
    
    def change_dialog(self, mod_num, to_dialog):
        if to_dialog == 'print':
            self.dis[0].mainDialog.hide()
            self.dis[1].mainDialog.show()
            self.dis[1].refresh_ui(gui_textlist[mod_num],mod_num)
        elif to_dialog == 'extend':
            self.dis[0].mainDialog.hide()
            self.dis[2].mainDialog.show()
            self.dis[2].refresh_ui(gui_textlist[mod_num],mod_num)
        else:
            self.dis[0].mainDialog.show()
            self.dis[1].mainDialog.hide()
            self.dis[2].mainDialog.hide()
            self.dis[0].refresh_ui(gui_textlist[mod_num],mod_num) 

    def set_listfocus(self, index):
        self.dis[2].listView.setFocus()
        self.dis[2].listView.setCurrentIndex(self.dis[2].listView.model().index(index,0))
        self.select_item = self.dis[2].itemList[index]
        print(self.select_item)

    def menu_guide(self, guide):
        if self.voice is None:
            print('스레드 없음')
        elif self.voice.isAlive():
            self.voice.close()

        self.dis[1].set_infotext(guide)
        # self.guide_voice = threading.Thread(target=tts.run_voice, args=(guide,))
        # self.guide_voice.start()
        self.voice = Thread(tts.run_voice, (guide,))
        self.voice.daemon = True
        self.voice.start()

    def print_title(self):
        print("음성프린트 기능을 클릭 하셨습니다.")
        while 1:
            self.dis[1].set_infotext(work_textdic['readytitle'])
            if isinstance(self.select_item,str):
                self.dis[1].set_infotext('파일 '+self.select_item+' 로 시작합니다.')
                return self.select_item
            try:
                title_word = stt.trans(credential_path)
            except:
                print("bad auth JSON")
                self.dis[1].set_infotext(work_textdic['fatal'])
                break
            if not isinstance(title_word,str) | (len(title_word) < 1):
                self.dis[1].set_infotext(work_textdic['overtime'])
                continue
            self.dis[1].set_infotext(title_word)
            self.dis[1].set_infotext(work_textdic['isright'])

            # if os.path.isfile('/mnt/usb'+title_word+'.txt'): # 라즈베리파이
            if os.path.isfile(title_word+'.txt'):
                self.dis[1].set_infotext(work_textdic['duplicate'])
                title_word = None
                continue
            else:
                self.dis[1].set_infotext('파일 '+title_word+' 로 시작합니다.')
                return title_word

    def print_body(self):
            self.dis[1].set_infotext(work_textdic['readybody'])
            while 1:
                try:
                    typing_text = stt.trans(credential_path)
                except:
                    print("bad auth JSON")
                    self.dis[1].set_infotext(work_textdic['fatal'])
                    break

                if not isinstance(typing_text,str):
                    self.dis[1].set_infotext(work_textdic['overtime'])
                    continue
                self.dis[1].set_infotext(typing_text)
                self.dis[1].set_infotext(work_textdic['isright'])
                return typing_text

    def print_record(self, record_name):
        # print("녹음프린트 기능을 클릭 하셨습니다.")
        self.dis[1].set_infotext(work_textdic['readyrecord'])

        record_text = stt.record(record_name, credential_path)
        return record_text

    def commit_text(self, title_word, input_text):
        # with open('/mnt/usb'+title_word+'.txt','w') as fileh: # 라즈베리파이
        if title_word[-4:] != '.txt':
            title_word = title_word+'.txt'
        with open(title_word,'a') as fileh:
            fileh.write(input_text+'\n')  
        self.dis[1].set_infotext(work_textdic['newline'])

    def print_document(self):
        print("문서프린트 기능을 클릭 하셨습니다.")
    
    def others(self):
        print("기타 기능을 클릭 하셨습니다.")

    def noone(self):
        return None

class Thread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self,name=name)
        self._stop = threading.Event()
        self.func = func
        self.args = args

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run (self):
        self.func(*self.args)

def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Dialog()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()