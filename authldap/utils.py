import re
from django.conf import settings


def validate_username(request):
    """ Returns a validated username with USERNAME_SUFFIX from settings """
    regex = re.compile('([^\\s]+)\\@[^\\s]+')

    # try settings.USERNAME_SUFFIX:
    if hasattr(settings, 'USERNAME_SUFFIX'):
        if (request.__getitem__('username').find(settings.USERNAME_SUFFIX)) >= 0:
            matched = regex.match(request.__getitem__('username'))
            if matched:
                name = "%s%s" % (matched.group(1), settings.USERNAME_NEW_SUFFIX)
                request.__setitem__('username', name)

    return request

def get_user_data(arr_list, data):
    """Returns a object with attributes from 'data' param """
    obj = {}
    for k, value in arr_list.items():
        obj[k] = data.__getattribute__(value)
    return obj