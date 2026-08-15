from rest_framework import serializers

from .models import StudentProfile


class StudentProfileSerializer(serializers.ModelSerializer):

    academic = serializers.SerializerMethodField()
    social = serializers.SerializerMethodField()
    preferences = serializers.SerializerMethodField()

    class Meta:
        model = StudentProfile
        fields = [
            "id",
            "academic",
            "skills",
            "social",
            "preferences",
        ]

    def get_academic(self, obj):
        return {
            "college": obj.user.college,
            "department": obj.user.department,
            "prn_number": obj.prn_number,
            "graduation_year": obj.graduation_year,
            "cgpa": obj.cgpa,
            "profile_image": (
                obj.profile_image.url
                if obj.profile_image
                else None
            ),
        }

    def get_social(self, obj):
        return {
            "linkedin": obj.linkedin,
            "github": obj.github,
            "portfolio": obj.portfolio,
        }

    def get_preferences(self, obj):
        return {
            "two_factor_enabled": obj.two_factor_enabled,
            "visibility": obj.visibility,
        }

    def update(self, instance, validated_data):

        request = self.context.get("request")

        # Academic fields
        if "prn_number" in request.data:
            instance.prn_number = request.data.get("prn_number")

        if "graduation_year" in request.data:
            instance.graduation_year = request.data.get("graduation_year")

        if "cgpa" in request.data:
            instance.cgpa = request.data.get("cgpa")

        # Skills
        if "skills" in request.data:
            instance.skills = request.data.get("skills")

        # Social links
        if "linkedin" in request.data:
            instance.linkedin = request.data.get("linkedin")

        if "github" in request.data:
            instance.github = request.data.get("github")

        if "portfolio" in request.data:
            instance.portfolio = request.data.get("portfolio")

        # Preferences
        if "two_factor_enabled" in request.data:
            instance.two_factor_enabled = request.data.get(
                "two_factor_enabled"
            )

        if "visibility" in request.data:
            instance.visibility = request.data.get("visibility")

        # Profile image
        if "profile_image" in request.FILES:
            instance.profile_image = request.FILES["profile_image"]

        instance.save()

        return instance