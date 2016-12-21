from api.exceptions import *
import api.vk as vk
import api.longpoll as longpoll


def main():
    poll = longpoll.LongPoll()
    while True:
        print(poll.get())

main()
