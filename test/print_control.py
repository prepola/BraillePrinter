import json
import time
import glob
import os

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
    while 1:
        if access_json(True) :
            name = get_name()
            if len(name) != 0:
                pass
            else :
                print('name Not found')
        else :
            print('Failed to get access flag , waiting for next time')
        access_json(False)
        time.sleep(1)


if __name__ == "__main__":
    main()