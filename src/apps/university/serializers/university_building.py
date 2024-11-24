from rest_framework import serializers
from apps.university.models import UniversityBuilding, University


class UniversityBuildingFullSerializer(serializers.ModelSerializer):
    university = serializers.PrimaryKeyRelatedField(queryset=University.objects.all())

    class Meta:
        model = UniversityBuilding
        fields = ['id', 'name', 'university', 'description', 'address']


class UniversityBuildingMiniSerializer(serializers.ModelSerializer):
    university = serializers.PrimaryKeyRelatedField(queryset=University.objects.all())

    class Meta:
        model = UniversityBuilding
        fields = ['id', 'name', 'university',]