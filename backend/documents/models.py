from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError



def validate_document_file(value):
    max_size = 5 * 1024 * 1024  # 5 MB

    if value.size > max_size:
        raise ValidationError("File size must not exceed 5 MB.")

    allowed_extensions = [".pdf", ".jpg", ".jpeg", ".png"]

    file_name = value.name.lower()

    if not any(file_name.endswith(ext) for ext in allowed_extensions):
        raise ValidationError(
            "Only PDF, JPG, JPEG and PNG files are allowed."
        )


class Document(models.Model):

    class Category(models.TextChoices):
        CERTIFICATE = "CERTIFICATE", "Certificate"
        MARKSHEET = "MARKSHEET", "Marksheet"
        INTERNSHIP = "INTERNSHIP", "Internship"
        PROJECT = "PROJECT", "Project"
        ACHIEVEMENT = "ACHIEVEMENT", "Achievement"
        OTHER = "OTHER", "Other"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        VERIFIED = "VERIFIED", "Verified"
        REJECTED = "REJECTED", "Rejected"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    title = models.CharField(max_length=200)

    category = models.CharField(
        max_length=20,
        choices=Category.choices
    )

    file = models.FileField(
        upload_to="documents/",
        validators=[validate_document_file]
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    rejection_reason = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.email}"