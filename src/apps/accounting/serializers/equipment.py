from rest_framework import serializers
from apps.accounting.models import Equipment
from apps.university.models import Location
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.utils.timezone import now

User = get_user_model()


class EquipmentMiniSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения информации об оборудовании."""

    class Meta:
        model = Equipment
        fields = ['id', 'name', 'inventory_number', 'status']


class EquipmentSerializer(serializers.ModelSerializer):
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)

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
                    'required': 'Поле "Название" обязательно для заполнения.',
                    'blank': 'Поле "Название" не должно быть пустым.',
                    'max_length': 'Слишком длинное название. Максимум 255 символов.',
                }
            },
            'inventory_number': {
                'error_messages': {
                    'required': 'Поле "Инвентарный номер" обязательно для заполнения.',
                    'blank': 'Поле "Инвентарный номер" не должно быть пустым.',
                    'max_length': 'Слишком длинный инвентарный номер. Максимум 32 символа.',
                }
            },
            'count': {
                'error_messages': {
                    'required': 'Поле "Количество" обязательно для заполнения.',
                    'blank': 'Поле "Количество" не должно быть пустым.',
                    'invalid': 'Введите положительное целое число.',
                }
            },
            # 'photo': {
            #     'error_messages': {
            #         'required': 'Поле "Фото" обязательно для заполнения.',
            #         'blank': 'Поле "Фото" не должно быть пустым.',
            #     }
            # },
            'status': {
                'error_messages': {
                    'required': 'Поле "Статус" обязательно для заполнения.',
                    'blank': 'Поле "Статус" не должно быть пустым.',
                    'invalid_choice': 'Выбран некорректный статус.',
                }
            },
            'location': {
                'error_messages': {
                    'required': 'Поле "Расположение" обязательно для заполнения.',
                    'blank': 'Поле "Расположение" не должно быть пустым.',
                }
            },
            'owner': {
                'error_messages': {
                    'required': 'Поле "Владелец" обязательно для заполнения.',
                    'blank': 'Поле "Владелец" не должно быть пустым.',
                }
            },
        }

    def validate_count(self, value):
        """
        Проверка, чтобы количество оборудования было положительным.
        """
        if value <= 0:
            raise ValidationError({'count': 'Количество оборудования должно быть больше нуля.'})
        return value

    def create(self, validated_data):
        if not validated_data.get('owner'):
            request = self.context.get('request')
            if request and request.user.is_authenticated:
                validated_data['owner'] = request.user
            else:
                raise ValidationError({'owner': 'Владелец должен быть указан или пользователь должен быть аутентифицирован.'})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Обновить поле updated_at при каждом обновлении.
        """
        validated_data['updated_at'] = now()
        return super().update(instance, validated_data)


class EquipmentViewOrListSerializer(EquipmentSerializer):

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


class EquipmentUpdateSerializer(EquipmentSerializer):
    pass
