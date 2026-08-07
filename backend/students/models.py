from django.conf import settings
from django.db import models


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    prn = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    division = models.CharField(max_length=10, blank=True)
    graduation_year = models.PositiveIntegerField()

    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.prn}"

class Skill(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="skills"
    )

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name    


class Project(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=300, blank=True)

    github_url = models.URLField(blank=True)
    project_url = models.URLField(blank=True)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title


class Internship(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="internships"
    )

    company = models.CharField(max_length=200)
    role = models.CharField(max_length=150)

    description = models.TextField(blank=True)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.company} - {self.role}"        