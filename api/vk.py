import os
import requests
from api.apihelper import check_fields

API = 'https://api.vk.com/method/'


class UsersGetException(Exception):
    pass


@check_fields('users_get')
def users_get(user_ids=1, fields=None, name_case='nom'):
    parameters = {'user_ids': user_ids,
                  'fields': fields,
                  'name_case': name_case,
                  'access_token': os.environ['VK_TOKEN'],
                  'v': os.environ['API_VERSION']}
    request = requests.get(API + 'users.get', params=parameters)
    response = request.json()
    if 'error' in response:
        raise UsersGetException('TODO')  # TODO
    elif 'response' in response:
        if len(response['response']) == 1:
            return response['response'][0]
        elif len(response['response']) > 1:
            return response['response']
        else:
            raise UsersGetException('TODO')  # TODO
