# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import User
class Entries(models.Model):
    @property
    def user(self):
        return User.objects.get(pk=self.user_id)