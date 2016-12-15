from parse import parse
from api.exceptions import *
import api.vk as vk


def main():
    #  print(vk.users_get(1, ['online', 'sex']))
    #  print(vk.wall_get('catcontrolcenter', 1))
    #  print(vk.likes_add(-135179098, 2))
    try:
        print(vk.messages_send(user_id=1, message='Test'))
    except VkException as e:
        print(str(e))
    #  print(vk.messages_get_history(peer_id=227957341, count=3))
    #  print(vk.friends_add(user_id=374781505))
    #  print(vk.wall_repost('wall-135179098_2'))
    return

main()
