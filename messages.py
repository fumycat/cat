import api.vk as vk
import json
import os
import time


# I
def get_all_dialogs(need_chats=0):
    """
    0 - only private messages
    1 - only chats
    2 - chats and private messages
    """
    final = []
    i = 0
    while True:
        response = vk.messages_get_dialogs(10, i*10)
        if not response['items']:
            break
        for item in response['items']:
            if need_chats == 0 and 'chat_id' in item['message']:  # ignore chats
                print(str(item))
                continue
            if need_chats == 1 and 'chat_id' not in item['message']:
                continue
            final.append(item)
        print(str(i*10) + ' of ' + str(response['count']))
        i += 1

    with open('output_m/pure_chats.json', 'w') as f:
        json.dump(final, f)
    return final


def get_all_messages_from_dialog(user_id):
    if os.path.exists('output_m/messages/' + str(user_id) + '.json'):
        print(str(user_id) + '.json already exists. Skipping...')
        return
    current_user_messages = []
    i = 0
    while True:
        try:
            response = vk.messages_get_history(peer_id=user_id, count=200, offset=i * 200)
        except:
            print('Error while getting message history - ' + str(i*200))
            print('Retrying')
            time.sleep(5)
            continue  # without increase i var (retry)
        # print(response)
        if not response['items']:
            break
        for item in response['items']:
            current_user_messages.append(item)
        print(str(i * 200) + ' of ' + str(response['count']) + ' messages (vk.com/id' + str(user_id) + ')')
        i += 1
    with open('output_m/messages/' + str(user_id) + '.json', 'w') as f:
        json.dump(current_user_messages, f)
    return


# II
def history():
    with open('output_m/pure_chats.json', 'r') as f:
        dialog_list = json.load(f)
    for i in dialog_list:
        get_all_messages_from_dialog(int(i['message']['chat_id']) + 2000000000)  # important shit

# get_all_dialogs(1)
history()
