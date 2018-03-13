import dialogs
import json
import os
import api.vk as vk
from time import sleep

output_directory = os.environ['OUT_DIR']
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
    if not os.path.exists(output_directory + '/counts.json'):
        print('First run...')
        data = {}
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
            last_count = data.get(str(user_id))
        if last_count is None:
            pass  # No info about count
        else:
            current_count = vk.messages_get_history(count=0, peer_id=user_id)['count']
            print(str(current_count) + ' - current count')
            print(str(last_count) + ' - last count')
            already = current_count - last_count
            if last_count == 0:
                already = current_count
            print(str(already) + ' new messages from peer ' + str(user_id))
            if already > 0:
                print('Downloading new messages...')
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
            else:
                print('Nothing to do')
                print('----------')
                return
            print('Completed. Updating ' + str(user_id) + '.json file')
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
        print('Downloading... ' + str(i / 200) + '/' + str(round(response['count'] / 200)) + ' (vk.com/id' + str(
            user_id) + ')')
        i += 200
    if already is None:
        print('Completed')
    with open(output_directory + '/messages/' + str(user_id) + '.json', 'w') as f:
        json.dump(current_user_messages, f)
    print('File ' + str(user_id) + '.json has been successfully saved')
    # Counts
    print('Updating counts.json')
    with open(output_directory + '/counts.json', 'r') as d:
        data = json.load(d)
    data[str(user_id)] = vk.messages_get_history(count=0, peer_id=user_id)['count']
    with open(output_directory + '/counts.json', 'w') as d:
        json.dump(data, d)
    print('Completed')
    print('----------')


def save_all_messages():
    with open(output_directory + '/dialogs.json') as f:
        dialog_list = json.load(f)
    for i in dialog_list:
        if 'chat_id' in i['message']:
            msg(int(i['message']['chat_id']) + 2000000000)
        else:
            msg(int(i['message']['user_id']))


if __name__ == '__main__':
    if not os.path.exists(output_directory + '/dialogs.json'):
        get_dialogs()
    save_all_messages()
