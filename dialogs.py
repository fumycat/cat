import os
import arrow
import json

import api.vk as vk
from api.exceptions import *
from api.vk_cache import Users

users = Users()


def get_user_info(user_id):
    try:
        return users.get(user_id, 'photo_50')
    except UsersGetException:
        return {'id': user_id, 'first_name': 'Unknown group', 'last_name': ''}


def dialogs(count, offset, parse, local=False):
    re = []
    response = []
    if not local:
        response = vk.messages_get_dialogs(count, offset)['items']
    else:
        with open(os.environ['OUT_DIR'] + '/dialogs.json') as d:
            response = json.load(d)

    if parse == False:
        return response
    #
    # from pprint import pprint
    # pprint(response)
    #
    j = 0
    for item in response:
        print('Getting info ' + str(item['message']['user_id']))
        last_date = arrow.get(int(item['message']['date'])).humanize(locale='ru_ru')
        body = item['message']['body']
        if body == '':
            body = 'No text here'
        if 'chat_id' in item['message']:
            title = item['message']['title']
            chat_id = str(int(item['message']['chat_id']) + 2000000000)
            if local:
                pic_url = 'http://vk.com/images/camera_50.png'
            else:
                pic_url = vk.get_chat_pic(int(chat_id) - 2000000000, 50)
            no_photo = True if pic_url == 'http://vk.com/images/camera_50.png' else False
            re.append({'title': title,
                       'chat_id': chat_id,
                       'last_date': last_date,
                       'body': body,
                       'pic_url': pic_url,
                       'no_photo': no_photo})
        else:
            s = get_user_info(item['message']['user_id'])
            title = s['first_name'] + ' ' + s['last_name']
            chat_id = item['message']['user_id']  # s['id']
            try:
                pic_url = s['photo_50']
            except:
                pic_url = ''
            no_photo = True if pic_url == 'http://vk.com/images/camera_50.png' else False
            re.append({'title': title,
                       'chat_id': chat_id,
                       'last_date': last_date,
                       'body': body,
                       'pic_url': pic_url,
                       'no_photo': no_photo})
        if local:
            re[-1]['chat_id'] = 'local/' + str(re[-1]['chat_id'])
        j += 1
        if j > count:
            break
    return re


def last_dialogs(count=30, parse=True):
    re = []
    x = count // 200
    y = count % 200
    i = 0
    while x > 0:
        res = dialogs(200, x * i, parse)
        for m in res:
            if m is not None:
                re.append(m)
            if not m:
                break
        x -= 1
        i += 1
    res = dialogs(y, 200 * i, parse)
    for j in res:
        if j is not None:
            re.append(j)
    return re


def local_dialogs(count=30):
    return dialogs(count, 0, True, True)

