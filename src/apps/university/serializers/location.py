from rest_framework import serializers
from apps.university.models import Location, Auditorium


class LocationSerializer(serializers.ModelSerializer):
    auditorium = serializers.PrimaryKeyRelatedField(queryset=Auditorium.objects.all())

    class Meta:
        model = Location
        fields = ['id', 'auditorium', 'description']
