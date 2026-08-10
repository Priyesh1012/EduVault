from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        ALUMNI = "ALUMNI", "Alumni"
        COMMITTEE = "COMMITTEE", "Committee"
        PLACEMENT = "PLACEMENT", "Placement"
        ADMIN = "ADMIN", "Admin"

    # We don't want Django's username to be part of registration.
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True
    )

    email = models.EmailField(unique=True)

    mobile_number = models.CharField(
        max_length=15
    )

    college = models.CharField(
        max_length=200
    )

    department = models.CharField(
        max_length=150
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT
    )

    def __str__(self):
        return f"{self.get_full_name()} - {self.role}"