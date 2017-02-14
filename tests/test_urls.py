#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_authldap
------------

Tests for `authldap` models module.
"""

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import (
    APIClient, APIRequestFactory, force_authenticate
)

from authldap.models import UserLog

class TestAuthldap(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user1',
            password="secret1",
            email="user1@user.com",
            first_name="new_user"
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password="secret2",
            email="user2@user.com",
            first_name="old_user",
            is_staff=True
        )

    def test_response_url(self):
        self.assertEqual(User.objects.count(), 2)
        response = self.client.post(
            reverse('token-auth'),
            {'username': 'user1',
             'password': 'secret1'}
        )

        token = Token.objects.get(user__username=self.user).key
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('id'), 1)
        self.assertEqual(response.data.get('email'), 'user1@user.com')
        self.assertEqual(response.data.get('name'), 'new_user')
        self.assertEqual(response.data.get('token'), token)
        self.assertFalse(response.data.get('is_staff'))
        self.assertEqual(UserLog.objects.filter(user=self.user).count(), 1)
        self.assertEqual(UserLog.objects.get(user=self.user).type, 'login')
        self.assertEqual(UserLog.objects.count(), 1)

        response = self.client.post(
            reverse('token-auth'),
            {'username': 'user2',
             'password': 'secret2'}
        )

        token = Token.objects.get(user=self.user2).key
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('id'), 2)
        self.assertEqual(response.data.get('email'), 'user2@user.com')
        self.assertEqual(response.data.get('name'), 'old_user')
        self.assertEqual(response.data.get('token'), token)
        self.assertTrue(response.data.get('is_staff'))
        self.assertEqual(UserLog.objects.filter(user=self.user2).count(), 1)
        self.assertEqual(UserLog.objects.get(user=self.user2).type, 'login')
        self.assertEqual(UserLog.objects.filter(type='login').count(), 2)
        self.assertEqual(UserLog.objects.count(), 2)

        # Deleting user 2 to validate creation user id
        self.user2.delete()

        self.user3 = User.objects.create_user(
            username='user3',
            password="secret3",
            email="user3@user.com",
            first_name="new_user_test",
        )

        response = self.client.post(
            reverse('token-auth'),
            {'username': 'user3',
             'password': 'secret3'}
        )

        self.assertEqual(response.data.get('id'), 3)


    def test_response_with_user_model_response(self):
        settings.AUTH_USER_RESPONSE = {
            'username': 'username'
        }

        response = self.client.post(
            reverse('token-auth'),
            {'username': 'user1',
             'password': 'secret1'}
        )        

        self.assertFalse(response.data.get('is_staff'))
        self.assertFalse(response.data.get('is_superuser'))
        self.assertEqual(response.data['username'], 'user1')

    def test_ldap_response(self):

        if hasattr(settings, 'LDAP_AUTH_URL')\
            and hasattr(settings, 'LDAP_USER')\
            and hasattr(settings, 'LDAP_PASSWORD'):
            response = self.client.post(
                reverse('token-auth'),
                {'username': settings.LDAP_USER,
                 'password': settings.LDAP_PASSWORD}
            )        
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.user.delete()


class TestAuthenticationUrl(TestCase):
    """docstring for TestAuthenticationUrl"""
    def setUp(self):
        self.url_change_pass = reverse('change-pass')
        self.url_login = reverse('token-auth')
        self.raw_pass = User.objects.make_random_password()
        self.user = User.objects.create_user(
            username='user1',
            password=self.raw_pass,
            email="user1@user.com",
            first_name="new_user"
        )

    def test_auth_url(self):
        
        login = self.client.post(
            reverse('token-auth'),
            {'username': 'user1',
             'password': self.raw_pass}
        )

        self.assertEqual(login.status_code, 200)
        self.assertEqual(login.data['email'], 'user1@user.com')
        token = login.data['token']

        client = APIClient()
        client.force_authenticate(user=self.user, token=token)

        request = client.put(
            self.url_change_pass,
            {
                'new_pass': 'user1',
                'old_pass': self.raw_pass
            }
        )

        self.assertEqual(request.status_code, 200)
        
        login_error = self.client.post(
            reverse('token-auth'),
            {'username': 'user1',
             'password': self.raw_pass}
        )
        self.assertEqual(login_error.status_code, 400)
        self.assertEqual(login_error.data['non_field_errors'],
            ['Unable to log in with provided credentials.'] )

        login = self.client.post(
            reverse('token-auth'),
            {'username': 'user1',
             'password': 'user1'}
        )
        self.assertEqual(login.status_code, 200)


    def test_last_login(self):

        user = User.objects.create_user(
            username='user2',
            password='another_pass',
            email="user2@user.com",
            first_name="another_user"
        )

        for i in range(10):

            login = self.client.post(
                reverse('token-auth'),
                {'username': 'user1',
                 'password': self.raw_pass}
            )
            self.assertEqual(login.status_code, 200)
            self.assertEqual(login.data['email'], 'user1@user.com')
            if i == 0:
                self.assertEqual(login.data['new_user'], True)
            else:    
                self.assertEqual(login.data['new_user'], False)

        login = self.client.post(
            reverse('token-auth'),
            {'username': 'user2',
             'password': 'another_pass'}
        )
        self.assertEqual(login.status_code, 200)
        self.assertEqual(login.data['email'], 'user2@user.com')
        self.assertEqual(login.data['new_user'], True)

        login = self.client.post(
            reverse('token-auth'),
            {'username': 'user2',
             'password': 'another_pass'}
        )
        self.assertEqual(login.status_code, 200)
        self.assertEqual(login.data['email'], 'user2@user.com')
        self.assertEqual(login.data['new_user'], False)

    def tearDown(self):
        for token in Token.objects.all():
            token.delete()

        for user in User.objects.all():
            user.delete()

        self.assertEqual(Token.objects.count(), 0)
        self.assertEqual(User.objects.count(), 0)