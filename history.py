import api.vk as vk
import datetime

cache = {}


def parse_message(msg, fwd=False):
    parsed_fwd_messages = []
    when = datetime.datetime.fromtimestamp(int(msg['date'])).strftime('%m-%d %H:%M:%S')
    text = msg['body']
    message_id = '' if fwd else str(msg['id'])
    s = user_info(msg['user_id']) if fwd else user_info(msg['from_id'])
    x = s['first_name'] + ' ' + s['last_name'] + '(' + str(msg['user_id']) + ')'
    if 'attachments' in msg:
        text = '[A] ' + text
    if 'fwd_messages' in msg:
        for fwd_message in msg['fwd_messages']:
            parsed_fwd_messages.insert(0, parse_message(fwd_message, fwd=True))

    parsed_message = f'{message_id} {when} {x} {text}'
    if parsed_fwd_messages:
        for i in parsed_fwd_messages:
            parsed_message += '\n   ' + i
    return parsed_message


def user_info(user_id):
    if user_id in cache:
        return cache[user_id]
    else:
        data = vk.users_get(user_id)
        cache[user_id] = data
        return data


def history(count=20, peer_id=1):
    resp = []
    some_history_dict = vk.messages_get_history(count=count, peer_id=peer_id, offset=0)

    for message in some_history_dict['items']:
        resp.insert(0, parse_message(message))
    return resp
