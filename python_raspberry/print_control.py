import json
import time
import glob
import os

import serial
import hbcvt as hc

def serial_init():
    return serial.Serial(
        port='COM4',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0
        )

def access_json(bool_data):
    return True

# def access_json(bool_data, name = ''):
#     with open('access.json', 'w') as j_handle:
#         data = json.load(j_handle)
#         if bool_data :
#             if !(bool(data['access'])):
#                 if name != '':
#                     data['name'] = name
#                 data['access'] = 'True'
#                 j_handle.write(data)
#             else: data['access'] = 'False'
#         else :
#             if bool(data['access']):
#                 data['access'] = 'False'
#                 j_handle.write(data)
#             else:
#                 print('invalid access')
#     return data['access']

def pop_text(title):
    # with open('/mnt/usb'+title+'.txt','w') as fileh: # 라즈베리파이
    if os.path.isfile(title):
        pass
    else:
        print('Not file found')
    print(title)
    with open(title, 'r') as j_handle:
        print_queue = json.load(j_handle)
        try:
            print_data = print_queue.pop(min(print_queue))
        except:
            return ''
    with open(title, 'w') as j_hand:
        temp_json = json.dumps(print_queue)
        j_hand.write(temp_json)
    return print_data



def print_con(name):
    ser = serial_init()
    dot_index = [None,[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]]
    state = str()
    dot_data_3 = []
    if access_json(True) :
        for file_name in glob.glob('{}.json'.format(name)):
            str_data = pop_text(file_name)
            if len(str_data) != 0:
                for word_data in hc.h2b.text(str_data):
                    for consonant_data in word_data[1]:
                        for dot_data_6 in consonant_data[1]:
                            data_up = dot_index.index(dot_data_6[:3])
                            data_up=str(data_up)
                            ser.write(data_up.encode('utf-8'))
                            print(data_up,dot_data_6[:3],consonant_data[0])
                            data_down = dot_index.index(dot_data_6[3:])
                            data_down=str(data_down)
                            print(data_down,dot_data_6[3:],consonant_data[0])
                            ser.write(data_down.encode('utf-8'))
                step_line_flag = '9'
                if ser.write(step_line_flag.encode('utf-8')) :
                    print('9')
                else:
                    print('not 9')
                state = 'Transfer complete'
            else :
                state = 'No have body. waiting for next time'
    else :
        state = 'Failed to get access flag, waiting for next time'
    access_json(False)
    print(state)

if __name__ == "__main__":
    # print_con('')
    ser = serial_init()
    ser.write('27439'.encode('utf-8'))