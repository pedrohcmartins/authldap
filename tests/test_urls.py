#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_authldap
------------

Tests for `authldap` models module.
"""

from django.test import TestCase, Client

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model


client = Client()

class TestAuthldap(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user1', 
            password="secret1", 
            email="user1@user.com",
            first_name="new_user"
            )
        self.user2 = User.objects.create_user(username='user2',
            password="secret2",
            email="user2@user.com",
            first_name="old_user",
            is_superuser=True
            )

    def test_response_url(self):
        self.assertEqual(User.objects.count(), 2)
        response = self.client.post(
            reverse('token-auth'),
            {'username': 'user1',
            'password': 'secret1'}
        )

        token = Token.objects.filter(user=self.user)[0].key
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('email'), 'user1@user.com')
        self.assertEqual(response.data.get('name'), 'new_user')
        self.assertEqual(response.data.get('token'), token)
        self.assertEqual(response.data.get('suser'), False)


        response = self.client.post(
            reverse('token-auth'),
            {'username': 'user2',
            'password': 'secret2'}
        )

        token = Token.objects.filter(user=self.user2)[0].key
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('email'), 'user2@user.com')
        self.assertEqual(response.data.get('name'), 'old_user')
        self.assertEqual(response.data.get('token'), token)
        self.assertEqual(response.data.get('suser'), True)

    def tearDown(self):
        self.user.delete()
        self.user2.delete()
