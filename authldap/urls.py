from django.conf.urls import url

from .views import AuthToken


app_name = 'authldap'

urlpatterns = [

    url(r'^login/', AuthToken.as_view(), name='token-auth')

]