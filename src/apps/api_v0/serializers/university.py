from rest_framework import serializers

from apps.university.models import University


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['fullname', 'abbreviation', 'description']
