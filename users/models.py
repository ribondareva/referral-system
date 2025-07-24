from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import random
import string


class UserManager(BaseUserManager):
    def create_user(self, phone, **extra_fields):
        if not phone:
            raise ValueError("Номер телефона обязателен")
        user = self.model(phone=phone, **extra_fields)
        user.set_unusable_password()
        user.save()
        return user


class User(AbstractBaseUser):
    phone = models.CharField(max_length=20, unique=True)
    invite_code = models.CharField(max_length=6, unique=True, blank=True)
    activated_code = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals'
    )

    USERNAME_FIELD = 'phone'
    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = self.generate_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_code():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
