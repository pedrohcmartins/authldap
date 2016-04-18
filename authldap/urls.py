from django.conf.urls import url

from .views import AuthToken, logoutView


app_name = 'authldap'

urlpatterns = [

    url(r'^login/', AuthToken.as_view(), name='token-auth'),
    url(r'^logout/', logoutView.as_view(), name='logout')

]
