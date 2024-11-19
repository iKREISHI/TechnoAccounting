from rest_framework import serializers

from apps.university.models import UniversityBuilding


class UniversityBuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityBuilding
        fields = ['university', 'name', 'description']
