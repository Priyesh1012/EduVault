from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import StudentProfile
from .serializers import StudentProfileSerializer


class StudentProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = StudentProfile.objects.get_or_create(
            user=self.request.user,
            defaults={
                "prn": f"PRN{self.request.user.id}",
                "department": "",
                "course": "",
                "graduation_year": 2027,
            },
        )

        return profile