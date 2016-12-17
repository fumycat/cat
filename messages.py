import api.vk as vk
import json


# I
def get_all_dialogs():
    final = []
    i = 0
    while True:
        response = vk.messages_get_dialogs(10, i*10)
        if not response['items']:
            break
        for item in response['items']:
            if 'chat_id' in item['message']:  # ignore chats
                continue
            final.append(item)
        print(str(i*10) + ' of ' + str(response['count']))
        i += 1

    with open('output/pure.json', 'w') as f:
        json.dump(final, f)


def get_all_messages_from_dialog(user_id):
    current_user_messages = []
    i = 0
    while True:
        response = vk.messages_get_history(user_id=user_id, count=10, offset=i * 10)
        # print(response)
        if not response['items']:
            break
        for item in response['items']:
            current_user_messages.append(item)
        print(str(i * 10) + ' of ' + str(response['count']) + ' messages (vk.com/id' + user_id + ')')
        i += 1
    with open('output/messages/' + str(user_id) + '.json', 'w') as f:
        json.dump(current_user_messages, f)
    return


# II
def history():
    with open('output/pure.json', 'r') as f:
        dialog_list = json.load(f)
    for i in dialog_list:
        get_all_messages_from_dialog(i['message']['user_id'])

# get_all_dialogs()
history()
