# Create your models here.
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser , PermissionsMixin
from .manager import UserManager
# Create your models here.


class User(AbstractUser , PermissionsMixin):
    username = models.CharField(max_length=150 , blank=True , null=True , default="")
    email = models.EmailField(db_index=True ,unique=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.email
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    