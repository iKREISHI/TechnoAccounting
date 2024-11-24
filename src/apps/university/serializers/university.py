from rest_framework import serializers
from apps.university.models import University


class UniversityFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['id', 'fullname', 'abbreviation', 'description']


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['id', 'fullname', 'abbreviation']
