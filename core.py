from parse import parse
from api.vk import users_get
from api.vk import wall_get
from api.vk import likes_add
from api.vk import messages_send
from api.vk import messages_get_dialogs
from api.vk import messages_get_history


def main():
    #  print(users_get(1, ['online', 'sex']))
    #  print(wall_get('catcontrolcenter', 1))
    #  print(likes_add(-135179098, 2))
    #  print(messages_send(domain='fumycat', message='Test'))
    print(messages_get_history(peer_id=227957341, count=3))
    return

main()
