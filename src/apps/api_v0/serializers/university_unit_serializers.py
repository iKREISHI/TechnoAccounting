from rest_framework import serializers
from apps.university.models import UniversityUnit


class UniversityUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityUnit
        fields = ['university', 'name', 'description']
