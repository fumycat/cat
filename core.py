from api.vk import users_get
from api.vk import wall_get


def main():
    #  print(users_get(1, ['online', 'sex']))
    print(wall_get('fumycat', 1))
    return

main()
