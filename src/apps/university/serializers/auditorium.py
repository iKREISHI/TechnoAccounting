from rest_framework import serializers
from apps.university.models import Auditorium, University, UniversityBuilding, UniversityUnit


class AuditoriumFullSerializer(serializers.ModelSerializer):

    university = serializers.PrimaryKeyRelatedField(queryset=University.objects.all())
    university_unit = serializers.PrimaryKeyRelatedField(queryset=UniversityUnit.objects.all())
    building = serializers.PrimaryKeyRelatedField(queryset=UniversityBuilding.objects.all())

    class Meta:
        model = Auditorium
        fields = ['id', 'name', 'university', 'university_unit', 'building', 'description']


class AuditoriumMiniSerializer(serializers.ModelSerializer):

    university = serializers.PrimaryKeyRelatedField(queryset=University.objects.all())
    university_unit = serializers.PrimaryKeyRelatedField(queryset=UniversityUnit.objects.all())
    building = serializers.PrimaryKeyRelatedField(queryset=UniversityBuilding.objects.all())

    class Meta:
        model = Auditorium
        fields = ['id', 'name', 'university', 'university_unit', 'building',]
