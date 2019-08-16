import sys
import os
import json
import time
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
        'print_delete':["입력 중", "이 내용으로 기록", "음성 재안내", "재입력", "입력 종료"],
        'print_input':["입력 중", "입력 중", "입력 중", "입력 중", "입력 중"],
        'isright':["입력 검토", "예", "음성 재안내", "재입력", "입력 종료"]
}

script = {
        'duplicate':'중복되는 파일이 존재합니다.\n다시 시도해주십시요.',
        'start':'안녕하세요\n입력시작 버튼을 누르면 입력을 시작합니다.',
        'readytitle':'기록을 시작하기전에 제목을 입력해야 합니다.\n준비가 되었다면 좌측 상단 버튼을 눌러 제목을 입력해주세요.',
        'readybody':'본문 입력을 시작합니다.\n좌측 상단 버튼을 눌러 기록을 시작해 주십시오',
        'readyrecord':'해당파일로 입력을 시작합니다.',
        'fatal':'음성인식을 실행할 수 없습니다.\ncredential path 및 Google Cloud Platform console을 확인해주세요.\n입력종료 버튼을 누르면 프린트과정이 종료됩니다.',
        'overtime':'입력 시간이 초과하였거나 입력에 실패하였습니다.\n다시 시도해주십시요.',
        'isright':'다음 내용이 맞습니까?',
        'commit':'입력되었습니다. 다음줄로 이동합니다.',
        'end_not_save':'현재 진행하던 내용이 저장되지 않습니다. 종료하시려면 버튼을 한번 더 입력해 주세요',
        'end':'종료하시려면 버튼을 한번 더 입력해 주세요',
        'empty_title':'아무 내용도 입력되어 있지 않습니다. 먼저 입력시작 버튼으로 입력을 시작해주세요',
        'empty_body':'현재 본문으로 아무 내용도 입력되어 있지 않습니다. 제목을 바꾸시려면 버튼을 한번 더 입력해주세요',
        'delete_guide_1':'방금 입력하신 내용',
        'delete_guide_2':'을 삭제합니다. 삭제 하시려면 버튼을 한번 더 입력해주세요.',
        'delete_process':'삭제가 진행중입니다. 잠시만 기다려 주십시오.',
        'delete_failed':'해당 내용이 이미 인쇄 대기열에 포함되어 삭제할 수 없습니다.',
        'delete_comp':'성공적으로 삭제 되었습니다.',
        'text_error':'스크립트를 읽을 수 없습니다. 스크립트 파일을 확인해주세요'
}

credential_path = 'C:\\Users\\jk691\\Documents\\hanium project-3d7b2a095e96.json'

def print_streaming():
    # self.make_voice('')
    # if isinstance(self.select_item,str):
    #     self.dis[1].set_infotext('파일 '+self.select_item+' 로 시작합니다.')
    #     return self.select_item
    try:
        stt_data = stt.trans(credential_path)
    except:
        print("bad auth JSON")
        return 'fatal'

    print('print_streaming:', stt_data)
    if not isinstance(stt_data,str) | (len(stt_data) < 1):
        return 'overtime'
    # elif os.path.isfile('/mnt/usb'+stt_data+'.txt'): # 라즈베리파이
    elif os.path.isfile(stt_data+'.txt'):
        return 'duplicate'
    else:
        return stt_data

def print_record(record_name):
    # print("녹음프린트 기능을 클릭 하셨습니다.")
    record_text = stt.record(record_name, credential_path)
    return record_text

def commit_text(stt_data, input_text):
    # with open('/mnt/usb'+stt_data+'.txt','w') as fileh: # 라즈베리파이
    with open('queue.json', 'r') as j_handle:
        print_queue = json.load(j_handle)
    while 1:
        time.sleep(1)
        if access_json(True):
            if len(print_queue) < 1 :
                print_queue[str(0)] = stt_data
                continue
            else:
                print_queue[str(int(max(print_queue)) + 1)] = input_text
                temp_json = json.dumps(print_queue)
            with open('queue.json', 'w') as j_handle:
                j_handle.write(temp_json)
            if stt_data[-4:] != '.txt':
                stt_data = stt_data+'.txt'
            print('commit_text:', input_text)
            with open(stt_data,'a') as fileh:
                fileh.write(input_text+'\n')
            return access_json(False)

def rollback_text(body):
    with open('queue.json', 'r') as j_handle:
        print_queue = json.load(j_handle)
    while 1:
        time.sleep(1)
        if access_json(True):
            if body == print_queue[max(print_queue)]:
                print_queue.pop(max(print_queue))
                temp_json = json.dump(print_queue)
            else:
                access_json(False)
                return False
                # self.set_mode('print_body', 'delete_failed')
                # break
            with open('queue.json', 'w') as j_handle:
                j_handle.write(temp_json)
            access_json(False)
            return True
        
def init_json():
    with open('queue.json', 'w') as j_handle:
        j_handle.write('{}')

def access_json(bool_data):
    return bool_data

class Ui_Dialog(generate_display):
    def __init__(self, mode, fontsize):
        super().__init__(mode, fontsize)

        self.play_voice = None
        self.end_flag = False
        self.current_voice = str()
        self.input_text = str()
        self.title = str()
        self.body = str()

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
        if self.debug : print('<', __name__, '>', 'set_mode:', mode, text)
        if text != '':
            self.add_log(text)
            self.make_voice(text)
        self.refresh_ui(gui_textlist.get(mode, gui_textlist['error']))
        return super().set_mode(mode)

    def make_voice(self, text):
        if self.debug : print('<', __name__, '>', 'make_voice:', text)
        if self.play_voice is not None:
            self.play_voice.stop()
            self.play_voice = None
        if text != '':
            if text in script:
                self.current_voice = script.get(text, script['text_error'])
                self.play_voice = tts.run_voice(script.get(text, script['text_error']))
            else:
                self.current_voice = text
                self.play_voice = tts.run_voice(text)
            return self.play_voice.start()

    def add_log(self, text):
        if self.debug : print('<', __name__, '>', 'add_log:', text)
        return self.workTable.append(script.get(text, text))

    def btn_1(self) :
        if self.debug : print('<', __name__, '>', 'btn_1')
        if self.get_mode() == 'print':
            self.set_mode('print_title', 'readytitle')
        elif self.get_mode() in ['print_title', 'print_body']:
            self.refresh_ui(gui_textlist.get('print_input', gui_textlist['error']))
            self.make_voice('')
            self.input_text = print_streaming()
            if self.input_text in script:
                self.set_mode(self.get_mode(), script[self.input_text])
            else:
                self.add_log(self.input_text + '\n' + script['isright'])
                self.make_voice(self.input_text + '\n' + script['isright'])
                self.set_mode('isright', '')
        elif self.get_mode() == 'isright':
            if len(self.title) < 1:
                self.title = self.input_text
            else :
                self.body = self.input_text
                commit_text(self.title, self.body)
            self.set_mode('print_body', script.get('commit', script['text_error']))

    def btn_2(self) :
        if self.debug : print('<', __name__, '>', 'btn_2')
        self.make_voice(self.current_voice)

    def btn_3(self) :
        if self.debug : print('<', __name__, '>', 'btn_3')
        if self.get_mode() in ['print', 'print_title']:
            self.set_mode(self.get_mode(), script.get('empty_title', script['text_error']))
        elif self.get_mode() == 'isright':
            if len(self.title) < 1:
                self.set_mode('print_title', 'readytitle') 
            else:
                self.set_mode('print_body', 'readybody')
        elif self.get_mode() == 'print_body':
            if len(self.body) < 1:
                self.set_mode(self.get_mode(), script.get('empty_body', script['text_error']))
            else:
                self.add_log(script['delete_guide_1'] + ' ' + self.body + ' ' + script['delete_guide_2'])
                self.make_voice(script['delete_guide_1'] + ' ' + self.body + ' ' + script['delete_guide_2'])
                self.set_mode('print_delete', '')
        elif self.get_mode() == 'print_delete':
            self.make_voice(script['delete_process'])
            if rollback_text() :
                self.set_mode('print_body', 'delete_comp')
            else :
                self.set_mode('print_body', 'delete_failed')
            
    def btn_4(self) :
        if self.debug : print('<', __name__, '>', 'btn_4')
        if not self.end_flag:
            self.set_mode(self.mode, 'end_not_save' if self.get_mode() == 'isright' else 'end')
            self.end_flag = True
        elif self.end_flag:
            init_json()
            self.set_mode('main')
            self.mainDialog.close()
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Dialog('print',30)
    ui.mainDialog.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()