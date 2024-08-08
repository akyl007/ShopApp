from django.contrib import admin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        user = self.model(username=username, password=password, **extra_fields)
        user.is_admin = True
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):

    username = models.CharField(max_length=30, unique=True,
                                verbose_name='Логин')
    phone = models.CharField(max_length=17, blank=True,
                             null=True, unique=True, verbose_name='Номер телефона')

    USERNAME_FIELD = 'username'

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Уникальное имя для обратной связи
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='Группы'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Уникальное имя для обратной связи
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='Разрешения'
    )

    objects = CustomUserManager()
