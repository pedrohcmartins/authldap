from django.conf.urls import url

from .views import AuthToken, LogoutView, ChangePasswordView


app_name = 'authldap'

urlpatterns = [

    url(r'^login/', AuthToken.as_view(), name='token-auth'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^change-pass/', ChangePasswordView.as_view(), name='change-pass'),

]
