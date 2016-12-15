class VkException(Exception):
    pass


class UsersGetException(VkException):
    pass


class LikesAddException(VkException):
    pass


class MessagesSendException(VkException):
    pass


class WallGetException(VkException):
    pass


class MessagesGetDialogsException(VkException):
    pass


class MessagesGetHistoryException(VkException):
    pass


class FriendsAddException(VkException):
    pass


class WallRepostException(VkException):
    pass
