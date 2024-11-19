from rest_framework import serializers

from apps.accounting.models import Equipment


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['name', 'inventory_number', 'count', 'photo', 'description',
                  'location', 'owner']
