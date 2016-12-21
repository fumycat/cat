import requests
import os


class LongPoll(object):
    def __init__(self):
        self.k = ''
        self.s = ''
        self.t = ''
        parameters = dict(access_token=os.environ['VK_TOKEN'], v=os.environ['API_VERSION'])
        request = requests.get('https://api.vk.com/method/messages.getLongPollServer', params=parameters)
        response = request.json()
        if 'response' in response:
            self.k = response['response']['key']
            self.s = response['response']['server']
            self.t = response['response']['ts']
        else:
            raise LongPollException('getLongPollServer error')

    def get(self):
        r = requests.get('https://%s?act=a_check&key=%s&ts=%s&wait=25&mode=2&version=1' % (self.s, self.k, self.t))
        response = r.json()
        if 'ts' in response:
            self.t = response['ts']
            return response['updates']
        else:
            raise LongPollException(str(response))


class LongPollException(Exception):
    pass
