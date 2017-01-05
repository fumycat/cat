import api.vk as vk


def parse_message(msg, fwd=False):
    """Returns list of message objects"""
    when = int(msg['date'])  # unix time
    message_id = '' if fwd else str(msg['id'])
    if 'attachments' in msg:
        pass  # TODO
    parsed_message = {'message_id': message_id, 'date': when, 'from': msg['user_id'], 'text': msg['body']}
    if 'fwd_messages' in msg:
        parsed_message['fwd'] = []
        for fwd_message in msg['fwd_messages']:
            parsed_message['fwd'].append(parse_message(fwd_message, True))
    return parsed_message


def history_generator(count=20, peer_id=1, offset=0):
    for message in vk.messages_get_history(count=count, peer_id=peer_id, offset=offset)['items']:
        yield parse_message(message)  # yield ?
