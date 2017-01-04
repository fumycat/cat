import api.vk as vk
from api.exceptions import *


def dialogs(count, offset):
    re = []
    response = vk.messages_get_dialogs(count, offset)
    if not response['items']:
        return None
    for item in response['items']:
        if 'chat_id' in item['message']:  # ignore chats
            re.append(item['message']['title'] + ' ' + str(int(item['message']['chat_id']) + 2000000000))
            continue
        try:
            s = vk.users_get(item['message']['user_id'])
        except UsersGetException:
            s = {'id': item['message']['user_id'], 'first_name': '', 'last_name': '-1'}
        re.append(f"{s['first_name']} {s['last_name']} {s['id']}")
    return re


def last_dialogs(count=30):
    re = []
    x = count // 200
    y = count % 200
    i = 0
    while x > 0:
        res = dialogs(x, x * i)
        for i in res:
            if i is not None:
                re.append(i)
        x -= 1
        i += 1
    res = dialogs(y, x * i)
    for i in res:
        if i is not None:
            re.append(i)
    return re


