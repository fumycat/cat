import api.vk as vk
import datetime


def history(count=20, peer_id=1):
    resp = []
    cache = {}
    some_history_dict = vk.messages_get_history(count=count, peer_id=peer_id, offset=0)

    for message in some_history_dict['items']:
        when = datetime.datetime.fromtimestamp(int(message['date'])).strftime('%Y-%m-%d %H:%M:%S')
        text = message['body']
        message_id = str(message['id'])
        if message['from_id'] in cache:
            s = cache[message['from_id']]
        else:
            s = vk.users_get(message['from_id'])
            cache[message['from_id']] = s
        if 'attachments' in message:
            text = '[A] ' + text
        x = s['first_name'] + ' ' + s['last_name'] + '(' + str(message['user_id']) + ')'
        resp.append(f'{message_id} {when} {x} {text}')
    return resp
