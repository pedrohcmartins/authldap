import re
from django.conf import settings


def validateUsername(request):
    
    regex = re.compile('([^\\s]+)\\@[^\\s]+')

    if settings.USERNAME_SUFIX is not None:
        if (request.__getitem__('username').find(settings.USERNAME_SUFIX)) >= 0:
            matched = regex.match(request.__getitem__('username'))
            if matched:
                name = "%s%s" % (matched.group(1), settings.USERNAME_NEW_SUFIX)
                request.__setitem__('username', name)

    return request