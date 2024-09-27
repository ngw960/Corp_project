from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsersManager(BaseUserManager):
    def create_user(self, user_id, password=None, **extra_fields):
        """사용자 생성 메서드"""
        if not user_id:
            raise ValueError("The User ID must be set")
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)  # 비밀번호 해시화
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password=None, **extra_fields):
        """관리자 사용자 생성 메서드"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(user_id, password, **extra_fields)

class Users(AbstractBaseUser):
    user_id  = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=200)
    name     = models.CharField(max_length=50)
    email    = models.EmailField(max_length=50, unique=True)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['name', 'email']

    objects = UsersManager()  # 사용자 매니저 설정

class Character(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)  # null 허용 및 blank=True 추가
    level = models.IntegerField(default=1)
    health = models.IntegerField(default=100)
    
    # AUTH_USER_MODEL 사용, related_name 수정
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='characters')  # 'character' -> 'characters'

    def __str__(self):
        return self.name
