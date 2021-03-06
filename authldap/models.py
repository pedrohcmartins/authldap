# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class UserLog(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username
