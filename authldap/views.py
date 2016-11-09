from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from authldap.utils import *
from authldap.models import UserLog

from django.contrib.auth.models import Permission


class AuthToken(ObtainAuthToken):
    def post(self, request):
        request = validate_username(request.data.copy())
        serializer = self.serializer_class(data=request)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        UserLog.objects.create(user=user, type='login')
        groups = [group['id'] for group in user.groups.values()]
        return Response({
            'id': user.id,
            'token': token.key,
            'name': user.first_name,
            'email': user.email,
            'is_staff': user.is_staff,
            'group': [group['name'] for group in user.groups.values()],
            'permissions': Permission.objects.filter(group__id__in=groups).values_list('codename',
                                                                                       flat=True)
        })


class LogoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated():
            user = request.user
            UserLog.objects.create(user=user, type='logout')
            # Token.objects.get(user=user).delete()
            return Response({
                'user': 'User logout success'
            })
        else:
            return Response({
                'user': 'User logout failed'
            })
