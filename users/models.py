from django.db import models
from django.contrib.auth.models import AbstractUser

from users.managers import CustomUserManager


class User(AbstractUser):
    '''
    The model to store users

    - username: is None (we don't authenticate with username)
    - email: the user email, unique 
    - phone: the user phone number
    - email_verified: whether email is verified or not
    '''
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=25, default='', blank=True)
    email_verified = models.BooleanField(default=False)
   

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.email
