from rest_framework import serializers
from apps.accounting.models import Equipment
from apps.university.models import Location
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()


class EquipmentSerializer(serializers.ModelSerializer):
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Equipment
        fields = [
            'id', 'name', 'inventory_number', 'count', 'photo',
            'description', 'status', 'location', 'registration_datetime',
            'updated_at', 'owner'
        ]

    def to_representation(self, instance):
        try:
            representation = super().to_representation(instance)
            representation['location'] = {
                'id': instance.location.id,
                'auditorium': instance.location.auditorium.name,
            }
            representation['owner'] = {
                'id': instance.owner.id,
                'username': instance.owner.username,
                'email': instance.owner.email,
            }
            return representation
        except Exception as e:
            raise ValidationError({'error': f"Ошибка в представлении данных: {str(e)}"})

    def validate_inventory_number(self, value):
        """
        Проверка на уникальность инвентарного номера.
        """
        if Equipment.objects.filter(inventory_number=value).exists():
            raise ValidationError({'inventory_number': 'Оборудование с таким инвентарным номером уже существует.'})
        return value

    def validate_count(self, value):
        """
        Проверка, чтобы количество оборудования было положительным.
        """
        if value <= 0:
            raise ValidationError({'count': 'Количество оборудования должно быть больше нуля.'})
        return value
