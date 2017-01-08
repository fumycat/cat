import api.vk as vk
import time
import pprint


def parse_post(post):
    return


def posts(hook, whereto):
    while True:
        pprint.pprint(hook.get())
        time.sleep(20)


class PostHook:
    def __init__(self, group_id):
        self.id = group_id
        self.last_post = int(time.time())
        vk.groups_get_by_id(self.id)  # check

    def get(self):
        wall = vk.wall_get(self.id)['items']
        response = []
        for i in wall:
            if i['date'] > self.last_post:
                response.append(i)
        for i in wall:
            if i['date'] > self.last_post:
                self.last_post = i['date']
        return response
