import arrow
import datetime
from pprint import pprint

import api.vk as vk
from api.vk_cache import Users

users = Users()


def parse_message(msg, fwd=False):
    """
    Returns list of message objects
    Example:
    {
    'message_id': '23',
    'date': 'an hour ago',
    'full_date': '12-25 11:23:00',
    'from': {'first_name': 'Pavel', ...},
    'text': 'Hello',
    'fwd_messages':
        [
        ...
        ],
    'no_photo': False,
    'attachments': [{...}]
    }
    """
    full_time = datetime.datetime.fromtimestamp(int(msg['date'])).strftime('%m-%d %H:%M:%S')
    when = arrow.get(int(msg['date'])).humanize(locale='ru')
    if 'from_id' in msg:
        from_user = users.get(msg['from_id'], 'photo_50')
    else:
        from_user = users.get(msg['user_id'], 'photo_50')
    no_photo = True if from_user['photo_50'] == 'http://vk.com/images/camera_50.png' else False
    message_id = '' if fwd else str(msg['id'])
    body = '!ПУСТОЕ СООБЩЕНИЕ!' if msg['body'] == '' else msg['body']
    parsed_message = {'message_id': message_id,
                      'date': when,
                      'full_date': full_time,
                      'from': from_user,
                      'text': body,
                      'no_photo': no_photo}
    if 'attachments' in msg:
        attach_data = msg['attachments']
        new_attach_data = []
        for attach in attach_data:
            if attach['type'] == 'photo':
                keys = []
                for k, v in attach['photo'].items():
                    keys.append(k)
                best_num = max(int(item.split('_')[1]) for item in keys if item.startswith('photo_'))
                user = users.get(attach['photo']['owner_id'])
                desc = attach['photo']['text'] + ' (' + user['first_name'] + ' ' + user['last_name'] + ')'
                user_url = 'vk.com/id' + str(user['id'])
                new_attach_data.append(dict(url=attach['photo']['photo_' + str(best_num)],
                                            type='photo',
                                            desc=desc,
                                            user_url=user_url))
        parsed_message['attachments'] = new_attach_data
    if 'fwd_messages' in msg:
        parsed_message['fwd'] = []
        for fwd_message in msg['fwd_messages']:
            parsed_message['fwd'].append(parse_message(fwd_message, True))
    return parsed_message


def history_generator(count=20, peer_id=1, offset=0):
    for message in vk.messages_get_history(count=count, peer_id=peer_id, offset=offset)['items']:
        yield parse_message(message)  # yield ?
