#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_authldap
------------

Tests for `authldap` models module.
"""

from django.test import TestCase, Client

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from authldap.models import UserLog

client = Client()


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


    def tearDown(self):
        self.user.delete()
