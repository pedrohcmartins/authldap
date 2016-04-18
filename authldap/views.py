from django.contrib.auth import logout
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from authldap.utils import *
from authldap.models import UserLog


class AuthToken(ObtainAuthToken):

    def post(self, request):
        request = validateUsername(request.data.copy())
        serializer = self.serializer_class(data=request)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        UserLog.objects.create(user=user, type='login')
        return Response({
            'token': token.key,
            'name': user.first_name,
            'email': user.email,
            'suser': user.is_superuser,
        })


class logoutView(APIView):

    def post(self, request):
        if request.user.is_authenticated():
            logout(request)
            UserLog.objects.create(user=user, type='logout')

            return Response({
                'user': 'User logout with success'
            })
