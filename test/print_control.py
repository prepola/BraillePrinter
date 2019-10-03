import json
import time
import glob
import os

import serial
import hbcvt.h2b.text as hc

def serial_init():
    return serial.Serial(
        port='COM1',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0
        )

def access_json(bool_data, name = ''):
    with open('access.json', 'w') as j_handle:
        data = json.load(j_handle)
        if bool_data :
            if !(bool(data['access'])):
                if name != '':
                    data['name'] = name
                data['access'] = 'True'
                j_handle.write(data)
            else: data['access'] = 'False'
        else :
            if bool(data['access']):
                data['access'] = 'False'
                j_handle.write(data)
            else:
                print('invalid access')
    return data['access']

def get_name():
    with open('access.json', 'w') as j_handle:
        data = json.load(j_handle)
        if len(data['name']) != 0 :
            return data['name']
        else :
            return ''

def pop_text(title):
    # with open('/mnt/usb'+title+'.txt','w') as fileh: # 라즈베리파이
    if os.path.isfile(title+'.json'):
        pass
    else:
        print('Not file found')
        
    with open(title+'.json', 'w') as j_handle:
        print_queue = json.load(j_handle)
        if body == print_queue[max(print_queue)]:
            print_data = print_queue.pop(max(print_queue))
            temp_json = json.dump(print_queue)
        else:
            return ''
        j_handle.write(temp_json)
        return print_data

def main():
    ser = serial_init()
    while 1:
        state = str()
        dot_data_3 = []
        if access_json(True) :
            name = get_name()
            if len(name) != 0:
                str_data = pop_text(name)
                if len(str_data) != 0:
                    for word_data in hc(str_data):
                        for consonant_data in word_data:
                            for dot_data_6 in consonant_data[1]:
                                dot_data_3.append(dot_data_6[:])
                    ser.write(bytearray(dot_data_3))
                    state = 'Transfer complete'
                else :
                    state = 'No have body. waiting for next time'
            else :
                state = 'name Not found'
        else :
            state = 'Failed to get access flag, waiting for next time'
        access_json(False)
        print(state)
        time.sleep(1)


if __name__ == "__main__":
    main()