from rest_framework import serializers

from apps.university.models import Auditorium


class AuditoriumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditorium
        fields = ['university', 'university_unit', 'name', 'description']
