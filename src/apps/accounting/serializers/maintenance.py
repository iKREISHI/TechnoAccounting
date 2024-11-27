from rest_framework import serializers
from apps.accounting.models import Equipment
from apps.accounting.models import Maintenance
from django.contrib.auth import get_user_model
from apps.accounting.serializers import EquipmentMiniSerializer

User = get_user_model()


class MaintenanceSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Maintenance."""
    equipment = EquipmentMiniSerializer(many=True, read_only=True)
    equipment_ids = serializers.PrimaryKeyRelatedField(
        queryset=Equipment.objects.all(), many=True, write_only=True, source='equipment'
    )
    service_worker = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )
    reporter = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )
    assigned_by = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        model = Maintenance
        fields = [
            'id',
            'equipment',
            'equipment_ids',
            'service_worker',
            'reporter',
            'assigned_by',
            'issue_description',
            'status',
            'start_time',
            'end_time',
        ]
        read_only_fields = ['start_time']

    def create(self, validated_data):
        equipment = validated_data.pop('equipment')
        if not equipment:
            raise serializers.ValidationError('Equipment not found.')
        for eq in equipment:
            if not eq:
                raise serializers.ValidationError('Equipment is required.')
            elif eq.status == 'serviced':
                raise serializers.ValidationError('Equipment is not be serviced.')
            eq.status = 'serviced'
            eq.save()
        maintenance = Maintenance.objects.create(**validated_data)
        maintenance.equipment.set(equipment)
        return maintenance

    def update(self, instance, validated_data):
        if 'equipment' in validated_data:
            equipment = validated_data.pop('equipment')
            instance.equipment.set(equipment)
        return super().update(instance, validated_data)
