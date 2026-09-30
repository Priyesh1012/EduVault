from django.urls import path

from .views import (
    CommitteeStudentsView,
    GraduateStudentView,
)

urlpatterns = [
    # Get all students
    path(
        "students/",
        CommitteeStudentsView.as_view(),
        name="committee-students",
    ),

    # Graduate a specific student
    path(
        "students/<int:student_id>/graduate/",
        GraduateStudentView.as_view(),
        name="graduate-student",
    ),
]