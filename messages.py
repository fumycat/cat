import api.vk as vk
import json


# I
def get_all_dialogs():
    final = []
    for i in range(1000):
        response = vk.messages_get_dialogs(10, i*10)
        if not response['items']:
            break
        for item in response['items']:
            if 'chat_id' in item['message']:  # ignore chats
                continue
            final.append(item)
        print(str(i*10) + ' of ' + str(response['count']))

    with open('output/pure.json', 'w') as f:
        json.dump(final, f)


def get_all_messages_from_dialog(user_id):
    current_user_messages = []
    for i in range(1000):
        response = vk.messages_get_history(user_id=user_id, count=10, offset=i * 10)
        print(response)  # DEL
        if not response['items']:
            break
        for item in response['items']:
            current_user_messages.append(item)
        print(str(i * 10) + ' of ' + str(response['count']) + ' messages')
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
