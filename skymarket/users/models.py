from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from users.managers import UserManager


class User(AbstractBaseUser):
    ADMIN = 'admin'
    USER = 'user'
    ROLES = [
        (ADMIN, ADMIN),
        (USER, USER),
    ]

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'role']

    objects = UserManager()

    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    phone = PhoneNumberField(blank=True, unique=True)
    email = models.EmailField(unique=True, max_length=254)
    role = models.CharField(max_length=5, choices=ROLES, default='user')
    image = models.ImageField(upload_to='avatars', null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["id"]

    def __str__(self):
        return self.email

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

    def has_module_perm(self, app_label):
        return self.is_admin
