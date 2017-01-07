import os
import subprocess
import threading
from pprint import pprint

import requests

import dialogs
import history
import message_id

text_help = """dialogs <count> - get dialog list
history <peer_id> <count> - get message history
msg <message_id> - get attachments from message
help - help
exit - exit"""

cache_dialogs = {}
cache_dir = '.cache/'  # dir for attachments
op = 'gnome-open'  # command for opening photos (only for unix)


def init():
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    print(text_help)
    main()


def parse_msg(msg, fwd=1):
    a = '{A}' if 'attachments' in msg else ''
    line = f"{msg['message_id']} {msg['date']} {msg['from']['first_name']} {msg['text']} {a}"
    if 'fwd' in msg:
        for m in msg['fwd']:
            space = '--' * fwd
            line = line + '\n' + space + parse_msg(m, fwd=fwd+1)
    return line


def get_photo(keys, attachment, attachment_type, msg_id):
    best_num = max(int(item.split('_')[1]) for item in keys if item.startswith('photo_'))
    pic_url = attachment[attachment_type]['photo_' + str(best_num)]
    photo = requests.get(pic_url)
    file_name = cache_dir + str(msg_id) + ' ' + pic_url.split('/')[-1]
    with open(file_name, 'wb') as pic:
        pic.write(photo.content)
    if os.name == 'posix':
        command = [op, file_name]
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait()
    else:
        subprocess.call(file_name, shell=True)


def main():
    while True:
        query = input('> ')
        if query == 'help':
            print(text_help)

        elif query.startswith('dialogs'):
            count = 20
            try:
                count = int(query.split(' ')[1])
            except (IndexError, ValueError):
                pass
            finally:
                counter = 0
                for i in dialogs.last_dialogs(count):
                    print(str(counter), i['title'], i['chat_id'])
                    cache_dialogs[counter] = i['chat_id']
                    counter += 1

        elif query.startswith('history'):
            count = 50
            try:
                peer = int(query.split(' ')[1])
                count = int(query.split(' ')[2])
            except (IndexError, ValueError):
                pass
            finally:
                if peer < 10000:
                    peer = cache_dialogs[peer]
                for i in reversed(list(history.history_generator(count=count, peer_id=peer, offset=0))):
                    print(parse_msg(i))
                    # pprint(i)

        elif query.startswith('msg'):
            resp = None
            msg_id = None
            try:
                msg_id = int(query.split(' ')[1])
                resp = message_id.msg(msg_id)
            except (IndexError, ValueError):
                print('Wrong data')
            try:
                for i in resp[0]['attachments']:
                    keys_list = []
                    if i['type'] == 'sticker':
                        for k, v in i['sticker'].items():
                            keys_list.append(k)
                        threading.Thread(target=get_photo, args=[keys_list, i, 'sticker', msg_id]).start()
                        print('Sticker from message ' + str(msg_id))
                    elif i['type'] == 'photo':
                        for k, v in i['photo'].items():
                            keys_list.append(k)
                        threading.Thread(target=get_photo, args=[keys_list, i, 'photo', msg_id]).start()
                        print('Photo from message ' + str(msg_id))
                    else:
                        pprint(resp)  # TODO
            except Exception:
                pprint(resp)

        elif query == 'exit':
            exit()

init()
