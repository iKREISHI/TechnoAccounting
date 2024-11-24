from rest_framework import serializers
from apps.university.models import UniversityUnit, University


class UniversityUnitFullSerializer(serializers.ModelSerializer):
    university = serializers.PrimaryKeyRelatedField(queryset=University.objects.all())  # Передача ID университета

    class Meta:
        model = UniversityUnit
        fields = ['id', 'name', 'university', 'abbreviation', 'description']
