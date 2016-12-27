import os
import requests
from api.apihelper import check_fields
from api.apihelper import result_parser
from api.exceptions import *

API = 'https://api.vk.com/method/'


# @check_fields('users_get')
def users_get(user_ids=1, fields=None, name_case='nom'):
    """Usage example: users_get(1, ['online', 'timezone'])"""
    if isinstance(user_ids, list):
        user_ids = ','.join([str(f) for f in user_ids])
    if isinstance(fields, list):
        fields = ','.join([str(f) for f in fields])
    parameters = dict(user_ids=user_ids, fields=fields, name_case=name_case, access_token=os.environ['VK_TOKEN'],
                      v=os.environ['API_VERSION'])
    request = requests.get(API + 'users.get', params=parameters)
    return result_parser(request.json(), UsersGetException)


def wall_get(target=0, count=None, offset=None, filter=None, fields=None):
    """Usage example: wall_get('catcontrolcenter', 10)"""
    if isinstance(fields, list):
        fields = ','.join([str(f) for f in fields])
    parameters = dict(fields=fields, offset=offset, count=count, filter=filter, access_token=os.environ['VK_TOKEN'],
                      v=os.environ['API_VERSION'], extended=0 if not fields else 1)
    if isinstance(target, str):
        parameters['domain'] = target
    else:
        parameters['owner_id'] = target

    request = requests.get(API + 'wall.get', params=parameters)
    return result_parser(request.json(), WallGetException)


def likes_add(owner_id=None, item_id=0, type='post', access_key=None):
    """Usage example: likes_add(-135179098, 2)"""
    parameters = dict(access_token=os.environ['VK_TOKEN'], v=os.environ['API_VERSION'], owner_id=owner_id,
                      item_id=item_id, type=type, access_key=access_key)
    request = requests.get(API + 'likes.add', params=parameters)
    if 'response' in request.json():
        return True
    else:
        return result_parser(request.json(), LikesAddException)


def messages_send(user_id=None, peer_id=None, domain=None, chat_id=None,
                  message=None, attachment=None, forward_messages=None, sticker_id=None):
    """Use try/catch"""
    parameters = dict(access_token=os.environ['VK_TOKEN'], v=os.environ['API_VERSION'], user_id=user_id,
                      peer_id=peer_id, domain=domain, chat_id=chat_id, message=message, attachment=attachment,
                      forward_messages=forward_messages, sticker_id=sticker_id)
    request = requests.get(API + 'messages.send', params=parameters)
    if 'response' in request.json():
        return True
    else:
        return result_parser(request.json(), MessagesSendException)


def messages_get_dialogs(count=None, offset=None, start_message_id=None, preview_length=None,
                         unread=None, important=None, unanswered=None):
    """Usage example: messages_get_dialogs(count=20)"""
    parameters = dict(access_token=os.environ['VK_TOKEN'], v=os.environ['API_VERSION'],
                      count=count, offset=offset, start_message_id=start_message_id,
                      preview_length=preview_length, unread=unread, important=important, unanswered=unanswered)
    request = requests.get(API + 'messages.getDialogs', params=parameters)
    return result_parser(request.json(), MessagesGetDialogsException)


def messages_get_history(count=None, offset=None, user_id=None, peer_id=None, start_message_id=None, rev=None):
    """Usage example: messages_get_history(peer_id=1, count=10)"""
    parameters = dict(access_token=os.environ['VK_TOKEN'], v=os.environ['API_VERSION'],
                      count=count, offset=offset, start_message_id=start_message_id,
                      user_id=user_id, peer_id=peer_id, rev=rev)
    request = requests.get(API + 'messages.getHistory', params=parameters, timeout=10.0)
    return result_parser(request.json(), MessagesGetHistoryException)


def friends_add(user_id=None, text=None, follow=None):
    """Usage example: friends_add(user_id=1)"""
    parameters = dict(access_token=os.environ['VK_TOKEN'], v=os.environ['API_VERSION'],
                      user_id=user_id, text=text, follow=follow)
    request = requests.get(API + 'friends.add', params=parameters)
    if 'response' in request.json():
        return True
    else:
        return result_parser(request.json(), FriendsAddException)


def wall_repost(object=None, message=None):
    """Usage example: wall_repost('wall-135179098_2', 'Nice meme')"""
    parameters = dict(access_token=os.environ['VK_TOKEN'], v=os.environ['API_VERSION'],
                      object=object, message=message)
    request = requests.get(API + 'wall.repost', params=parameters)
    return result_parser(request.json(), WallRepostException)


def messages_get_by_id(message_ids=None):
    """Returns list of messages"""
    parameters = dict(access_token=os.environ['VK_TOKEN'], v=os.environ['API_VERSION'], message_ids=message_ids)
    request = requests.get(API + 'messages.getById', params=parameters)
    response = request.json()
    if 'response' in response:
        return response['response']['items']
    else:
        raise MessagesGetByIdException


# # TODO
# def photos_get_by_id(photos=None):
#     """Doc"""
#     parameters = dict(access_token=os.environ['VK_TOKEN'], v=os.environ['API_VERSION'], photos=photos)
#     request = requests.get(API + 'photos.getById', params=parameters)
#     response = request.json()
#     if 'response' in response:
#         return response['response']
#
#
# # TODO
# def docs_get_by_id(docs=None):
#     """Doc"""
#     parameters = dict(access_token=os.environ['VK_TOKEN'], v=os.environ['API_VERSION'], docs=docs)
#     request = requests.get(API + 'docs.getById', params=parameters)
#     response = request.json()
#     if 'response' in response:
#         return response['response']
#     else:
#         return response
