import api.vk as vk


class Users:

    def __init__(self):
        self.cache = {}

    def get(self, user_id, fields=None):
        if user_id in self.cache:
            return self.cache[user_id]
        else:
            data = vk.users_get(user_id, fields)
            self.cache[user_id] = data
            return data
