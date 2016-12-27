import api.vk as vk
import datetime
import sys

some_history_dict = vk.messages_get_history(count=sys.argv[2], peer_id=sys.argv[1])

for message in some_history_dict['items']:
    when = datetime.datetime.fromtimestamp(int(message['date'])).strftime('%Y-%m-%d %H:%M:%S')
    text = message['body']
    out = 'OUT' if message['out'] == 1 else 'IN'
    a = str(message['id'])
    if 'attachments' in message:
        a += ' a'
    print(a, when, out, text)
