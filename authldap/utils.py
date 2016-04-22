import re
from django.conf import settings


def validate_username(request):
    
    regex = re.compile('([^\\s]+)\\@[^\\s]+')

    if settings.USERNAME_SUFFIX is not None:
        if (request.__getitem__('username').find(settings.USERNAME_SUFFIX)) >= 0:
            matched = regex.match(request.__getitem__('username'))
            if matched:
                name = "%s%s" % (matched.group(1), settings.USERNAME_NEW_SUFFIX)
                request.__setitem__('username', name)

    return request
