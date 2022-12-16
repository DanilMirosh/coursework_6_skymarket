from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser):
    ADMIN = 'admin'
    USER = 'user'
    ROLES = [
        (ADMIN, ADMIN),
        (USER, USER)
    ]

    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=150, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(unique=True, max_length=50)
    password = models.CharField(max_length=200)
    role = models.CharField(max_length=5, choices=ROLES, default='user', null=True)
    image = models.ImageField(upload_to='user_avatars/', null=True)
    is_active = models.BooleanField(null=True, default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', "role"]

    objects = UserManager()

    @property
    def is_admin(self):
        return self.role == User.ADMIN

    @property
    def is_user(self):
        return self.role == User.USER

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['email']

    def __str__(self):
        return self.email
