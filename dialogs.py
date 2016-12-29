import api.vk as vk
import sys


def last_dialogs(count):
    for i in range(count):
        response = vk.messages_get_dialogs(10, i*10)
        if not response['items']:
            break
        for item in response['items']:
            if 'chat_id' in item['message']:  # ignore chats
                continue
            s = vk.users_get(item['message']['user_id'])
            print(s['first_name'], s['last_name'], s['id'])
    return


last_dialogs(int(sys.argv[1]))

