from threading import Thread

from post_hook import posts, PostHook


if_list = ['catcontrolcenter']
of_list = ['catcontrolcenter']

for if_group in if_list:
    h = PostHook(if_group)
    Thread(target=posts, args=[h, of_list]).start()
