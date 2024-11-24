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

        read_only_fields = ['registration_datetime', 'updated_at']

        extra_kwargs = {
            'name': {
                'error_messages': {
                    'required': 'Название должно быть обязательно',
                    'max_length': 'Название слишком длинное',
                    'min_length': 'Название слишком короткое',
                    'blank': 'Название не должно быть пустым',
                }
            },
            'inventory_number': {
                'error_messages': {
                    'required': 'Инвентарный номер должен быть обязательным',
                    'max_length': 'Инвентарный номер слишком длинный',
                    'blank': 'Инвентарный номер не должен быть пустым'
                }
            },
            'count': {
                'error_messages': {
                    'required': 'Количество должно быть обязательным',
                    'blank': 'Количество оборудования не должен быть пустым'
                }
            },
            'photo': {
                'error_messages': {
                    "required": "Загрузите фотографию.",
                    "blank": "Фотография не может быть пустой.",
                }
            },
            'description': {},
            'status': {
                'error_messages': {
                    'required': 'Статус должен быть обязательным',
                    'blank': 'Статус оборудования не должен быть пустым'
                }
            },
            'location': {
                'error_messages': {
                    'required': 'Расположение должно быть обязательным',
                    'blank': 'Расположение оборудования не должен быть пустым'
                }
            },
            'registration_datetime': {

            }
        }

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

    def validate_count(self, value):
        """
        Проверка, чтобы количество оборудования было положительным.
        """
        if value <= 0:
            raise ValidationError({'count': 'Количество оборудования должно быть больше нуля.'})
        return value
