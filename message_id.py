import api.vk as vk
import sys


print(vk.messages_get_by_id(sys.argv[1]))

