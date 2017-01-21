import dialogs
import json
import os
import api.vk as vk
from time import sleep

output_directory = 'out'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    print('Creating ' + output_directory + ' directory')


def get_dialogs():
    print('Downloading dialog list...')

    dialog_list = dialogs.last_dialogs(count=40000, parse=False)
    with open(output_directory + '/dialogs.json', 'w') as f:
        print('Saving to file...')
        json.dump(dialog_list, f)


def msg(user_id):
    if os.path.exists(output_directory + 'counts.json'):
        print('First run...')
        data = {}
        # with open(output_directory + '/dialogs.json', 'r') as d:
        #     dialogs_list = json.load(d)
        # for i in dialogs_list:
        #     if 'chat_id' in i['message']:
        #         peer_id = int(i['message']['chat_id']) + 2000000000
        #     else:
        #         peer_id = int(i['message']['user_id'])
        #     data[peer_id] = vk.messages_get_history(count=0, peer_id=peer_id)['count']
        with open(output_directory + '/counts.json', 'w') as f:
            json.dump(data, f)
    # Main
    if not os.path.exists(output_directory + '/messages'):
        os.makedirs(output_directory + '/messages')
        print('Creating messages directory')
    already = None
    current_user_messages = []
    if os.path.exists(output_directory + '/messages/' + str(user_id) + '.json'):
        with open(output_directory + '/counts.json', 'r') as d:
            data = json.load(d)
        data.get(user_id)
        if data is None:
            pass  # No info about count
        else:
            already = data - vk.messages_get_history(count=0, peer_id=user_id)['count']
            print(str(already) + ' new messages from ' + str(user_id))
            if already > 0:
                x = already // 200
                y = already % 200
                j = 0
                while x > 0:
                    res = vk.messages_get_history(peer_id=user_id, count=200, offset=200 * j)
                    for m in res:
                        if m is not None:
                            current_user_messages.append(m)
                        if not m:
                            break
                    x -= 1
                    j += 1
                res = vk.messages_get_history(peer_id=user_id, count=y, offset=200 * j)
                for k in res:
                    if k is not None:
                        current_user_messages.append(k)
            with open(output_directory + '/messages/' + str(user_id) + '.json', 'r') as f:
                what_i_have = json.load(f)
            current_user_messages = current_user_messages + what_i_have
            # [5, 4, 3] + [2, 1] = [5, 4, 3, 2, 1]


    i = 0
    while already is None:
        try:
            response = vk.messages_get_history(peer_id=user_id, count=200, offset=i)
        except:
            print('Error while getting message history. Page ' + str(i))
            print('Retrying')
            sleep(5)
            continue  # without increase i var (retry)
        # print(response)
        if not response['items']:
            break
        for item in response['items']:
            current_user_messages.append(item)
        print(str(i) + '/' + str(response['count'] / 200) + ' messages (vk.com/id' + str(user_id) + ')')
        i += 200
    with open(output_directory + '/messages/' + str(user_id) + '.json', 'w') as f:
        json.dump(current_user_messages, f)
    # Counts
    with open(output_directory + '/counts.json', 'r') as d:
        data = json.load(d)
    data[user_id] = vk.messages_get_history(count=0, peer_id=user_id)['count']
    with open(output_directory + '/counts.json', 'w') as d:
        json.dump(data, d)
