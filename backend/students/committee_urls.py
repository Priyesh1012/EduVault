from django.urls import path
from .views import GraduateStudentView

urlpatterns = [
    path(
        "students/<int:student_id>/graduate/",
        GraduateStudentView.as_view(),
        name="graduate-student"
    ),
]