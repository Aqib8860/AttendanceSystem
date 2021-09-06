from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager

# Create your models here.


USER_TYPE = (
    ("Admin", "Admin"),
    ("Student", "Student"),
    ("Teacher", "Teacher"),
)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    address = models.TextField()
    subscribed = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


class Attendance(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True, null=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)