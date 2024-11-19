from rest_framework import serializers

from apps.accounting.models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['building', 'auditorium', 'description']
