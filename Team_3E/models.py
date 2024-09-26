from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Users(AbstractBaseUser):
    user_id     = models.CharField(max_length = 50, unique = True)
    password    = models.CharField(max_length = 200)
    name        = models.CharField(max_length = 50)
    email       = models.EmailField(max_length = 50)

    USERNAME_FIELD = 'user_id'

