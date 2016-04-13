import re
from django.conf import settings


def validateUsername(request):
    
    regex = re.compile('([^\\s]+)\\@[^\\s]+')

    if settings.USERNAME_SUFIX is not None:
        if request.get('username').find(settings.USERNAME_SUFIX) > 0:
            matched = regex.match(request.get('username'))

            if matched:
                value = "%s%s" % (matched.group(1), settings.USERNAME_NEW_SUFIX)
                request.__setitem__('username', value)


    return request