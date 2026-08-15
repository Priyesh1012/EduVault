from django.conf import settings
from django.db import models


class StudentProfile(models.Model):

    class Visibility(models.TextChoices):
        INSTITUTIONAL = "INSTITUTIONAL", "Institutional"
        PUBLIC = "PUBLIC", "Public"
        PRIVATE = "PRIVATE", "Private"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    prn_number = models.CharField(
        max_length=50,
        blank=True
    )

    graduation_year = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True
    )

    profile_image = models.ImageField(
        upload_to="profile_images/",
        null=True,
        blank=True
    )

    skills = models.JSONField(
        default=list,
        blank=True
    )

    linkedin = models.URLField(
        blank=True
    )

    github = models.URLField(
        blank=True
    )

    portfolio = models.URLField(
        blank=True
    )

    two_factor_enabled = models.BooleanField(
        default=False
    )

    visibility = models.CharField(
        max_length=20,
        choices=Visibility.choices,
        default=Visibility.INSTITUTIONAL
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.email} Profile"