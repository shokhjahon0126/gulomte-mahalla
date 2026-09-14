from django.db import models
from django.contrib.auth.models import AbstractUser


class UserRole(models.TextChoices):
    ADMIN = 'admin', 'Admin'


class User(AbstractUser):
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.ADMIN,
        verbose_name="Role"
    )

    class Meta:
        verbose_name = "User"
        ordering = ['-id']
        
    def __str__(self):
        return f"{self.username} ({self.full_name})"
