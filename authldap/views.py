from django.contrib.auth.models import Permission
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.response import Response

from authldap.models import UserLog
from authldap.utils import *


class AuthToken(ObtainAuthToken):
    def post(self, request, **kwargs):
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
            'is_superuser': user.is_superuser,
            'coordenacao_regional': user.coordenacao_regional,
            'group': [group['name'] for group in user.groups.values()],
            'permissions': Permission.objects.filter(group__id__in=groups).values_list('codename',
                                                                                       flat=True)
        })


class LogoutView(APIView):
    @staticmethod
    def post(request):
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
