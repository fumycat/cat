from api.exceptions import *
import api.vk as vk
from api.longpoll import LongPoll
from api.longpoll import LongPollException


def main():
    poll = LongPoll()
    while True:
        try:
            data = poll.get()
            print(data)  # DEL
            if not data:
                continue  # skip empty
            # in case of message
            # data[0] - ignore
            # data[1] - message id
            # data[2] - ??
            # data[3] - user id
            # data[4] - unix time
            # data[5] - chat name
            # data[6] - text
            # data[-1] - attachments
        except LongPollException:
            poll = LongPoll()


main()
