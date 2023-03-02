from django.db import models
from enum import Enum


class PowerShare(Enum):
    SUPERADMIN = 'superadmin'
    USER = 'user'
    STAFF = 'staff'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

# class that resgisters new users


class User(models.Model):
    fullname = models.CharField(max_length=200, blank=True)
    username = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)
    current_position = models.CharField(max_length=100, blank=True)
    access = models.CharField(
        choices=PowerShare.choices(), default=PowerShare.STAFF, max_length=50)
    status = models.CharField(max_length=100, default="true")

    def __str__(self):
        return self.username
