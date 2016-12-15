import os
import requests
from api.apihelper import check_fields
from api.apihelper import result_parser

API = 'https://api.vk.com/method/'


class UsersGetException(Exception):
    pass


class LikesAddException(Exception):
    pass


class MessagesSendException(Exception):
    pass


class WallGetException(Exception):
    pass


@check_fields('users_get')
def users_get(user_ids=1, fields=None, name_case='nom'):
    if isinstance(user_ids, list):
        user_ids = ','.join([str(f) for f in user_ids])
    if isinstance(fields, list):
        fields = ','.join([str(f) for f in fields])
    parameters = dict(user_ids=user_ids, fields=fields, name_case=name_case, access_token=os.environ['VK_TOKEN'],
                      v=os.environ['API_VERSION'])
    request = requests.get(API + 'users.get', params=parameters)
    response = request.json()
    return result_parser(response, UsersGetException)


def wall_get(target=0, count=None, offset=None, filter=None, fields=None):
    if isinstance(fields, list):
        fields = ','.join([str(f) for f in fields])
    parameters = dict(fields=fields, offset=offset, count=count, filter=filter, access_token=os.environ['VK_TOKEN'],
                      v=os.environ['API_VERSION'], extended=0 if not fields else 1)
    if isinstance(target, str):
        parameters['domain'] = target
    else:
        parameters['owner_id'] = target

    request = requests.get(API + 'wall.get', params=parameters)
    print(request.url)
    response = request.json()
    return result_parser(response, WallGetException)


def likes_add(owner_id=None, item_id=0, type='post', access_key=None):
    parameters = dict(access_token=os.environ['VK_TOKEN'], v=os.environ['API_VERSION'], owner_id=owner_id,
                      item_id=item_id, type=type, access_key=access_key)
    request = requests.get(API + 'likes.add', params=parameters)
    if 'response' in request.json():
        return True
    else:
        return result_parser(request.json(), LikesAddException)


def messages_send(user_id=None, peer_id=None, domain=None, chat_id=None,
                  message=None, attachment=None, forward_messages=None, sticker_id=None):
    parameters = dict(access_token=os.environ['VK_TOKEN'], v=os.environ['API_VERSION'], user_id=user_id,
                      peer_id=peer_id, domain=domain, chat_id=chat_id, message=message, attachment=attachment,
                      forward_messages=forward_messages, sticker_id=sticker_id)
    request = requests.get(API + 'messages.send', params=parameters)
    if 'response' in request.json():
        return True
    else:
        return result_parser(request.json(), MessagesSendException)
