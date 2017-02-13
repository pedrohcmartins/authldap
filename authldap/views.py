from django.conf import settings
from django.contrib.auth.models import Permission

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.generics  import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authldap.models import UserLog
from authldap.utils import validate_username, get_user_data
from authldap.serializers import ChangePasswordSerializer


class AuthToken(ObtainAuthToken):
    def post(self, request, **kwargs):
        request = validate_username(request.data.copy())
        serializer = self.serializer_class(data=request)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        UserLog.objects.create(user=user, type='login')
        groups = [group['id'] for group in user.groups.values()]

        response = {
            'token': token.key,
            'id': user.id,
            'name': user.first_name,
            'email': user.email,
            'group': [group['name'] for group in user.groups.values()],
            'permissions': Permission.objects.filter(
                    group__id__in=groups
                    ).values_list('codename', flat=True)
        }

        if hasattr(settings, 'AUTH_USER_RESPONSE'):
            response.update(
                get_user_data(settings.AUTH_USER_RESPONSE, user)
            )

        return Response(response, status=status.HTTP_200_OK)


class LogoutView(APIView):
    @staticmethod
    def post(request):
        if request.user.is_authenticated():
            user = request.user
            UserLog.objects.create(user=user, type='logout')

            return Response({
                'user': 'User logout success'
            }, status=status.HTTP_200_OK)

        return Response({
            'user': 'User logout failed'
        })


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = settings.AUTH_USER_MODEL

    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_pass")):
                return Response({"data": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_pass"))
            self.object.save()
            return Response({"data": ["Password update succesfull"]}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
