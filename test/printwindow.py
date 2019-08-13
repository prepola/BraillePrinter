import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, Qt

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from display import generate_display
from python_raspberry import stt
import tts

gui_textlist = {
        'error':["프로그램 재시작 필요", "-", "-", "-", "-"],
        'print':["음성프린트", "입력 시작", "음성 재안내", "정정 및 수정", "입력 종료"],
        'print_title':["음성프린트", "입력 시작", "음성 재안내", "정정 및 수정", "입력 종료"],
        'print_body':["입력 중", "이 내용으로 기록", "음성 재안내", "재입력", "입력 종료"],
        'print_input':["입력 중", "입력 중", "입력 중", "입력 중", "입력 중"],
        'isright':["입력 검토", "예", "음성 재안내", "재입력", "입력 종료"]
}

work_textdic = {
        'duplicate':'중복되는 파일이 존재합니다.\n다시 시도해주십시요.',
        'start':'안녕하세요\n입력시작 버튼을 누르면 입력을 시작합니다.',
        'readytitle':'기록을 시작하기전에 제목을 입력해야 합니다.\n준비가 되었다면 좌측 상단 버튼을 눌러 제목을 입력해주세요.',
        'readybody':'본문 입력을 시작합니다.\n좌측 상단 버튼을 눌러 기록을 시작해 주십시오',
        'readyrecord':'해당파일로 입력을 시작합니다.',
        'fatal':'음성인식을 실행할 수 없습니다.\ncredential path 및 Google Cloud Platform console을 확인해주세요.\n입력종료 버튼을 누르면 프린트과정이 종료됩니다.',
        'overtime':'입력 시간이 초과하였거나 입력에 실패하였습니다.\n다시 시도해주십시요.',
        'isright':'다음 내용이 맞습니까?',
        'commit':'입력되었습니다\n다음줄로 이동합니다.',
        'end_ans':'현재 진행하던 내용이 저장되지 않습니다. 종료하시려면 버튼을 한번 더 입력해 주세요',
        '':''
}

credential_path = 'C:\\Users\\jk691\\Documents\\hanium project-3d7b2a095e96.json'

class Ui_Dialog(generate_display):
    def __init__(self, mode, fontsize):
        super().__init__(mode, fontsize)

        self.play_voice = None
        self.end_flag = False
        self.current_voice = str()
        self.input_title = str()

        self.create_worktable()
        self.set_buttonsize()
        self.set_layout()
        self.set_clickevent(self.btn_1, self.btn_2, self.btn_3, self.btn_4)
        self.set_mode('print', 'start')

    def create_worktable(self):
        self.workTable = QtWidgets.QTextBrowser(self.mainDialog)
        self.workTable.setMinimumSize(QtCore.QSize(0, 245))
        self.workTable.setMaximumSize(QtCore.QSize(1200, 245))
        self.workTable.setStyleSheet('font-size:'+str(self.fontsize)+'px;')

    def set_buttonsize(self) :
        for i in range(4):
            self.mainBtn[i].setMinimumSize(QtCore.QSize(300, 75))
    
    def set_layout(self):
        self.mainLayout_2.setContentsMargins(20, 30, 20, 30)
        self.mainLayout_4.addLayout(self.mainLayout_3, 1, 0, 1, 1)
        self.mainLayout_4.addLayout(self.mainLayout, 2, 0, 1, 1)
        self.mainLayout_3.addWidget(self.workTable, 0, 0, 1, 1)

    def set_mode(self, mode, text = ''):
        self.current_voice = text
        if text != '':
            self.add_log(text)
            self.make_voice(text)
        self.refresh_ui(gui_textlist.get(mode, gui_textlist['error']))
        return super().set_mode(mode)

    def make_voice(self, text):
        if self.play_voice is not None:
            self.play_voice.stop()
            self.play_voice = None
        if text in work_textdic:
            self.play_voice = tts.run_voice(work_textdic.get(text, work_textdic['']))
        else:
            self.play_voice = tts.run_voice(text)
        return self.play_voice.start()

    def add_log(self, text):
        return self.workTable.append(work_textdic.get(text, work_textdic['']))

# TODO: 수정해야 되는 부분

    def print_title(self):
        print("음성프린트 기능을 클릭 하셨습니다.")
        while 1:
            # if isinstance(self.select_item,str):
            #     self.dis[1].set_infotext('파일 '+self.select_item+' 로 시작합니다.')
            #     return self.select_item
            try:
                title_word = stt.trans(credential_path)
            except:
                print("bad auth JSON")
                return 'fatal'

            if not isinstance(title_word,str) | (len(title_word) < 1):
                return 'overtime'
            # elif os.path.isfile('/mnt/usb'+title_word+'.txt'): # 라즈베리파이
            elif os.path.isfile(title_word+'.txt'):
                return 'duplicate'
            else:
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
        record_text = stt.record(record_name, credential_path)
        return record_text

    def commit_text(self, title_word, input_text):
        # with open('/mnt/usb'+title_word+'.txt','w') as fileh: # 라즈베리파이
        if title_word[-4:] != '.txt':
            title_word = title_word+'.txt'
        with open(title_word,'a') as fileh:
            fileh.write(input_text+'\n')  

# TODO: 여기까지

    def btn_1(self) :
        if self.get_mode() == 'print':
            self.set_mode('print_title', 'readytitle')
        elif self.get_mode() == 'print_title':
            self.refresh_ui(gui_textlist.get('print_input', gui_textlist['error']))
            input_title = self.print_title()
            if input_title in gui_textlist:
                self.set_mode(self.get_mode(), input_title)
            else:
                self.set_mode('isright', 'isright')
                self.add_log(input_title)
                self.make_voice(input_title)

    def btn_2(self) :
        self.make_voice(self.current_voice)

    def btn_3(self) :
        if self.get_mode() == 'print':
            self.set_mode('doc_main')

    def btn_4(self) :
        if not self.end_flag:
            self.set_mode(self.mode, 'end_ans')
            self.end_flag = True
        elif self.end_flag:
            self.set_mode('main')
            self.mainDialog.close()
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Dialog('print',30)
    ui.mainDialog.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()