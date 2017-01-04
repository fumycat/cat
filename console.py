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
exit - exit"""

cache_dialogs = {}

def get_photo(keys, attachment, attachment_type):
    best_num = max(int(item.split('_')[1]) for item in keys if item.startswith('photo_'))
    pic_url = attachment[attachment_type]['photo_' + str(best_num)]
    photo = requests.get(pic_url)
    file_name = str(msg_id) + ' ' + pic_url.split('/')[-1]
    with open(file_name, 'wb') as pic:
        pic.write(photo.content)
    command = ['gnome-open', file_name]
    process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    process.wait()

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
                print(str(counter), i)
                cache_dialogs[counter] = int(i.split(' ')[-1])
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
            for i in history.history(count=count, peer_id=peer):
                print(i)

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
                    threading.Thread(target=get_photo, args=[keys_list, i, 'sticker']).start()
                    print('Sticker from message ' + str(msg_id))
                elif i['type'] == 'photo':
                    for k, v in i['photo'].items():
                        keys_list.append(k)
                    threading.Thread(target=get_photo, args=[keys_list, i, 'photo']).start()
                    print('Photo from message ' + str(msg_id))
                else:
                    pprint(resp)  # TODO
        except Exception as e:
            print(e)
            pprint(resp)

    elif query == 'exit':
        exit()
