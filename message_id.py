import api.vk as vk


def msg(message_id):
    return vk.messages_get_by_id(message_id)

