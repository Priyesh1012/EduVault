from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import StudentProfile
from .serializers import StudentProfileSerializer

from django.db import transaction
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .permissions import IsCommittee
from .models import StudentProfile
from .serializers import GraduateStudentSerializer


class ProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = StudentProfile.objects.get_or_create(
            user=self.request.user
        )

        return profile



User = get_user_model()


class GraduateStudentView(APIView):
    permission_classes = [IsAuthenticated, IsCommittee]

    @transaction.atomic
    def patch(self, request, student_id):
        try:
            student = User.objects.get(id=student_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Student not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if student.role != "STUDENT":
            return Response(
                {"error": "Only students can be graduated."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = GraduateStudentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        profile, created = StudentProfile.objects.get_or_create(
            user=student
        )

        profile.graduation_status = "GRADUATED"
        profile.graduation_date = serializer.validated_data["graduation_date"]
        profile.save()

        student.role = "ALUMNI"
        student.save(update_fields=["role"])

        return Response(
            {
                "message": "Student graduated successfully.",
                "user_id": student.id,
                "role": student.role,
                "graduation_status": profile.graduation_status,
                "graduation_date": profile.graduation_date,
            },
            status=status.HTTP_200_OK
        )    

class CommitteeStudentsView(APIView):
    permission_classes = [IsAuthenticated, IsCommittee]

    def get(self, request):
        students = User.objects.filter(role="STUDENT")

        data = []

        for student in students:
            profile = StudentProfile.objects.filter(
                user=student
            ).first()

            data.append({
                "id": student.id,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "email": student.email,
                "role": student.role,
                "graduation_status": (
                    profile.graduation_status
                    if profile
                    else "ONGOING"
                ),
                "graduation_date": (
                    profile.graduation_date
                    if profile
                    else None
                ),
            })

        return Response(data)