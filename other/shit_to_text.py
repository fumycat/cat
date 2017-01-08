import json
import os
import datetime
import api.vk as vk

cache = {}

for obj in os.listdir('output_m/messages'):
    with open('output_m/messages/' + obj, 'r') as f:
        data = json.load(f)
        for message in data:
            when = datetime.datetime.fromtimestamp(int(message['date'])).strftime('%Y-%m-%d %H:%M:%S')
            text = message['body']
            out = 'O' if message['out'] == 1 else 'I'
            a = str(message['id'])
            c = obj if 'chat_id' in message else ''
            if 'attachments' in message:
                a += '(A)'
            if message['from_id'] in cache:
                s = cache[message['from_id']]
            else:
                s = vk.users_get(message['from_id'])
                cache[message['from_id']] = s
            x = s['first_name'] + ' ' + s['last_name'] + '(' + str(message['user_id']) + ')' + '(' + c + ')' + out
            print(a, when, x, text)
    print('SPLITSPLITSPLIT')

# TODO
