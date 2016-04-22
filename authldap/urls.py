from django.conf.urls import url

from .views import AuthToken, LogoutView


app_name = 'authldap'

urlpatterns = [

    url(r'^login/', AuthToken.as_view(), name='token-auth'),
    url(r'^logout/', LogoutView.as_view(), name='logout')

]
