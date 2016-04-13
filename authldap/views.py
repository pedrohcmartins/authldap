from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from authldap.utils import * 


class AuthToken(ObtainAuthToken):

    def post(self, request):
        request = validateUsername(request.data.copy())
        serializer = self.serializer_class(data=request)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
                'token': token.key, 
                'user': user.username,
                'name': user.first_name,
                'email': user.email,
                'suser': user.is_superuser,
                })