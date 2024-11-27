from datetime import timedelta

from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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
            elif eq.status in ['available', 'rented']:
                eq.status = 'serviced'
                eq.save()
            else:
                raise serializers.ValidationError('Equipment is not available.')
        maintenance = Maintenance.objects.create(**validated_data)
        maintenance.equipment.set(equipment)
        return maintenance

    def update(self, instance, validated_data):
        if 'equipment' in validated_data:
            equipment = validated_data.pop('equipment')
            instance.equipment.set(equipment)
        return super().update(instance, validated_data)

    def validate(self, data):
        print(data)

        # Проверка наличия списка оборудования только при создании
        if not self.instance:  # Только для создания новой записи
            equipment_ids = data.get("equipment_ids", [])
            equipments = data.get("equipment", [])
            if not equipment_ids and not equipments:
                raise serializers.ValidationError({"equipment_ids": "Equipment is required."})

            # Проверка наличия всех переданных идентификаторов оборудования
            found_equipment_ids = set(Equipment.objects.filter(id__in=equipment_ids).values_list('id', flat=True))
            if set(equipment_ids) != found_equipment_ids:
                raise serializers.ValidationError({"equipment_ids": "One or more Equipment IDs not found."})

        # Проверка времени завершения только при наличии end_time в данных
        if "end_time" in data and data["end_time"] < now():
            raise serializers.ValidationError({"end_time": "End time must be in the future."})

        return data


