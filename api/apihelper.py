fields_list_user = ['photo_id', 'verified', 'sex', 'bdate', 'city', 'country', 'home_town', 'has_photo', 'photo_50',
                    'photo_100', 'photo_200_orig', 'photo_200', 'photo_400_orig', 'photo_max', 'photo_max_orig',
                    'online',
                    'lists', 'domain', 'has_mobile', 'contacts', 'site', 'education', 'universities', 'schools',
                    'status',
                    'last_seen', 'followers_count', 'common_count', 'occupation', 'nickname', 'relatives', 'relation',
                    'personal', 'connections', 'exports', 'wall_comments', 'activities', 'interests', 'music', 'movies',
                    'tv', 'books', 'games', 'about', 'quotes', 'can_post', 'can_see_all_posts', 'can_see_audio',
                    'can_write_private_message', 'can_send_friend_request', 'is_favorite', 'is_hidden_from_feed',
                    'timezone',
                    'screen_name', 'maiden_name', 'crop_photo', 'is_friend', 'friend_status', 'career', 'military',
                    'blacklisted', 'blacklisted_by_me']

fields_list_group = ['city', ' country', ' place', ' description', ' wiki_page', ' members_count', ' counters',
                     ' start_date', ' finish_date', ' can_post', ' can_see_all_posts', ' activity', ' status',
                     ' contacts', ' links', ' fixed_post', ' verified', ' site', ' can_create_topic']

checker = {'users_get': fields_list_user,
           'groups_get': fields_list_group}


class FieldsException(Exception):
    pass


def check_fields(which):
    def check_fields_dec(fun):
        def wrapper(*args):
            if len(list(args)) > 1:
                if isinstance(list(args)[1], str):
                    if list(args)[1] not in checker[which]:
                        raise FieldsException('Invalid field')
                else:
                    for field in list(args)[1]:
                        if field not in checker[which]:
                            raise FieldsException('Invalid field')
            return fun(*args)

        return wrapper

    return check_fields_dec


def result_parser(response, exception):
    if 'error' in response:
        raise exception('TODO')  # TODO
    elif 'response' in response:
        if len(response['response']) == 1:
            return response['response'][0]
        elif len(response['response']) > 1:
            return response['response']
        else:
            raise exception('TODO')  # TODO
