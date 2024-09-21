from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Users(AbstractBaseUser):
    user_id = models.CharField(max_length = 50, unique = True)
    password = models.CharField(max_length = 50)
    name = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 50)
    money = models.IntegerField(default = 5000)
    sword_level = models.IntegerField(default = 0)

    USERNAME_FIELD = 'user_id'


class Posts(models.Model):
    connected_user = models.ForeignKey(Users, on_delete = models.CASCADE, related_name = 'posts')
    title = models.CharField(max_length = 50)
    content = models.TextField()
    author = models.CharField(max_length = 50, default = "")


class Messages(models.Model):
    connected_user = models.ForeignKey(Users, on_delete = models.CASCADE, related_name = 'messages')
    recipient = models.CharField(max_length = 50)
    title = models.CharField(max_length = 50)
    content = models.TextField()

